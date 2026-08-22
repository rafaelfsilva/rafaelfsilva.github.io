#!/usr/bin/env python3
"""
Funding portfolio totals, computed from the awards listed in _data/rafael.yml.

The total awarded amount and the award count are never stored in the YAML: they
are derived here so the CV, resume, and website can never drift apart. The Liquid
equivalent used by the website lives in _includes/funding_totals.html -- keep the
two in sync.

Prose in the YAML (intro, about_sections, leadership_highlights) uses the tokens
%FUNDING_TOTAL% and %FUNDING_COUNT%, which apply_funding_tokens() resolves.
"""

import re

FUNDING_CATEGORIES = ('doe', 'nsf', 'darpa', 'international')

TOTAL_TOKEN = '%FUNDING_TOTAL%'
COUNT_TOKEN = '%FUNDING_COUNT%'


def parse_amount(amount_str):
    """Strip currency symbols/separators and return the numeric value."""
    if not amount_str:
        return 0
    cleaned = re.sub(r'[^0-9.]', '', str(amount_str))
    try:
        return float(cleaned)
    except ValueError:
        return 0


def funding_totals(data):
    """Return {'total', 'count', 'millions', 'label'} for the funding portfolio."""
    funding = (data or {}).get('funding', {}) or {}

    total = 0.0
    count = 0
    for category in FUNDING_CATEGORIES:
        for award in funding.get(category, []) or []:
            total += parse_amount(award.get('amount'))
            count += 1

    millions = total / 1_000_000 if total else 0
    label = f"${int(millions)}M+" if total >= 1_000_000 else f"${total:,.0f}"

    return {'total': total, 'count': count, 'millions': millions, 'label': label}


def apply_funding_tokens(value, totals):
    """Recursively resolve the funding tokens in every string within `value`."""
    if isinstance(value, str):
        return (value
                .replace(TOTAL_TOKEN, totals['label'])
                .replace(COUNT_TOKEN, str(totals['count'])))
    if isinstance(value, list):
        return [apply_funding_tokens(item, totals) for item in value]
    if isinstance(value, dict):
        return {k: apply_funding_tokens(v, totals) for k, v in value.items()}
    return value


def resolve_funding_tokens(data):
    """Resolve funding tokens across a freshly loaded rafael.yml payload."""
    return apply_funding_tokens(data, funding_totals(data))
