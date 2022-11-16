import time
from dataclasses import dataclass
import enum
import threading
import json
import logging

class PetajSpecoj(enum.Enum):
    """ 
    PetajSpecoj estas la enumo por la specoj da petoj kiujn oni povas uzi

    Tiuj ĉi estas uzataj kiam novajn petojn kreas kaj sendas la programo, al la servilo.
    La nomoj de la specoj estas memklarigeblaj
    """
    GET = enum.auto()
    POST = enum.auto()
    DELETE = enum.auto()

@dataclass
class Peto:
    """
    Klazo por reprezenti unuopan peton al la servilo, kiu enhavas la informaĵon por la specifa peto.
    
    Ĉi tiu estas kreata kiam aga funkcio (t.e listigiVortojn, serĉiVorton, ktp), kaj la peton devas envicigi la motoro por sendi al la servilo.
    La peto reprezentas la aktualan peton kiun sendas la motoro, ekzemple:
        
        Peto(PetajSpecoj.GET, 'serĉiVorton', "/", time.time(), {"vortoj", "s"}) fariĝas jene:
            GET /?vortoj=s HTTP/1.1

    speco: La speco de la peto estas uzata por krei la ĝustan mesaĝon per requests.py
    nomo: La nomo estas uzata por trovi la ĝustajn respondojn inter fadenoj (vidu la dokojn de la motoro MiaVortaro klazo)
    vojo: La vojo laŭ la servilo, al kiu la peto estas sendata (/, /ensaluti, /registri, ktp)
    tempo: Tiam, kiam la peto estas kreata (ne uzata nune sed estontece la libraro ja uzos ĝin pli ofte)
    parametroj: La parametroj kiujn enhavas la peto kiam ĝi estas sendita al la servilo, ekzemple, "/?listo=10"
    korpo: La korpo aŭ la tutaĵo de la peto, per kiu la servilo faras aferojn laŭ la peto, ekzemple, ŝanĝi vortojn, ensaluti per konto-detaloj, ktp
    """
    speco       : int
    nomo        : str
    vojo        : str
    tempo       : int
    parametroj  : dict[str, str]
    korpo       : str

@dataclass
class Respondo:
    ##
    ##  Respondo(PetajSpecoj.GET, 200, 'serĉiVorton', "/", time.time(), "{...}") fariĝas jene:
    ##      HTTP/1.1 200 OK
    ##      { ... }
    ##
    speco : int
    kodo  : int
    nomo  : str
    vojo  : str
    tempo : int
    korpo : str

class PetaroŜloso:
    def __init__(self):
        self.__ŝlosita = False
        self.__petaro = []

    def preniPeton(self, penoj=0):
        if penoj == 5:
            return None

        if self.__ŝlosita:
            time.sleep(0.1)
            return preniPeton(penoj+1)
        
        if len(self.__petaro) == 0:
            return None

        self.__ŝlosita = True
        peto = self.__petaro.pop()
        self.__ŝlosita = False
        return peto

    def enmetiPeton(self, peto, penoj=0):
        if penoj == 5:
            return False

        if self.__ŝlosita:
            time.sleep(0.1)
            return enmetiPeton(peto, penoj+1)

        self.__ŝlosita = True
        self.__petaro.append(peto)
        self.__ŝlosita = False
        return True

class Fadeno:
    def __init__(self, notilo, nomo, revoko):
        self.__kurado_flago = False
        self.__revoko = revoko
        self.__notilo = notilo
        self.__fadeno = threading.Thread(target=self.kuro)

        self.__nomo = nomo

    def elŝalti(self):
        if self.__kurado_flago:
            self.__kurado_flago = False

        self.__fadeno.join()
        
    def ŝalti(self):
        self.__kurado_flago = True
        self.__fadeno.start()

    def kuro(self):
        if self.__kurado_flago is False:
            self.__notilo.error("La fadenon devas alŝalti oni, kaj neniu faris tion.")
            return

        while self.__kurado_flago is True:
            try:
                if not self.__revoko():
                    self.__notilo.error("Revoko malsukcesis, legu la antaŭajn konsilajn notojn")
                time.sleep(0.5)
            except Exception as e:
                continue
            except Error as e:
                continue

class EraroPrizorganto:
    def __init__(self, notilo):
        self.__notilo = notilo

    def peto_eraro(self, peto, respondo, escepto):
        eraro_mesaĝo = str(escepto)

        eraro_ŝnuro = ""
        eraro_ŝnuro += "Malsukcesis sendi GET peton:"
        eraro_ŝnuro += f"    - Kiam la peton sendas: {peto.method} {peto.url}?{peto.params}"
        eraro_ŝnuro += f"    - Auth: {peto.auth}"
        eraro_ŝnuro += f"    - Peto-korpo: {peto.data}"
        eraro_ŝnuro += "Kaj la respondon havigis:"
        eraro_ŝnuro += f"    - Status Code: {respondo.status_code}"
        eraro_ŝnuro += f"    - Vojo: {respondo.url}"
        eraro_ŝnuro += f"    - Kialo: {respondo.reason}"
        eraro_ŝnuro += f"    - Korpo: {respondo.text()}"

        self.__notilo.error(eraro_ŝnuro)


import requests

