# Ŝanĝnoto
Jen la ŝanĝoj de miavortaro-py 0.2-alpha

1. Aldonis `__enter__` kaj `__exit__` al MiaVortaro klazo por ke oni povas uzi `with` blokojn (#4, ac)
2. Aldonis `EraroPrizorganto` klazo por prizorgi la kompleksajn erarojn, speciale prizorgi la erarojn de `requests` (ne ankoraŭ finigita) (#4, ac)
3. Ŝanĝis `listigiVortojn` por uzi `tranĉi` parametro anstataŭ `listo`, laŭ la nova versio de MiaVortaro-servilo (#4, ac)
4. `Rajtiganto` por rajtigi la uzanton (#5, ac)
5. `PetoSendanto` por facile kaj komune sendi petojn (#5, ac)
6. Ĵetono al `MiaVortaro`, kaj `Peto` (#5, ac)
7. Uzi `verify=` sendante petojn per `request.post` kaj uzi `Authorization: Bearer {ĵetono}` en la kapo de la peto (#5, ac)
8. Provizora SSL-atestilo por sendi POST kun ĵetono (#5, ac)
9. Ŝanĝis `__enter__` kaj `__exit__` por envoki `komencu` kaj `ĉesu` respektive (master, ac)
10. Aldonis kapablon por forigi vortojn (master, ac)