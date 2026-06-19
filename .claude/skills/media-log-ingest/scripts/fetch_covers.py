#!/usr/bin/env python3
"""Stage 4 (mechanical): fetch cover thumbnails from Wikipedia, cached incrementally.

For each item whose title is not already in the cache, query the Wikipedia REST
summary API and keep the thumbnail URL. Threaded and incremental: safe to interrupt
and re-run, it only fetches what's missing. The cache is a working file, not a skill
asset (see SKILL.md): a warm cache from a previous run can be passed via --out.

Usage:
  python fetch_covers.py --in work/films.json --out work/covers.json
  python fetch_covers.py --in work/books.json --out work/book_covers.json --suffix "(novel)"

Title field defaults to "name" (the filename stem from parse.py). For films named
"Title (YYYY)" the year is used to disambiguate the Wikipedia article lookup.
"""

import os
import re
import json
import argparse
import threading
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

API = "https://en.wikipedia.org/api/rest_v1/page/summary/"


def candidates(title, suffix):
    m = re.match(r"^(.*)\s\((\d{4})\)$", title)
    name, year = (m.group(1).strip(), m.group(2)) if m else (title, None)
    name = name.replace("…", "").strip()
    out = []
    if year:
        out.append(f"{name} ({year} {suffix})" if suffix else f"{name} ({year})")
    if suffix:
        out.append(f"{name} ({suffix})")
    out.append(name)
    return out


def fetch_summary(article):
    url = API + urllib.parse.quote(article.replace(" ", "_"), safe="")
    req = urllib.request.Request(url, headers={"User-Agent": "vault-media-log/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=6) as r:
            d = json.loads(r.read().decode("utf-8"))
    except Exception:
        return None
    if d.get("type") == "disambiguation":
        return None
    return d.get("thumbnail", {}).get("source")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="aggregate JSON from parse.py")
    ap.add_argument("--out", required=True, help="cover cache JSON (reused as warm cache)")
    ap.add_argument("--field", default="name", help="title field to look up (default: name)")
    ap.add_argument("--suffix", default="film", help="disambiguation hint, e.g. film / novel; '' to disable")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    items = json.load(open(args.inp, encoding="utf-8"))
    cache = json.load(open(args.out, encoding="utf-8")) if os.path.exists(args.out) else {}
    titles = [it[args.field] for it in items if it.get(args.field) and it[args.field] not in cache]
    lock = threading.Lock()
    done = 0

    def work(t):
        for c in candidates(t, args.suffix):
            s = fetch_summary(c)
            if s:
                return (t, s)
        return (t, "")

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for t, s in ex.map(work, titles):
            with lock:
                cache[t] = s
                done += 1
                if done % 20 == 0:
                    json.dump(cache, open(args.out, "w", encoding="utf-8"), ensure_ascii=False)

    json.dump(cache, open(args.out, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"covers cached: {len(cache)} | with image: {sum(1 for v in cache.values() if v)} | newly fetched: {len(titles)}")


if __name__ == "__main__":
    main()
