# miavortaro.py 0.2-alpha
Tiu ĉi libraro Python-a estas oficiala libraro por integri komunikadon inter aliaj apoj kaj MiaVortaro per Python

## Kiel Uzi
Jen kiel uzi ĝin sen la rajtigo
```python
## Unue: Importi miavortaro.MiaVortaro
from miavortaro import MiaVortaro

## Due: Krei novan MiaVortaro-objekton, tiu ĉi estas la motoro
with MiaVortaro() as miavortaro:
    ## Opcio: Voki "listigiVortojn" por listigi vortojn pere de iom sametempe
    ##  Rimarku, ke la defaŭlta valoro de la funkcio estas 10, kaj oni povas enmeti
    ##     iun alian valoron volante
    vortoj = miavortaro.listigiVortojn()
    print(vortoj)
    ## Opcio: Voki "serĉiVorton" por serĉi tra la tuta servilo vortojn 
    #   kiuj kongruas kun la enigaĵo 
    #   (ekzemple, ĉi tie "en" donu al vi ĉiujn vortojn kiuj enhavas "en")
    rezulto = miavortaro.serĉiVorton("en")
    print(rezulto)
```

Jen kiel uzi ĝin kun la rajtigo (rimarku: nuntempe, nur mi povas uzi ĝin ĝis mi integras manieron por havi adminajn kontojn estontece)

```python
from miavortaro import MiaVortaro

from pprint import pprint

with MiaVortaro("Admin", "zamenhof7881") as miavortaro:
    respondo = miavortaro.aldoniVorton("enmeti", "meti en")
    if respondo is None:
        print("Ne povis aldoni aŭ ŝanĝi vorton")
        exit(1)
    elif respondo.kodo != 200:
        print(f"Malsukcesis aldoni/ŝanĝi vorton: {respondo.kodo}")
        exit(1)
    else:
        print("Sukcesas!")
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
    pprint(rezulto) #[]
```

Baldaŭ mi aldonos adminajn kontojn

## Rimarkoj
1. Tuje, miavortaro estas ankoraŭ programata, kaj neniuj povas nune uzi miavortaro-n ĝis ĝi estas preta por eldoni pere de AWS. Mi (Alex) devas kalkuli la kostojn de la servilo kaj la administradon de la apo. Ĝis tiam, mi daŭras plibonigi la librarojn kaj la tutan apon ankaŭ.
2. Oni devas kurigi la tutan apon el https://github.com/AlexCouch/miavortaro, kaj ankaŭ mi aldonos ilon por plenigi la servilon kun vortoj baldaŭ por ke oni ne devas konstante plenigi la servilon mane.
3. Neniu povas aldoni vortojn ankoraŭ. Mi havas la manieron por aldoni vortojn, sed mi laboras plibonigi la funkcion de la aldonado de vortoj, do baldaŭ oni povas submeti vortojn estontece, sed mi ne certas tiel kiel mi deziras ke, oni submetu vortojn sekure.
4. La nuna versio de la libraro postulas SSL-atestilon, do nune la libraro kunvenas kun la SSL-atestilo ĉiuokaze. Ĝis la SSL-atestilon povas validigi mi, ĝi devas esti uzata ĉi tie nuntempe. Kiam la retregnon aĉetas mi, mi ĝisdatigos tiun ĉi por ke ĝi ne plu uzas la SSL-atestilon.