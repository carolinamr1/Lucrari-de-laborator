# Laborator: funcții, metode și importuri pe web
# Student: <Morozovschii Carolina>

import time
import requests
from typing import Dict, List, Optional

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Exercițiul 21. Prima funcție
def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Efectuează o cerere GET către URL-ul specificat și returnează obiectul răspuns."""
    return requests.get(url, timeout=timeout)

print("Ex21 - Status fetch:", fetch(BASE_URL).status_code)

# Exercițiul 22. Returnarea unei singure valori
def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    res = fetch(url)
    return res.status_code

for path in ["/", "/robots.txt", "/sitemap.xml"]:
    print(f"Ex22 - Status {path}:", get_status(BASE_URL + path))
    time.sleep(1)

# Exercițiul 23. Parametri impliciți
print("Ex23 - Implicit timeout:", fetch(BASE_URL).status_code)
print("Ex23 - Custom timeout:", fetch(BASE_URL, timeout=3).status_code)

# Exercițiul 24. O singură sarcină pe funcție & Exercițiul 25. Docstring-uri & Exercițiul 26. Adnotări de tip
def get_title(html: str) -> str:
    """Extrage și curăță titlul dintr-un cod sursă HTML.
    
    Primeste un string HTML și returnează textul din tagul <title>.
    """
    start = html.find("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start + len("<title>"):end].strip()
    return "Fără titlu"

print("Ex25 - Help get_title:")
help(get_title)

# Exercițiul 27. Fără opriri neașteptate
def page_exists(url: str) -> bool:
    """Verifică dacă o pagină există fără a opri programul la erori de rețea."""
    try:
        res = requests.get(url, timeout=TIMEOUT)
        return res.status_code < 400
    except requests.RequestException:
        return False

print("Ex27 - Există domeniul invalid?:", page_exists("https://this-domain-does-not-exist.invalid"))

# Exercițiul 28. Returnarea unui dicționar
def check_paths(base: str, paths: List[str]) -> Dict[str, int]:
    """Returnează un dicționar cu codurile de stare pentru fiecare cale."""
    results = {}
    for p in paths:
        full_url = base.rstrip("/") + "/" + p.lstrip("/")
        try:
            res = requests.get(full_url, timeout=TIMEOUT)
            results[p] = res.status_code
        except requests.RequestException:
            results[p] = 0
        time.sleep(1)
    return results

print("Ex28 - Check paths:", check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

# Exercițiul 29. Argumente cu nume
def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Returnează valoarea unui antet specific dintr-un URL."""
    try:
        res = requests.get(url, timeout=TIMEOUT)
        return res.headers.get(name, default)
    except requests.RequestException:
        return default

print("Ex29 - Server header:", get_header(BASE_URL, name="Server"))

# Exercițiul 30. Antete de securitate
def security_headers(url: str) -> Dict[str, bool]:
    """Verifică prezența celor 5 antete esențiale de securitate."""
    sec_list = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    try:
        res = requests.get(url, timeout=TIMEOUT)
        return {h: h in res.headers for h in sec_list}
    except requests.RequestException:
        return {h: False for h in sec_list}

print("Ex30 - Sec headers:", security_headers(BASE_URL))

# Exercițiul 31. Funcții care apelează funcții
def score_headers(results: Dict[str, bool]) -> str:
    """Returnează un scor sub formă de șir 'X/Y' bazat pe antetele prezente."""
    present = sum(1 for val in results.values() if val)
    total = len(results)
    return f"{present}/{total}"

print("Ex31 - Scor antete:", score_headers(security_headers(BASE_URL)))

# Exercițiul 32. Două funcții, o sarcină
def fetch_robots(base: str) -> Optional[str]:
    """Descarcă fișierul robots.txt sau returnează None dacă lipsește/eșuează."""
    try:
        res = requests.get(base.rstrip("/") + "/robots.txt", timeout=TIMEOUT)
        if res.status_code == 200:
            return res.text
        return None
    except requests.RequestException:
        return None

def disallowed_paths(robots_text: Optional[str]) -> List[str]:
    """Extrage căile interzise (Disallow) din textul robots.txt."""
    if not robots_text:
        return []
    paths = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                val = parts[1].strip()
                if val:
                    paths.append(val)
    return paths

robots = fetch_robots(BASE_URL)
print("Ex32 - Căi interzise:", disallowed_paths(robots))

# Exercițiul 33. Oricâte argumente
def response_times(*urls: str) -> Dict[str, float]:
    """Măsoară timpul de răspuns pentru oricâte URL-uri primite ca argumente."""
    times = {}
    for url in urls:
        try:
            t0 = time.perf_counter()
            requests.get(url, timeout=TIMEOUT)
            t1 = time.perf_counter()
            times[url] = round(t1 - t0, 4)
        except requests.RequestException:
            times[url] = -1.0
        time.sleep(1)
    return times

print("Ex33 - Timpi răspuns:", response_times(BASE_URL, ECHO_URL))

# Exercițiul 34. Argumente cu nume colectate
def log(message: str, **details) -> None:
    """Afișează un mesaj urmat de perechile cheie=valoare din kwargs."""
    details_str = " | ".join(f"{k}={v}" for k, v in details.items())
    if details_str:
        print(f"{message} | {details_str}")
    else:
        print(message)

log("verificat", url=BASE_URL, status=200)

