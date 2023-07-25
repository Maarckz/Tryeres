import requests
import time
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def crawl(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        directories = {urljoin(url, link['href']) for link in links if 'href' in link.attrs}
        return directories
    return []

def extract_info(url):
    dynamic_urls = []
    emails = set()
    phones = set()
    forms = []
    subdomains = set()

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and ("?" in href or "/" in href) or href.startswith('/') or href.startswith('?'):
                dynamic_urls.append(urljoin(url, href))

        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                if href.startswith("mailto:"):
                    emails.add(href[7:])
                elif href.startswith("tel:") or "phone=" in href:
                    phones.add(href[4:])

        for form in soup.find_all('form'):
            forms.append(url)

        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                parsed_uri = urlparse(href)
                domain = '{uri.netloc}'.format(uri=parsed_uri).split(':')[0]
                subdomains.add(domain)

    return dynamic_urls, emails, phones, forms, subdomains

def process_url(url):
    visited_urls = set()
    if url in visited_urls:
        return
    visited_urls.add(url)
    directories = crawl(url)
    print("\n\nEfetuando WebCrawling em ", url)
    for directory in sorted(directories):
        print('\n\033[0;31m============================================================================================>>\033[m',time.strftime("\033[7;32m %d/%m/%y \033[m"))
        print(directory)
        print('\033[0;31m============================================================================================>>\033[m',time.strftime("\033[7;32m %H:%M:%S \033[m"))

        dynamic_urls, emails, phones, forms, subdomains = extract_info(directory)

        if dynamic_urls:
            print('\nURLs INTERNAS:')
            for url in dynamic_urls:
                print(url)
     
        if emails:
            print('\nEMAILS:')
            for email in emails:
                print(email)
      
        if phones:
            print('\nTELEFONES:')
            for phone in phones:
                print(phone)
       
        if forms:
            print('\nFORMULÁRIOS:')
            for form in forms:
                print(form)
      
        if subdomains:
            print('\nSITES:')
            for subdomain in subdomains:
                print(subdomain)

def links(target):
    url_process = ['http://' + target]
    sit = 'n'#input('Deseja salvar e não exibir o WebCrawl? (S/N) ')
    if(sit.lower() == 's'):
        with open('craw.txt', 'w') as f:
            while url_process:
                url_atual = url_process.pop()
                os.dup2(f.fileno(), 1)
                process_url(url_atual)
                os.dup2(os.dup(2), 1) 
        print("WebCrawler salvo com sucesso!")
    else:
        url_atual = url_process.pop()
        process_url(url_atual)

links('www.google.com')