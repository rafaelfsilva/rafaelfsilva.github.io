#!/usr/bin/env python3
"""
Generate the two-page résumé PDF from scripts/resume/template.html.

The narrative lives in the HTML template. Every figure that changes over time
(funding, citations, publications, community size, BoF sessions, awards) is
computed from the site's data files when the script runs, so the résumé stays
consistent with the website and the CV.

Requirements:
    pip install pyyaml
    Google Chrome or Chromium, used headlessly to render HTML to PDF
    (set CHROME_PATH to pick a specific binary)

Usage:
    python scripts/generate_resume.py

Output:
    files/cv/RafaelFerreiraDaSilva-resume.pdf
"""

import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from funding_utils import funding_totals, parse_amount  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESUME_DIR = PROJECT_ROOT / 'scripts' / 'resume'
OUTPUT_PDF = PROJECT_ROOT / 'files' / 'cv' / 'RafaelFerreiraDaSilva-resume.pdf'

# DOE awards starting in or after this year count as "new" under the current
# role (Section Head since 2025).
RECENT_AWARDS_SINCE = 2025
EXPECTED_PAGES = 2

NUMBER_WORDS = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
                'eight', 'nine', 'ten', 'eleven', 'twelve')

CHROME_CANDIDATES = (
    'google-chrome',
    'google-chrome-stable',
    'chromium',
    'chromium-browser',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
)

TOKEN = re.compile(r'\{\{\s*(\w+)\s*\}\}')


# ----------------------------------------------------------------------------
# Formatting helpers
# ----------------------------------------------------------------------------

def as_word(n):
    """Spell out small counts, as running text reads better that way."""
    return NUMBER_WORDS[n] if 0 <= n < len(NUMBER_WORDS) else str(n)


def floor_to(n, step):
    return int(n) // step * step


def year_span(years, sep):
    if not years:
        return ''
    lo, hi = min(years), max(years)
    return str(lo) if lo == hi else f"{lo}{sep}{hi}"


def join_and(items):
    items = list(items)
    if len(items) <= 2:
        return ' and '.join(items)
    return ', '.join(items[:-1]) + ', and ' + items[-1]


def kpi(value):
    """Metric for the KPI strip, with a trailing '+' raised to superscript."""
    value = html.escape(str(value))
    return f"{value[:-1]}<sup>+</sup>" if value.endswith('+') else value


# ----------------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------------

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def start_year(period):
    match = re.search(r'\d{4}', str(period or ''))
    return int(match.group()) if match else 0


def project_count(data, name):
    for project in data.get('research_projects', []):
        if project.get('name') == name:
            return str(project.get('count', '')).strip()
    raise SystemExit(f"Research project '{name}' not found in _data/rafael.yml")


def count_publications(bib_path):
    text = bib_path.read_text(encoding='utf-8')
    return len(re.findall(r'^@(?!string|comment|preamble)\w+\s*\{', text, re.M | re.I))


