# Laborator: funcții, metode și importuri pe web
# Student: <Morozovschii Carolina>

import time
import requests
import urllib.parse
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
import datetime

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# Exercițiul 35. Descompunerea unui URL
parsed = urllib.parse.urlparse("https://cybercor.org/path?x=1#top")
print(f"Ex35 - scheme: {parsed.scheme}, netloc: {parsed.netloc}, path: {parsed.path}, query: {parsed.query}, fragment: {parsed.fragment}")

# Exercițiul 36. Compunerea URL-urilor
for rel in ["/about", "contact.html", "../index.html"]:
    full = urllib.parse.urljoin(BASE_URL, rel)
    print(f"Ex36 - Relative: {rel} -> Absolute: {full}")

# Exercițiul 37. Extragerea legăturilor
def extract_links(html: str) -> list:
    """Extrage toate legăturile href din HTML fără duplicate."""
    raw_links = re.findall(r'href="([^"]+)"', html, re.IGNORECASE)
    return list(set(raw_links))

res_main = requests.get(BASE_URL, timeout=TIMEOUT)
links = extract_links(res_main.text)
print(f"Ex37 - Legături găsite ({len(links)}):", links[:5])

# Exercițiul 38. Interne sau externe?
def split_links(links: list, domain: str) -> tuple:
    """Separă legăturile în interne și externe."""
    internal = []
    external = []
    base_netloc = urllib.parse.urlparse(domain).netloc.lower()
    
    for l in links:
        full_url = urllib.parse.urljoin(domain, l)
        netloc = urllib.parse.urlparse(full_url).netloc.lower()
        if netloc == base_netloc or not netloc:
            internal.append(full_url)
        else:
            external.append(full_url)
    return list(set(internal)), list(set(external))

int_links, ext_links = split_links(links, BASE_URL)
print(f"Ex38 - Interne: {len(int_links)} | Externe: {len(ext_links)}")

# Exercițiul 39. Propriile metode
class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            attrs_dict = dict(attrs)
            src = attrs_dict.get("src") or attrs_dict.get("SRC")
            if src:
                self.images.append(src)

# Testul Exercițiului 39
test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)
print("Ex39 - Imagini test găsite:", finder.images)

assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp",
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul Ex39 a trecut!")

# Rulare pe pagina reală
finder_real = ImageFinder()
finder_real.feed(res_main.text)
print(f"Ex39 - Real: {len(finder_real.images)} imagini găsite pe {BASE_URL}")

# Exercițiul 40. Amprenta paginii
def page_fingerprint(url: str) -> str:
    """Returnează hash-ul SHA-256 al conținutului paginii."""
    r = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(r.content).hexdigest()

fp1 = page_fingerprint(BASE_URL)
time.sleep(1)
fp2 = page_fingerprint(BASE_URL)
print("Ex40 - FP1:", fp1)
print("Ex40 - FP2:", fp2)

# Exercițiul 41. Salvarea în JSON
with open("headers.json", "w", encoding="utf-8") as f:
    json.dump(dict(res_main.headers), f, indent=2)

with open("headers.json", "r", encoding="utf-8") as f:
    loaded_headers = json.load(f)
print("Ex41 - Antet reîncărcat:", loaded_headers.get("Content-Type"))

# Exercițiul 42. Interogare DNS
def resolve(hostname: str) -> str:
    """Returnează adresa IP a host-ului."""
    return socket.gethostbyname(hostname)

host = urllib.parse.urlparse(BASE_URL).netloc
print(f"Ex42 - Adresă IP pentru {host}:", resolve(host))

# Exercițiul 43. Expirarea certificatului
def cert_days_left(hostname: str) -> int:
    """Returnează numărul de zile rămase până la expirarea certificatului SSL."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            not_after_str = cert['notAfter']
            expire_date = datetime.datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")
            now = datetime.datetime.utcnow()
            days = (expire_date - now).days
            return days

print("Ex43 - Zile certificat rămase:", cert_days_left(host))