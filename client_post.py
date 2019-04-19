import requests
import os
import time
import platform
import sys

PARAMS = CMD = USERNAME = PASSWORD = API = ""
HOST = "localhost"
PORT = "1104"


def __postcr__():
    return "http://"+HOST+":"+PORT+"/"+CMD+"?"


def print_data(data):
    print ("message : %s",data["message"])
    print ("status : %s", data["status"])
    print ("code : %s", data["code"])
    i = 0
    for x in data["blocks"]:
        print ("block  "+ str(i) + ":")
        print ("subject : "+ str(data["blocks"][str(x)]["subject"]))
        print ("body : "+ str(data["blocks"][str(x)]["body"]))
        print ("status : " + str(data["blocks"][str(x)]["status"]))
        print ("id : " + str(data["blocks"][str(x)]["id"]))
        print ("")
        i+=1

def print_message(d):
    print (d["message"])


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def show_func():
    print("USERNAME : "+USERNAME+"\n"+"API : " + API)
    print("""What Do You Prefer To Do :
    1. send ticket
    2. get ticket
    3. close ticket
    4. Logout
    5. Exit
    """)

def show_func2():
    print("USERNAME : " + USERNAME + "\n" + "API : " + API)
    print("""What Do You Prefer To Do :
        1. get all tickets
        2. response to ticket
        3. change ticket status
        4. Logout
        5. Exit
        """)

while True:
    clear()
    print("""WELCOME TO BANK CLIENT
    Please Choose What You Want To Do :
    0. signup
    1. sign in as client 
    2. sign in as admin
    3. exit
    """)
    status = sys.stdin.readline()
    if status[:-1] == '0':
        clear()
        print("Enter Your username : ")
        username = sys.stdin.readline()[:-1]
        print("Enter your password :")
        password = sys.stdin.readline()[:-1]
        print("Enter your fistname :")
        firstname = sys.stdin.readline()[:-1]
        print("Enter your lastname :")
        lastname = sys.stdin.readline()[:-1]
        print("Enter your rule : client,admin")
        rule = sys.stdin.readline()[:-1]
        CMD = "signup"
        PARAMS = {'username': username, 'password': password, 'firstname': firstname, 'lastname': lastname,
                  'rule': rule}
        data = requests.post(__postcr__(), params=PARAMS).json()
        print_message(data)
        continue
    elif status[:-1] == '1':
        clear()
        while True:
            print("USERNAME : ")
            USERNAME = sys.stdin.readline()[:-1]
            print("PASSWORD : ")
            PASSWORD = sys.stdin.readline()[:-1]
            CMD = "login"
            PARAMS = {'username':USERNAME,'password':PASSWORD}
            r = requests.post(__postcr__(),params=PARAMS).json()
            print_message(r)
            if r['status'] == 'OK':
                clear()
                print("USERNAME AND PASSWORD IS CORRECT\nLogging You in ...")
                API = r['api']
                time.sleep(2)
                break
            else:
                clear()
                print("USERNAME AND PASSWORD IS INCORRECT\nTRY AGAIN ...")
                time.sleep(2)
        while True:
            clear()
            show_func()
            func_type = sys.stdin.readline()
            if func_type[:-1] == '1':
                clear()
                CMD = "sendticket"
                print ("Enter your subject :")
                Subject = sys.stdin.readline()[:-1]
                print ("Enter your message :")
                Body = sys.stdin.readline()[:-1]
                PARAMS = {'token':API,'subject':Subject,'body':Body,'sender':USERNAME}
                data = requests.post(__postcr__(),params=PARAMS).json()
                print_message(data)
                input("Press Any Key To Continue ...")
            if func_type[:-1] == '2':
                clear()
                CMD = "getticketcli"
                PARAMS = {'token': API}
                data = requests.post(__postcr__(), params=PARAMS).json()
                print_data(data)

                input("Press Any Key To Continue ...")
            if func_type[:-1] == '3':
                clear()

                print("Enter Your id to close : ")
                id_2 = sys.stdin.readline()[:-1]
                CMD = "closeticket"
                PARAMS = {'token': API, 'id': id_2}
                data = requests.post(__postcr__(),params=PARAMS).json()
                print_message(data)
                input("Press Any Key To Continue ...")
            if func_type[:-1] == '4':
                clear()
                print("Enter Your username : ")
                username = sys.stdin.readline()[:-1]
                print("Enter your password :")
                password = sys.stdin.readline()[:-1]
                CMD = "logout"
                PARAMS = {'username': username, 'password': password}
                data = requests.post(__postcr__(), params=PARAMS).json()
                print_message(data)
                break
                input("Press Any Key To Continue ...")
            if func_type[:-1] == '5':
                sys.exit()

    elif status[:-1] == '2':
        clear()
        while True:
            print("USERNAME : ")
            USERNAME = sys.stdin.readline()[:-1]
            print("PASSWORD : ")
            PASSWORD = sys.stdin.readline()[:-1]
            CMD = "login"
            PARAMS = {'username':USERNAME,'password':PASSWORD}
            r = requests.post(__postcr__(),params=PARAMS).json()
            print_message(r)
            if r['status'] == 'OK':
                clear()
                print("USERNAME AND PASSWORD IS CORRECT\nLogging You in ...")
                API = r['api']
                time.sleep(2)
                break
            else:
                clear()
                print("USERNAME AND PASSWORD IS INCORRECT\nTRY AGAIN ...")
                time.sleep(2)
        while True:
            show_func2()
            func_type = sys.stdin.readline()
            if func_type[:-1] == '1':
                clear()
                CMD = "getticketmod"
                PARAMS = {'token': API}
                data = requests.post(__postcr__(), params=PARAMS).json()
                print_data(data)

                input("Press Any Key To Continue ...")
            elif func_type[:-1] == '2':
                clear()
                CMD = "restoticketmod"
                print("Enter the id that you want to response :")
                id_2 = sys.stdin.readline()[:-1]
                print("Enter your response :")
                body = sys.stdin.readline()[:-1]
                PARAMS = {'token': API,'id':id_2,'body':body}
                data = requests.post(__postcr__(), params=PARAMS).json()
                print_message(data)

                input("Press Any Key To Continue ...")
            elif func_type[:-1] == '3':
                clear()
                CMD = "changestatus"
                print("Enter the id that you want to response :")
                id_2 = sys.stdin.readline()[:-1]
                print("Enter new status :(open,close,inprogress)")
                prog = sys.stdin.readline()[:-1]
                PARAMS = {'token': API,'id':id_2,'status':prog}
                data = requests.post(__postcr__(), params=PARAMS).json()
                print_message(data)
            elif func_type[:-1] == '4':
                clear()
                print("Enter Your username : ")
                username = sys.stdin.readline()[:-1]
                print("Enter your password :")
                password = sys.stdin.readline()[:-1]
                CMD = "logout"
                PARAMS = {'username': username, 'password': password}
                data = requests.post(__postcr__(), params=PARAMS).json()
                print_message(data)
                break
            if func_type[:-1] == '5':
                sys.exit()
    elif status[:-1] == '3':
        sys.exit()
    else:
        print("Wrong Choose Try Again")
