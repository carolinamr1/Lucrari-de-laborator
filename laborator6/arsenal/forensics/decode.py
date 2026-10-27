import base64
import re
from urllib.parse import unquote
import json
import argparse


# A1: textul poate fi transformat în octeți și înapoi în hex
text = "Salut"
octeti = text.encode("utf-8")
print("Octeți:", octeti)
print("Primul octet:", octeti[0])
print("Hex:", octeti.hex())
print("Refăcut din hex:", bytes.fromhex(octeti.hex()))


# A2: ghicește tipul codării după caractere
def ghici_strat(s):
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"

    if len(s) > 0 and len(s) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", s):
        return "hex"

    if len(s) > 0 and re.fullmatch(r"[A-Za-z0-9+/]*={0,2}", s):
        try:
            base64.b64decode(s, validate=True)
            return "base64"
        except Exception:
            pass

    return "necunoscut"


# A3: decodează stratul identificat
def desfa(s):
    strat = ghici_strat(s)

    if strat == "base64":
        rezultat = base64.b64decode(s, validate=True)
    elif strat == "hex":
        rezultat = bytes.fromhex(s)
    elif strat == "url":
        rezultat = unquote(s).encode("utf-8")
    else:
        rezultat = s.encode("utf-8")

    return strat, rezultat


print("Test URL:", ghici_strat("%2Fetc"))
print("Test hex:", ghici_strat("48656c6c6f"))

strat, rezultat = desfa("U2FsdXQ=")
print("Test Base64:", strat, rezultat)
def citibil(b):
    return all(32 <= octet < 127 for octet in b)


def desfa_straturi(text):
    valoare = text.strip()

    for _ in range(8):
        strat, rezultat = desfa(valoare)

        if strat == "necunoscut":
            return rezultat

        # Dacă rezultatul e text imprimabil, verificăm dacă mai e codat.
        if citibil(rezultat):
            text_nou = rezultat.decode("ascii")
            if ghici_strat(text_nou) == "necunoscut":
                return rezultat
            valoare = text_nou
        else:
            try:
                valoare = rezultat.decode("ascii")
            except UnicodeDecodeError:
                return rezultat

    return rezultat


with open("probe/mesaj.txt", "r", encoding="utf-8") as fisier:
    mesaj_codat = fisier.read()

mesaj_clar = desfa_straturi(mesaj_codat)
print("Mesaj decodat:", mesaj_clar.decode("utf-8"))
from pathlib import Path


def sparge_xor(cale):
    date = Path(cale).read_bytes()

    for cheie in range(256):
        clar = bytes(octet ^ cheie for octet in date)

        if citibil(clar):
            print("Cheia XOR:", cheie, f"(0x{cheie:02X})")
            print("Mesaj:", clar.decode("ascii"))
            return

    print("Nu am găsit o cheie care să producă text imprimabil.")


sparge_xor("probe/xor.bin")
import hashlib


def sparge_hashuri():
    cale_hashuri = Path("probe/hashuri.txt")
    cale_cuvinte = Path("probe/wordlist.txt")

    hashuri = cale_hashuri.read_text(encoding="utf-8").splitlines()
    cuvinte = cale_cuvinte.read_text(encoding="latin1").splitlines()

    for tinta in hashuri:
        tinta = tinta.strip()

        for cuvant in cuvinte:
            rezultat = hashlib.md5(cuvant.encode("utf-8")).hexdigest()

            if rezultat == tinta:
                print("Hash găsit:", tinta)
                print("Parola:", cuvant)
                break


sparge_hashuri()
fisa = {
    "straturi": ["base64", "base64", "hex"],
    "rezultat": mesaj_clar.decode("utf-8")
}

cale_fisa = Path("arsenal/forensics/fisa.json")
cale_fisa.write_text(
    json.dumps(fisa, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("Fișa salvată în:", cale_fisa)
parser = argparse.ArgumentParser()
parser.add_argument("intrare", nargs="?", help="Șirul de decodat sau calea fișierului")
parser.add_argument("--fisier", action="store_true", help="Intrarea este o cale de fișier")

argumente = parser.parse_args()

if argumente.intrare:
    if argumente.fisier:
        text_intrare = Path(argumente.intrare).read_text(
            encoding="utf-8"
        ).strip()
    else:
        text_intrare = argumente.intrare

    rezultat = desfa_straturi(text_intrare)
    print("Rezultat:", rezultat.decode("utf-8", errors="replace"))