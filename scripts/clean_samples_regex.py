import pandas as pd
import re
from datetime import datetime

INPUT_FILE = "data/raw/lab3-messy-data/messy_samples.csv"
OUTPUT_FILE = "output/samples_regex_cleaned.csv"


def clean_sample_id(value):
    value = str(value).strip().upper()
    match = re.fullmatch(r"S-?(\d{4})", value)
    return "S" + match.group(1) if match else value


def clean_name(value):
    return str(value).strip().title()


def clean_dob(value):
    value = str(value).strip()

    formats = [
        "%m/%d/%Y",
        "%m/%d/%y",
        "%m.%d.%y",
        "%Y-%m-%d",
        "%d-%b-%Y"
    ]

    for fmt in formats:
        try:
            d = datetime.strptime(value, fmt)
            return d.strftime("%Y-%m-%d")
        except ValueError:
            pass

    return None


def clean_sex(value):
    if pd.isna(value):
        return "Unknown"

    value = str(value).strip().lower()

    if value in ["m", "male"]:
        return "Male"
    elif value in ["f", "female"]:
        return "Female"
    elif value in ["u", "unknown"]:
        return "Unknown"

    return "Unknown"


def clean_site(value):
    value = str(value).strip().lower()
    value = re.sub(r"[\s_-]+", "", value)

    if value == "sitea":
        return "Site A"
    elif value == "siteb":
        return "Site B"
    elif value == "sitec":
        return "Site C"

    return value


def clean_glucose(value):
    match = re.search(r"\d+(?:\.\d+)?", str(value))
    return float(match.group()) if match else None


def clean_unit(value):
    value = str(value).strip().lower()

    if value == "mg/dl":
        return "mg/dL"
    elif value == "mmol/l":
        return "mmol/L"

    return value


def to_mg_dl(value, unit):
    if unit == "mg/dL":
        return value
    elif unit == "mmol/L":
        return round(value * 18.0182, 1)

    return None


def main():
    df = pd.read_csv(INPUT_FILE)

    df["sample_id"] = df["sample_id"].apply(clean_sample_id)
    df["patient_name"] = df["patient_name"].apply(clean_name)
    df["dob"] = df["dob"].apply(clean_dob)
    df["sex"] = df["sex"].apply(clean_sex)
    df["enrollment_site"] = df["enrollment_site"].apply(clean_site)

    df["glucose_value"] = df["glucose_value"].apply(clean_glucose)
    df["glucose_unit"] = df["glucose_unit"].apply(clean_unit)

    df["glucose_mg_dl"] = df.apply(
        lambda row: to_mg_dl(
            row["glucose_value"],
            row["glucose_unit"]
        ),
        axis=1
    )

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Cleaned {len(df)} records.")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()