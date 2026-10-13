import requests
url ="https://example.com/login"
r = requests.get(url)



SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
      pass
  if path.startawith('/'):
      path = path[1:]
   return f"https://{host}/{path}"


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""

 pass
if url.startswith("https://example.com")
return True
else if url.startswith("http://example.com")
return False

def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    pass
  try:
        r = requests.get(url, timeout=5)
        print(f"Status: {r.status_code}")
        print(f"Content-Type: {r.headers.get('Content-Type', 'N/A')}")
    except requests.exceptions.RequestException as e:
        print(f"Eroare de conexiune: {}")




def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    pass
  try:
        r = requests.get(url, timeout=5)
        return {
            "status": r.status_code,
            "content_type": r.headers.get("Content-Type", "unknown"),
            "length": len(r.content),
            "server": r.headers.get("Server", "unknown")
        }
    except requests.exceptions.RequestException as e:
        return {"status": None, "error": f"Eroare: {}"}
    
def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    pass
  for url in SITES:
        rezultat = check_site(url)
        rezultat["url"] = url
        rezultate.append(rezultat)
        
    reusite = [r for r in rezultate if r["status"] == 200]
    reusite.sort(key=lambda x: x.get("length", 0), reverse=True)
    
    for r in reusite:
        print(f"{r['url']} -> {r['status']}, {r['length']} octeți")
        
    esuate = len(rezultate) - len(reusite)
    print(f"Reușite: {len(reusite)} Eșuate: {esuate}")

def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    pass
 try:
        response = requests.get(url, timeout=5)

        present = []
        missing = []

        received_headers = {
            header.lower()
            for header in response.headers
        }

        for header in SECURITY_HEADERS:
            if header.lower() in received_headers:
                present.append(header)
            else:
                missing.append(header)

        if SECURITY_HEADERS:
            score = round(
                len(present) / len(SECURITY_HEADERS) * 100
            )
        else:
            score = 0

        return {
            "present": present,
            "missing": missing,
            "score": score
        }

    except requests.RequestException as error:
        return {
            "status": None,
            "error": str(error)
        }


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    pass
last_status = None
    last_error = None
    requests_sent = 0

    for _ in range(max(0, attempts)):
        try:
            response = requests.get(url, timeout=5)
            requests_sent += 1
            last_status = response.status_code
            last_error = None

            if response.status_code < 500:
                return {
                    "status": last_status,
                    "attempts": requests_sent
                }

        except requests.RequestException as error:
            requests_sent += 1
            last_error = str(error)

    if last_status is None:
        return {
            "status": None,
            "error": last_error or "Cererea a eșuat",
            "attempts": requests_sent
        }

    return {
        "status": last_status,
        "attempts": requests_sent
    }

