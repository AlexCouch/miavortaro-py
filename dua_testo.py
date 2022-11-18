from miavortaro import MiaVortaro

from pprint import pprint

with MiaVortaro("Admin", "zamenhof7881") as miavortaro:
    # respondo = miavortaro.aldoniVorton("enmeti", "meti en")
    # if respondo is None:
    #     print("Ne povis aldoni aŭ ŝanĝi vorton")
    #     exit(1)
    # elif respondo.kodo != 200:
    #     print(f"Malsukcesis aldoni/ŝanĝi vorton: {respondo.kodo}")
    #     exit(1)
    # else:
    #     print("Sukcesas!")
    respondo = miavortaro.forigiVorton("enmeti")
    if respondo is None:
        print("Ne povis forigi vorton")
        exit(1)
    elif respondo.kodo != 200:
        print(f"Malsukcesis forigi vorton: {respondo.kodo}")
        exit(1)
    else:
        print("Sukcesas!")
    rezulto = miavortaro.serĉiVorton("en")
    pprint(rezulto)