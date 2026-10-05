import pandas as pd
import re
from datetime import datetime

INPUT_FILE = "data/raw/lab3-messy-data/messy_samples.csv"
OUTPUT_FILE = "output/samples_regex_cleaned.csv"


# -----------------------------
# Sample ID
# -----------------------------
def clean_sample_id(value):
    if pd.isna(value):
        return None

    value = str(value).strip().upper()

    # Convert forms like s-0003 to S0003
    match = re.fullmatch(r"S-?(\d{4})", value)

    if match:
        return "S" + match.group(1)

    return value


# -----------------------------
# Patient name
# -----------------------------
def clean_patient_name(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    # Standardize capitalization:
    # J. SMITH -> J. Smith
    # S. DAVIS -> S. Davis
    return value.title()


# -----------------------------
# Date of birth
# -----------------------------
def clean_dob(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    # YYYY-MM-DD
    match = re.fullmatch(
        r"(\d{4})-(\d{1,2})-(\d{1,2})",
        value
    )

    if match:
        year, month, day = match.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"

    # MM/DD/YYYY
    match = re.fullmatch(
        r"(\d{1,2})/(\d{1,2})/(\d{4})",
        value
    )

    if match:
        month, day, year = match.groups()
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"

    # MM/DD/YY
    match = re.fullmatch(
        r"(\d{1,2})/(\d{1,2})/(\d{2})",
        value
    )

    if match:
        month, day, year = match.groups()

        year = int(year)

        # Since these are dates of birth:
        # 00-26 -> 2000-2026
        # 27-99 -> 1927-1999
        if year <= 26:
            year += 2000
        else:
            year += 1900

        return f"{year:04d}-{int(month):02d}-{int(day):02d}"

    # MM.DD.YY
    match = re.fullmatch(
        r"(\d{1,2})\.(\d{1,2})\.(\d{2})",
        value
    )

    if match:
        month, day, year = match.groups()

        year = int(year)

        if year <= 26:
            year += 2000
        else:
            year += 1900

        return f"{year:04d}-{int(month):02d}-{int(day):02d}"

    # DD-Mon-YYYY
    match = re.fullmatch(
        r"(\d{1,2})-([A-Za-z]{3})-(\d{4})",
        value
    )

    if match:
        try:
            date = datetime.strptime(value, "%d-%b-%Y")
            return date.strftime("%Y-%m-%d")
        except ValueError:
            return None

    return None


# -----------------------------
# Sex
# -----------------------------
def clean_sex(value):
    if pd.isna(value):
        return "Unknown"

    value = str(value).strip().lower()

    if re.fullmatch(r"(m|male)", value):
        return "Male"

    if re.fullmatch(r"(f|female)", value):
        return "Female"

    if re.fullmatch(r"(u|unknown)", value):
        return "Unknown"

    # Blank or anything unexpected
    return "Unknown"


# -----------------------------
# Enrollment site
# -----------------------------
def clean_site(value):
    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    # Remove spaces, hyphens and underscores
    normalized = re.sub(r"[\s_-]+", "", value)

    if normalized == "sitea":
        return "Site A"

    if normalized == "siteb":
        return "Site B"

    if normalized == "sitec":
        return "Site C"

    return value.title()


# -----------------------------
# Glucose value
# -----------------------------
def clean_glucose_value(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    # Extract numeric portion from values such as 241.2*
    match = re.search(r"[-+]?\d+(?:\.\d+)?", value)

    if match:
        return float(match.group())

    return None


# -----------------------------
# Flag values containing *
# -----------------------------
def glucose_flag(value):
    if pd.isna(value):
        return False

    return bool(re.search(r"\*", str(value)))


# -----------------------------
# Glucose units
# -----------------------------
def clean_glucose_unit(value):
    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    if re.fullmatch(r"mg/dl", value, re.IGNORECASE):
        return "mg/dL"

    if re.fullmatch(r"mmol/l", value, re.IGNORECASE):
        return "mmol/L"

    return value


# -----------------------------
# Convert glucose to mg/dL
# -----------------------------
def convert_glucose_to_mg_dl(row):
    value = row["glucose_numeric"]
    unit = row["glucose_unit_clean"]

    if pd.isna(value):
        return None

    if unit == "mg/dL":
        return round(value, 1)

    if unit == "mmol/L":
        # Standard glucose conversion:
        # mmol/L × 18.0182 = mg/dL
        return round(value * 18.0182, 1)

    return None


def main():
    df = pd.read_csv(INPUT_FILE)

    # Preserve original raw values where useful
    df["sample_id_clean"] = df["sample_id"].apply(clean_sample_id)

    df["patient_name_clean"] = (
        df["patient_name"]
        .apply(clean_patient_name)
    )

    df["dob_clean"] = df["dob"].apply(clean_dob)

    df["sex_clean"] = df["sex"].apply(clean_sex)

    df["enrollment_site_clean"] = (
        df["enrollment_site"]
        .apply(clean_site)
    )

    df["glucose_numeric"] = (
        df["glucose_value"]
        .apply(clean_glucose_value)
    )

    df["glucose_flagged"] = (
        df["glucose_value"]
        .apply(glucose_flag)
    )

    df["glucose_unit_clean"] = (
        df["glucose_unit"]
        .apply(clean_glucose_unit)
    )

    df["glucose_mg_dl"] = df.apply(
        convert_glucose_to_mg_dl,
        axis=1
    )

    # Final clean table
    cleaned = pd.DataFrame({
        "sample_id": df["sample_id_clean"],
        "patient_name": df["patient_name_clean"],
        "dob": df["dob_clean"],
        "sex": df["sex_clean"],
        "enrollment_site": df["enrollment_site_clean"],
        "glucose_mg_dl": df["glucose_mg_dl"],
        "glucose_flagged": df["glucose_flagged"],
        "notes": df["notes"]
    })

    cleaned.to_csv(OUTPUT_FILE, index=False)

    print(cleaned)
    print()
    print(f"Cleaned {len(cleaned)} records.")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
