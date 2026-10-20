# main.py
# Laborator: funcții, metode și importuri pe web
# Student: <Morozovschii Carolina>

import argparse
import csv
import datetime
import webtools
from webtools import get_title, security_headers, DEFAULT_HEADERS

def main():
    print("DEFAULT_HEADERS din modul:", DEFAULT_HEADERS)
    
    # Exercițiul 48. Argumente din linia de comandă
    parser = argparse.ArgumentParser(description="Generează raportul web pentru un URL.")
    parser.add_argument("url", nargs="?", default="https://cybercor.org", help="URL-ul de analizat")
    args = parser.parse_args()
    
    target_url = args.url

    # Exercițiul 49. Un raport CSV
    paths_to_check = ["/", "/robots.txt", "/sitemap.xml"]
    print("Se generează report.csv...")
    with open("report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "status", "checked_at"])
        for p in paths_to_check:
            full = target_url.rstrip("/") + "/" + p.lstrip("/")
            st = webtools.get_status(full)
            writer.writerow([p, st, datetime.datetime.now().isoformat()])
    print("Salvat în report.csv")

    # Exercițiul 50. Proiect final
    webtools.site_report(target_url)

if __name__ == "__main__":
    main()