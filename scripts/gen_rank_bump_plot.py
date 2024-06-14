from pathlib import Path

import pandas as pd

DATA_DIR = "../data"
HUGO_DIR = f"{DATA_DIR}/hugo"
DEST_DIR = f"{DATA_DIR}/rank"


for file in Path(f"{HUGO_DIR}").glob("*.csv"):
    df = pd.read_csv(file)  # noqa: PD901
    pivot_df = df.pivot_table(index="Matches", columns="Team", values="Rank").astype(
        int
    )
    pivot_df.to_csv(f"{DEST_DIR}/{file.name}", index=False)
