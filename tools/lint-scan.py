#!/usr/bin/env python3
"""lint-scan.py — mechanical tier of /wiki-lint (proposal-012, step 1a).

Read-only scanner for this vault's wiki. Emits findings as JSON (default)
or text to stdout; the AGENT writes the narrative lint report. There is
no write path: the script never modifies vault files (boundary-score.py
model — keeping it read-only removes a write-path attack surface).

It implements the mechanical/hybrid-mechanical checks from the wiki-lint
function map (meta/ideas/vault-lint-tooling/wiki-lint-function-map.md):
M1 index coverage, M2 wikilink resolution, M3 tag registry/budget,
M4 frontmatter/schema shape, M5 source-path/raw coverage,
M6 navigation/pointer hygiene, M7 overview staleness, plus N4 encoding/
line-ending/partial-write watch. Semantic judgment (contradictions,
stale-claim, hub-concept, synthesis readiness, prose) stays with the
agent; --semantic-pack emits a compact bundle of files/findings the agent
should read next so the expensive model does not read the whole vault.

Schema-derived values (entity_type enum, hovedtags, reserved DNA names,
model baseline, registered tags) are READ from meta/vault-config.md and
wiki/tags.md rather than hardcoded, to shrink the drift surface
(proposal-012 point 3). The few values that remain inline below are
marked SCHEMA-DERIVED so wiki-lint Check 9 can watch them.

CLI (function-map "proposed split"):
  lint-scan.py --mechanical --json      # deterministic findings, JSON (default)
  lint-scan.py --mechanical --text      # same, human-readable summary
  lint-scan.py --semantic-pack          # compact file/finding bundle for the agent
  lint-scan.py --fix-safe               # emit safe-fix CANDIDATES as JSON (read-only; no apply)
  lint-scan.py --peek                   # structured diagnostics; no scan

Exit codes (tiling-check.py ABI):
  0  success
  2  usage error
  3  config missing/unparseable (required enums could not be read)
The caller (wiki-lint Phase 0a) branches on the exit code; if python or
this script is absent the caller falls back to doing the checks itself,
so this is a soft accelerator, not a hard dependency.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = VAULT_ROOT / "wiki"
RAW_DIR = VAULT_ROOT / "raw"
CONFIG_PATH = VAULT_ROOT / "meta" / "vault-config.md"
TAGS_PATH = WIKI_DIR / "tags.md"
CLAUDE_PATH = VAULT_ROOT / "CLAUDE.md"

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_NO_CONFIG = 3

MAX_BODY_BYTES = 512 * 1024

# --- SCHEMA-DERIVED constants (wiki-lint Check 9 must watch these) ----------
# These are not in a machine-readable block in vault-config yet, so they stay
# inline. CLAUDE.md §B.3 is the authority; if it changes, update here AND let
# Check 9 flag the drift.
KIND_ENUM = {"entity", "concept", "source", "synthesis"}            # §B.3 frontmatter
NAV_BASENAMES = {"index", "log", "overview", "tags", "home"}        # §B.2 navigational
TAG_BUDGET_MAX = 4                                                  # §B.3 tags
TRIGGER_SKILL_OK = {"wiki-ingest", "wiki-query", "wiki-synthesis", "wiki-lint"}  # §B.4.1
TRIGGER_MODE_OK = {"user-requested", "user-selected", "agent-followon"}         # §B.4.1
# raw plugin-sync / aggregate exceptions (§B.2 + vault-config "Plugin-sync roots")
RAW_OVERHEAD = {"raw/snipd/base/snipd.base", "raw/snipd/readme.md"}
RAW_SKIP_PREFIXES = ("raw/assets/", "raw/media_logs/")
ASSET_EXTS = ("png", "jpg", "jpeg", "gif", "svg", "pdf", "webp")
# ---------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
EMBED_RE = re.compile(r"!\[\[([^\]]+)\]\]")
LINK_RE = re.compile(r"(?<!\!)\[\[([^\]]+)\]\]")
_FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def log(msg):
    print(msg, file=sys.stderr)


# --- config / registry reading (proposal-012 point 3) ----------------------

def _backtick_tokens(section_text):
    return re.findall(r"`([^`]+)`", section_text)


def _section(text, header_regex, stop=r"\n#{1,3} "):
    m = re.search(header_regex + r"(.*?)(?=" + stop + r"|\Z)", text, re.DOTALL)
    return m.group(1) if m else ""


def read_config():
    """Read schema-derived enums from vault-config.md + tags.md.

    Returns (cfg, warnings). On a hard miss (config file absent) the caller
    should exit EXIT_NO_CONFIG. Individual missing sections degrade to empty
    with a warning so a partial config still yields useful output.
    """
    warnings = []
    if not CONFIG_PATH.exists():
        return None, ["vault-config.md not found"]
    ctext = CONFIG_PATH.read_text(encoding="utf-8")

    # entity_type enum: "- `person` — ..." bullets under "## Entity types"
    et_sec = _section(ctext, r"##\s*Entity types\b")
    entity_types = set(re.findall(r"^-\s*`(\w+)`", et_sec, re.MULTILINE))
    if not entity_types:
        warnings.append("entity_type enum not parsed from vault-config")

    # hovedtags: backtick list under "## Hovedtags"
    hv_sec = _section(ctext, r"##\s*Hovedtags\b")
    hovedtags = set(t for t in _backtick_tokens(hv_sec) if re.fullmatch(r"[a-z_]+", t))
    if not hovedtags:
        warnings.append("hovedtags not parsed from vault-config")

    # reserved DNA names under "## Reserved Vault DNA names"
    dna_sec = _section(ctext, r"##\s*Reserved Vault DNA names\b")
    reserved = set(t.lower() for t in _backtick_tokens(dna_sec) if t.lower().endswith(".md"))
    if not reserved:
        warnings.append("reserved DNA names not parsed from vault-config")

    # model baseline: backtick id under "## Model-id baseline"
    mb_sec = _section(ctext, r"##\s*Model-id baseline\b")
    mb = _backtick_tokens(mb_sec)
    model_baseline = mb[0] if mb else ""
    if not model_baseline:
        warnings.append("model baseline not parsed from vault-config")

    # registered tags from the live registry wiki/tags.md. Match tag entries as
    # list items ("- `slug` — def"), NOT a global backtick scan: tags.md has
    # backticks in prose (CLAUDE.md refs, the Format line, §-refs) that would
    # offset backtick pairing and capture prose instead of tag names.
    registered_tags = set()
    if TAGS_PATH.exists():
        ttext = TAGS_PATH.read_text(encoding="utf-8")
        for m in re.finditer(r"^\s*[-*]\s*`([a-z0-9_]+)`", ttext, re.MULTILINE):
            registered_tags.add(m.group(1))
        if not registered_tags:
            warnings.append("no tag entries parsed from wiki/tags.md")
    else:
        warnings.append("wiki/tags.md not found")

    cfg = {
        "entity_types": entity_types,
        "hovedtags": hovedtags,
        "reserved_dna": reserved,
        "model_baseline": model_baseline,
        "registered_tags": registered_tags,
    }
    return cfg, warnings


# --- frontmatter + wikilink parsing (lifted from boundary-score.py) ---------

def parse_frontmatter(text):
    """Line-based frontmatter parse (no YAML dep, proposal-012 point C).

    Cannot distinguish block-vs-inline list shape (§B.3 'sources must be
    block-style'); that nuance is left to the semantic tier on purpose.
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_raw, body = m.group(1), text[m.end():]
    fm, cur = {}, None
    for line in fm_raw.splitlines():
        if not line.strip():
            continue
        km = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if km and not line[0].isspace():
            cur = km.group(1)
            val = km.group(2).strip()
            if val == "":
                fm[cur] = []
            elif val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                fm[cur] = [] if not inner else [x.strip().strip('"').strip("'") for x in inner.split(",")]
            else:
                fm[cur] = val.strip('"').strip("'")
        elif re.match(r"^\s*-\s+", line) and cur is not None:
            item = re.sub(r"^\s*-\s+", "", line).strip().strip('"').strip("'")
            if isinstance(fm.get(cur), list):
                fm[cur].append(item)
            else:
                fm[cur] = [item]
    return fm, body


def extract_links(body, regex):
    """Extract link/embed targets, skipping fenced code blocks (CommonMark:
    backtick AND tilde fences, length-tracked). Lifted from boundary-score.py."""
    cleaned, fence_char, fence_len = [], None, 0
    for line in body.splitlines():
        fm = _FENCE_RE.match(line)
        if fm:
            char, length = fm.group(2)[0], len(fm.group(2))
            if fence_char is None:
                fence_char, fence_len = char, length
                continue
            if char == fence_char and length >= fence_len:
                fence_char, fence_len = None, 0
                continue
        if fence_char is not None:
            continue
        cleaned.append(line)
    scan = "\n".join(cleaned)
    return [m.group(1) for m in regex.finditer(scan)]


def norm_target(t):
    return t.split("|")[0].split("#")[0].strip()


# --- vault scan -------------------------------------------------------------

def scan_vault():
    """Walk wiki/, return (pages, indexes). pages[rel] holds parsed fields.
    Also builds vault-wide name/asset indexes for cross-layer link resolution."""
    pages = {}
    basename_index = defaultdict(list)
    alias_index = defaultdict(list)
    # vault-wide existence sets (wiki + meta + root) for cross-layer links
    all_md_base, all_md_rel, all_assets, all_asset_rel = set(), set(), set(), set()
    for dp, dirs, files in os.walk(VAULT_ROOT):
        rp = os.path.relpath(dp, VAULT_ROOT).replace("\\", "/")
        if rp.startswith("personal") or rp.startswith(".git") or rp.startswith(".obsidian"):
            dirs[:] = [d for d in dirs if not (rp == "." and d in (".git", ".obsidian", "personal"))]
            if rp.startswith((".git", ".obsidian", "personal")):
                continue
        for f in files:
            low = f.lower()
            rel = (rp + "/" + f).replace("\\", "/").lstrip("./")
            if low.endswith(".md"):
                all_md_base.add(low[:-3])
                all_md_rel.add(rel[:-3].lower())
            elif low.rsplit(".", 1)[-1] in ASSET_EXTS:
                all_assets.add(low)
                all_asset_rel.add(rel.lower())

    for dp, _, files in os.walk(WIKI_DIR):
        for f in files:
            if not f.endswith(".md"):
                continue
            path = Path(dp) / f
            rel = path.relative_to(VAULT_ROOT).as_posix()
            # Read bytes so the CRLF check works: read_text uses universal
            # newlines and would silently convert \r\n -> \n.
            try:
                data = path.read_bytes()
                text = data.decode("utf-8")
            except (OSError, UnicodeDecodeError):
                pages[rel] = {"rel": rel, "base": f[:-3], "unreadable": True,
                              "has_crlf": False, "fm": {}}
                continue
            has_crlf = b"\r\n" in data
            # Detect CRLF from bytes (above), but normalize for parsing so the
            # frontmatter/line regexes (which expect \n) work on CRLF files.
            text = text.replace("\r\n", "\n").replace("\r", "\n")
            fm, body = parse_frontmatter(text)
            base = f[:-3]
            firstline = ""
            for ln in body.splitlines():
                s = ln.strip()
                if s and not s.startswith("#") and not s.startswith(">"):
                    firstline = s
                    break
            aliases = fm.get("aliases", [])
            if isinstance(aliases, str):
                aliases = [aliases]
            pages[rel] = {
                "rel": rel, "base": base, "fm": fm, "body": body, "text": text,
                "kind": fm.get("kind", ""), "ingest_model": fm.get("ingest_model", ""),
                "updated": fm.get("updated", ""), "created": fm.get("created", ""),
                "entity_type": fm.get("entity_type", ""),
                "trigger_skill": fm.get("trigger_skill", ""),
                "trigger_mode": fm.get("trigger_mode", ""),
                "aliases": [a for a in aliases if a],
                "tags": fm.get("tags", []) if isinstance(fm.get("tags", []), list) else [fm.get("tags")],
                "sources": fm.get("sources", []), "source_path": fm.get("source_path", []),
                "has_infobox": "[!infobox]" in text, "firstline": firstline,
                "body_len": len(body), "unreadable": False, "has_crlf": has_crlf,
            }
            basename_index[base.lower()].append(rel)
            for a in pages[rel]["aliases"]:
                alias_index[str(a).lower()].append(rel)
    idx = {
        "basename": basename_index, "alias": alias_index,
        "all_md_base": all_md_base, "all_md_rel": all_md_rel,
        "all_assets": all_assets, "all_asset_rel": all_asset_rel,
    }
    return pages, idx


def resolve_page(target, idx):
    """('wiki', rel) | ('other', None) | (None, raw) — cross-layer aware."""
    t = norm_target(target)
    if not t:
        return ("", None)
    key = t.lower()
    last = key.rsplit("/", 1)[-1]
    if key in idx["basename"]:
        return ("wiki", idx["basename"][key][0])
    if key in idx["alias"]:
        return ("wiki", idx["alias"][key][0])
    if "/" in key and last in idx["basename"]:
        return ("wiki", idx["basename"][last][0])
    if "/" in key and last in idx["alias"]:
        return ("wiki", idx["alias"][last][0])
    if key in idx["all_md_rel"] or key in idx["all_md_base"] or last in idx["all_md_base"]:
        return ("other", None)
    return (None, t)


def resolve_embed(target, idx):
    t = norm_target(target).lower()
    last = t.rsplit("/", 1)[-1]
    return (t in idx["all_assets"] or last in idx["all_assets"] or t in idx["all_asset_rel"]
            or t in idx["all_md_base"] or last in idx["all_md_base"] or t in idx["all_md_rel"])


def is_agent_first(rel):
    """§B.2 audience axis: log + dated reports are agent-first; their broken
    links / prose are out of scope. Used to bucket findings, not drop them."""
    low = rel.lower()
    base = low.rsplit("/", 1)[-1]
    return (base in ("log.md",) or "/rapporter/" in low or "/arkiv/" in low)


# --- checks -----------------------------------------------------------------

def run_checks(pages, idx, cfg):
    F = {}
    content = {r: p for r, p in pages.items()
               if p.get("kind") in KIND_ENUM and not p.get("unreadable")}

    # graph: inbound + broken (split active vs agent-first)
    inbound = defaultdict(set)
    broken_active, broken_agent = defaultdict(list), defaultdict(list)
    broken_embeds = defaultdict(list)
    for rel, p in pages.items():
        if p.get("unreadable"):
            continue
        body = p["body"]
        for raw in extract_links(body, EMBED_RE):
            if not resolve_embed(raw, idx):
                broken_embeds[rel].append(norm_target(raw))
        for raw in extract_links(body, LINK_RE):
            kindr, tgt = resolve_page(raw, idx)
            if kindr is None:
                (broken_agent if is_agent_first(rel) else broken_active)[rel].append(tgt)
            elif kindr == "wiki" and tgt and tgt != rel:
                inbound[tgt].add(rel)

    # M2/3 orphans (content pages, exclude nav + agent-first)
    F["orphans"] = sorted(
        rel for rel, p in content.items()
        if p["base"].lower() not in NAV_BASENAMES and not is_agent_first(rel)
        and len(inbound.get(rel, ())) == 0)

    F["broken_links_active"] = {r: v for r, v in sorted(broken_active.items())}
    F["broken_links_agentfirst_count"] = sum(len(v) for v in broken_agent.values())
    F["broken_embeds"] = {r: v for r, v in sorted(broken_embeds.items())}

    # M4 frontmatter shape
    missing_fm, kind_bad = [], []
    et_missing, et_bad, syn_bad = [], [], []
    for rel, p in pages.items():
        if p.get("unreadable"):
            continue
        if p["base"].lower() in NAV_BASENAMES:
            continue
        k = p.get("kind", "")
        if not k:
            continue  # non-nav, kind-less handled by nav check; rare
        if k not in KIND_ENUM:
            kind_bad.append({"file": rel, "kind": k})
        req = ["kind", "title", "created", "updated", "ingest_model"]
        miss = [x for x in req if not p["fm"].get(x)]
        if miss:
            missing_fm.append({"file": rel, "missing": miss})
        if k == "entity":
            et = p.get("entity_type", "")
            if not et:
                et_missing.append(rel)
            elif cfg["entity_types"] and et not in cfg["entity_types"]:
                et_bad.append({"file": rel, "entity_type": et})
        if k == "synthesis":
            probs = []
            ts, tm = p.get("trigger_skill", ""), p.get("trigger_mode", "")
            if not ts:
                probs.append("missing trigger_skill")
            elif ts not in TRIGGER_SKILL_OK:
                probs.append(f"bad trigger_skill={ts}")
            if not tm:
                probs.append("missing trigger_mode")
            elif tm not in TRIGGER_MODE_OK:
                probs.append(f"bad trigger_mode={tm}")
            if probs:
                syn_bad.append({"file": rel, "problems": probs})
    F["missing_frontmatter"] = missing_fm
    F["kind_out_of_enum"] = kind_bad
    F["entity_type_missing"] = sorted(et_missing)
    F["entity_type_bad"] = et_bad
    F["synthesis_trigger_issues"] = syn_bad

    # 9g reserved DNA collisions
    F["dna_collisions"] = sorted(
        rel for rel, p in pages.items()
        if not p.get("unreadable") and (p["base"].lower() + ".md") in cfg["reserved_dna"])

    # M4 model id distribution + 9-id normalization (generic alias) + parity
    model_dist = Counter(p.get("ingest_model", "") or "(none)" for p in content.values())
    GENERIC = {"gpt-5", "claude", "gpt", "claude-opus", "gpt-4"}
    F["model_distribution"] = dict(model_dist.most_common())
    F["model_generic_alias"] = sorted(
        {p["ingest_model"] for p in content.values() if p.get("ingest_model") in GENERIC})
    F["model_generic_alias_count"] = sum(
        c for m, c in model_dist.items() if m in GENERIC)
    F["model_baseline"] = cfg["model_baseline"]
    F["model_off_baseline_count"] = sum(
        c for m, c in model_dist.items()
        if cfg["model_baseline"] and m not in (cfg["model_baseline"], "(none)"))

    # M3 tags: registry parity, dead tags, over-budget
    tag_use = Counter()
    over_budget = []
    for rel, p in content.items():
        tags = [t for t in p["tags"] if t]
        for t in tags:
            tag_use[t] += 1
        if len(tags) > TAG_BUDGET_MAX:
            over_budget.append({"file": rel, "count": len(tags), "tags": tags})
    unregistered = sorted(t for t in tag_use if cfg["registered_tags"] and t not in cfg["registered_tags"])
    registered_unused = sorted(cfg["registered_tags"] - set(tag_use)) if cfg["registered_tags"] else []
    dead = sorted({t: c for t, c in tag_use.items()
                   if c <= 1 and t not in cfg["hovedtags"]}.items(), key=lambda x: x[0])
    F["tag_usage"] = dict(tag_use.most_common())
    F["tags_unregistered"] = unregistered
    F["tags_registered_unused"] = registered_unused
    F["tags_dead_subtags"] = [{"tag": t, "uses": c} for t, c in dead]
    F["tags_over_budget"] = over_budget

    # M5 raw coverage
    covered = set()
    for p in pages.values():
        for sp in (p.get("source_path") or []):
            covered.add(str(sp).strip().replace("\\", "/").lower())
    uncovered_snipd, uncovered_other = [], []
    raw_total = 0
    if RAW_DIR.is_dir():
        for dp, _, files in os.walk(RAW_DIR):
            rpd = Path(dp).relative_to(VAULT_ROOT).as_posix()
            for f in files:
                if not f.endswith(".md"):
                    continue
                rel = (rpd + "/" + f)
                low = rel.lower()
                if low in RAW_OVERHEAD or low.startswith(RAW_SKIP_PREFIXES):
                    continue
                raw_total += 1
                if low in covered:
                    continue
                (uncovered_snipd if "/snipd/" in low else uncovered_other).append(rel)
    F["raw_total_md"] = raw_total
    F["raw_uncovered_snipd"] = sorted(uncovered_snipd)
    F["raw_uncovered_other"] = sorted(uncovered_other)

    # M7 overview staleness
    overview = pages.get("wiki/overview.md")
    newest_syn = ""
    newest_syn_file = ""
    for rel, p in pages.items():
        if p.get("kind") == "synthesis" and not is_agent_first(rel):
            u = p.get("updated", "")
            if u and u > newest_syn:
                newest_syn, newest_syn_file = u, rel
    if overview:
        ov_u = overview.get("updated", "")
        F["overview_staleness"] = {
            "overview_updated": ov_u, "newest_synthesis": newest_syn,
            "newest_synthesis_file": newest_syn_file,
            "stale": bool(newest_syn and ov_u and ov_u < newest_syn),
        }

    # M6 navigation/pointer hygiene: latest-lint pointer in CLAUDE.md §B.0
    pointer = {}
    if CLAUDE_PATH.exists():
        ctext = CLAUDE_PATH.read_text(encoding="utf-8")
        pm = re.search(r"most recent lint report:\s*\[\[([^\]]+)\]\]", ctext)
        lint_reports = sorted(
            p["base"] for r, p in pages.items()
            if p["base"].lower().startswith("lint - 2") and not p.get("unreadable"))
        newest_lint = lint_reports[-1] if lint_reports else ""
        cur = pm.group(1) if pm else ""
        pointer = {"current": cur, "newest_lint_report": newest_lint,
                   "stale": bool(newest_lint and cur and cur != newest_lint)}
    F["latest_lint_pointer"] = pointer

    # N4 encoding / partial-write watch
    enc = []
    for rel, p in pages.items():
        if p.get("unreadable"):
            enc.append({"file": rel, "issue": "unreadable/invalid-utf8"})
            continue
        t = p.get("text", "")
        if p.get("has_crlf"):
            enc.append({"file": rel, "issue": "CRLF line endings"})
        if t.startswith("---") and FRONTMATTER_RE.match(t) is None:
            enc.append({"file": rel, "issue": "frontmatter opener without valid close (partial write?)"})
    F["encoding_watch"] = enc

    return F


def build_meta(pages, cfg, warnings):
    kinds = Counter(p.get("kind", "") or "(none)" for p in pages.values())
    return {
        "vault_root": str(VAULT_ROOT),
        "page_counts": dict(kinds.most_common()),
        "total_pages": len(pages),
        "config_warnings": warnings,
        "schema_derived_inline": {
            "kind_enum": sorted(KIND_ENUM), "tag_budget_max": TAG_BUDGET_MAX,
            "nav_basenames": sorted(NAV_BASENAMES),
            "trigger_skill_ok": sorted(TRIGGER_SKILL_OK),
            "trigger_mode_ok": sorted(TRIGGER_MODE_OK),
        },
        "config_read": {
            "entity_types": sorted(cfg["entity_types"]),
            "hovedtags": sorted(cfg["hovedtags"]),
            "model_baseline": cfg["model_baseline"],
            "registered_tags_count": len(cfg["registered_tags"]),
            "reserved_dna_count": len(cfg["reserved_dna"]),
        },
    }


def safe_fix_candidates(F):
    """Emit safe-fix CANDIDATES only (read-only; the agent/operator applies).
    Function map: only blank/unknown one-off tags, index add, pointer update
    are 'safe'; everything else needs judgment."""
    cands = []
    if F.get("latest_lint_pointer", {}).get("stale"):
        lp = F["latest_lint_pointer"]
        cands.append({"action": "update-latest-lint-pointer", "file": "CLAUDE.md",
                      "from": lp["current"], "to": lp["newest_lint_report"],
                      "note": "protected §B.0 single-line edit; wiki-lint Phase 6 exception"})
    for t in F.get("tags_dead_subtags", []):
        cands.append({"action": "review-dead-tag", "tag": t["tag"], "uses": t["uses"],
                      "note": "remove from tags.md + using page only after human review"})
    return cands


def semantic_pack(pages, F):
    """Compact bundle of files/findings the agent should read next, so the
    expensive model narrows its reading instead of scanning the whole vault."""
    pack = {
        "note": "Read these to form semantic conclusions (contradictions, "
                "stale claims, hub seeds, prose). lint-scan covers the mechanical tier.",
        "broken_link_pages_active": sorted(F["broken_links_active"].keys()),
        "synthesis_field_issues": [x["file"] for x in F["synthesis_trigger_issues"]],
        "raw_uncovered_clusters": {
            "snipd": F["raw_uncovered_snipd"][:40],
            "other": F["raw_uncovered_other"][:60],
        },
        "overview_staleness": F.get("overview_staleness", {}),
        "stranger_test_first_line_candidates": [
            {"file": r, "firstline": p["firstline"][:160]}
            for r, p in sorted(pages.items())
            if p.get("kind") in ("source", "entity", "concept")
            and re.match(r"^(Skaperprofil|Denne (siden|noden|profilen))", p.get("firstline", ""))
        ][:60],
        "infobox_missing_candidates": sorted(
            r for r, p in pages.items()
            if p.get("kind") in ("source", "entity", "concept")
            and not p.get("has_infobox") and p.get("body_len", 0) > 500),
    }
    return pack


def text_summary(meta, F):
    out = []
    out.append("# lint-scan (mechanical tier)")
    out.append(f"vault: {meta['vault_root']}")
    out.append(f"pages: {meta['page_counts']} total={meta['total_pages']}")
    if meta["config_warnings"]:
        out.append("config WARNINGS: " + "; ".join(meta["config_warnings"]))
    out.append("")
    out.append(f"orphans: {len(F['orphans'])}")
    out.append(f"broken links (active pages): {sum(len(v) for v in F['broken_links_active'].values())} "
               f"across {len(F['broken_links_active'])} pages; agent-first (excluded): {F['broken_links_agentfirst_count']}")
    out.append(f"broken embeds: {sum(len(v) for v in F['broken_embeds'].values())}")
    out.append(f"missing frontmatter: {len(F['missing_frontmatter'])}; kind-out-of-enum: {len(F['kind_out_of_enum'])}")
    out.append(f"entity_type missing: {len(F['entity_type_missing'])}; bad: {len(F['entity_type_bad'])}")
    out.append(f"synthesis trigger issues: {len(F['synthesis_trigger_issues'])}")
    out.append(f"DNA collisions: {len(F['dna_collisions'])}")
    out.append(f"model: baseline={F['model_baseline']} off-baseline={F['model_off_baseline_count']} "
               f"generic-alias={F['model_generic_alias_count']} {F['model_generic_alias']}")
    out.append(f"tags: unregistered={F['tags_unregistered']} dead={[d['tag'] for d in F['tags_dead_subtags']]} "
               f"over-budget={len(F['tags_over_budget'])} registered-unused={F['tags_registered_unused']}")
    out.append(f"raw uncovered: snipd={len(F['raw_uncovered_snipd'])} other={len(F['raw_uncovered_other'])} (of {F['raw_total_md']} raw .md)")
    ov = F.get("overview_staleness", {})
    out.append(f"overview stale: {ov.get('stale')} (overview={ov.get('overview_updated')} vs newest syn={ov.get('newest_synthesis')})")
    lp = F.get("latest_lint_pointer", {})
    out.append(f"latest-lint pointer stale: {lp.get('stale')} (current={lp.get('current')} newest={lp.get('newest_lint_report')})")
    out.append(f"encoding watch: {len(F['encoding_watch'])}")
    return "\n".join(out)


def main(argv):
    # Force UTF-8 stdout/stderr so JSON with Norwegian chars is parseable by
    # the caller regardless of the Windows console code page (cp1252 default).
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--mechanical", action="store_true", help="run deterministic checks (default)")
    ap.add_argument("--json", action="store_true", help="JSON output (default)")
    ap.add_argument("--text", action="store_true", help="human-readable summary")
    ap.add_argument("--semantic-pack", action="store_true", help="compact bundle for the agent")
    ap.add_argument("--fix-safe", action="store_true", help="emit safe-fix candidates (read-only)")
    ap.add_argument("--peek", action="store_true", help="structured diagnostics; no scan")
    args = ap.parse_args(argv)

    if args.peek:
        diag = {"script": str(Path(__file__).resolve()), "python": sys.executable,
                "vault_root": str(VAULT_ROOT), "wiki_exists": WIKI_DIR.is_dir(),
                "config_exists": CONFIG_PATH.exists(), "tags_exists": TAGS_PATH.exists()}
        print(json.dumps(diag, indent=2))
        return EXIT_OK if CONFIG_PATH.exists() else EXIT_NO_CONFIG

    cfg, warnings = read_config()
    if cfg is None:
        log("ERR: vault-config.md not found; cannot read schema enums")
        return EXIT_NO_CONFIG

    pages, idx = scan_vault()
    F = run_checks(pages, idx, cfg)
    meta = build_meta(pages, cfg, warnings)

    if args.semantic_pack:
        print(json.dumps({"meta": meta, "semantic_pack": semantic_pack(pages, F)}, indent=2, ensure_ascii=False))
        return EXIT_OK
    if args.fix_safe:
        print(json.dumps({"meta": meta, "fix_safe_candidates": safe_fix_candidates(F)}, indent=2, ensure_ascii=False))
        return EXIT_OK
    if args.text:
        print(text_summary(meta, F))
        return EXIT_OK
    # default: --mechanical --json
    print(json.dumps({"meta": meta, "findings": F}, indent=2, ensure_ascii=False))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
