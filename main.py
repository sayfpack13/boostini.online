import concurrent.futures

import requests
import queue
import threading
from random_username.generate import generate_username


headers={
    "x-requested-with": "XMLHttpRequest"
}
url="https://boostini.online/requests.php?f=register"

file = open("users.txt", "a")
file.write("\n")
counter=0

def create_account(id):
    username = generate_username()[0]
    email = username + "@gmail.com"
    password = email

    data = {
        'username': username,
        'email': email,
        'password': password,
        'confirm_password': password,
        'gender': 'male',
        'accept_terms': 'on'
    }
    response = requests.post(url=url, data=data, headers=headers)

    global counter
    if(response.text.__contains__("Successfully")):
        file.write(email+":"+password+"\n")
        counter += 1
        msg="Success: "+username
    else:
        msg=response.text[response.text.rfind(">")+1:-3].strip()

    print(str(id)+") "+msg)

def start():
    count=int(input("Account Number: "))


    with concurrent.futures.ThreadPoolExecutor() as executor:
        res = [executor.submit(create_account,a+1) for a in range (count)]
        concurrent.futures.wait(res)

    file.close()
    print("\nCreated: "+str(counter)+"/"+str(count))

start()
