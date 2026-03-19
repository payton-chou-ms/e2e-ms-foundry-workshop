# Workshop Documentation

This folder contains the MkDocs documentation for the Foundry IQ + Fabric IQ Workshop.

## Source Of Truth

Use `workshop/docs/` as the only authored source for user-facing workshop content.

- `workshop/site/` is generated output from local MkDocs builds.
- root `site/` is generated output from the GitHub Pages workflow.
- `guides/` should contain distribution artifacts or audit notes, not a second authored copy of the same instructions.

## Local Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Serve Locally

```bash
mkdocs serve
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to preview.

### Build Static Site

```bash
mkdocs build
```

Output is in the `site/` folder.

## Deploy to GitHub Pages

```bash
mkdocs gh-deploy
```

This builds the site and pushes to the `gh-pages` branch.

## Structure

```
workshop/
├── mkdocs.yml              # MkDocs configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── docs/
    ├── index.md           # Overview
    ├── 00-get-started/    # Prerequisites & workshop flow
    ├── 01-deploy/         # Deploy Solution
    │   ├── index.md
    │   ├── 00-admin-deploy-share.md
    │   ├── 00-participant-run-validate.md
    │   ├── 01-deploy-azure.md
    │   ├── 02-setup-fabric.md
    │   ├── 03-configure.md
    │   └── 04-run-scenario.md
    ├── 02-customize/      # Customize for Your Customer
    │   ├── index.md
    │   ├── 02-generate.md
    │   └── 03-demo.md
    ├── 03-understand/     # Understand the Technology
    │   ├── index.md
    │   ├── 01-foundry-iq.md
    │   └── 02-fabric-iq.md
    └── 04-cleanup/        # Cleanup & Next Steps
```
