#!/usr/bin/env python3
"""optimize-images.py — right-size oversized vault images (local disk / Sync).

Vault images are local-cold (gitignored), so this is about disk + Obsidian Sync
weight, not git. Dry-run by default: prints what it WOULD do and the projected
saving. Nothing is touched until you pass --apply, and --apply backs up every
original (lossy resize is irreversible and these files have no git history).

Policy:
  - Candidate = longest edge > --max-dim (default 2000px) OR size > --max-kb (800).
  - Resize longest edge down to --max-dim, preserving aspect ratio.
  - JPEG: re-encode at --quality (default 85). PNG: resized but kept lossless
    (so diagrams/screenshots with text are not wrecked by lossy artifacts).
  - Skips anything already within limits.

Usage:
  python3 tools/optimize-images.py [DIRS...] [--max-dim 2000] [--max-kb 800] [--quality 85] [--apply]
  (default DIRS: raw/assets personal)

Originals are copied to `_image-originals/<original-path>` (add it to .gitignore)
on --apply. Review the result in Obsidian, then delete that folder when happy.
Uses macOS `sips`. Diagrams whose legibility needs full resolution (e.g. a dense
mind-map) should be excluded by path; check the dry-run before applying.
"""
import os, sys, subprocess, argparse, shutil

EXT = (".png", ".jpg", ".jpeg")

def dims(p):
    try:
        out = subprocess.check_output(["sips", "-g", "pixelWidth", "-g", "pixelHeight", p],
                                      text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return None, None
    w = h = None
    for line in out.splitlines():
        s = line.strip()
        if s.startswith("pixelWidth:"):  w = int(s.split(":")[1])
        if s.startswith("pixelHeight:"): h = int(s.split(":")[1])
    return w, h

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="*", default=["raw/assets", "personal"])
    ap.add_argument("--max-dim", type=int, default=2000)
    ap.add_argument("--max-kb", type=int, default=800)
    ap.add_argument("--quality", type=int, default=85)
    ap.add_argument("--exclude", default="", help="comma-separated path substrings to skip")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    dirs = a.dirs or ["raw/assets", "personal"]
    skips = [s for s in a.exclude.split(",") if s]

    cands = []
    for d in dirs:
        for root, _, files in os.walk(d):
            if "_image-originals" in root:
                continue
            for fn in files:
                if fn.lower().endswith(EXT):
                    p = os.path.join(root, fn)
                    if any(s in p for s in skips):
                        continue
                    cands.append(p)

    before = after_est = 0
    acted = 0
    print(f"{'before':>8} {'after~':>8}  dims            file")
    for p in sorted(cands):
        kb = os.path.getsize(p) // 1024
        w, h = dims(p)
        if not w:
            continue
        long = max(w, h)
        if long <= a.max_dim and kb <= a.max_kb:
            continue
        # rough projection: scale area; jpeg gets an extra factor
        scale = min(1.0, a.max_dim / long)
        est = kb * (scale * scale)
        if p.lower().endswith((".jpg", ".jpeg")):
            est *= 0.6
        est = max(int(est), 20)
        before += kb; after_est += est; acted += 1
        nd = f"{int(w*scale)}x{int(h*scale)}" if scale < 1 else f"{w}x{h}"
        print(f"{kb:>7}K {est:>7}K  {nd:<15} {p}")

        if a.apply:
            bak = os.path.join("_image-originals", p)
            os.makedirs(os.path.dirname(bak), exist_ok=True)
            shutil.copy2(p, bak)
            cmd = ["sips"]
            if scale < 1:
                cmd += ["--resampleHeightWidthMax", str(a.max_dim)]
            if p.lower().endswith((".jpg", ".jpeg")):
                cmd += ["-s", "formatOptions", str(a.quality)]
            cmd += [p]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"\n{acted} files over the limit.  {before//1024} MB -> ~{after_est//1024} MB "
          f"(estimate, saves ~{(before-after_est)//1024} MB)")
    if not a.apply:
        print("DRY RUN — nothing changed. Run with --apply to act "
              "(originals are backed up to _image-originals/).")

if __name__ == "__main__":
    main()
