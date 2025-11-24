# EvidenceSeeker-Ergebnisse

This repository hosts the results of the [EvidenceSeeker](https://github.com/debatelab/evidence-seeker) project, automatically built and deployed as a static website using MkDocs and GitHub Pages.

## 🌐 Live Site

The site is automatically deployed to GitHub Pages and can be accessed at the repository's GitHub Pages URL.

## 📋 Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── pages.yml           # GitHub Actions workflow for automated deployment
├── data/                        # Source data organized by date
│   └── YYYY_MM_DD/
│       ├── *.md                # Markdown result files
│       └── *.yaml              # YAML result data files
├── docs/                        # MkDocs documentation source
│   ├── extra_styles.css        # Custom CSS styles
│   ├── main_idea.md            # Documentation page explaining the concept
│   ├── img/                    # Images and icons
│   └── results/                # Generated result pages (created by hooks)
├── hooks/
│   └── initialisation.py       # MkDocs hook for generating result pages
├── overrides/                   # Theme customization
│   └── partials/
│       ├── copyright.html
│       └── source.html
├── src/                         # Source code (if any)
├── templates/                   # Jinja2 templates for page generation
│   ├── index.tmpl              # Template for index page
│   └── result.tmpl             # Template for individual result pages
├── mkdocs.yml                   # MkDocs configuration file
├── requirements.txt             # Python dependencies
└── LICENSE
```

## 🚀 Automated GitHub Pages Deployment

The site is automatically built and deployed using GitHub Actions as defined in `.github/workflows/pages.yml`.

### How It Works

1. **Trigger**: The workflow runs:
   - Every day at 2:00 AM UTC (cron: `0 2 * * *`)
   - Manually via the "Actions" tab in GitHub (workflow_dispatch)

2. **Build Process**:
   - Checks out the repository
   - Sets up Python 3.12
   - Installs dependencies from `requirements.txt`
   - Runs `mkdocs build` to generate the static site
   - Adds a `.nojekyll` file to ensure GitHub Pages serves the site correctly
   - Uploads the built site as an artifact

3. **Deployment**:
   - Deploys the built site to GitHub Pages
   - The site becomes available at the configured GitHub Pages URL

### Required Permissions

The workflow requires the following permissions:
- `contents: read` - To read the repository content
- `pages: write` - To deploy to GitHub Pages
- `id-token: write` - For authentication

## 🔨 Building Locally for Testing

To test the site locally before pushing changes:

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/debatelab/evidence-seeker-results.git
   cd evidence-seeker-results
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Build and Preview

#### Option 1: Live Development Server (Recommended)

Start a local development server with auto-reload:

```bash
mkdocs serve
```

This will:
- Build the site
- Start a local server at `http://127.0.0.1:8000`
- Automatically rebuild when you make changes
- Execute the initialization hook to generate result pages

#### Option 2: Build Static Site

To build the site without serving it:

```bash
mkdocs build
```

The built site will be in the `./site` directory. You can then serve it with any static file server, for example:

```bash
python -m http.server --directory site 8000
```

### Clean Build

To remove the built site and start fresh:

```bash
rm -rf site
mkdocs build
```

## 🎨 MkDocs Configuration

The site is configured in `mkdocs.yml` with the following features:

### Theme
- **Material for MkDocs** theme with custom overrides
- German language (`language: de`)
- Deep purple primary color with indigo accent
- Custom favicon and logo

### Markdown Extensions
- `attr_list` & `md_in_html` - Enhanced HTML/attribute support
- `pymdownx.emoji` - Emoji support with Material icons
- `admonition` & `pymdownx.details` - Collapsible content blocks
- `pymdownx.superfences` - Advanced code blocks
- `abbr` & `pymdownx.snippets` - Abbreviations and content snippets

### Hooks
- `hooks/initialisation.py` - Runs at build time to:
  - Load result data from `data/` directory
  - Generate result pages in `docs/results/`
  - Create the index page with all results

### Navigation
- Home page (index.md)
- Grundidee (main_idea.md) - Explains the concept

## 🔗 Links

- **Main Project**: [debatelab/evidence-seeker](https://github.com/debatelab/evidence-seeker)
- **Documentation**: [EvidenceSeeker Docs](https://debatelab.github.io/evidence-seeker)
- **Results Site**: This repository's GitHub Pages

## 📝 License

See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This repository is automatically updated with results from the EvidenceSeeker project. For contributions to the main project, please visit the [evidence-seeker repository](https://github.com/debatelab/evidence-seeker).
