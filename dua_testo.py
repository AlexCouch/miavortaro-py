from miavortaro import MiaVortaro

miavortaro = MiaVortaro("Admin", "zamenhof7881")
miavortaro.komencu()
respondo = miavortaro.aldoniVorton("enmeti", "meti en")
if respondo is None:
    print("Ne povis aldoni aŭ ŝanĝi vorton")
elif respondo.kodo != 200:
    print(f"Malsukcesis aldoni/ŝanĝi vorton: {respondo.kodo}")
else:
    print("Sukcesas!")
miavortaro.ĉesu()