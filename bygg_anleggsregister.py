#!/usr/bin/env python3
"""
Bygg et samlet anleggsregister fra alle NVE JSONL-filer.
Hver record får en GID (Global ID) på format PREFIX.ID basert på anleggsreg_prefix.csv.
"""

from __future__ import annotations
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List

PREFIX_CONFIG = Path("anleggsreg_prefix.csv")
OUTPUT_FILE = Path("anleggsregister.jsonl")


def load_prefix_config() -> List[Dict[str, str]]:
    """Last inn prefix-konfigurasjon fra CSV"""
    config = []
    with PREFIX_CONFIG.open(encoding="utf-8-sig") as f:  # utf-8-sig for å håndtere BOM
        reader = csv.DictReader(f)
        for row in reader:
            config.append({
                "prefix": row["PREFIX"].strip(),
                "tema": row["TEMA"].strip(),
                "fil": row["FIL"].strip(),
                "id_felt": row["ID_FELT"].strip(),
            })
    return config


def process_file(fil: str, prefix: str, tema: str, id_felt: str) -> int:
    """Prosesser en JSONL-fil og skriv til anleggsregister med GID"""
    file_path = Path(fil)

    if not file_path.exists():
        print(f"⚠️  Hopper over {fil} (finnes ikke)")
        return 0

    count = 0
    skipped = 0

    with file_path.open(encoding="utf-8") as infile, \
         OUTPUT_FILE.open("a", encoding="utf-8") as outfile:

        for line_num, line in enumerate(infile, 1):
            line = line.strip()
            if not line:
                continue

            try:
                record = json.loads(line)

                # Hent ID-verdi
                id_value = record.get(id_felt)

                if id_value is None:
                    print(f"  ⚠️  {fil}:{line_num} mangler {id_felt}, hopper over")
                    skipped += 1
                    continue

                # Lag GID
                gid = f"{prefix}.{id_value}"

                # Bygg ny ordnet dict med AnleggsType først, GID andre
                ordered_record = {
                    "AnleggsType": tema,
                    "GID": gid,
                }

                # Legg til resten av feltene fra original record
                for key, value in record.items():
                    if key not in ordered_record:
                        ordered_record[key] = value

                # Legg til metadata sist
                ordered_record["_kildefil"] = fil
                ordered_record["_id_felt"] = id_felt

                # Skriv til output
                outfile.write(json.dumps(ordered_record, ensure_ascii=False) + "\n")
                count += 1

            except json.JSONDecodeError as e:
                print(f"  ⚠️  {fil}:{line_num} JSON-feil: {e}")
                skipped += 1
            except Exception as e:
                print(f"  ⚠️  {fil}:{line_num} Feil: {e}")
                skipped += 1

    if skipped > 0:
        print(f"  ✓  {fil}: {count:,} records (+{skipped} hoppet over)")
    else:
        print(f"  ✓  {fil}: {count:,} records")

    return count


def main() -> None:
    print("Bygger anleggsregister fra NVE-data...")
    print(f"Leser konfigurasjon fra {PREFIX_CONFIG}")

    # Last inn konfigurasjon
    try:
        config = load_prefix_config()
    except FileNotFoundError:
        sys.exit(f"❌  Finner ikke {PREFIX_CONFIG}")
    except Exception as e:
        sys.exit(f"❌  Feil ved lesing av {PREFIX_CONFIG}: {e}")

    print(f"Fant {len(config)} kildefiler i konfigurasjonen\n")

    # Slett eksisterende output-fil
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()
        print(f"Slettet eksisterende {OUTPUT_FILE}\n")

    # Prosesser hver fil
    total_records = 0
    processed_files = 0

    for item in config:
        prefix = item["prefix"]
        tema = item["tema"]
        fil = item["fil"]
        id_felt = item["id_felt"]

        count = process_file(fil, prefix, tema, id_felt)
        if count > 0:
            processed_files += 1
        total_records += count

    print(f"\n{'='*60}")
    print(f"✅  Fullført!")
    print(f"   Prosesserte filer: {processed_files}/{len(config)}")
    print(f"   Totalt records: {total_records:,}")
    print(f"   Output: {OUTPUT_FILE}")
    print(f"{'='*60}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\n⏹️  Avbrutt av bruker.")
