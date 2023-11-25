import socket

def get_ip_addresses(domain):
    try:
        ip_addresses = socket.gethostbyname_ex(domain)
        print(ip_addresses)
        return ip_addresses[2]
    except socket.gaierror as e:
        print(f"Error resolving {domain}: {e}")
        return []

domain_name = "financials.psx.com.pk"
ip_addresses = get_ip_addresses(domain_name)

if ip_addresses:
    print(f"IP addresses for {domain_name}: {', '.join(ip_addresses)}")
else:
    print(f"No IP addresses found for {domain_name}")
