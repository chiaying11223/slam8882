"""
rename_slam.py
Step 1: Print h1 titles from slam-01.html .. slam-27.html
Step 2: Rename files
Step 3: Update all links in all .html files in the folder
Step 4: Verify no bare slam-XX.html references remain
"""

from pathlib import Path
import re

FOLDER = Path(__file__).parent

RENAME_MAP = {
    "slam-01.html": "slam-01-manguan-intro.html",
    "slam-02.html": "slam-02-maintenance.html",
    "slam-03.html": "slam-03-serial-code.html",
    "slam-04.html": "slam-04-bind-phone.html",
    "slam-05.html": "slam-05-pc-version.html",
    "slam-06.html": "slam-06-small-bet.html",
    "slam-07.html": "slam-07-game-intro.html",
    "slam-08.html": "slam-08-mahjong.html",
    "slam-09.html": "slam-09-rebate.html",
    "slam-10.html": "slam-10-gift-pack.html",
    "slam-11.html": "slam-11-pick-machine.html",
    "slam-12.html": "slam-12-machine-settings.html",
    "slam-13.html": "slam-13-machine-trade.html",
    "slam-14.html": "slam-14-guild-system.html",
    "slam-15.html": "slam-15-guild-leader.html",
    "slam-16.html": "slam-16-guild-redpacket.html",
    "slam-17.html": "slam-17-guild-serial.html",
    "slam-18.html": "slam-18-guild-recommend.html",
    "slam-19.html": "slam-19-coin-dealer-safe.html",
    "slam-20.html": "slam-20-coin-dealer-recommend.html",
    "slam-21.html": "slam-21-line-community.html",
    "slam-22.html": "slam-22-official-support.html",
    "slam-23.html": "slam-23-storm-set.html",
    "slam-24.html": "slam-24-dragon-fury.html",
    "slam-25.html": "slam-25-immortal-legend.html",
    "slam-26.html": "slam-26-complete-guide.html",
    "slam-27.html": "slam-27-coin-dealer-intro.html",
}

# ── Step 1: Print h1 titles ──────────────────────────────────────────────────
print("=" * 60)
print("STEP 1 — H1 titles")
print("=" * 60)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)

for old_name in sorted(RENAME_MAP):
    path = FOLDER / old_name
    if path.exists():
        text = path.read_text(encoding="utf-8", errors="replace")
        m = H1_RE.search(text)
        h1 = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else "(no h1 found)"
    else:
        h1 = "(FILE NOT FOUND)"
    print(f"  {old_name:20s}  →  {h1}")

# ── Step 2: Rename files ─────────────────────────────────────────────────────
print()
print("=" * 60)
print("STEP 2 — Renaming files")
print("=" * 60)
renamed = 0
skipped = 0
for old_name, new_name in RENAME_MAP.items():
    src = FOLDER / old_name
    dst = FOLDER / new_name
    if src.exists():
        src.rename(dst)
        print(f"  RENAMED  {old_name}  →  {new_name}")
        renamed += 1
    else:
        print(f"  SKIP     {old_name}  (not found)")
        skipped += 1
print(f"\n  Total renamed: {renamed}, skipped: {skipped}")

# ── Step 3: Update links in ALL .html files ───────────────────────────────────
print()
print("=" * 60)
print("STEP 3 — Updating links in all .html files")
print("=" * 60)

# Sort longest new name first to avoid partial-match issues
sorted_pairs = sorted(RENAME_MAP.items(), key=lambda kv: len(kv[0]), reverse=True)

html_files = sorted(FOLDER.glob("*.html"))
total_replacements = 0

for html_path in html_files:
    content = html_path.read_text(encoding="utf-8", errors="replace")
    original = content
    file_replacements = 0
    for old_name, new_name in sorted_pairs:
        if old_name in content:
            count = content.count(old_name)
            content = content.replace(old_name, new_name)
            file_replacements += count
    if file_replacements:
        html_path.write_text(content, encoding="utf-8")
        print(f"  {html_path.name:45s}  {file_replacements:3d} replacement(s)")
        total_replacements += file_replacements

print(f"\n  Total replacements across all files: {total_replacements}")

# ── Step 4: Verify no bare slam-XX.html references remain ────────────────────
print()
print("=" * 60)
print("STEP 4 — Verification")
print("=" * 60)

BARE_RE = re.compile(r"slam-\d{2}\.html")
issues_found = False

for html_path in sorted(FOLDER.glob("*.html")):
    text = html_path.read_text(encoding="utf-8", errors="replace")
    matches = BARE_RE.findall(text)
    if matches:
        print(f"  WARNING  {html_path.name}: still contains {set(matches)}")
        issues_found = True

if not issues_found:
    print("  OK — no bare slam-XX.html references found in any file.")

print()
print("Done.")
