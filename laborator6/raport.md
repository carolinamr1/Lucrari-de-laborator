# Raport — Laboratorul 6

## Lucrarea A — Decoder

În `mesaj.txt` am găsit trei straturi de codare: Base64, Base64 și hex. Mesajul decodat este:

`FLAG{straturi_de_encoding}`

Fișierul `xor.bin` a fost decodat prin încercarea cheilor XOR de un octet. Cheia găsită este `128`, adică `0x80`. Mesajul conține:

`FLAG{xor_un_octet}`

Hashurile au câte 32 de caractere, deci sunt MD5. Cu wordlist-ul am găsit parolele:

- `password`
- `dragon`
- `qwerty`
- `letmein`
- `monkey`

## Lucrarea B — Forensics și steganografie

Semnăturile fișierelor confirmă că `foto.jpg` este JPEG, iar `ascuns.png` este PNG.

Din metadatele EXIF ale fotografiei am găsit producătorul `Apple`, modelul `iPhone 13` și data `2026:09:14 10:30:00`. Coordonatele GPS convertite în grade zecimale sunt aproximativ:

- Latitudine: `47.016667`
- Longitudine: `28.857500`

În fișierul `ascuns.png` am găsit semnătura unei arhive ZIP lipite la finalul imaginii. Arhiva extrasă conține `secret.txt`, cu mesajul:

`FLAG{ascuns_prin_carving}`

Am ascuns un mesaj în ultimii biți ai canalelor RGB și l-am extras din `stego.png`. Mesajul obținut este:

`FLAG{ascuns_in_pixeli}`