#!/usr/bin/env python3
"""pdf2md.py — convert a PDF to Markdown while preserving embedded images.

General-purpose PDF → Markdown converter for the vault. Extracts the text layer
and every embedded raster image, writes one .md plus an assets/ folder, and
prints a report so the original PDF is only deleted after capture is verified.

This is the GENERAL tool (text + images, one file out). Splitting a book into
one file per chapter/story is a separate, per-book step (the table of contents
differs every time); see the Kafka conversion for that pattern.

Usage:
    python3 tools/pdf2md.py <input.pdf> [--outdir DIR] [--report]

    --report   Analyze only: page count, text size, image count, scanned-or-not.
               Writes nothing. Use this before deciding to convert/delete.
    --outdir   Destination folder (default: alongside the PDF, named after it).

Dependencies: PyMuPDF (`pip3 install --user pymupdf`). Optional: poppler
(`brew install poppler`) enables `pdfimages`/`pdftotext` as a cross-check.

Deletion policy: delete the source PDF only after the report shows text + all
images captured (no "looks scanned / needs OCR" warning, image counts match).
Scanned PDFs have no text layer; this tool flags them for OCR rather than
silently producing an empty file.
"""
import sys, os, re, argparse

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("Mangler PyMuPDF. Installer med: pip3 install --user pymupdf")


def reflow(text):
    """Join PDF line-wrapped lines into clean paragraphs (blank line = break)."""
    # strip stray control chars from extraction (NUL etc.) so the .md stays text
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    out = []
    for para in re.split(r'\n[ \t]*\n', text.strip()):
        para = re.sub(r'[ \t]*\n[ \t]*', ' ', para).strip()
        para = re.sub(r' {2,}', ' ', para)
        if para:
            out.append(para)
    return "\n\n".join(out)


def analyze(doc):
    """Return (pages, text_chars, image_count, looks_scanned)."""
    text_chars = 0
    image_count = 0
    pages_with_text = 0
    for page in doc:
        t = page.get_text("text")
        text_chars += len(t.strip())
        if len(t.strip()) > 40:
            pages_with_text += 1
        image_count += len(page.get_images(full=True))
    # Heuristic: many pages, almost no text, but images present -> scanned.
    looks_scanned = (doc.page_count > 0
                     and pages_with_text < doc.page_count * 0.2
                     and image_count >= doc.page_count * 0.5)
    return doc.page_count, text_chars, image_count, looks_scanned


def convert(pdf_path, outdir):
    doc = fitz.open(pdf_path)
    stem = os.path.splitext(os.path.basename(pdf_path))[0]
    assets = os.path.join(outdir, "assets")
    os.makedirs(outdir, exist_ok=True)

    md = [f"# {stem}\n"]
    saved = 0
    for pno, page in enumerate(doc, 1):
        body = reflow(page.get_text("text"))
        # strip the recurring "Page N" footer some PDFs carry
        body = re.sub(r'(?m)^\s*Page \d+\s*$', '', body).strip()
        if body:
            md.append(body)
        for ino, img in enumerate(page.get_images(full=True), 1):
            xref = img[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha >= 4:  # CMYK/other -> RGB
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                os.makedirs(assets, exist_ok=True)
                name = f"p{pno:03d}-img{ino:02d}.png"
                pix.save(os.path.join(assets, name))
                md.append(f"![{stem} – s.{pno} bilde {ino}](assets/{name})")
                saved += 1
                pix = None
            except Exception as e:
                md.append(f"<!-- klarte ikke hente bilde p{pno} #{ino}: {e} -->")

    out_md = os.path.join(outdir, f"{stem}.md")
    with open(out_md, "w") as f:
        f.write("\n\n".join(md) + "\n")
    return out_md, saved


def main():
    ap = argparse.ArgumentParser(description="PDF -> Markdown med bildebevaring")
    ap.add_argument("pdf")
    ap.add_argument("--outdir")
    ap.add_argument("--report", action="store_true", help="Analyser uten å skrive")
    args = ap.parse_args()

    if not os.path.isfile(args.pdf):
        sys.exit(f"Finner ikke: {args.pdf}")

    doc = fitz.open(args.pdf)
    pages, chars, imgs, scanned = analyze(doc)
    print(f"PDF:    {args.pdf}")
    print(f"Sider:  {pages}")
    print(f"Tekst:  {chars} tegn  (~{chars//1800} sider med tekst)")
    print(f"Bilder: {imgs} innebygde")
    if scanned:
        print("ADVARSEL: ser skannet ut (lite tekstlag). Trenger OCR – "
              "tekst blir tom uten. IKKE slett PDF-en før OCR er gjort.")
    if args.report:
        print("\n(report-modus: ingenting skrevet)")
        return

    outdir = args.outdir or os.path.join(
        os.path.dirname(args.pdf) or ".",
        os.path.splitext(os.path.basename(args.pdf))[0])
    out_md, saved = convert(args.pdf, outdir)
    print(f"\nSkrev:  {out_md}")
    print(f"Bilder lagret: {saved}/{imgs} -> {os.path.join(outdir,'assets')}/")
    ok = (not scanned) and chars > 200 and saved == imgs
    print("\nTrygt å slette original-PDF? " +
          ("JA – tekst + alle bilder fanget." if ok
           else "NEI – sjekk advarsler/bildeantall over først."))


if __name__ == "__main__":
    main()
