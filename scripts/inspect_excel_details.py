import glob, os, openpyxl

wbs = sorted(glob.glob('workbooks/*.xlsx'))
for w in wbs:
    wb = openpyxl.load_workbook(w, data_only=True)
    print(f"=== {os.path.basename(w)} ({os.path.getsize(w):,} bytes) ===")
    for sname in wb.sheetnames:
        ws = wb[sname]
        headers = [str(ws.cell(1, c).value) for c in range(1, min(ws.max_column+1, 8))]
        row2 = [str(ws.cell(2, c).value) for c in range(1, min(ws.max_column+1, 5))]
        print(f"  Sheet: '{sname}' | Dimensions: {ws.max_row} rows x {ws.max_column} cols")
        print(f"    Headers: {' | '.join(headers)}")
        print(f"    Row 2  : {' | '.join(row2)}")
    print()
