import argparse
import json
from collections import Counter

from arsenal.aparare.parse_auth import citeste_esecuri


def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    return sorted(
        [(ip, n) for ip, n in counts.items() if n >= prag],
        key=lambda element: element[1],
        reverse=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("log")
    parser.add_argument("--prag", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    esecuri = citeste_esecuri(args.log)
    counts = Counter(e["ip"] for e in esecuri)
    sus = suspecti(counts, args.prag)

    if args.json:
        raport = {
            "esecuri": esecuri,
            "pe_ip": counts,
            "suspecti": sus,
        }
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    print("Esecuri de autentificare:", len(esecuri))
    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")
    print(f"Suspecti (prag {args.prag}):")
    for ip, n in sus:
        print(f"  {ip}  ({n} incercari)  BRUTE FORCE")


if __name__ == "__main__":
    main()
