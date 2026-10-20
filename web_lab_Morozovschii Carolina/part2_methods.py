# Laborator: funcții, metode și importuri pe web
# Student: <Morozovschii Carolina>

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Exercițiul 9. Elementele de bază ale răspunsului
res = requests.get(BASE_URL, timeout=TIMEOUT)
print("status_code:", res.status_code) 
print("ok:", res.ok)                    
print("url:", res.url)               
print("encoding:", res.encoding)       
# Exercițiul 10. Tratarea erorilor cu o metodă
res.raise_for_status()  
time.sleep(1)

try:
    bad_res = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    bad_res.raise_for_status()
except requests.HTTPError as e:
    print(f"Ex10 - Eroare HTTP prinsă cu succes: {e}")

# Exercițiul 11. Toate antetele
print("--- Antete primite ---")
for key, value in res.headers.items():
    print(f"{key}: {value}")

# Exercițiul 12. Metode de dicționar
server = res.headers.get("Server", "lipsește")
content_type = res.headers.get("Content-Type", "lipsește")
content_type_lower = res.headers.get("content-type", "lipsește")
print(f"Ex12 - Server: {server} | Content-Type: {content_type} | lower: {content_type_lower}")

# Exercițiul 13. Înlănțuirea metodelor de șir
count_cyber = res.text.lower().count("cyber")
print(f"Ex13 - Cuvântul 'cyber' apare de {count_cyber} ori.")

# Exercițiul 14. Găsirea titlului
html_text = res.text
start_idx = html_text.find("<title>") + len("<title>")
end_idx = html_text.find("</title>")
if start_idx != -1 and end_idx != -1:
    title = html_text[start_idx:end_idx].strip()
    print("Ex14 - Titlu pagină:", title)

# Exercițiul 15. Numărarea liniilor
lines = html_text.splitlines()
print(f"Ex15 - Număr linii: {len(lines)}")
if lines:
    longest_line = max(lines, key=len)
    print(f"Ex15 - Lungimea celei mai lungi linii: {len(longest_line)}")

# Exercițiul 16. Verificarea HTTPS
if res.url.startswith("https://"):
    print("Ex16 - Conexiune securizată")
else:
    print("Ex16 - Conexiune nesecurizată")

# Exercițiul 17. Urmărirea redirecționărilor
time.sleep(1)
res_redir = requests.get("http://cybercor.org", timeout=TIMEOUT)
print("Ex17 - Istoric redirecționări:")
for r in res_redir.history:
    print(f"  {r.status_code} -> {r.url}")
print("URL final:", res_redir.url)

# Exercițiul 18. HEAD versus GET
time.sleep(1)
res_head = requests.head(BASE_URL, timeout=TIMEOUT)
res_get = requests.get(BASE_URL, timeout=TIMEOUT)
print(f"Ex18 - Lungime corp HEAD: {len(res_head.content)} | GET: {len(res_get.content)}")


# Exercițiul 19. Cookie-uri
if res_get.cookies:
    for cookie in res_get.cookies:
        print(f"Cookie: {cookie.name} | Secure: {cookie.secure}")
else:
    print("Ex19 - Niciun cookie setat")

# Exercițiul 20. Sesiuni
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-Student"})
time.sleep(1)
res_sess = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
data = res_sess.json()
print("Ex20 - Antete confirmate de server:", data.get("headers", {}).get("User-Agent"))

