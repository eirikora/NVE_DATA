#!/usr/bin/env python3
"""
Last ned alle aktuelle lag (1–6) fra NVE «Varme» og lagre som én samlet fil:
 • varmeanlegg.jsonl
 • varmeanlegg.csv

Lag 0 gir 400-feil – hoppes over.
"""

from pathlib import Path
import csv, json, time, requests

BASE = "https://nve.geodataonline.no/arcgis/rest/services/Mapservices/Varme/MapServer"

# ─── Hvilke felter vi vil beholde fra hvert lag ──────────────────────────
KEEP = {
    1: ["OBJECTID", "anlegg", "eier", "kommune"],
    2: ["OBJECTID", "aktor", "dagensInstallerteEffekt_MW", "navn", "sted", "typeSenter"],
    3: ["OBJECTID", "navn", "eier", "kapasitet"],
    4: ["OBJECTID", "Anlegg", "Kommune", "Selskap", "Summert"],
    5: ["OBJECTID", "Anlegg", "Kommune", "Selskap", "Summert"],
    6: ["OBJECTID", "Anlegg", "Kommune", "Selskap", "Summert"],
}

# lag-type legges som varmeType-felt i hver record
VARME_TYPE = {
    1: "industri",
    2: "datasenter",
    3: "avfallsforbrenning",
    4: "fjernvarme_konsesjon",
    5: "fjernvarme_effekt",
    6: "fjernvarme_produksjon",
}

PARAMS = {
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "true",
    "outSR": 4326,
    "f": "json",
    "resultRecordCount": 1000,
}

def centroid_from_rings(rings):
    """Grov centroid av polygon(rings) → lat, lon (None,None hvis tom)."""
    sx = sy = n = 0
    for ring in rings or []:
        for x, y, *_ in ring:
            sx += x
            sy += y
            n += 1
    return (sy / n, sx / n) if n else (None, None)

# Samle alle anlegg i én liste
all_rows = []

for layer in range(1, 7):               # lag 1–6
    url = f"{BASE}/{layer}/query"
    keep = KEEP[layer]
    varme_type = VARME_TYPE[layer]

    offset = 0
    while True:
        rsp = requests.get(url, params=PARAMS | {"resultOffset": offset}, timeout=60)
        try:
            rsp.raise_for_status()
        except Exception as e:
            print(f"⚠️  Lag {layer}: HTTP-feil {e}; hopper over dette laget.")
            break

        data = rsp.json()
        if "error" in data:
            print(f"⚠️  Lag {layer}: {data['error']}; hopper over.")
            break

        feats = data.get("features", [])
        for f in feats:
            a = f.get("attributes", {})

            row = {k: a.get(k) for k in keep}  # ønskede felter
            row["varmeType"] = varme_type      # legg til type

            geom = f.get("geometry", {}) or {}
            if "x" in geom and "y" in geom:    # punktlag
                row["lat"], row["lon"] = geom["y"], geom["x"]
            else:                              # polygon – beregn centroid
                row["lat"], row["lon"] = centroid_from_rings(geom.get("rings"))

            all_rows.append(row)

        print(f" Lag {layer} ({varme_type}) – offset {offset:>5}  +{len(feats):>4}  →  {len(all_rows)} totalt")

        if len(feats) < PARAMS["resultRecordCount"]:
            break
        offset += PARAMS["resultRecordCount"]
        time.sleep(0.25)

# ── Skriv samlede filer ────────────────────────────────────────────────────
if all_rows:
    out_jsonl = Path("varmeanlegg.jsonl")
    out_csv   = Path("varmeanlegg.csv")

    with out_jsonl.open("w", encoding="utf-8") as jf:
        for r in all_rows:
            jf.write(json.dumps(r, ensure_ascii=False) + "\n")

    # Finn alle unike felt fra alle lag
    all_fields = set()
    for r in all_rows:
        all_fields.update(r.keys())

    # Ordne feltene: OBJECTID først, varmeType, så resten, lat/lon sist
    field_order = ["OBJECTID", "varmeType"]
    field_order += sorted([f for f in all_fields if f not in ["OBJECTID", "varmeType", "lat", "lon"]])
    field_order += ["lat", "lon"]

    with out_csv.open("w", newline="", encoding="utf-8") as cf:
        w = csv.DictWriter(cf, fieldnames=field_order)
        w.writeheader()
        w.writerows(all_rows)

    print(f"\n✅  Totalt {len(all_rows)} varmeanlegg lagret til {out_jsonl} / {out_csv}")
else:
    print("\n⚠️  Ingen varmeanlegg lastet ned")
