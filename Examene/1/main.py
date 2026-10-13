from checker import (
    SITES,
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check
)

# Partea 1: build_url si is_https
print("Partea 1 - build_url:")
print(build_url("example.com", "login"))
print(build_url("example.com", "/login"))

print("Partea 1 - is_https:")
print(is_https("https://example.com"))
print(is_https("http://example.com"))

# Partea 2: show_response
print("\nPartea 2 - show_response:")
show_response("https://example.com")
show_response("https://httpbin.org/status/404")

# Partea 3: check_site
print("\nPartea 3 - check_site:")
print(check_site(SITES[0]))
print(check_site(
    "https://this-site-does-not-exist.invalid"
))

# Partea 4: scan_sites
print("\nPartea 4 - scan_sites:")
scan_sites()

# Partea 5: check_headers
print("\nPartea 5 - check_headers:")
print(check_headers(SITES[0]))
print(check_headers(
    "https://this-site-does-not-exist.invalid"
))

# Partea 6: retry_check
print("\nPartea 6 - retry_check:")
print(retry_check("https://httpbin.org/status/200"))
print(retry_check("https://httpbin.org/status/404"))
