# tools/

Versioned helper scripts for the vault. Outside wiki operations (not hooks, not
subagents). Run them manually; they never fire automatically.

## pdf2md.py — PDF → Markdown (preserves images)

**Use this whenever a PDF should become markdown** (books, documents, resources).
General-purpose: extracts the text layer *and* every embedded image, writes one
`.md` plus an `assets/` folder, and prints a report.

```
python3 tools/pdf2md.py <input.pdf> --report     # analyze only (pages, text, images, scanned?)
python3 tools/pdf2md.py <input.pdf>              # convert -> <stem>/<stem>.md + <stem>/assets/
```

**Workflow / deletion policy:**
1. Run with `--report` first.
2. Convert. The tool **preserves images/graphs** into `assets/` and references them inline.
3. **Delete the source PDF only after** the report's verdict says "safe to delete" — i.e. text captured, all images saved, and it is not a scanned/OCR-needed PDF. The tool refuses to greenlight scanned PDFs (no text layer → would need OCR via `tesseract`, not yet installed).

**Conventions:**
- Books live in `inbox/books/`, one `.md` per book.
- For a *collection* (e.g. Kafka *The Complete Stories*), split into one file per
  text by parsing the table of contents, plus an `index.md`. `pdf2md.py` does the
  whole-PDF conversion; the per-chapter/story split is a per-book step (every TOC
  differs). Watch for ebook artifacts: titles broken across lines, and OCR typos
  in body headings (e.g. "A Common Contusion" for "Confusion").
- Bulky source PDFs stay local-cold via `.gitignore` (`inbox/**/*.pdf`,
  `raw/**/*.pdf`); the resulting markdown is tracked (mind copyright before
  committing full source texts to a public repo).

**Dependencies:** PyMuPDF (`pip3 install --user pymupdf`). Optional cross-check
tools from poppler (`brew install poppler`): `pdftotext`, `pdfimages`, `pdfinfo`,
`pdftoppm` (the last also lets Claude render PDF pages visually).

## Other scripts

- **lint-scan.py** — read-only mechanical pre-pass for `/wiki-lint` (stdout JSON). See CLAUDE.md §B.13.
- **optimize-images.py** — downscale/recompress oversized images referenced from wiki pages.
