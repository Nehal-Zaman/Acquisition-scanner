from termcolor import colored
from bs4 import BeautifulSoup
import requests
import argparse

def make_request(url):
    # Sending an HTTP GET request
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    return requests.get(url, headers=headers)

def get_acquisitions(org):
    # Make HTTP request to index.co
    org = org.lower()
    url = f"https://index.co/company/{org}/acquirees"
    r = make_request(url)

    # Parsing and returning the acquisition data
    if "Sorry! We were unable to find this page" in r.text:
        return []
    else:
        acquisitions = []
        soup = BeautifulSoup(r.content, "html5lib")
        results = soup.find_all("strong", class_="c_identityChip-name")
        for i in results:
            t = i.get_text()
            if t not in acquisitions and t.lower() != org:
                acquisitions.append(t)
        return acquisitions

if __name__ == "__main__":

    # Parsing options
    parser = argparse.ArgumentParser(description="A script to fetch acquisition data of a company")
    parser.add_argument("-o", "--org", type=str, required=True, help="specify organisation to find acquisitions")
    parser.add_argument("-q", "--quiet", action="store_true", help="do not show the banner")
    args = parser.parse_args()

    # Printing the banner
    if not args.quiet:
        print("-----------------------")
        print(" ACQUISITION SCANNER")
        print(" Coded By: @n3hal_")
        print("-----------------------")

    if args.org:
        
        # Getting acquisitions data
        org = args.org
        acquisitions = get_acquisitions(org)

        # Printing acquisitions data
        if len(acquisitions) != 0:
            for acquisition in acquisitions:
                print(acquisition)
        else:
            print(colored("No acquisitions found.", "red"))