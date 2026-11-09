import os, glob, pandas as pd

csvs = sorted(glob.glob('data/raw/*.csv'))
for c in csvs:
    df = pd.read_csv(c)
    print(f"=== {os.path.basename(c)}: {len(df):,} Rows x {len(df.columns)} Columns ===")
    print(f"Columns: {', '.join(df.columns)}")
    print("Sample Row 0:")
    row0 = df.iloc[0].to_dict()
    for k, v in list(row0.items())[:6]:
        print(f"  {k}: {v}")
    print()
