from miavortaro import MiaVortaro

from pprint import pprint

with MiaVortaro() as miavortaro:
    vortoj = miavortaro.listigiVortojn()
    pprint(vortoj)
    rezulto = miavortaro.serĉiVorton("en")
    pprint(rezulto)