class MiaVortaro:
    def __init__(self):
        self.__lasta_respondo = None
        self.__lasta_peto = None
        self.__lasta_stato = None

        self.__miavortaro_retregno = "http://localhost:5000"
        
        #Listo da Petoj
        self.__jenaj_petoj = PetaroŜloso()
        self.__nunaj_respondoj = {}

        self.__peta_prilaboranto = None

        self.__notilo = None
        self.__tempolimo = 5 #sekundoj

        self.__eraro_prizorganto = None

    def __enter__(self):
        return MiaVortaro()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return

    def prilaboriPetojn(self):
        peto = self.__jenaj_petoj.preniPeton()
        if peto is None:
            return True
        respondo = None
        tempo = None
        ##NOTE: Eble ni ŝanĝu `requests.get` al `requess.async.get` por ke ni povus utiligi async-funkciecon
        self.__notilo.debug(f"Sendanta peton al {self.__miavortaro_retregno + peto.vojo}?{peto.parametroj}")
        if peto.speco is PetajSpecoj.GET:
            try:
                respondo = requests.get(self.__miavortaro_retregno + peto.vojo, params=peto.parametroj, headers={'Content-Type': 'application/json'})
                now = time.time()
            except ConnectionError as e:
                self.__notilo.exception(f"Malsukcesis konekti", exec_info=e)
                return False
            except requests.exceptions.ConnectionError as e:
                self.__notilo.exception(f"Malsukcesis konekti: {e}")
                return False
            except requests.exceptions.RequestException as e:
                ##TODO: Ni devas movi tion ĉi en novan funkcion en alia klazo
                ##TODO: Kaj ankaŭ ni devas aldoni erarojn al eraro-listo iam
                self.__eraro_prizorganto.peto_eraro(e.peto, e.respondo, e)
                return False
            except Exception as e:
                self.__notilo.exception(f"Ekcepto okazis: {e}")
                return False
        else:
            self.__notilo.critical("Aliaj petaj specoj ne ankoraŭ pretas")
            return False
        korpo = respondo.text
        self.__nunaj_respondoj[peto.nomo] = Respondo(peto.speco, respondo.status_code, peto.nomo, respondo.url, tempo, respondo.text)
        self.__notilo.debug(korpo)
        return True
        

    def komencu(self, tempolimo=5):
        self.__tempolimo = tempolimo

        self.__notilo = logging.getLogger("miavortaro")
        self.__eraro_prizorganto = EraroPrizorganto(self.__notilo)

        ##Kreu la konsolan traktilon kaj aldonu al ĝi la formatilo, kaj tiam aldonu ĝin al la notilo
        konsolo = logging.StreamHandler()
        formatilo = logging.Formatter('[%(filename)s:%(lineno)s - %(funcName)s][%(levelname)s] %(message)s')
        konsolo.setFormatter(formatilo)
        self.__notilo.addHandler(konsolo)

        self.__peta_prilaboranto = Fadeno(self.__notilo, "peta_prilaboranto", self.prilaboriPetojn)
        self.__peta_prilaboranto.ŝalti()

    def ĉesu(self):
        self.__peta_prilaboranto.elŝalti()

    def __atendiRespondon(self, nomo):
        komenco = time.time()
        lasta_kontrolo = komenco
        respondo = None

        while True:
            if lasta_kontrolo - komenco > self.__tempolimo:
                break

            ##NOTE: Ni devas igi self.__nunaj_respondoj esti samtempa (concurrent)
            if nomo in self.__nunaj_respondoj:
                respondo = self.__nunaj_respondoj.pop(nomo)
                break

            nun = time.time()
            diferenco = nun - lasta_kontrolo
            if diferenco < 1:
                time.sleep(1 - diferenco)
                lasta_kontrolo = nun
                continue
        return respondo

    def __senduPeton(self, speco, nomo, vojo, parametroj, korpo):
        self.__jenaj_petoj.enmetiPeton(Peto(speco, nomo, vojo, time.time(), parametroj, korpo))
        respondo = self.__atendiRespondon(nomo)
        if respondo is None:
            self.__notilo.error("Ne povis havigi respondon de la servilo. Aŭ reprovu poste aŭ kontaktu la adminon de la servilo por helpo.")
            return None
        return respondo

    def __senduGET(self, nomo, vojo, parametroj, korpo):
        return self.__senduPeton(PetajSpecoj.GET, nomo, vojo, parametroj, korpo)

    def serĉiVorton(self, vorto):
        ## Paŝo 1: Sendu la serĉiVorton peton al la servilo kaj atendu la respondon per self.__senduPeton
        respondo = self.__senduGET(nomo = "serĉiVorton", vojo = "/", parametroj = {"vortoj": vorto}, korpo = None)
        if respondo is None:
            return None
        ## Paŝo 2: Traduki la respondo-korpon al Vortaro objekto (Dictionary object)
        return json.loads(respondo.korpo)

    def listigiVortojn(self, komenco=0, fino=10):
        respondo = self.__senduGET(nomo = "listigiVortojn", vojo = "/", parametroj = {"tranĉi": f"{komenco},{fino}"}, korpo = None)
        if respondo is None:
            return None
        return json.loads(respondo.korpo)

        