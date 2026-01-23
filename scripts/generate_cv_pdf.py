#!/usr/bin/env python3
"""
Generate a comprehensive PDF CV from the YAML data file, including all publications and activities.

Requirements:
    pip install reportlab pyyaml bibtexparser

Usage:
    python scripts/generate_cv_pdf.py

Output:
    Generates full CV PDF in files/cv/ directory
"""

import yaml
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
import re
try:
    import bibtexparser
    BIBTEX_AVAILABLE = True
except ImportError:
    BIBTEX_AVAILABLE = False
    print("Warning: bibtexparser not installed. Publications will be skipped.")
    print("Install with: pip install bibtexparser")
try:
    from pylatexenc.latex2text import LatexNodes2Text
    LATEX_AVAILABLE = True
except ImportError:
    LATEX_AVAILABLE = False
    print("Warning: pylatexenc not installed. LaTeX accents may not render correctly.")
    print("Install with: pip install pylatexenc")


class CVGenerator:
    """Generate a comprehensive PDF CV from YAML data."""

    def __init__(self, yaml_path, project_root):
        """Initialize the CV generator with data from YAML file."""
        with open(yaml_path, 'r') as f:
            self.data = yaml.safe_load(f)

        self.project_root = project_root
        self.palette = {
            'ink': colors.HexColor('#111827'),
            'accent': colors.HexColor('#2563eb'),
            'muted': colors.HexColor('#6b7280'),
            'light': colors.HexColor('#f8fafc'),
            'border': colors.HexColor('#e5e7eb')
        }
        self.styles = self._create_styles()
        self.story = []

        # Load activities data
        self._load_activities()

        # Load publications
        self.publications = self._load_publications()

    def _load_activities(self):
        """Load all activities YAML files."""
        activities_dir = os.path.join(self.project_root, '_data')
        self.activities = {}

        activity_files = {
            'chair': 'activities_chair.yml',
            'pc': 'activities_pc.yml',
            'conference': 'activities_conference.yml',
            'journal': 'activities_journal.yml',
            'editor': 'activities_editor.yml',
            'funding': 'activities_funding.yml',
            'sc': 'activities_sc.yml'
        }

        for key, filename in activity_files.items():
            filepath = os.path.join(activities_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    self.activities[key] = yaml.safe_load(f)

    def _load_publications(self):
        """Load publications from BibTeX file."""
        if not BIBTEX_AVAILABLE:
            return []

        bib_path = os.path.join(self.project_root, '_bibliography', 'references.bib')
        if not os.path.exists(bib_path):
            print(f"Warning: BibTeX file not found at {bib_path}")
            return []

        try:
            with open(bib_path, 'r', encoding='utf-8') as f:
                bib_database = bibtexparser.load(f)

            # Sort by year (descending)
            pubs = sorted(bib_database.entries,
                         key=lambda x: int(x.get('year', '0')),
                         reverse=True)
            print(f"Loaded {len(pubs)} publications from BibTeX file")
            return pubs
        except Exception as e:
            print(f"Error loading BibTeX file: {e}")
            return []

    def _create_styles(self):
        """Create custom paragraph styles for the CV."""
        styles = getSampleStyleSheet()

        # Title style (Name)
        styles.add(ParagraphStyle(
            name='CVName',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=self.palette['ink'],
            spaceAfter=2,
            alignment=TA_LEFT,
            leading=26,
            fontName='Helvetica-Bold'
        ))

        # Subtitle style (Titles)
        styles.add(ParagraphStyle(
            name='CVTitle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=self.palette['accent'],
            spaceAfter=10,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            leading=14
        ))

        # Section heading
        styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=styles['Heading2'],
            fontSize=10,
            textColor=self.palette['accent'],
            spaceBefore=12,
            spaceAfter=4,
            fontName='Helvetica-Bold',
        ))

        # Subsection heading
        styles.add(ParagraphStyle(
            name='SubsectionHeading',
            parent=styles['Normal'],
            fontSize=10,
            textColor=self.palette['ink'],
            spaceBefore=6,
            spaceAfter=2,
            fontName='Helvetica-Bold'
        ))

        # Body text
        styles.add(ParagraphStyle(
            name='CVBody',
            parent=styles['Normal'],
            fontSize=9.5,
            textColor=self.palette['ink'],
            spaceAfter=4,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=12
        ))

        # Small text
        styles.add(ParagraphStyle(
            name='CVSmall',
            parent=styles['Normal'],
            fontSize=8.5,
            textColor=self.palette['muted'],
            spaceAfter=3,
            fontName='Helvetica',
            leading=10
        ))

        # Highlight box style
        styles.add(ParagraphStyle(
            name='HighlightBox',
            parent=styles['Normal'],
            fontSize=9,
            textColor=self.palette['accent'],
            spaceAfter=4,
            fontName='Helvetica-Bold',
            leading=12
        ))

        # Metric style
        styles.add(ParagraphStyle(
            name='Metric',
            parent=styles['Normal'],
            fontSize=18,
            textColor=self.palette['accent'],
            spaceAfter=2,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Metric label style
        styles.add(ParagraphStyle(
            name='MetricLabel',
            parent=styles['Normal'],
            fontSize=8,
            textColor=self.palette['muted'],
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))

        # Contact info
        styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=styles['Normal'],
            fontSize=8.5,
            textColor=self.palette['muted'],
            spaceAfter=2,
            alignment=TA_RIGHT,
            fontName='Helvetica',
            leading=10
        ))

        # Right-aligned metadata
        styles.add(ParagraphStyle(
            name='EntryMeta',
            parent=styles['Normal'],
            fontSize=8.5,
            textColor=self.palette['muted'],
            spaceAfter=2,
            alignment=TA_RIGHT,
            fontName='Helvetica'
        ))

        # Publication style
        styles.add(ParagraphStyle(
            name='Publication',
            parent=styles['Normal'],
            fontSize=8.5,
            textColor=self.palette['ink'],
            spaceAfter=4,
            fontName='Helvetica',
            leading=10,
            leftIndent=0.12*inch,
            firstLineIndent=-0.12*inch
        ))

        return styles

    def _strip_html(self, text):
        """Remove HTML tags from text."""
        if not text:
            return ""
        # Remove <a> tags but keep the text
        text = re.sub(r'<a[^>]*>', '', text)
        text = re.sub(r'</a>', '', text)
        # Remove other HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()

    def _normalize_bibtex_text(self, text):
        """Convert BibTeX/LaTeX markup to readable text."""
        if not text:
            return ""
        cleaned = text.replace('{', '').replace('}', '')
        if LATEX_AVAILABLE:
            return LatexNodes2Text().latex_to_text(cleaned).strip()
        return cleaned.strip()

    def _parse_amount(self, amount_str):
        """Parse currency amounts into a float for sorting."""
        if not amount_str:
            return 0
        cleaned = re.sub(r'[^0-9.]', '', str(amount_str))
        try:
            return float(cleaned)
        except ValueError:
            return 0

    def _emphasize_numbers(self, text):
        """Bold numeric impact signals inside text."""
        if not text:
            return ""
        return re.sub(r'(\$?\d[\d,]*\+?M?)', r'<b>\1</b>', text)

    def _add_header(self):
        """Add header with name, titles, and contact information."""
        personal = self.data.get('personal', {})

        # Name
        name = personal.get('name', '')
        title = personal.get('title', '')
        full_name = f"{name}, {title}" if title else name
        left_column = [Paragraph(full_name, self.styles['CVName'])]

        # Titles
        titles = []
        for pos in personal.get('titles_full', []):
            title_text = pos.get('title', '')
            if pos.get('interim'):
                title_text += ' (Interim)'
            titles.append(title_text)

        if titles:
            left_column.append(Paragraph(' • '.join(titles), self.styles['CVTitle']))

        # Contact information
        contact = personal.get('contact', {})
        office = personal.get('office', {})

        right_column = []
        if office.get('institution'):
            right_column.append(Paragraph(office['institution'], self.styles['ContactInfo']))

        contact_primary = []
        if contact.get('email'):
            contact_primary.append(contact['email'])
        if contact.get('website'):
            contact_primary.append(contact['website'])
        if contact_primary:
            right_column.append(Paragraph(' · '.join(contact_primary), self.styles['ContactInfo']))

        contact_secondary = []
        if contact.get('phone'):
            contact_secondary.append(contact['phone'])
        if contact_secondary:
            right_column.append(Paragraph(' · '.join(contact_secondary), self.styles['ContactInfo']))

        if not right_column:
            right_column = [Paragraph('', self.styles['ContactInfo'])]

        header_table = Table(
            [[left_column, right_column]],
            colWidths=[4.6*inch, 2.3*inch]
        )
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LINEBELOW', (0, 0), (-1, -1), 1.2, self.palette['accent'])
        ]))

        self.story.append(header_table)

    def _add_executive_summary(self):
        """Add executive summary with key metrics and highlights."""
        personal = self.data.get('personal', {})
        intro = personal.get('intro', '')

        # Add cleaned intro text (remove HTML)
        if intro:
            clean_intro = self._strip_html(intro)
            self.story.append(Paragraph(clean_intro, self.styles['CVBody']))
            self.story.append(Spacer(1, 0.08*inch))

        # Integrated highlights and signature initiatives
        research = self.data.get('research', {})
        highlights = research.get('leadership_highlights', [])
        accomplishments = []

        for item in highlights[:4]:
            accomplishments.append(item)

        funding = self.data.get('funding', {})
        funding_count = sum(len(funding.get(cat, [])) for cat in ['doe', 'nsf', 'darpa', 'international'])
        if funding_count:
            accomplishments.append(f"{funding_count} competitively reviewed grants led or co-led")

        awards = self.data.get('awards', [])
        if awards:
            accomplishments.append(f"{len(awards)} best paper awards at international conferences")

        if self.publications:
            recent_pubs = [p for p in self.publications if int(p.get('year', '0')) >= 2020]
            accomplishments.append(f"{len(self.publications)} peer-reviewed publications ({len(recent_pubs)} since 2020)")

        memberships = self.data.get('personal', {}).get('memberships', [])
        senior = [m for m in memberships if 'Senior' in m.get('level', '')]
        if senior:
            orgs = ', '.join(sorted({m.get('organization', '') for m in senior if m.get('organization')}))
            if orgs:
                accomplishments.append(f"Senior Member of {orgs}")

        projects = self.data.get('research_projects', [])
        initiative_parts = []
        for project in projects:
            name = project.get('name', '')
            count = str(project.get('count', '')).strip()
            if name and count:
                initiative_parts.append(f"<b>{name}</b> ({count})")
            elif name:
                initiative_parts.append(f"<b>{name}</b>")

        if accomplishments:
            highlight_line = '; '.join([self._emphasize_numbers(item) for item in accomplishments])
            self.story.append(Paragraph(highlight_line, self.styles['CVBody']))
            self.story.append(Spacer(1, 0.05*inch))

        if initiative_parts:
            initiatives_line = "Signature initiatives: " + '; '.join(initiative_parts) + "."
            self.story.append(Paragraph(initiatives_line, self.styles['CVBody']))
            self.story.append(Spacer(1, 0.08*inch))

    def _add_signature_initiatives(self):
        """Add signature initiatives/projects with impact metrics."""
        projects = self.data.get('research_projects', [])
        if not projects:
            return

        self._add_section('Signature Initiatives')

        for project in projects:
            name = project.get('name', '')
            count = str(project.get('count', '')).strip()
            description = project.get('description', '')

            left_flowables = [Paragraph(f"<b>{name}</b>", self.styles['CVBody'])]
            if description:
                left_flowables.append(Paragraph(description, self.styles['CVSmall']))

            right_flowables = []
            if count:
                right_flowables.append(Paragraph(count, self.styles['EntryMeta']))
                right_flowables.append(Paragraph('Impact signals', self.styles['CVSmall']))

            self.story.append(self._two_column_row(left_flowables, right_flowables))
            self.story.append(Spacer(1, 0.03*inch))

        self.story.append(Spacer(1, 0.06*inch))

    def _add_major_funding(self, top_n=4):
        """Highlight the most significant funded programs."""
        funding = self.data.get('funding', {})
        if not funding:
            return

        entries = []
        categories = [
            ('doe', 'DOE'),
            ('nsf', 'NSF'),
            ('darpa', 'DARPA'),
            ('international', 'International')
        ]

        for key, label in categories:
            for award in funding.get(key, []):
                amount = award.get('amount', '')
                entries.append({
                    'title': award.get('title', ''),
                    'role': award.get('role', ''),
                    'period': award.get('period', ''),
                    'amount': amount,
                    'amount_value': self._parse_amount(amount),
                    'label': label,
                    'program': award.get('program', '')
                })

        if not entries:
            return

        entries.sort(key=lambda x: x['amount_value'], reverse=True)
        featured = entries[:top_n]

        self._add_section('Major Funded Programs')

        for entry in featured:
            title = entry['title']
            role = entry['role']
            program = entry['program']
            period = entry['period']
            amount = entry['amount']
            label = entry['label']

            left_flowables = [Paragraph(f"<b>{title}</b>", self.styles['CVBody'])]
            meta_parts = [part for part in [role, program, label] if part]
            if meta_parts:
                left_flowables.append(Paragraph(' • '.join(meta_parts), self.styles['CVSmall']))

            right_flowables = []
            if amount:
                right_flowables.append(Paragraph(amount, self.styles['EntryMeta']))
            if period:
                right_flowables.append(Paragraph(period, self.styles['EntryMeta']))

            self.story.append(self._two_column_row(left_flowables, right_flowables))
            self.story.append(Spacer(1, 0.03*inch))

        self.story.append(Spacer(1, 0.08*inch))

    def _add_section(self, title):
        """Add a section heading."""
        self.story.append(Paragraph(title.upper(), self.styles['SectionHeading']))
        self.story.append(HRFlowable(width="100%", thickness=0.6,
                                     color=self.palette['border']))
        self.story.append(Spacer(1, 0.04*inch))

    def _two_column_row(self, left_flowables, right_flowables, col_widths=None):
        """Create a two-column row with aligned metadata."""
        if not isinstance(left_flowables, list):
            left_flowables = [left_flowables]
        if not isinstance(right_flowables, list):
            right_flowables = [right_flowables]
        if not right_flowables:
            right_flowables = [Spacer(1, 0)]
        table = Table([[left_flowables, right_flowables]],
                      colWidths=col_widths or [4.9*inch, 2.0*inch])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2)
        ]))
        return table

    def _add_appointments(self):
        """Add current and past appointments."""
        appointments = self.data.get('appointments', {})

        self._add_section('Professional Appointments')

        # Current positions
        current = appointments.get('current', [])
        if current:
            for appt in current:
                institution = appt.get('institution', '')
                country = appt.get('country', '')
                inst_line = f"{institution}, {country}" if country else institution

                self.story.append(self._two_column_row(
                    Paragraph(f"<b>{inst_line}</b>", self.styles['SubsectionHeading']),
                    Paragraph('', self.styles['EntryMeta'])
                ))

                for pos in appt.get('positions', []):
                    title = pos.get('title', '')
                    period = pos.get('period', '')
                    division = pos.get('division', '')

                    pos_text = f"{title}"
                    if division:
                        pos_text += f", {division}"
                    self.story.append(self._two_column_row(
                        Paragraph(pos_text, self.styles['CVBody']),
                        Paragraph(period, self.styles['EntryMeta'])
                    ))

                self.story.append(Spacer(1, 0.05*inch))

        # Past positions
        past = appointments.get('past', [])
        if past:
            for appt in past:
                institution = appt.get('institution', '')
                country = appt.get('country', '')
                dept = appt.get('department', '')

                inst_line = institution
                if dept:
                    inst_line += f", {dept}"
                if country:
                    inst_line += f", {country}"

                self.story.append(self._two_column_row(
                    Paragraph(f"<b>{inst_line}</b>", self.styles['SubsectionHeading']),
                    Paragraph('', self.styles['EntryMeta'])
                ))

                for pos in appt.get('positions', []):
                    title = pos.get('title', '')
                    period = pos.get('period', '')

                    self.story.append(self._two_column_row(
                        Paragraph(title, self.styles['CVBody']),
                        Paragraph(period, self.styles['EntryMeta'])
                    ))

                self.story.append(Spacer(1, 0.05*inch))

    def _add_education(self):
        """Add education section."""
        education = self.data.get('education', [])
        if not education:
            return

        self._add_section('Education')

        for edu in education:
            degree = edu.get('degree', '')
            year = edu.get('year', '')
            institution = edu.get('institution', '')
            country = edu.get('country', '')

            self.story.append(self._two_column_row(
                Paragraph(f"<b>{degree}</b>", self.styles['SubsectionHeading']),
                Paragraph(str(year), self.styles['EntryMeta'])
            ))

            inst_line = f"{institution}, {country}" if country else institution
            self.story.append(Paragraph(inst_line, self.styles['CVBody']))

            if edu.get('thesis_title'):
                self.story.append(Paragraph(
                    f"<i>Thesis: {edu['thesis_title']}</i>",
                    self.styles['CVSmall']
                ))

            self.story.append(Spacer(1, 0.05*inch))

    def _add_research(self):
        """Add research interests section."""
        research = self.data.get('research', {})
        if not research:
            return

        self._add_section('Research Focus')

        description = research.get('description', '')
        if description:
            clean_desc = self._strip_html(description)
            self.story.append(Paragraph(clean_desc, self.styles['CVBody']))
            self.story.append(Spacer(1, 0.04*inch))

        areas = research.get('areas', [])
        if areas:
            areas_text = '; '.join([f"<b>{area}</b>" for area in areas])
            focus_line = f"Focus areas: {areas_text}."
            self.story.append(Paragraph(focus_line, self.styles['CVBody']))
            self.story.append(Spacer(1, 0.08*inch))

    def _add_selected_publications(self, count=10):
        """Add selected recent publications."""
        if not self.publications:
            return

        self._add_section(f'Selected Recent Publications (Last {count})')

        pub_number = len(self.publications)
        shown = 0

        for pub in self.publications:
            if shown >= count:
                break

            # Format publication
            authors = self._normalize_bibtex_text(pub.get('author', ''))
            title = self._normalize_bibtex_text(pub.get('title', ''))
            year = pub.get('year', 'n.d.')

            # Get venue info
            venue = pub.get('booktitle') or pub.get('journal') or ''
            venue = self._normalize_bibtex_text(venue)

            # Build citation
            citation_parts = []
            if authors:
                # Bold my name in author list
                authors = authors.replace('Ferreira da Silva, Rafael', '<b>Ferreira da Silva, Rafael</b>')
                authors = authors.replace('da Silva, Rafael Ferreira', '<b>da Silva, Rafael Ferreira</b>')
                citation_parts.append(authors)

            if title:
                citation_parts.append(f'"{title}"')

            if venue:
                citation_parts.append(f"<i>{venue}</i>")

            # Add year and DOI
            if year:
                citation_parts.append(str(year))

            if pub.get('doi'):
                citation_parts.append(f"DOI: {pub.get('doi')}")

            citation = '. '.join(citation_parts) + '.'

            # Add numbering to citation
            numbered_citation = f"[{pub_number}] {citation}"
            self.story.append(Paragraph(numbered_citation, self.styles['Publication']))
            pub_number -= 1
            shown += 1

        self.story.append(Spacer(1, 0.08*inch))

    def _add_publications(self):
        """Add all publications from BibTeX."""
        if not self.publications:
            return

        self._add_section(f'Publications ({len(self.publications)} total)')

        current_year = None
        pub_number = len(self.publications)  # Start from total and count down

        for pub in self.publications:
            year = pub.get('year', 'n.d.')

            # Add year heading
            if year != current_year:
                current_year = year
                self.story.append(Spacer(1, 0.04*inch))
                self.story.append(Paragraph(
                    f"<b>{year}</b>",
                    self.styles['SubsectionHeading']
                ))

            # Format publication
            authors = self._normalize_bibtex_text(pub.get('author', ''))
            title = self._normalize_bibtex_text(pub.get('title', ''))

            # Get venue info
            venue = pub.get('booktitle') or pub.get('journal') or ''
            venue = self._normalize_bibtex_text(venue)

            # Build citation
            citation_parts = []
            if authors:
                # Bold my name in author list
                authors = authors.replace('Ferreira da Silva, Rafael', '<b>Ferreira da Silva, Rafael</b>')
                authors = authors.replace('da Silva, Rafael Ferreira', '<b>da Silva, Rafael Ferreira</b>')
                citation_parts.append(authors)

            if title:
                citation_parts.append(f'"{title}"')

            if venue:
                citation_parts.append(f"<i>{venue}</i>")

            # Add year and DOI
            if year:
                citation_parts.append(str(year))

            if pub.get('doi'):
                citation_parts.append(f"DOI: {pub.get('doi')}")

            citation = '. '.join(citation_parts) + '.'

            # Add numbering to citation
            numbered_citation = f"[{pub_number}] {citation}"
            self.story.append(Paragraph(numbered_citation, self.styles['Publication']))
            pub_number -= 1

    def _add_funding(self):
        """Add all funding awards."""
        funding = self.data.get('funding', {})
        if not funding:
            return

        self._add_section('Funding Awards')

        # Total funding summary
        total = funding.get('total_funding', {})
        if total:
            summary = f"<b>Total: {total.get('amount', '')}</b> across {total.get('projects', '')} competitively reviewed proposals"
            self.story.append(Paragraph(summary, self.styles['CVBody']))
            self.story.append(Spacer(1, 0.08*inch))

        # DOE Awards
        doe = funding.get('doe', [])
        if doe:
            self.story.append(Paragraph('<b>U.S. Department of Energy (DOE)</b>',
                                       self.styles['SubsectionHeading']))
            for award in doe:
                title = award.get('title', '')
                period = award.get('period', '')
                amount = award.get('amount', '')
                role = award.get('role', '')

                self.story.append(self._two_column_row(
                    Paragraph(f"<b>{title}</b>", self.styles['CVBody']),
                    Paragraph(amount, self.styles['EntryMeta'])
                ))
                detail_parts = [part for part in [role, period] if part]
                self.story.append(Paragraph(', '.join(detail_parts), self.styles['CVSmall']))
                self.story.append(Spacer(1, 0.03*inch))
            self.story.append(Spacer(1, 0.04*inch))

        # NSF Awards
        nsf = funding.get('nsf', [])
        if nsf:
            self.story.append(Paragraph('<b>U.S. National Science Foundation (NSF)</b>',
                                       self.styles['SubsectionHeading']))
            for award in nsf:
                title = award.get('title', '')
                period = award.get('period', '')
                amount = award.get('amount', '')
                role = award.get('role', '')

                self.story.append(self._two_column_row(
                    Paragraph(f"<b>{title}</b>", self.styles['CVBody']),
                    Paragraph(amount, self.styles['EntryMeta'])
                ))

                awards_list = award.get('awards', [])
                award_nums = ', '.join([f"#{a.get('id', '')}" for a in awards_list if a.get('id')])

                detail_parts = [part for part in [role, period] if part]
                detail = ', '.join(detail_parts)
                if award_nums:
                    detail += f" ({award_nums})"

                self.story.append(Paragraph(detail, self.styles['CVSmall']))
                self.story.append(Spacer(1, 0.03*inch))
            self.story.append(Spacer(1, 0.04*inch))

        # DARPA Awards
        darpa = funding.get('darpa', [])
        if darpa:
            self.story.append(Paragraph('<b>U.S. Defense Advanced Research Projects Agency (DARPA)</b>',
                                       self.styles['SubsectionHeading']))
            for award in darpa:
                title = award.get('title', '')
                period = award.get('period', '')
                amount = award.get('amount', '')
                role = award.get('role', '')

                self.story.append(self._two_column_row(
                    Paragraph(f"<b>{title}</b>", self.styles['CVBody']),
                    Paragraph(amount, self.styles['EntryMeta'])
                ))
                detail_parts = [part for part in [role, period] if part]
                self.story.append(Paragraph(', '.join(detail_parts), self.styles['CVSmall']))
                self.story.append(Spacer(1, 0.03*inch))
            self.story.append(Spacer(1, 0.04*inch))

        # International/Other
        intl = funding.get('international', [])
        if intl:
            self.story.append(Paragraph('<b>International Funding / Collaborations / Others</b>',
                                       self.styles['SubsectionHeading']))
            for award in intl:
                title = award.get('title', '')
                period = award.get('period', '')
                amount = award.get('amount', '')
                role = award.get('role', '')

                self.story.append(self._two_column_row(
                    Paragraph(f"<b>{title}</b>", self.styles['CVBody']),
                    Paragraph(amount, self.styles['EntryMeta'])
                ))

                detail_parts = [part for part in [role, period] if part]
                self.story.append(Paragraph(', '.join(detail_parts), self.styles['CVSmall']))
                self.story.append(Spacer(1, 0.03*inch))

    def _add_awards(self):
        """Add awards and honors section with enhanced visual design."""
        awards = self.data.get('awards', [])
        if not awards:
            return

        self._add_section(f'Awards & Honors ({len(awards)} Best Paper Awards)')

        for award in awards:
            title = award.get('title', '')
            year = award.get('year', '')
            event = award.get('event', '')
            org = award.get('organization', '')
            paper = award.get('paper', '')

            award_line = f"<b>{title}</b>"
            if event:
                award_line += f" • {event}"
            elif org:
                award_line += f" • {org}"

            self.story.append(self._two_column_row(
                Paragraph(award_line, self.styles['CVBody']),
                Paragraph(str(year), self.styles['EntryMeta'])
            ))

            if paper:
                self.story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;<i>{paper}</i>", self.styles['CVSmall']))

            self.story.append(Spacer(1, 0.02*inch))

    def _add_professional_activities(self):
        """Add all professional activities."""
        activities = self.data.get('professional_activities', {})

        if not self.activities and not activities:
            return

        self._add_section('Professional Activities')

        # Steering Committees (from rafael.yml)
        steering_committees = activities.get('steering_committees', [])
        if steering_committees:
            self.story.append(Paragraph('<b>Steering Committees</b>',
                                       self.styles['SubsectionHeading']))
            for item in steering_committees:
                org = item.get('organization', '')
                role = item.get('role', '')
                period = item.get('period', '')

                self.story.append(self._two_column_row(
                    Paragraph(f"{role}, {org}", self.styles['CVBody']),
                    Paragraph(period, self.styles['EntryMeta'])
                ))
            self.story.append(Spacer(1, 0.06*inch))

        # Advisory Boards (from rafael.yml)
        advisory_boards = activities.get('advisory_boards', [])
        if advisory_boards:
            self.story.append(Paragraph('<b>Advisory Boards</b>',
                                       self.styles['SubsectionHeading']))
            for item in advisory_boards:
                name = item.get('name', '')
                board_type = item.get('type', '')
                period = item.get('period', '')
                note = item.get('note', '')

                text = f"{name} ({board_type})"
                if note:
                    text += f" — {note}"

                self.story.append(self._two_column_row(
                    Paragraph(text, self.styles['CVBody']),
                    Paragraph(period, self.styles['EntryMeta'])
                ))
            self.story.append(Spacer(1, 0.06*inch))

        # Conference Chair Roles
        chair_data = self.activities.get('chair', [])
        if chair_data:
            self.story.append(Paragraph('<b>Conference/Workshop Chair Roles</b>',
                                       self.styles['SubsectionHeading']))
            for conf in chair_data:
                conf_name = conf.get('conference', '')
                series = conf.get('series', '')
                for entry in conf.get('entries', []):
                    role = entry.get('role', '')
                    year = entry.get('year', '')
                    location = entry.get('location', '')

                    text = f"{role}, {conf_name}"
                    if series:
                        text += f" ({series})"
                    text += f", {location}, {year}"

                    self.story.append(Paragraph(text, self.styles['CVBody']))
            self.story.append(Spacer(1, 0.06*inch))

        # Program Committee
        pc_data = self.activities.get('pc', [])
        if pc_data:
            self.story.append(Paragraph('<b>Program Committee Member</b>',
                                       self.styles['SubsectionHeading']))

            # Group by conference
            for conf in pc_data:
                conf_name = conf.get('conference', '')
                series = conf.get('series', '')
                entries = conf.get('entries', [])

                years = [str(e.get('year', '')) for e in entries]
                years_str = ', '.join(years)

                text = conf_name
                if series:
                    text += f" ({series})"
                text += f": {years_str}"

                self.story.append(Paragraph(text, self.styles['CVBody']))
            self.story.append(Spacer(1, 0.06*inch))

        # Editorial positions
        editorial = activities.get('editorial', [])
        if editorial:
            self.story.append(Paragraph('<b>Editorial Positions</b>',
                                       self.styles['SubsectionHeading']))
            for item in editorial:
                journal = item.get('journal', '')
                role = item.get('role', '')
                period = item.get('period', '')

                self.story.append(Paragraph(
                    f"{role}, <i>{journal}</i> ({period})",
                    self.styles['CVBody']
                ))
            self.story.append(Spacer(1, 0.06*inch))

        # Funding Reviewer
        funding_rev = activities.get('funding_reviewer', [])
        if funding_rev:
            self.story.append(Paragraph('<b>Funding Review Panels</b>',
                                       self.styles['SubsectionHeading']))
            for item in funding_rev:
                agency = item.get('agency', '')
                role = item.get('role', '')
                period = item.get('period', '')

                self.story.append(Paragraph(
                    f"{role}, {agency} ({period})",
                    self.styles['CVBody']
                ))

    def _add_invited_talks(self):
        """Add all invited talks."""
        talks = self.data.get('invited_talks', [])
        if not talks:
            return

        self._add_section('Invited Talks')

        for year_group in talks:
            year = year_group.get('year', '')
            entries = year_group.get('entries', [])

            self.story.append(Paragraph(f"<b>{year}</b>", self.styles['SubsectionHeading']))

            for talk in entries:
                title = talk.get('title', '')
                event = talk.get('event', '')
                location = talk.get('location', '')

                self.story.append(Paragraph(
                    f"<b>{title}</b>",
                    self.styles['CVBody']
                ))
                self.story.append(Paragraph(
                    f"{event}, {location}",
                    self.styles['CVSmall']
                ))
                self.story.append(Spacer(1, 0.03*inch))

    def _add_teaching(self):
        """Add teaching experience."""
        teaching = self.data.get('teaching', [])
        if not teaching:
            return

        self._add_section('Teaching Experience')

        for course in teaching:
            institution = course.get('institution', '')
            course_name = course.get('course', '')
            level = course.get('level', '')
            semester = course.get('semester', '')

            self.story.append(self._two_column_row(
                Paragraph(f"<b>{course_name}</b> ({level})", self.styles['SubsectionHeading']),
                Paragraph(semester, self.styles['EntryMeta'])
            ))
            self.story.append(Paragraph(
                f"{institution}",
                self.styles['CVBody']
            ))
            self.story.append(Spacer(1, 0.04*inch))

    def _add_students(self):
        """Add students and mentoring section."""
        students = self.data.get('students', {})
        if not students:
            return

        self._add_section('Students & Mentoring')

        # PhD Students
        phd = students.get('phd', [])
        if phd:
            self.story.append(Paragraph('<b>PhD Students</b>',
                                       self.styles['SubsectionHeading']))
            for student in phd:
                name = student.get('name', '')
                degree = student.get('degree', '')
                period = student.get('period', '')

                self.story.append(Paragraph(
                    f"{name}, {degree} ({period})",
                    self.styles['CVBody']
                ))
            self.story.append(Spacer(1, 0.05*inch))

        # Student Workers
        workers = students.get('worker', [])
        if workers:
            self.story.append(Paragraph('<b>Student Workers / Interns</b>',
                                       self.styles['SubsectionHeading']))
            for student in workers:
                name = student.get('name', '')
                degree = student.get('degree', '')
                period = student.get('period', '')

                self.story.append(Paragraph(
                    f"{name}, {degree} ({period})",
                    self.styles['CVBody']
                ))
            self.story.append(Spacer(1, 0.05*inch))

        # Directed Research
        dr = students.get('dr', [])
        if dr:
            self.story.append(Paragraph('<b>Directed Research Students</b>',
                                       self.styles['SubsectionHeading']))
            for student in dr:
                name = student.get('name', '')
                degree = student.get('degree', '')
                period = student.get('period', '')

                self.story.append(Paragraph(
                    f"{name}, {degree} ({period})",
                    self.styles['CVBody']
                ))
            self.story.append(Spacer(1, 0.05*inch))

        # Thesis Committee
        committee = students.get('thesis_committee', [])
        if committee:
            self.story.append(Paragraph('<b>Thesis Committee Member</b>',
                                       self.styles['SubsectionHeading']))
            for student in committee:
                name = student.get('name', '')
                degree = student.get('degree', '')
                institution = student.get('institution', '')
                year = student.get('year', '')

                self.story.append(Paragraph(
                    f"{name}, {degree}, {institution} ({year})",
                    self.styles['CVBody']
                ))

    def _add_affiliations(self):
        """Add memberships and certifications."""
        personal = self.data.get('personal', {})
        memberships = personal.get('memberships', [])
        certifications = personal.get('certifications', [])

        if not memberships and not certifications:
            return

        self._add_section('Affiliations & Certifications')

        if memberships:
            self.story.append(Paragraph('<b>Professional Memberships</b>',
                                       self.styles['SubsectionHeading']))
            for membership in memberships:
                org = membership.get('organization', '')
                level = membership.get('level', '')
                period = membership.get('period', '')
                title = org
                if level:
                    title += f", {level}"
                self.story.append(self._two_column_row(
                    Paragraph(title, self.styles['CVBody']),
                    Paragraph(period, self.styles['EntryMeta'])
                ))
            self.story.append(Spacer(1, 0.05*inch))

        if certifications:
            self.story.append(Paragraph('<b>Certifications</b>',
                                       self.styles['SubsectionHeading']))
            for cert in certifications:
                title = cert.get('title', '')
                organization = cert.get('organization', '')
                date = cert.get('date', '')
                left_text = title
                if organization:
                    left_text += f", {organization}"
                self.story.append(self._two_column_row(
                    Paragraph(left_text, self.styles['CVBody']),
                    Paragraph(date, self.styles['EntryMeta'])
                ))

    def _add_footer(self):
        """Add footer separator."""
        self.story.append(Spacer(1, 0.2*inch))
        self.story.append(HRFlowable(width="100%", thickness=0.5,
                                     color=self.palette['border']))
        updated = datetime.now().strftime("%B %Y")
        self.story.append(Spacer(1, 0.06*inch))
        self.story.append(Paragraph(f"Last updated: {updated}", self.styles['CVSmall']))

    def generate(self, output_path):
        """Generate the comprehensive PDF CV."""
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.65*inch,
            leftMargin=0.65*inch,
            topMargin=0.65*inch,
            bottomMargin=0.65*inch
        )

        # Build the CV content - organized for maximum recruiter impact
        print("Building CV sections...")

        # Page 1: Header and Executive Summary with metrics
        self._add_header()
        self._add_executive_summary()

        # Page 1-2: Professional experience
        self._add_major_funding()
        self._add_appointments()
        self._add_education()
        self._add_research()

        # Page 2-3: Recent work and awards
        self._add_selected_publications(count=10)
        self._add_awards()

        # Compact funding summary
        self._add_funding()

        # Page break before supporting sections
        # self.story.append(PageBreak())

        # Supporting sections: Activities, talks, teaching
        self._add_professional_activities()
        self._add_invited_talks()
        self._add_teaching()
        self._add_affiliations()
        self._add_students()

        # Page break before full publication list
        # self.story.append(PageBreak())

        # Complete publication record
        self._add_publications()

        self._add_footer()

        # Build PDF
        print("Generating PDF...")
        doc.build(self.story)
        print(f"✓ Comprehensive CV generated successfully: {output_path}")


def main():
    """Main function to generate the comprehensive CV."""
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    yaml_path = os.path.join(project_root, '_data', 'rafael.yml')

    # Output path with current date
    output_filename = 'RafaelFerreiraDaSilva-cv.pdf'
    output_path = os.path.join(project_root, 'files', 'cv', output_filename)

    # Check if YAML file exists
    if not os.path.exists(yaml_path):
        print(f"Error: YAML file not found at {yaml_path}")
        return

    print(f"Generating comprehensive CV from {yaml_path}...")
    print(f"Loading publications and activities data...")

    # Generate CV
    generator = CVGenerator(yaml_path, project_root)
    generator.generate(output_path)

    print(f"\n✓ CV Location: {output_path}")
    print(f"✓ File size: {os.path.getsize(output_path) / 1024:.1f} KB")

    if generator.publications:
        print(f"✓ Included {len(generator.publications)} publications")

    activity_counts = sum(len(v) if isinstance(v, list) else 0 for v in generator.activities.values())
    if activity_counts:
        print(f"✓ Included professional activities from {len(generator.activities)} categories")


if __name__ == '__main__':
    main()
