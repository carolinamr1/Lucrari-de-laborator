# Laborator: funcții, metode și importuri pe web
# Student: <Morozovschii Carolina>

import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Exercițiul 1. Primul import
import requests
print("Versiune requests:", requests.__version__)

import urllib.request

# Exercițiul 2. Două stiluri de import
res1 = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex2 - Stil 1 status:", res1.status_code)

from requests import get
res2 = get(BASE_URL, timeout=TIMEOUT)
print("Ex2 - Stil 2 status:", res2.status_code)


# Exercițiul 3. Alias-uri
import requests as rq
res3 = rq.get(BASE_URL, timeout=TIMEOUT)
print("Ex3 - Status cu alias:", res3.status_code)

# Exercițiul 4. Doar biblioteca standard
req = urllib.request.Request(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
    print("Ex4 - urllib status:", response.status)
    body_bytes = response.read()
    body_text = body_bytes.decode("utf-8")
    print("Ex4 - Primele 200 caractere:", body_text[:200])

# Exercițiul 5. Priviți în interiorul unui modul
print("Ex5 - Dir requests:", dir(requests)[:10])


# Exercițiul 6. Citiți documentația

res_timeout = requests.get(BASE_URL, timeout=5)
print("Ex6 - Cerere cu timeout reușită, status:", res_timeout.status_code)

# Exercițiul 7. Cronometrarea unei cereri
t_start = time.perf_counter()
res_time = requests.get(BASE_URL, timeout=TIMEOUT)
t_end = time.perf_counter()
duration_perf = t_end - t_start
duration_elapsed = res_time.elapsed.total_seconds()
print(f"Ex7 - Măsurat cu perf_counter: {duration_perf:.4f}s | time.elapsed: {duration_elapsed:.4f}s")

# Exercițiul 8. Când un import eșuează
try:
    import bs4
    print("Ex8 - BeautifulSoup4 este instalat!")
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")

