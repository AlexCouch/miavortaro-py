La Motoro
=========
La motoro havas 2 fadenojn, kiuj funkcias jene:
    1. La Ĉefa Fadeno, de la uzanto, per kiu la vokanto loĝas.
    2. La Prilaboranto fadeno, kiu prilaboras super la petoj de la uzanto.

Estas 3 paŝoj en la motoro:
    1. Komenco
    2. Kurado
    3. Ĉeso/Halto

Komenco
-------
La komenco enmetas la komencigajn informojn en la motoron por noti, prilabori super petoj, kaj aŭskulti respondojn al petoj.
La notilo estas la "python logging" libraro, kiu enhavas la funkciecojn por noti la erarojn kaj ĝustigajn notojn, ktp.
Estas ankaŭ templimo por la penoj de la sendado de petoj. La petoj estas seditaj kaj tuje sekve la respondoj estas atenditaj ĝis respondo alvenas.
Se respondo ne alvenas post 5 sekundoj, tiam la atendanto ne plu atendas la respondon (vidu la `petojn <petoj.html#atendanto>`__ por legi kiel la petoj estas senditaj kaj kiel respondoj estas atenditaj)