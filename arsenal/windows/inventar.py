"""Inventar de procese Windows si raportarea evenimentelor suspecte."""

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
SUSPECTE_ID = {4625, 1102, 7045}


@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self) -> bool:
        cale = self.cale.casefold()
        return any(indiciu.casefold() in cale for indiciu in CAI_SUSPECTE)


@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self) -> bool:
        return self.id in SUSPECTE_ID or self.nivel.casefold() == "critical"


def procese_din_json(cale: str | Path) -> list[Proces]:
    """Citeste procesele dintr-un fisier JSON si le transforma in obiecte."""
    with open(cale, encoding="utf-8-sig") as f:
        return [Proces(**date) for date in json.load(f)]


def evenimente_din_json(cale: str | Path) -> list[Eveniment]:
    """Citeste evenimentele dintr-un fisier JSON si le transforma in obiecte."""
    with open(cale, encoding="utf-8-sig") as f:
        return [Eveniment(**date) for date in json.load(f)]


@dataclass
class Inventar:
    procese: list[Proces]

    @classmethod
    def din_json(cls, cale: str | Path) -> "Inventar":
        return cls(procese_din_json(cale))

    def __len__(self) -> int:
        return len(self.procese)

    def suspecte(self) -> list[Proces]:
        return [proces for proces in self.procese if proces.e_suspect()]

    def pe_user(self) -> dict[str, list[str]]:
        grupuri: dict[str, list[str]] = {}
        for proces in self.procese:
            grupuri.setdefault(proces.user, []).append(proces.nume)
        return grupuri


def _raport_json(procese: list[Proces], evenimente: list[Eveniment]) -> str:
    raport: dict[str, Any] = {
        "procese_suspecte": [asdict(proces) for proces in procese],
        "evenimente_alarma": [asdict(eveniment) for eveniment in evenimente],
    }
    return json.dumps(raport, ensure_ascii=False, indent=2)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Inventariaza procese si alerte Windows.")
    parser.add_argument("capturi", help="Folderul cu procese.json si evenimente.json")
    parser.add_argument("--json", action="store_true", help="Afiseaza raportul de alarme in JSON")
    args = parser.parse_args()

    folder = Path(args.capturi)
    inventar = Inventar.din_json(folder / "procese.json")
    evenimente = evenimente_din_json(folder / "evenimente.json")
    procese_suspecte = inventar.suspecte()
    alarme = [eveniment for eveniment in evenimente if eveniment.e_suspect()]

    if args.json:
        print(_raport_json(procese_suspecte, alarme))
        return

    print(f"Procese: {len(inventar)} | suspecte: {len(procese_suspecte)}")
    for proces in procese_suspecte:
        print(f"  [{proces.pid}] {proces.nume}  ({proces.user})  {proces.cale}")
    print(f"Evenimente: {len(evenimente)} | alarma: {len(alarme)}")
    for eveniment in alarme:
        print(
            f"  {eveniment.id} [{eveniment.nivel}] {eveniment.cont}: "
            f"{eveniment.mesaj}"
        )


if __name__ == "__main__":
    main()
