# CV Generation Scripts

This directory contains scripts for generating comprehensive CV documents from the centralized data file (`_data/rafael.yml`), including all publications from BibTeX and professional activities.

## Generate Complete PDF CV

### Prerequisites

Create a virtual environment and install the required Python packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

Or install individually:
```bash
pip install reportlab pyyaml bibtexparser
```

### Usage

```bash
source .venv/bin/activate  # Activate virtual environment if needed
python scripts/generate_cv_pdf.py
```

This will generate a comprehensive PDF CV with:
- **Executive Summary** with key metrics (funding, publications, awards)
- **Modern, recruiter-friendly layout** highlighting major accomplishments first
- **All data from YAML file** (`_data/rafael.yml`)
- **All publications** from BibTeX file (`_bibliography/references.bib`)
- **All professional activities** from activities YAML files (`_data/activities_*.yml`)
- **Professional formatting** optimized for impact and readability
- **Current date in filename** (e.g., `RafaelFerreiraDaSilva-cv-2026-01.pdf`)
- **Output location**: `files/cv/`

### What's Included

The CV is organized for maximum recruiter impact with major accomplishments highlighted first:

#### Page 1: Executive Summary & Highlights
- **Header**: Name, titles, contact information
- **Executive Summary**: Professional introduction with key metrics dashboard
  - Total funded projects and funding amount
  - Total publications count
  - Best paper awards count
- **Key Accomplishments**: Bulleted highlights of major funding, awards, and leadership

#### Page 1-2: Professional Experience & Background
- **Professional Appointments**: Current and past positions with full details
- **Education**: All degrees with thesis information
- **Research Interests**: Complete list of research areas

#### Page 2-3: Recent Work & Recognition
- **Selected Recent Publications**: Last 10 publications for quick scanning
- **Awards & Honors**: All best paper awards with visual indicators
- **Funding Awards**: Complete funding history (DOE, NSF, DARPA, international)

#### Supporting Sections
- **Professional Activities**: Steering committees, chair roles, program committees, editorial positions
- **Invited Talks**: Complete chronological list
- **Teaching & Mentoring**: Courses taught, PhD students, interns, thesis committees

#### Complete Publications Record
- **All Publications**: Full numbered list sorted by year (156 total)
- **Auto-formatting**: Your name automatically bolded in author lists
- **DOI links**: Included when available

### Output Statistics

The script will display:
- Total number of publications included
- Number of activity categories loaded
- Final PDF file size

Example output:
```
Generating comprehensive CV from _data/rafael.yml...
Loading publications and activities data...
Loaded 150 publications from BibTeX file
Building CV sections...
Generating PDF...
✓ Comprehensive CV generated successfully

✓ CV Location: files/cv/RafaelFerreiraDaSilva-cv-2025-01.pdf
✓ File size: 285.3 KB
✓ Included 150 publications
✓ Included professional activities from 7 categories
```

### Customization

To modify the CV layout or content:
1. Edit `generate_cv_pdf.py`
2. Modify the `CVGenerator` class methods
3. Adjust styles in `_create_styles()` method
4. Change colors, fonts, spacing, or sections as needed

### Color Scheme

The CV uses a professional blue/gray color scheme:
- **Headings**: `#1a365d` (dark blue)
- **Subheadings**: `#2d3748` (dark gray)
- **Body text**: `#4a5568` (medium gray)
- **Small text**: `#718096` (light gray)
- **Accents**: `#cbd5e0` (very light gray)

### Font Sizes

- Name: 22pt (bold)
- Titles: 11pt
- Section headings: 13pt (bold)
- Subsection headings: 10pt (bold)
- Body text: 9pt
- Small text/captions: 8.5pt

### Page Layout

- **Page size**: US Letter (8.5" × 11")
- **Margins**: 0.65" on all sides
- **Spacing**: Optimized for readability and impact
- **Page breaks**: Strategic breaks to separate core content from supporting materials
- **Visual elements**: Metrics dashboard with bordered table, trophy icons for awards
- **Recruiter-optimized**: Most important information (summary, accomplishments, recent work) on first 2-3 pages

### Dependencies

- **reportlab**: High-quality PDF generation
- **pyyaml**: YAML file parsing
- **bibtexparser**: BibTeX bibliography parsing

### Troubleshooting

If bibtexparser is not installed, the script will run but skip the publications section with a warning:
```
Warning: bibtexparser not installed. Publications will be skipped.
Install with: pip install bibtexparser
```

### Future Enhancements

Possible additions:
- LaTeX CV generation option
- HTML CV export
- Configurable templates/themes
- Citation count integration
- h-index display
