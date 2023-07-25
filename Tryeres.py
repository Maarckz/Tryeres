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
        directories = {urljoin(url, link['href']) for link in links if 'href' in link.attrs}
        return directories
    return []

def ext_info(url):
    dynamic_urls = []
    emails = set()
    tel = set()
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
                    tel.add(href[4:])

        for form in soup.find_all('form'):
            forms.append(url)

        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                parsed_uri = urlparse(href)
                domain = '{uri.netloc}'.format(uri=parsed_uri).split(':')[0]
                subdomains.add(domain)

    return dynamic_urls, emails, tel, forms, subdomains

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

        dynamic_urls, emails, tel, forms, subdomains = ext_info(directory)

        if dynamic_urls:
            print('\nURLs INTERNAS:')
            for url in dynamic_urls:
                print(url)
     
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

###############################################################################################################################################

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

###############################################################################################################################################

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


'''
nmap -n -sP www.wedologos.com.br
nmap -n -v -Pn -sS www.wedologos.com.br | grep "open port"
nmap -n -v -Pn -sU www.wedologos.com.br | grep "open port" 

whois $TARGET 2> /dev/null | tee $LOOT_DIR/osint/whois-$TARGET.txt 2> /dev/null 
dig www.wedologos.com.br txt | egrep -i 'spf|DMARC|dkim'
dig iport._domainkey.www.wedologos.com.br txt txt | egrep -i 'spf|DMARC|DKIM'
dig _dmarc.${TARGET} txt | egrep -i 'spf|DMARC|DKIM' | tee -a $LOOT_DIR/nmap/email-$TARGET.txt 2>/dev/null
curl -s https://www.ultratools.com/tools/ipWhoisLookupResult\?ipAddress\=www.wedologos.com.br | grep -A2 label | grep -v input | grep span | cut -d">" -f2 | cut -d"<" -f1 | sed 's/\&nbsp\;//g'
wget -q http://www.intodns.com/$TARGET -O $LOOT_DIR/osint/intodns-$TARGET.html 2> /dev/null

cp -f /etc/theHarvester/api-keys.yaml ~/api-keys.yaml 2> /dev/null
cd ~ 2> /dev/null
theHarvester -d $TARGET -b all 2> /dev/null | tee $LOOT_DIR/osint/theharvester-$TARGET.txt 2> /dev/null 

curl -s https://www.email-format.com/d/$TARGET| grep @$TARGET | grep -v div | sed "s/\t//g" | sed "s/ //g" 2> /dev/null | tee $LOOT_DIR/osint/email-format-$TARGET.txt 2> /dev/null 
urlcrazy $TARGET 2> /dev/null | tee $LOOT_DIR/osint/urlcrazy-$TARGET.txt 2> /dev/null
echo -e "$OKBLUE[$RESET${OKRED}i${RESET}$OKBLUE]$OKGREEN metagoofil -d $TARGET -t doc,pdf,xls,csv,txt -l 25 -n 25 -o $LOOT_DIR/osint/ -f $LOOT_DIR/osint/$TARGET.html 2> /dev/null | tee $LOOT_DIR/osint/metagoofil-$TARGET.txt 2> /dev/null
python metagoofil.py -d $TARGET -t doc,pdf,xls,csv,txt -l 25 -n 25 -o $LOOT_DIR/osint/ -f $LOOT_DIR/osint/$TARGET.html 2> /dev/null | tee $LOOT_DIR/osint/metagoofil-$TARGET.txt 2> /dev/null 

curl --insecure -L -s "https://urlscan.io/api/v1/search/?q=domain:$TARGET" 2> /dev/null | egrep "country|server|domain|ip|asn|$TARGET|prt"| sort -u | tee $LOOT_DIR/osint/urlscanio-$TARGET.txt 2> /dev/null
h8mail -q domain --target $TARGET -o $LOOT_DIR/osint/h8mail-$TARGET.csv 2> /dev/null
python3 gitGraber.py -q "\"org:$ORGANIZATION\"" -s 2>&1 | tee $LOOT_DIR/osint/gitGrabber-$ORGANIZATION.txt 2> /dev/null
goohak $TARGET > /dev/null
php /usr/share/sniper/bin/inurlbr.php --dork "site:$TARGET" -s inurlbr-$TARGET | tee $LOOT_DIR/osint/inurlbr-$TARGET
'''


'''
zaproxy
sublist3r
davtest
sqlmap
GOWITNESS
findomain
subfinder
crlfuzz
arachni scan
hakrawler

apt install golang
apt install -y python3-paramiko
apt install -y nfs-common
apt install -y nodejs
apt install -y wafw00f
apt install -y xdg-utils
apt install -y ruby
apt install -y rubygems
apt install -y python
apt install -y dos2unix
apt install -y aha
apt install -y libxml2-utils
apt install -y rpcbind
apt install -y cutycapt
apt install -y host
apt install -y whois
apt install -y dnsrecon
apt install -y curl
apt install -y nmap
apt install -y php7.4
apt install -y php7.4-curl
apt install -y hydra
apt install -y sqlmap
apt install -y nbtscan
apt install -y nikto
apt install -y whatweb
apt install -y sslscan
apt install -y jq
apt install -y golang
apt install -y adb
apt install -y xsltproc
apt install -y ldapscripts
apt install -y libssl-dev 2> /dev/null
apt install -y python-pip 2> /dev/null
apt purge -y python3-pip
apt install -y python3-pip
apt install -y xmlstarlet
apt install -y net-tools
apt install -y p7zip-full
apt install -y jsbeautifier
apt install -y theharvester 2> /dev/null
apt install -y phantomjs 2> /dev/null
apt install -y chromium 2> /dev/null
apt install -y xvfb
apt install -y urlcrazy
apt install -y iputils-ping
apt install -y enum4linux
apt install -y dnsutils'''
