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
        
        Peto(PetajSpecoj.GET, 'serĉiVorton', "/", time.time(), {"vortoj", "s"}, "", "") fariĝas jene:
            GET /?vortoj=s HTTP/1.1

    speco: La speco de la peto estas uzata por krei la ĝustan mesaĝon per requests.py
    nomo: La nomo estas uzata por trovi la ĝustajn respondojn inter fadenoj (vidu la dokojn de la motoro MiaVortaro klazo)
    vojo: La vojo laŭ la servilo, al kiu la peto estas sendata (/, /ensaluti, /registri, ktp)
    tempo: Tiam, kiam la peto estas kreata (ne uzata nune sed estontece la libraro ja uzos ĝin pli ofte)
    parametroj: La parametroj kiujn enhavas la peto kiam ĝi estas sendita al la servilo, ekzemple, "/?listo=10"
    rajtigo: La ĵetono uzata por rajtigi la uzanton
    korpo: La korpo aŭ la tutaĵo de la peto, per kiu la servilo faras aferojn laŭ la peto, ekzemple, ŝanĝi vortojn, ensaluti per konto-detaloj, ktp
    """
    speco       : int
    nomo        : str
    vojo        : str
    tempo       : int
    parametroj  : dict[str, str]
    rajtigo     : str
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

class PetoSendanto:
    def __init__(self, retregno, notilo, eraro_prizorganto):
        self.__retregno = retregno
        self.__notilo = notilo
        self.__eraro_prizorganto = eraro_prizorganto
        
    def kreiEraron(self, peto, ekcepto):
        self.__notilo.exception(f"Malsukcesis sendi {PetajSpecoj(peto.speco).name} peton:")
        self.__notilo.exception(f"    - Kiam la peton sendas: {ekcepto.request.method} {ekcepto.request.url}?{ekcepto.params}")
        self.__notilo.exception(f"    - Auth: {ekcepto.auth}")
        self.__notilo.exception(f"    - Peto-korpo: {ekcepto.data}")
        self.__notilo.exception(f"Kaj la respondon havigis:")
        self.__notilo.exception(f"    - Status Code: {ekcepto.response.status_code}")
        self.__notilo.exception(f"    - Vojo: {ekcepto.response.url}")
        self.__notilo.exception(f"    - Kialo: {ekcepto.response.reason}")
        self.__notilo.exception(f"    - Korpo: {ekcepto.response.json()}")

    def __sendiGET(self, peto):
        try:
            respondo = requests.get(self.__retregno + peto.vojo, params=peto.parametroj, headers={'Content-Type': 'application/json'}, verify="keystore.pem")
            now = time.time()
            return self.__havigiRespondon(peto, respondo)
        except requests.exceptions.SSLError as e:
            self.__notilo.exception(f"SSL eraro okazis: {e}")
            return None
        except requests.exceptions.RequestException as e:
            self.kreiEraron(peto, e)
            return None
        except Exception as e:
            self.__notilo.exception(f"Ekcepto okazis: {e}")
            return None

    def __sendiPOST(self, peto):
        try:
            respondo = requests.post(self.__retregno + peto.vojo, params=peto.parametroj, headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {peto.rajtigo}'
            }, data=peto.korpo, verify="keystore.pem")
            now = time.time()
            return self.__havigiRespondon(peto, respondo)
        except requests.exceptions.RequestException as e:
            self.kreiEraron(peto, e)
            return None
        except Exception as e:
            self.__notilo.exception(f"Ekcepto okazis: {e}")
            return None

    def __sendiDELETE(self, peto):
        try:
            respondo = requests.delete(self.__retregno + peto.vojo, params=peto.parametroj, headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {peto.rajtigo}'
            }, data=peto.korpo, verify="keystore.pem")
            now = time.time()
            return self.__havigiRespondon(peto, respondo)
        except requests.exceptions.RequestException as e:
            self.kreiEraron(peto, e)
            return None
        except Exception as e:
            self.__notilo.exception(f"Ekcepto okazis: {e}")
            return None

    def __havigiRespondon(self, peto, respondo):
        return Respondo(peto.speco, respondo.status_code, peto.nomo, peto.vojo, time.time(), respondo.text)

    def sendiPeton(self, peto):
        respondo = None
        try:
            if peto.speco is PetajSpecoj.GET:
                respondo = self.__sendiGET(peto)
            elif peto.speco is PetajSpecoj.POST:
                respondo = self.__sendiPOST(peto)
            elif peto.speco is PetajSpecoj.DELETE:
                respondo = self.__sendiDELETE(peto)
        except Exception as e:
            self.__notilo.exception("Ne povis sendi la peton", exc_info=e)
        
        return respondo


class Rajtiganto:
    def __init__(self, uzantnomo, pasvorto, peto_sendanto, notilo):
        self.__uzantnomo = uzantnomo
        self.__pasvorto = pasvorto

        self.__peto_sendanto = peto_sendanto
        self.__notilo = notilo
        self.__rajtigita = False
        self.__ĵetono = ""

    def rajtigo(self):
        self.__rajtigita = False
        respondo = self.__peto_sendanto.sendiPeton(
            Peto(PetajSpecoj.POST, "ensaluti", "/ensaluti", time.time(), {}, "", json.dumps({
                "username": self.__uzantnomo,
                "password": self.__pasvorto
            })
        ))
        if not respondo:
            self.__notilo.critical("Io okazis, legu la antaŭajn konsilajn notojn")
            return None
        if respondo.kodo != 200:
            return respondo
        korpo = respondo.korpo
        korpo_json = json.loads(korpo)
        self.__ĵetono = korpo_json["token"]
        return respondo

    def sendiPeton(self, peto):
        # Paŝo 1. Kontroli ĉu estas ĵetono metita
        # Paŝo 1.1. Se ne estas ĵetono metita, fari paŝon 2, alie, fari paŝon 3
        if self.__ĵetono == "":
            # Paŝo 2. Provi rajtigi la uzanton per la uzantnomo kaj pasvorto            
            # Paŝo 2.2. Se la respondo sukcesis, fari paŝon 3, alie, reveni kun la rezulto
            rajtiga_rezulto = self.rajtigo()
            if not rajtiga_rezulto:
                return None
            if rajtiga_rezulto.kodo != 200:
                self.__notilo.error(f"Ne povis rajtigi: {rajtiga_rezulto.korpo}")
                return rajtiga_rezulto
        # Paŝo 3. Provi sendi la peton kaj kontroli la rezulton
        # Paŝo 3.1. Se la rezulto malsukcesas, refari paŝon 2
        peto.rajtigo = self.__ĵetono
        respondo = self.__peto_sendanto.sendiPeton(peto)
        if respondo.kodo != 200:
            if respondo.kodo == 401:
                # Paŝo 3.2 Se ni provas 5-foje, reveni kun la respondo, alie, fari paŝon 4
                sukcesa_flago = False
                for i in range(5):
                    rajtiga_rezulto = self.rajtigo()
                    if not rajtiga_rezulto:
                        return None
                    if rajtiga_rezulto.kodo != 200:
                        continue
                    sukcesa_flago = True
                    break
                if not sukcesa_flago:
                    self.__notilo.error(f"Ne povis rajtigi por sendi peton post 5-foje: {rajtiga_rezulto.korpo}")
                    return rajtiga_rezulto
                # Paŝo 4. Sendi la peton kaj reveni kun la respondo
                malnova_rajtigo = peto.rajtigo
                peto.rajtigo = self.__ĵetono
                return self.__peto_sendanto.sendiPeton(peto)
        return respondo
        
import requests

class MiaVortaro:
    def __init__(self, uzantnomo=None, pasvorto=None):
        self.__lasta_respondo = None
        self.__lasta_peto = None
        self.__lasta_stato = None

        self.__miavortaro_retregno = "https://localhost:8443"
        
        #Listo da Petoj
        self.__jenaj_petoj = PetaroŜloso()
        self.__nunaj_respondoj = {}

        self.__peta_prilaboranto = None

        self.__notilo = None
        self.__tempolimo = 5 #sekundoj
        
        self.__peto_sendanto = None
        self.__rajtiganto = None

        self.__uzantnomo = uzantnomo
        self.__pasvorto = pasvorto

        self.__eraro_prizorganto = None

    def __enter__(self):
        self.komencu()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.ĉesu()

    def prilaboriPetojn(self):
        peto = self.__jenaj_petoj.preniPeton()
        if peto is None:
            return True
        respondo = None
        tempo = None
        ##NOTE: Eble ni ŝanĝu `requests.get` al `requests.async.get` por ke ni povus utiligi async-funkciecon
        if peto.speco is PetajSpecoj.POST or peto.speco is PetajSpecoj.DELETE:
            respondo = self.__rajtiganto.sendiPeton(peto)
        else:
            respondo = self.__peto_sendanto.sendiPeton(peto)
        korpo = respondo.korpo
        self.__nunaj_respondoj[peto.nomo] = respondo
        # self.__notilo.debug(korpo)
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

        self.__peto_sendanto = PetoSendanto(self.__miavortaro_retregno, self.__notilo, None)
        self.__rajtiganto = Rajtiganto(self.__uzantnomo, self.__pasvorto, self.__peto_sendanto, self.__notilo)

        if self.__uzantnomo and self.__pasvorto:
            self.__rajtiganto.rajtigo()

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
        self.__jenaj_petoj.enmetiPeton(Peto(speco, nomo, vojo, time.time(), parametroj, "", korpo))
        respondo = self.__atendiRespondon(nomo)
        if respondo is None:
            self.__notilo.error("Ne povis havigi respondon de la servilo. Aŭ reprovu poste aŭ kontaktu la adminon de la servilo por helpo.")
            return None
        return respondo

    def __senduGET(self, nomo, vojo, parametroj, korpo):
        return self.__senduPeton(PetajSpecoj.GET, nomo, vojo, parametroj, korpo)

    def __senduPOST(self, nomo, vojo, parametroj, korpo):
        return self.__senduPeton(
            PetajSpecoj.POST, nomo, vojo, parametroj, korpo
        )

    def __senduDELETE(self, nomo, vojo, parametroj, korpo):
        return self.__senduPeton(
            PetajSpecoj.DELETE, nomo, vojo, parametroj, korpo
        )


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

    def aldoniVorton(self, vorto, priskribo):
        respondo = self.__senduPOST(
            "aldoniVorton", "/", {}, json.dumps({"word": vorto, "definition": priskribo})
        )
        if respondo is None:
            return None
        return respondo

    def forigiVorton(self, vorto):
        respondo = self.__senduDELETE("forigiVorton", "/", {}, vorto)
        if respondo is None:
            return None
        return respondo
        