import requests
import dns.resolver
import whois
import json
import argparse
import sys
from salvo import run

registrant = 'Registrant Organization: Exness Global Limited'

### We think that we know one domain name that we can trust 
### as a domain that is 100% belongs to organization
def trusted_domain(name):
    return(resolve_arecords(name))


### Resolving all possible second level domain names
### and searching for those who belongs to company
def resolve_domains(name):
    domains = []
    with open('tlds.txt', 'r', encoding="utf8") as f:
        i = 1 
        tlds = f.readlines() 
        for t in tlds:
            domain = "{}.{}".format(name, t.strip())
            sys.argv[-1] = 'https://{}'.format(domain)
            try:
                print("[{}] {}".format(i, resolve_arecords(domain)[0]))
                domains.append(domain)                     
            except:
                ConnectionError, IOError, TypeError
                continue
            i += 1
        return(domains)


### Resolving all possible domain names to get their A records
def resolve_arecords(name):
    ips = []
    for qtype in 'A':
        answer = dns.resolver.resolve(name, qtype, raise_on_no_answer=False)
        if answer.rrset is not None:
            for data in answer:
                ips.append(data.address)
        else:
            break
        return(name, ips)


### Checking if domain belongs to company
### 
def domain_check(name, address):
    for a in address:
        if org_check(name) or a in trusted_ips:
            domain_record = "\n\n\n{} belongs to Exness and hosted in {}\
            (IP:{})\n".format(name, ip_geolocation(a), address)
        return(domain_record)


### Checking if WhoIs record contains valid Registrant information
### about Exness organization
def org_check(name):
    if registrant in whois.whois(name).text:
        return True


### Requesting geolocation of resoloved addresses
def ip_geolocation(ip):
    try:
        r = requests.get("https://geolocation-db.com/json/{}".format(ip))
        response = json.loads(r.text)
    except ConnectionError:
        print("Could not connect to geolocation DB. Try again later.")
    return(response['country_name'])


def main():
    sld = args.url.split('.')[0]
    try:
        domains_list = resolve_domains(sld)
    except KeyboardInterrupt:
        print("Stopping scaner.py")
    ### Checking valid input from user ###
    while True:
        try:
            select = input("Please select one of URL to launch preformance test. Put a number of it:\n")
            ### Redefine argument to use it with testing library
            sys.argv[-1] = 'https://{}'.format(domains_list[int(select)-1])
        except ValueError:
            print("You must enter an integer value.")
            continue
        except IndexError:
            print("You must enter a number from 1 to {}\n".format(len(domains_list)))
            continue
        
        if 1 <= int(select) <= len(domains_list):
            break
        else:
            select = input("You must enter a number from 1 to {}\n".format(len(domains_list)))
            sys.argv[-1] = 'https://{}'.format(domains_list[int(select)-1])
            

    print('\n\n\t###########\n')
    print('Testing {}'.format(sys.argv[-1]))
    print('We will gather statistics about web site.')
    print('\n\t###########\n\n')

    ### This launches salvo for load testing ###
    try:
        run.main()
    except IndexError:
        print("Problems with connection to resource {}".format(sys.argv[-1]))

    print(domain_check(resolve_arecords(domains_list[int(select)-1])[0], \
        resolve_arecords(domains_list[int(select)-1])[1]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Utility for organization domains lookup and web load testing"
    )
    parser.add_argument(
        "-d", "--duration", help="Duration in seconds", type=int, default=10
    )
    parser.add_argument(
        "-c", "--concurrency", help="Concurrency", type=int, default=5
    )
    parser.add_argument(
        "url",
        help="Domain that belongs to organization",
        type=str,
        default=None,
    )
    args = parser.parse_args()
    ### Trusted IP addresses are used to check if domain belongs to company 
    ### even if WhoIs doesn't have information about registrant
    trusted_ips = trusted_domain(args.url)[1]
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping scaner.py")