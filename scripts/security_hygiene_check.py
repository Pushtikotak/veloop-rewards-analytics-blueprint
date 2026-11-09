"""
Security and Hygiene Audit Script
Author: Pushti Kotak
Task: Data Analyst Internship Task 01
Purpose: Verify zero credentials, API keys, passwords, enrollment numbers, or temporary files.
"""

import os
import re

regex_patterns = {
    'Private Key': re.compile(r'-----BEGIN [A-Z]+ PRIVATE KEY-----'),
    'AWS Key': re.compile(r'AKIA[0-9A-Z]{16}'),
    'Hardcoded Secret': re.compile(r'(?i)(api_key|secret_key|access_token)\s*=\s*[\'"][a-zA-Z0-9_\-]{16,}[\'"]'),
    'Hardcoded Password': re.compile(r'(?i)password\s*=\s*[\'"][^\'"]{6,}[\'"]'),
    'Enrollment Number': re.compile(r'(?i)enrollment\s*(?:no|number|#)?\s*[:=]\s*[0-9]+')
}

temp_extensions = {'.tmp', '.bak', '.swp', '.swo', '.pyc', '.DS_Store'}
temp_prefixes = {'~', '~$'}

found_secrets = []
found_temp_files = []

for root, dirs, files in os.walk('.'):
    if '.git' in dirs:
        dirs.remove('.git')
    if '.venv' in dirs:
        dirs.remove('.venv')
    if 'data' in dirs:
        dirs.remove('data')
    for f in files:
        fp = os.path.join(root, f)
        # Check temporary files
        _, ext = os.path.splitext(f)
        if ext.lower() in temp_extensions or any(f.startswith(p) for p in temp_prefixes):
            found_temp_files.append(fp)
            
        # Check text files for credentials
        if ext.lower() in {'.md', '.py', '.sql', '.dax', '.mermaid', '.json', '.txt', '.toml'}:
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                    for idx, line in enumerate(fh, 1):
                        for name, pat in regex_patterns.items():
                            if pat.search(line):
                                found_secrets.append((fp, idx, name, line.strip()[:80]))
            except Exception:
                pass

print(f"Total Temporary / Unnecessary Files Found: {len(found_temp_files)}")
for tf in found_temp_files:
    print(f"  [TEMP] {tf}")

print(f"Total Hardcoded Secrets / Credentials Found: {len(found_secrets)}")
for sc in found_secrets:
    print(f"  [SECRET] {sc}")

if len(found_temp_files) == 0 and len(found_secrets) == 0:
    print("HYGIENE STATUS: 100% CLEAN - READY FOR PUBLIC GITHUB REPOSITORY")
