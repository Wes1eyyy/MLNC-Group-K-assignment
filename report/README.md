# LaTeX Report Directory

## Purpose
This directory contains the LaTeX source files for the final report submission.

## Development Plan

### Directory Structure:
- **main.tex** - Main LaTeX document that includes all sections
- **sections/** - Individual section files for modularity
  - introduction.tex
  - methodology.tex
  - feature_engineering.tex
  - model_development.tex
  - results.tex
  - discussion.tex
  - conclusion.tex
- **references.bib** - BibTeX bibliography file
- **figures/** - Symbolic link or copy of figures from ../figures/

### Compilation Instructions:

To compile the report:
```bash
cd report/
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Or use latexmk for automatic compilation:
```bash
latexmk -pdf main.tex
```

### Writing Guidelines:

1. **Structure**
   - Follow academic paper format
   - Each section should flow logically
   - Use subsections for organization
   - Include abstract (150-250 words)

2. **Length**
   - Check assignment requirements for page limits
   - Typically 8-12 pages for this type of project
   - Be concise but complete

3. **Figures and Tables**
   - Number all figures and tables
   - Add descriptive captions
   - Reference in text before they appear
   - Use high-quality images (300 DPI)

4. **Citations**
   - Cite all sources and methods used
   - Use consistent citation style
   - Include 10-15+ relevant references

5. **Style**
   - Use third person, passive voice
   - Be precise and technical
   - Avoid colloquialisms
   - Proofread carefully

6. **Equations**
   - Number important equations
   - Define all variables
   - Use consistent notation

### Quality Checklist:
- [ ] All sections completed
- [ ] Figures numbered and captioned
- [ ] Tables formatted properly
- [ ] References cited correctly
- [ ] Bibliography complete
- [ ] No LaTeX compilation errors
- [ ] Consistent formatting
- [ ] Proofread for typos and grammar
- [ ] Page limits met
- [ ] All requirements addressed

### Submission:
- Final file: report.pdf
- Include in submission package with notebook and CSV
