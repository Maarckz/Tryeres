#!/usr/bin/env python
version = "v1.1-dev"

import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

banner = f"""\033[1;33m
MMMMMMMMMM\033[34m< < < < < < < < < < < < < < < < < < < < < < < < < < <\033[m \033[1;33m
M¨¨¨¨¨¨¨¨M                                                                
Mmmm  mmmM                                                                
MMMM  MMMM 88d888b. dP    dP .d8888b. 88d888b. .d8888b. .d8888b. 
MMMM  MMMM 88'  `88 88    88 88ooood8 88'  `88 88ooood8 Y8ooooo. 
MMMM  MMMM 88       88.  .88 88.  ... 88       88.  ...       88 
MMMM  MMMM dP       `8888P88 `88888P' dP       `88888P' `88888P' 
MMMMMMMMMM               .88\033[m   \033[1;30m __ _  ___ ____ _________/ /_____      \033[m                               
  .___,    .___,     \033[1;33md8888P\033[m \033[1;30m   /  ' \/ _ `/ _ `/ __/ __/  '_/_ /\033[m
  (o o)    (o o)             \033[1;30m /_/_/_/\_,_/\_,_/_/  \__/_/\_\/__/ \033[m
 (  V  )  (  V  )             \033[0;31m>DefCyberTool\033[m             \033[7;32m{version}\033[m
/\033[1;35m--\033[mm\033[1;35m-\033[mm\033[1;35m------\033[mm-m\033[1;35m--\033[m/              
"""
press = '(Pressione qualquer tecla para voltar ao menu inicial)'
Ctrl_C = 'Você pressionou Ctrl+C para interromper o programa!'



def remover_arquivos():                             
    with open("./remove.txt", "r") as f:            ###################################
        lst = f.readlines()                         #  Este trecho do código serve    #
    remove = '\n'                                   #  para apagar cada arquivo       #
    lst = [l.replace(remove, "") for l in lst]      #  mencionado em um arquivo .txt  #
    for l in lst:                                   ###################################
        os.system(f'rm -rf {l}')                    




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


def recon():
    try:
        target = input('Por onde Começo?(URL) ')
        parse = target.split('.')
        domain = '.'.join(parse[1:])

        if target == None or target == 0 or target == '':
            print('Você precisa digitar uma URL válida.')
            input(press)
        else:
            response = requests.get('http://'+target)
            if response.status_code != 200:
                print(f'O statuscode é: {response.status_code}')
                input(press)
            else:
                comandos = (
                    f'whois {target}',
                    f'ping -c 1 -t 5 {target}',
                    f'dig {target}',
                    f'sudo nmap -Pn-T4 {target}',
                    f'curl -Is {target} && curl -Is http://{target} && curl -Is https://{target}',
                    f'wafw00f {target}',
                    f'dnsenum {domain} -p 15',
                )
                for comando in comandos:
                    print('\n\033[0;31m============================================================================================>>\033[m',time.strftime("\033[7;32m %d/%m/%y \033[m"))
                    print('\033[0;31m============================================================================================>>\033[m',time.strftime("\033[7;32m %H:%M:%S \033[m"))
                    os.system(comando) 
                
                links(target)
    except KeyboardInterrupt:
        print('\n'+Ctrl_C)

def install():
    os.system('touch .ok')
    with open('.ok', 'r') as f:
        content = f.read()
        if content == "":
            autoriz = input('Este SCRIPT precisa instalar algumas ferramentas. Deseja continuar? (S/N) ')
            if autoriz.lower() == 's':
                try:
                    os.system('''
                    apt update
                    ''')
                    os.system('echo "ok" > .ok')
                except Exception as e:
                    print(f"Erro durante a atualização: {str(e)}")
        else:
            print("Pacotes necessários instalados.")

def status():
    status = '''ps -ef | egrep "sniper|slurp|hydra|ruby|python|dirsearch|amass|nmap|metasploit|curl|wget|nikto" && echo "NETWORK CONNECTIONS..." && netstat -an | egrep "TIME_WAIT|EST"'''
    os.system(status)

def menu():
    os.system('clear')
    print(banner)
    print('''MENU:\n
[1] - Vamos lá!
[2] - Status
[0] - Exit
''')
    try:    
        op = int(input('Escolha uma opção: '))
    
        if op == 1:
            recon()
        elif op == 2:
            status()
        elif op == 0:
            print('Volte sempre! ¯\_(ツ)_/¯')
            exit(1)
        elif op > 2:
            print('Digite uma entrada válida.')
            input(press)
            menu()
    except ValueError as e:
        print(f'Ocorreu um erro {e}.')
        input(press)
        menu()
    except KeyboardInterrupt:
        print('\n'+Ctrl_C)

if os.geteuid() == 0:
    menu()
else:
    print("Execute o SCRIPT como superusuário (root).")
  
