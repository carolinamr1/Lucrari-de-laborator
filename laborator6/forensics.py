from pathlib import Path
import re
import zipfile

from PIL import Image, ExifTags


PROBE = Path("probe")


# B1: identifică tipul după semnătura reală a fișierului
def tip_real(cale):
    inceput = Path(cale).read_bytes()[:8]

    if inceput.startswith(b"%PDF"):
        return "PDF"
    if inceput.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG"
    if inceput.startswith(b"\xff\xd8"):
        return "JPEG"
    if inceput.startswith(b"PK\x03\x04"):
        return "ZIP sau DOCX"

    return "necunoscut"


print("foto.jpg:", tip_real(PROBE / "foto.jpg"))
print("ascuns.png:", tip_real(PROBE / "ascuns.png"))


# B2: afișează secvențele de text imprimabil din fișier
date_png = (PROBE / "ascuns.png").read_bytes()
print("\nText imprimabil găsit în ascuns.png:")

for secventa in re.findall(rb"[ -~]{4,}", date_png):
    print(secventa.decode("ascii"))


# B3: citește metadatele EXIF și coordonatele GPS
imagine = Image.open(PROBE / "foto.jpg")
exif = imagine.getexif()

print("\nMetadate EXIF:")
for id_tag, valoare in exif.items():
    nume = ExifTags.TAGS.get(id_tag, id_tag)
    if id_tag != 34853:
        print(nume, "=", valoare)

gps_raw = exif.get_ifd(34853)
gps = {
    ExifTags.GPSTAGS.get(id_tag, id_tag): valoare
    for id_tag, valoare in gps_raw.items()
}

print("\nMetadate GPS:", gps)


def in_grade_zecimale(coordonate, directie):
    grade, minute, secunde = [float(x) for x in coordonate]
    rezultat = grade + minute / 60 + secunde / 3600

    if directie in ("S", "W"):
        rezultat = -rezultat

    return rezultat


latitudine = in_grade_zecimale(
    gps["GPSLatitude"], gps["GPSLatitudeRef"]
)
longitudine = in_grade_zecimale(
    gps["GPSLongitude"], gps["GPSLongitudeRef"]
)

print("Latitudine:", latitudine)
print("Longitudine:", longitudine)


# B4: găsește și extrage ZIP-ul lipit la sfârșitul imaginii PNG
pozitie = date_png.find(b"PK\x03\x04")

if pozitie == -1:
    print("\nNu am găsit arhiva ZIP.")
else:
    cale_zip = Path("gasit.zip")
    cale_zip.write_bytes(date_png[pozitie:])
    print("\nArhiva extrasă la octetul:", pozitie)

    with zipfile.ZipFile(cale_zip) as arhiva:
        print("Fișiere în arhivă:", arhiva.namelist())
        for nume in arhiva.namelist():
            continut = arhiva.read(nume).decode("utf-8")
            print(nume, "conține:", continut)
            # B5: ascunde mesajul în ultimii biți ai canalelor RGB
def ascunde_mesaj(cale_imagine, mesaj, cale_iesire):
    imagine = Image.open(cale_imagine).convert("RGB")
    pixeli = list(imagine.getdata())

    date_mesaj = mesaj.encode("utf-8") + b"\0"
    biti = "".join(f"{octet:08b}" for octet in date_mesaj)

    canale = [canal for pixel in pixeli for canal in pixel]

    if len(biti) > len(canale):
        raise ValueError("Mesajul este prea lung pentru imagine.")

    for i, bit in enumerate(biti):
        canale[i] = (canale[i] & 254) | int(bit)

    pixeli_noi = [
        tuple(canale[i:i + 3])
        for i in range(0, len(canale), 3)
    ]

    imagine.putdata(pixeli_noi)
    imagine.save(cale_iesire, format="PNG")
    print("\nImaginea cu mesajul ascuns a fost salvată:", cale_iesire)


# B6: citește ultimii biți și reconstruiește mesajul
def dezvaluie_mesaj(cale_imagine):
    imagine = Image.open(cale_imagine).convert("RGB")
    biti = "".join(
        str(canal & 1)
        for pixel in imagine.getdata()
        for canal in pixel
    )

    rezultat = bytearray()

    for i in range(0, len(biti) - 7, 8):
        octet = int(biti[i:i + 8], 2)

        if octet == 0:
            break

        rezultat.append(octet)

    return rezultat.decode("utf-8")


cale_stego = Path("stego.png")
ascunde_mesaj(
    PROBE / "foto.jpg",
    "FLAG{ascuns_in_pixeli}",
    cale_stego
)

mesaj_extras = dezvaluie_mesaj(cale_stego)
print("Mesajul dezvăluit:", mesaj_extras)