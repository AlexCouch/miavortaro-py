from miavortaro import MiaVortaro

with MiaVortaro() as miavortaro:
    miavortaro.komencu()
    vortoj = miavortaro.listigiVortojn()
    print(vortoj)
    rezulto = miavortaro.serĉiVorton("en")
    print(rezulto)
    miavortaro.ĉesu()