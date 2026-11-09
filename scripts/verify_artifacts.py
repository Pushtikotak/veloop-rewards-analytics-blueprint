import os
import re
import xml.etree.ElementTree as ET

print("=== 6. VERIFY ERD, SQL DDL, WIREFRAMES & DAX ===")

# 1. SQL DDL Verification
ddl_path = "models/schema_ddl.sql"
with open(ddl_path, "r", encoding="utf-8") as f:
    ddl_sql = f.read()

tables = re.findall(r'CREATE TABLE\s+([a-zA-Z0-9_]+)', ddl_sql, re.IGNORECASE)
pks = re.findall(r'PRIMARY KEY', ddl_sql, re.IGNORECASE)
fks = re.findall(r'REFERENCES\s+([a-zA-Z0-9_]+)', ddl_sql, re.IGNORECASE)
indexes = re.findall(r'CREATE INDEX\s+([a-zA-Z0-9_]+)', ddl_sql, re.IGNORECASE)
checks = re.findall(r'CHECK\s*\(', ddl_sql, re.IGNORECASE)

print(f"SQL Schema DDL ({ddl_path}):")
print(f"  Tables Created ({len(tables)}): {', '.join(tables)}")
print(f"  Primary Keys: {len(pks)}")
print(f"  Foreign Key References: {len(fks)}")
print(f"  B-Tree Indexes Created: {len(indexes)}")
print(f"  Check Constraints: {len(checks)}")

# 2. Mermaid ERD
mermaid_path = "models/logical_data_model.mermaid"
with open(mermaid_path, "r", encoding="utf-8") as f:
    mermaid_content = f.read()

entities_in_mermaid = re.findall(r'([a-zA-Z0-9_]+)\s*\{', mermaid_content)
relationships_in_mermaid = re.findall(r'([a-zA-Z0-9_]+)\s*\|\|--[o|]\{?\s*([a-zA-Z0-9_]+)', mermaid_content)
print(f"\nMermaid ER Diagram ({mermaid_path}):")
print(f"  Entities Defined ({len(entities_in_mermaid)}): {', '.join(entities_in_mermaid)}")
print(f"  Relationships Mapped: {len(relationships_in_mermaid)}")

# 3. Dashboard Wireframes SVGs
wireframe_dir = "dashboards/wireframes"
svg_files = sorted(os.listdir(wireframe_dir))
print(f"\nDashboard Wireframes ({wireframe_dir}):")
for svg in svg_files:
    if svg.endswith(".svg"):
        sp = os.path.join(wireframe_dir, svg)
        try:
            tree = ET.parse(sp)
            root = tree.getroot()
            text_nodes = list(root.iter("{http://www.w3.org/2000/svg}text"))
            print(f"  [VALID SVG] {svg:<30} Size: {os.path.getsize(sp):>6} bytes | Text Elements: {len(text_nodes)}")
        except Exception as e:
            print(f"  [INVALID SVG] {svg}: {e}")

# 4. DAX Measures
dax_path = "dashboards/dax_measures.dax"
with open(dax_path, "r", encoding="utf-8") as f:
    dax_text = f.read()

measures = re.findall(r'([a-zA-Z0-9_]+)\s*:=', dax_text)
print(f"\nPower BI DAX Measures ({dax_path}):")
print(f"  Measures Defined ({len(measures)}): {', '.join(measures)}")
