# miavortaro.py 0.1-alpha
Tiu ĉi libraro Python-a estas oficiala libraro por integri komunikadon inter aliaj apoj kaj MiaVortaro per Python

## Kiel Uzi
```python
## Unue: Importi miavortaro.MiaVortaro
from miavortaro import MiaVortaro

## Due: Krei novan MiaVortaro-objekton, tiu ĉi estas la motoro
miavortaro = MiaVortaro()
## Trie: Envoki la "komencu" agon de la motoro
miavortaro.komencu()
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
## Haltu/Ĉesu la motoron
miavortaro.ĉesu()
```

## Rimarkoj
1. Tuje, miavortaro estas ankoraŭ programata, kaj neniuj povas nune uzi miavortaro-n ĝis ĝi estas preta por eldoni pere de AWS. Mi (Alex) devas kalkuli la kostojn de la servilo kaj la administradon de la apo. Ĝis tiam, mi daŭras plibonigi la librarojn kaj la tutan apon ankaŭ.
2. Oni devas kurigi la tutan apon el https://github.com/AlexCouch/miavortaro, kaj ankaŭ mi aldonos ilon por plenigi la servilon kun vortoj baldaŭ por ke oni ne devas konstante plenigi la servilon memstare.
3. Neniu povas aldoni vortojn ankoraŭ. Mi havas la manieron por aldoni vortojn, sed mi laboras plibonigi la funkcion de la aldonado de vortoj, do baldaŭ oni povas submeti vortojn estontece, sed mi ne certas tiel kiel mi deziras ke, oni submetu vortojn sekure.