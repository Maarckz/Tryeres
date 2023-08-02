#!/usr/bin/env python
version = "v2.12-dev"

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
    with open("./remover.txt", "r") as f:           ###################################
        lst = f.readlines()                         #  Este trecho do código serve    #
    remove = '\n'                                   #  para apagar cada arquivo       #
    lst = [l.replace(remove, "") for l in lst]      #  mencionado em cada linha em    #
    for l in lst:                                   #  um arquivo .txt                #
        os.system(f'rm -rf {l}')                    ###################################



def crawl(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        hrefcode = {urljoin(url, link['href']) for link in links if 'href' in link.attrs}
        return hrefcode
    return []

def ext_info(url):
    durls = []
    emails = set()
    tel = set()
    forms = []
    subdomains = set()

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        for link in soup.find_all('a'):
            href = link.get('href')
            if link is soup.find('id'):
                print(link)
            elif link is not None:
                try:
                    if href and href.startswith('/') or href.startswith('?'):
                        durls.append(urljoin(url, href))
                    else:
                        print(href)
                except AttributeError as e:
                    print(link,href,e)
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                if href.startswith("mailto:"):
                    emails.add(href[7:])
                elif href.startswith("tel:") or "phone=" in href:
                    tel.add(href[4:])

        for form in soup.find_all('form'):
            forms.append(url)

        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                parsed_uri = urlparse(href)
                domain = '{uri.netloc}'.format(uri=parsed_uri).split(':')[0]
                subdomains.add(domain)

    return durls, emails, tel, forms, subdomains

def process_url(url):
    visit_urls = set()
    if url in visit_urls:
        return
    visit_urls.add(url)
    divurls = crawl(url)
    print("\n\nEfetuando WebCrawling em ", url)
    for divurl in sorted(divurls):
        print('\n\033[0;31m============================================================================================>>\033[m',time.strftime("\033[7;32m %d/%m/%y \033[m"))
        print(divurl)
        print('\033[0;31m============================================================================================>>\033[m',time.strftime("\033[7;32m %H:%M:%S \033[m"))

        durls, emails, tel, forms, subdomains = ext_info(divurl)

        if durls:
            print('\nURLs INTERNAS:')
            for url in durls:
                print(url)
                try:
                    links(url)
                except requests.exceptions.ConnectionError as err:
                    pass
        if emails:
            print('\nEMAILS:')
            for email in emails:
                print(email)
      
        if tel:
            print('\nTELEFONES:')
            for phone in tel:
                print(phone)
       
        if forms:
            print('\nFORMULÁRIOS:')
            for form in forms:
                print(form)
      
        if subdomains:
            print('\nSITES:')
            for subdomain in subdomains:
                print(subdomain)
        if durls:
            print('\nURLs INTERNAS:')
            for url in durls:
                print(url)
                # Chamada recursiva para o novo link encontrado
                
def links(target):
    url_process = ['http://' + target]
    url_atual = url_process.pop()
    process_url(url_atual)
    
    sit = input('\nDeseja salvar qo WebCrawl? (S/N) ')
    if(sit.lower() == 's'):
        print('Aguarde enquanto o arquivo está sendo salvo ...')
        with open('craw.txt', 'w') as f:
            while url_process:
                url_atual = url_process.pop()
                os.dup2(f.fileno(), 1)
                process_url(url_atual)
                os.dup2(os.dup(2), 1) 
        print("WebCrawler salvo com sucesso!")

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
                    f'sslscan {target}',
                    #f'nmap -Pn --script vuln -T4 {target}',
                    f'nmap -A -T4 {target}',
                    f'whatweb -v {target}',   
                    f'curl -Is {target} && curl -Is http://{target} && curl -Is https://{target}',
                    f'curl http://{target}/robots.txt',
                    f'curl https://{target}/robots.txt',
                    f'wafw00f {target}',
                    f'fierce --domain {domain}',
                    f'dnsrecon -d {domain}',
                    f'enum4linux {target}',
                )
                for comando in comandos:
                    print('\n\033[0;31m============================================================================================>>\033[m',time.strftime("\033[7;32m %d/%m/%y \033[m"))
                    print(comando)
                    print('\033[0;31m============================================================================================>>\033[m',time.strftime("\033[7;32m %H:%M:%S \033[m"))
                    os.system(comando) 
                
                links(target)
                os.system('sqlmap -u {target} --crawl=2 --batch')
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
                    apt-get install python3 python3-pip whois sslscan nmap whatweb curl wafw00f fierce dnsrecon sqlmap
                    sudo apt install snapd
                    snap install enum4linux
                    ''')
                    bibliotecas = ['beautifulsoup4', 'requests', 'urllib3']
                    for biblioteca in bibliotecas:
                        try:
                            os.system(f'pip3 install {biblioteca}')
                        except Exception as e:
                            print(f"Erro ao instalar {biblioteca}: {e}")
                    with open('.ok', 'w') as f:
                        f.write("ok")
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
            install()
            os.system('clear')
            print(banner)
            recon()
        elif op == 2:
            install()
        elif op == 3:
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

