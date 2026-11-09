import re
import os
import glob

print("=== 7. INTERNAL LINK & REFERENCE VERIFICATION ===")
md_files = glob.glob("docs/*.md") + ["README.md", "models/README.md", "dashboards/dashboard_specs.md"]
broken_links = []
valid_links = 0

for mdf in md_files:
    base_dir = os.path.dirname(mdf)
    with open(mdf, "r", encoding="utf-8") as f:
        content = f.read()
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    for text, link in links:
        if link.startswith("http") or link.startswith("#") or link.startswith("mailto:"):
            continue
        target_path = link.split("#")[0]
        if not target_path:
            continue
        full_target = os.path.normpath(os.path.join(base_dir, target_path))
        if not os.path.exists(full_target):
            broken_links.append((mdf, link, full_target))
        else:
            valid_links += 1

print(f"Total markdown files checked: {len(md_files)}")
print(f"Total valid internal links: {valid_links}")
print(f"Total broken links detected: {len(broken_links)}")
for src, link, full in broken_links:
    print(f"  IN {src}: Link '{link}' -> NOT FOUND at {full}")
