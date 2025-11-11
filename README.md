# NVE DATA

Dette prosjektet inneholder verktøy for å laste ned NVEs åpne datasett.

---

## Forutsetninger

* Python 3.11.9 anbefales (testet versjon)

---

## Installasjon

1. **Klon/last ned repositoriet**:

```bash
git clone https://github.com/eirikora/NVE_DATA.git
cd NVE_DATA
```

2. **Opprett et virtuelt Python miljø (valgfritt, men anbefalt)**:

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
```

3. **Installer alle nødvendige biblioteker**:

```bash
pip install -r requirements.txt
```

---

## Bruk

### 1. Last ned NVE-data

Gå inn i `nve_data/`-mappen og kjør alle skriptene for å hente ned og lagre alle metadata om elver, innsjøer og anlegg i både .csv og .jsonl format:

```bash
python lastned_nve_solkraft.py
python lastned_nve_vannkraftverk.py
python lastned_nve_varme.py
python lastned_nve_vindkraftverk.py
python lastned_nve_elvenett_del1.py
python lastned_nve_elvenett_del2.py
python lastned_nve_havvind.py
python lastned_nve_innsjøer.py
```

---

## Lisens og status

Dette er et eksperimentelt prosjekt utviklet av [Eirik Y. Øra](https://github.com/eirikora).
Ingen garantier for at scriptene er feilfrie på dette tidspunkt.
Bidrag og forslag til forbedringer er velkomne!
