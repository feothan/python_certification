# clean_data.py
# ------------------------------------------------------------
# Cleans a messy CSV file: normalizes names, dates, removes dups
# and saves the cleaned version in the same folder as the input.
# ------------------------------------------------------------

from pathlib import Path
import pandas as pd
import re, io

# --- 1. regex to remove comma from month-date strings like "Feb 2, 2024"
MONTH_COMMA = re.compile(
    r'((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*)\s+(\d{1,2}),\s+(\d{4})'
)

def clean_client_data(input_file: str, output_file: str | None = None) -> None:
    # A) establish in/out paths so output lands beside the input file
    in_path = Path(input_file)
    out_path = Path(output_file) if output_file else in_path.with_name("clean_clients.csv")

    # --- 2. read and pre-sanitize the text
    raw = in_path.read_text(encoding="utf-8")
    raw = MONTH_COMMA.sub(r"\1 \3 \4", raw)

    # --- 3. parse CSV
    df = pd.read_csv(io.StringIO(raw))

    # --- 4. normalize names
    def normalize_name(name):
        if not isinstance(name, str):
            return None
        name = name.strip()
        if "," in name:
            last, first = name.split(",", 1)
            return f"{first.strip().title()} {last.strip().title()}"
        return name.title()

    df["name"] = df["name"].apply(normalize_name)

    # --- 5. normalize dates
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce").dt.strftime("%Y-%m-%d")

    # --- 6. drop dups & incomplete rows
    df = df.drop_duplicates().dropna(subset=["email", "start_date"])

    # --- 7. write out right next to input file
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print("Cleaned data saved to:", out_path.resolve())


# --- 8. run when executed directly
if __name__ == "__main__":
    clean_client_data("raw_clients.csv")
