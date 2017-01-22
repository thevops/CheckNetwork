# Python 3
# Linux

import netifaces # 0.10.5
import subprocess
import pyspeedtest # https://github.com/fopina/pyspeedtest
from time import sleep
import os


# kolorowanie konsoli
class clr:
    OKGREEN = "\033[92m"
    GREEN = "\033[1;32m"
    GREENUNDER  =   "\033[4;32m"
    #RED2 = "\033[91m" # not bold
    WARNING = "\033[93m"
    BASICY = "\033[0;33m"
    YELLOW = "\033[1;33m"
    BRED = "\033[0;31m"
    RED = "\033[1;31m" # bold
    UNDERLINE = "\033[4m"
    ENDC = "\033[0m"

def logo():
	print("   _____ _               _      _   _      _                      _    ")
	print("  / ____| |             | |    | \ | |    | |                    | |   ")
	print(" | |    | |__   ___  ___| | __ |  \| | ___| |___      _____  _ __| | __")
	print(" | |    | '_ \ / _ \/ __| |/ / | . ` |/ _ \ __\ \ /\ / / _ \| '__| |/ /")
	print(" | |____| | | |  __/ (__|   <  | |\  |  __/ |_ \ V  V / (_) | |  |   < ")
	print("  \_____|_| |_|\___|\___|_|\_\ |_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\ ")
	print("Krzysztof Łuczak\n\n")
	sleep(1)

def interfaces():
	print("\n\t"+clr.RED+"List interfaces"+clr.ENDC)
	for iface in netifaces.interfaces():
		mac_addr = netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]['addr']
		try:
			ip_addr = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
			netmask = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['netmask']
		except:
			ip_addr = ""
			netmask = ""
		print('{}:\n\tMAC:\t{}\n\tIPv4:\t{}\n\tMask:\t{}'.format(iface, mac_addr, clr.GREEN+ip_addr+clr.ENDC, netmask))



def ping():
	print("\n\t"+clr.RED+"Check DNS"+clr.ENDC)
	# ping domain
	try:
		print("\n"+clr.YELLOW+"PING: google.com"+clr.ENDC)
		domain = subprocess.Popen(["ping", "-c 2", "google.com"], stdout=subprocess.PIPE).communicate()[0]
		domain = domain.decode('UTF-8').split("\n")
		print(' '.join(domain[1].replace("(","").replace(")","").split(" ")[4:]))  # take first line
		print(' '.join(domain[2].replace("(","").replace(")","").split(" ")[4:]))  # take second line
	except:
		print("Domain error !")

	# ping IPv4 address
	try:
		print(clr.YELLOW+"PING: 46.238.98.154 (google.com)"+clr.ENDC)
		domain_ip = subprocess.Popen(["ping", "-c 2", "46.238.98.154"], stdout=subprocess.PIPE).communicate()[0]
		if 'ttl' not in domain_ip.decode('UTF-8'):  #  ping lose = ttl not in return
			raise
		domain_ip = domain_ip.decode('UTF-8').split("\n")
		print(' '.join(domain_ip[1].split(" ")[3:]))
		print(' '.join(domain_ip[2].split(" ")[3:]))
	except:
		print("Domain IPv4 error !")

	# ping IPv4 address of DNS
	try:
		print(clr.YELLOW+"PING: 8.8.8.8 (google DNS)"+clr.ENDC)
		domain_ip = subprocess.Popen(["ping", "-c 2", "8.8.8.8"], stdout=subprocess.PIPE).communicate()[0]
		if 'ttl' not in domain_ip.decode('UTF-8'):
			raise
		domain_ip = domain_ip.decode('UTF-8').split("\n")
		print(' '.join(domain_ip[1].split(" ")[3:]))
		print(' '.join(domain_ip[2].split(" ")[3:]))
	except:
		print("Google DNS error !")

	# ping IPv4 address of DNS
	try:
		print(clr.YELLOW+"PING: 217.30.129.149 (netia DNS)"+clr.ENDC)
		domain_ip = subprocess.Popen(["ping", "-c 2", "217.30.129.149"], stdout=subprocess.PIPE).communicate()[0]
		if 'ttl' not in domain_ip.decode('UTF-8'):
			raise
		domain_ip = domain_ip.decode('UTF-8').split("\n")
		print(' '.join(domain_ip[1].split(" ")[3:]))
		print(' '.join(domain_ip[2].split(" ")[3:]))
	except:
		print("Netia DNS error !")

	# ping IPv4 address of default gateway (Access Point, router, DHCP server,...)
	try:
		response = subprocess.Popen(["ip", "route", "show", "default"], stdout=subprocess.PIPE).communicate()[0]
		default_route = response.decode('utf-8').split("\n")[0].split(" ")[2]
		default_iface = response.decode('utf-8').split("\n")[0].split(" ")[4]
		print(clr.YELLOW+"PING: "+default_route+" ("+default_iface+")"+clr.ENDC)
		gateway = subprocess.Popen(["ping", "-c 2", default_route], stdout=subprocess.PIPE).communicate()[0]
		if 'ttl' not in gateway.decode('UTF-8'):
			raise
		gateway = gateway.decode('UTF-8').split("\n")
		print(' '.join(gateway[1].split(" ")[3:]))
		print(' '.join(gateway[2].split(" ")[3:]))
	except:
		print("Gateway error !")


def speedtest():
	print("\n\t"+clr.RED+"SpeedTest"+clr.ENDC)
	st = pyspeedtest.SpeedTest()
	
	print(clr.YELLOW+"Ping:\t\t"+clr.ENDC,end="")
	ping_ms = st.ping()
	print(clr.GREEN+'{:.2f} ms'.format(ping_ms)+clr.ENDC)

	print(clr.YELLOW+"Download speed:\t"+clr.ENDC, end="")
	down = st.download()
	print(clr.GREEN+'{:.2f} Mbps'.format(down/1000000)+clr.ENDC)

	print(clr.YELLOW+"Upload speed:\t"+clr.ENDC,end="")
	upl = st.upload()
	print(clr.GREEN+'{:.2f} Mbps'.format(upl/1000000)+clr.ENDC)

def traceroute():
	print("\n\t"+clr.RED+"Traceroute (google.com)"+clr.ENDC)
	os.system("sudo traceroute -I google.com")
	print()


def main():
	logo()
	try:
		interfaces()
		input(clr.UNDERLINE+"\nPress enter for continue or Ctrl+C for exit"+clr.ENDC)
		ping()
		input(clr.UNDERLINE+"\nPress enter for continue or Ctrl+C for exit"+clr.ENDC)
		speedtest()
		input(clr.UNDERLINE+"\nPress enter for continue or Ctrl+C for exit"+clr.ENDC)
		traceroute()
	except KeyboardInterrupt:
		print()
		return

if __name__ == '__main__':
	main()