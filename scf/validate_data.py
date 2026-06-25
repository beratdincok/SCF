from pathlib import Path
import sys
import pandas as pd

BASE = Path(__file__).resolve().parent
AIRLINES = BASE / "data" / "airlines.csv"
SERVICES = BASE / "data" / "services.csv"
REQUIRED = [
    "airline_code", "category", "service_name", "ikarus_section", "ikarus_field",
    "entry_rule", "unit", "required", "when_to_enter", "verification_source",
    "notes", "sort_order"
]


def main() -> int:
    airlines = pd.read_csv(AIRLINES, dtype=str).fillna("")
    services = pd.read_csv(SERVICES, dtype=str).fillna("")
    errors: list[str] = []

    if airlines["code"].duplicated().any():
        errors.append("airlines.csv içinde mükerrer kod var.")

    missing = [column for column in REQUIRED if column not in services.columns]
    if missing:
        errors.append("services.csv eksik sütunlar: " + ", ".join(missing))
    else:
        unknown = sorted(set(services["airline_code"].str.upper()) - set(airlines["code"].str.upper()) - {""})
        if unknown:
            errors.append("Tanımsız havayolu kodları: " + ", ".join(unknown))

    if errors:
        print("VERİ DOĞRULAMA BAŞARISIZ")
        for error in errors:
            print("-", error)
        return 1

    print(f"Doğrulama başarılı: {len(airlines)} havayolu, {len(services)} hizmet satırı.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
