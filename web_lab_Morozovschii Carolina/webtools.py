# webtools.py - Modul reutilizabil
# Laborator: funcții, metode și importuri pe web
# Student: <Morozovschii Carolina>

import time
import requests
import urllib.parse
import re
import socket
import ssl
import datetime
from typing import Dict, List, Optional, Tuple

DEFAULT_HEADERS = {"User-Agent": "WebLab-Student"}
TIMEOUT = 10

def fetch(url: str, headers: dict = DEFAULT_HEADERS, timeout: int = TIMEOUT) -> requests.Response:
    """Trimite o cerere GET către un URL specificat."""
    return requests.get(url, headers=headers, timeout=timeout)

def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    res = fetch(url)
    return res.status_code

def get_title(html: str) -> str:
    """Extrage titlul paginii dintr-un șir HTML."""
    start = html.find("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start + len("<title>"):end].strip()
    return "Fără titlu"

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
        res = fetch(url)
        return {h: h in res.headers for h in sec_list}
    except requests.RequestException:
        return {h: False for h in sec_list}

def score_headers(results: Dict[str, bool]) -> str:
    """Returnează un scor sub formă de șir 'X/Y'."""
    present = sum(1 for val in results.values() if val)
    return f"{present}/{len(results)}"

def resolve(hostname: str) -> str:
    """Returnează adresa IP a host-ului."""
    try:
        return socket.gethostbyname(hostname)
    except socket.error:
        return "N/A"

def cert_days_left(hostname: str) -> int:
    """Returnează numărul de zile rămase până la expirarea certificatului SSL."""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expire_date = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                return (expire_date - datetime.datetime.utcnow()).days
    except Exception:
        return 0

def fetch_robots(base: str) -> Optional[str]:
    """Descarcă textul din robots.txt."""
    try:
        res = fetch(base.rstrip("/") + "/robots.txt")
        return res.text if res.status_code == 200 else None
    except requests.RequestException:
        return None

def disallowed_paths(robots_text: Optional[str]) -> List[str]:
    """Extrage căile Disallow din robots.txt."""
    if not robots_text:
        return []
    paths = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            parts = line.split(":", 1)
            if len(parts) > 1 and parts[1].strip():
                paths.append(parts[1].strip())
    return paths

def extract_links(html: str) -> list:
    """Extrage toate legăturile href fără duplicate."""
    return list(set(re.findall(r'href="([^"]+)"', html, re.IGNORECASE)))

def split_links(links: list, domain: str) -> Tuple[List[str], List[str]]:
    """Separă legăturile în interne și externe."""
    internal, external = [], []
    base_netloc = urllib.parse.urlparse(domain).netloc.lower()
    for l in links:
        full_url = urllib.parse.urljoin(domain, l)
        netloc = urllib.parse.urlparse(full_url).netloc.lower()
        if netloc == base_netloc or not netloc:
            internal.append(full_url)
        else:
            external.append(full_url)
    return list(set(internal)), list(set(external))

def site_report(url: str) -> dict:
    """Generează și salvează raportul complet al site-ului."""
    import json
    
    res = fetch(url)
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.netloc
    
    # Redirecționări
    http_url = "http://" + hostname
    try:
        res_http = requests.get(http_url, timeout=TIMEOUT)
        redir_str = " -> ".join([f"{r.status_code}" for r in res_http.history] + [res_http.url])
    except requests.RequestException:
        redir_str = "N/A"

    sec_res = security_headers(url)
    sec_score = score_headers(sec_res)
    ip_addr = resolve(hostname)
    days_cert = cert_days_left(hostname)
    
    raw_links = extract_links(res.text)
    int_l, ext_l = split_links(raw_links, url)
    
    robots = fetch_robots(url)
    disallowed = disallowed_paths(robots)
    
    report_data = {
        "url": res.url,
        "status_code": res.status_code,
        "title": get_title(res.text),
        "ip_address": ip_addr,
        "redirects": redir_str,
        "security_score": sec_score,
        "cert_days_left": days_cert,
        "internal_links": len(int_l),
        "external_links": len(ext_l),
        "disallowed_paths": disallowed
    }
    
    print(f"=== Raport site: {url} ===")
    print(f"Cod de stare:      {report_data['status_code']}")
    print(f"Titlu:             {report_data['title']}")
    print(f"Adresă IP:         {report_data['ip_address']}")
    print(f"Redirecționări:    {report_data['redirects']}")
    print(f"Scor securitate:   {report_data['security_score']}")
    print(f"Certificat:        {report_data['cert_days_left']} de zile rămase")
    print(f"Legături:          {report_data['internal_links']} interne, {report_data['external_links']} externe")
    print(f"Căi interzise:     {', '.join(report_data['disallowed_paths'])}")
    
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
        
    print("Salvat în report.json")
    return report_data

if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))