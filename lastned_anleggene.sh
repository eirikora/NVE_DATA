#!/bin/bash
echo "Laster ned alle NVE-data..."
echo

python3 lastned_nve_andre_inntak.py
python3 lastned_nve_andre_utlop.py
python3 lastned_nve_andre_vassdragsanlegg.py
python3 lastned_nve_dammer.py
# python3 lastned_nve_delfelt.py
# python3 lastned_nve_elvenett_del1.py
# python3 lastned_nve_elvenett_del2.py
python3 lastned_nve_havvind.py
python3 lastned_nve_ikke_utbygd_dam.py
python3 lastned_nve_ikke_utbygd_inntakspunkt.py
python3 lastned_nve_ikke_utbygd_magasin.py
python3 lastned_nve_ikke_utbygd_vannkraftverk.py
python3 lastned_nve_ikke_utbygd_vannvei.py
# python3 lastned_nve_innsjøer.py
python3 lastned_nve_inntakspunkt.py
python3 lastned_nve_magasiner.py
python3 lastned_nve_solkraft.py
python3 lastned_nve_utlopspunkt.py
python3 lastned_nve_vannkraftverk.py
python3 lastned_nve_vannveier.py
python3 lastned_nve_varme.py
# python3 lastned_nve_vassdragregine.py
python3 lastned_nve_vindkraftverk.py

echo
echo "Bygger anleggsregister..."
python3 bygg_anleggsregister.py

echo
echo "Ferdig!"