def compute_values(root):
    """Every token the template uses, computed from the site's data files."""
    data = load_yaml(root / '_data' / 'rafael.yml')
    scholar = load_yaml(root / '_data' / 'scholar_metrics.yml')
    bofs = load_yaml(root / '_data' / 'activities_bof.yml') or []

    funding = funding_totals(data)

    recent = [a for a in data.get('funding', {}).get('doe', [])
              if start_year(a.get('period')) >= RECENT_AWARDS_SINCE]
    recent_total = sum(parse_amount(a.get('amount')) for a in recent)

    awards = data.get('awards', [])
    best_papers = [a for a in awards
                   if re.search(r'\bbest\b.*\bpaper\b', a.get('title', ''), re.I)
                   and 'candidate' not in a.get('title', '').lower()]

    citations = int(scholar.get('citations', 0))
    publications = count_publications(root / '_bibliography' / 'references.bib')
    wci_members = project_count(data, 'Workflows Community Initiative')
    bof_series = dict.fromkeys(s['series'] for s in bofs if s.get('series'))

    return {
        'base_href': RESUME_DIR.as_uri() + '/',
        'funding_label': funding['label'],
        'kpi_funding': kpi(funding['label']),
        'kpi_citations': kpi(f"{floor_to(citations, 100):,}+"),
        'h_index': str(scholar.get('h_index', '')),
        'publications': f"{floor_to(publications, 5)}+",
        'honors_count': str(len(awards)),
        'recent_doe_count_word': as_word(len(recent)),
        'recent_doe_total': f"${floor_to(recent_total / 1_000_000, 1)}M+",
        'recent_doe_years': year_span([start_year(a.get('period')) for a in recent], '–'),
        'wci_members': wci_members,
        'kpi_wci_members': kpi(wci_members),
        'wfcommons_articles': project_count(data, 'WfCommons'),
        'wrench_articles': project_count(data, 'WRENCH'),
        'bof_count': str(len(bofs)),
        'bof_lead_word': as_word(sum(1 for s in bofs if s.get('role') == 'Lead Organizer')),
        'bof_venues': join_and(bof_series),
        'bof_years': year_span([int(s['year']) for s in bofs], ' – '),
        'best_paper_word': as_word(len(best_papers)).capitalize(),
        'best_paper_years': year_span([int(a['year']) for a in best_papers], ' – '),
    }


def render(template, values):
    missing = sorted({name for name in TOKEN.findall(template) if name not in values})
    if missing:
        raise SystemExit(f"Template uses undefined values: {', '.join(missing)}")

    def fill(match):
        name = match.group(1)
        value = values[name]
        # kpi_* values carry intended markup; everything else is plain text.
        return value if name.startswith('kpi_') else html.escape(value)

    return TOKEN.sub(fill, template)


# ----------------------------------------------------------------------------
# PDF rendering
# ----------------------------------------------------------------------------

def find_chrome():
    if os.environ.get('CHROME_PATH'):
        return os.environ['CHROME_PATH']
    for candidate in CHROME_CANDIDATES:
        path = shutil.which(candidate) or (candidate if os.path.isfile(candidate) else None)
        if path:
            return path
    raise SystemExit("Chrome or Chromium not found; install one or set CHROME_PATH.")


def html_to_pdf(chrome, html_path, pdf_path):
    cmd = [chrome, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
           f'--print-to-pdf={pdf_path}', html_path.as_uri()]
    if sys.platform.startswith('linux'):
        # Ubuntu 24.04 restricts the user namespaces Chrome's sandbox needs.
        # The page is our own local template, so rendering unsandboxed is safe.
        cmd.insert(1, '--no-sandbox')

    if pdf_path.exists():
        pdf_path.unlink()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if result.returncode != 0 or not pdf_path.exists():
        sys.stderr.write(result.stderr)
        raise SystemExit(f"Chrome failed to render the résumé (exit {result.returncode}).")


def page_count(pdf_path):
    """Page count from the PDF's page tree; None if it can't be read."""
    match = re.search(rb'/Type\s*/Pages\b[^>]*?/Count\s+(\d+)', pdf_path.read_bytes())
    return int(match.group(1)) if match else None


def main():
    values = compute_values(PROJECT_ROOT)
    template = (RESUME_DIR / 'template.html').read_text(encoding='utf-8')
    page = render(template, values)

    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        html_path = Path(tmp) / 'resume.html'
        html_path.write_text(page, encoding='utf-8')
        html_to_pdf(find_chrome(), html_path, OUTPUT_PDF)

    pages = page_count(OUTPUT_PDF)
    print(f"✓ Résumé generated: {OUTPUT_PDF} ({pages or '?'} pages)")
    if pages and pages != EXPECTED_PAGES:
        message = (f"Résumé is {pages} pages, expected {EXPECTED_PAGES}; "
                   "trim scripts/resume/template.html")
        prefix = '::warning::' if os.environ.get('GITHUB_ACTIONS') else 'Warning: '
        print(prefix + message)


if __name__ == '__main__':
    main()
