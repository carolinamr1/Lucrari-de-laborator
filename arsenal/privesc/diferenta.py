from arsenal.privesc.enum import GTFO, citeste_linii, nume


def cai(fisier):
    return set(citeste_linii(fisier))


baza = cai("arsenal/privesc/start/baza_suid.txt")
acum = cai("arsenal/privesc/start/suid.txt")
print("baza:", len(baza), " acum:", len(acum))

noi = acum - baza
print(len(noi), "SUID noi fata de sistemul curat")
for cale in sorted(noi):
    print(" ", cale)

risc = {
    nume(cale): ("mare" if nume(cale) in GTFO else "normal")
    for cale in noi
}
periculoase = [cale for cale in sorted(noi) if nume(cale) in GTFO]
print("periculoase NOI:", periculoase)
