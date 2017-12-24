import socket,os,time,hashlib,logging
from conf import settings
from modules import display
from modules.log import *

Home = '' # home dir
User = '' # current user


def run():
    global User
    global Home
    print("Load local system...")
    time.sleep(1)
    flag = True
    while flag:
        print('FTP SYSTEM'.center(30,'*'))
        if not User:
            login()
        print("\033[1;34;1myou can press 'help' to continue\033[0m")
        command = input("\033[1;32;1mcommand:>>\033[0m").strip()
        list_command = command.split()

        if list_command[0].startswith('ls'):
            ls()
        elif list_command[0] == 'logout':# logout local system
            print('\033[1;31;1mlogout local system...\033[0m')
            User = ''
            Home = ''
        elif list_command[0] == 'login':
            interaction()
        elif list_command[0] == 'df':
            df()
        elif list_command[0] == 'cd':
            cd()
        elif list_command[0] == 'help':
            print(display.HelpMenu)
        else:
            print("\033[1;32;1mInvalid input!!!\033[0m")


def login():
    import json
    global User
    global Home
    while True:
        user = input("\033[1;32;1musername:\033[0m").strip()
        psd = input("\033[1;32;1mpasswod:\033[0m").strip()
        # user = 'admin'
        # psd = '123456'
        with open("%s/users/users.db"%settings.DATABASE, 'r') as f:
            users = json.load(f)
            if user in users:
                if psd == users[user]:
                    print("\033[1;34;1mlogin successful!\033[0m")
                    User = user
                    path = "%s/client/%s" % (settings.DATABASE, User)
                    if not os.path.exists(path):
                        os.makedirs(path)
                        print("\033[1;34;1mCreated new dir for user!\033[0m")
                    Home = path
                    logging.info("\033[1;34;1muser login local system\033[0m")
                    return True
                else:
                    print("\033[1;31;1mIncorrect password!\033[0m")
                    logging.info('\033[1;31;1muser login failed\033[0m')
            else:
                print("\033[1;31;1mNo such user!\033[0m")
                logging.info('\033[1;31;1muser login failed\033[0m')

def rz(command,sk):
    '''
    upload files from server
    :param command: string type
    :param socket:
    :return:
    '''
    list_command = command.split()
    file_path = "%s/%s" % (Home, list_command[1])
    if os.path.isfile(file_path): # remain exclude 'file/..'
        sk.send(command.encode()) # send command

        response = sk.recv(1024).decode()
        print("response:", response)
        if response == 'ready':
            md5_check = hashlib.md5()
            with open(file_path, 'rb') as f:
                for line in f:
                    md5_check.update(line)
            sk.send(md5_check.hexdigest().encode()) #send md5_check

            exist_size = int(sk.recv(1024).decode()) # start size to send,always 0
            print("exist size need [%s] to send:"%exist_size)
            file_size = os.stat(file_path).st_size
            sk.send(str(file_size).encode())  # send file total size

            data = sk.recv(1024).decode()
            print("can I start? --respond:",data)

            with open(file_path, 'rb') as f:
                f.seek(exist_size)  # location to file
                for line in f:
                    sk.send(line)
                    exist_size += len(line)
                    print("Transfer:{p} %".format(p=int(100 * exist_size / file_size)), end='\r')
            print('\033[1;34;1mSend completely! 100%\033[0m')

            ###confirm whether received
            result = sk.recv(1024).decode()
            print("\033[1;32;1mtransfer result:\033[0m", result)
        else:
            print("\033[1;31;1mfailed...\033[0m")
    else:
        print("\033[1;31;1mInvalid file!\033[0m")

def sz(command,sk):
    '''
    downoad file from server
    :param command: list type
    :return:
    '''
    filename = command.split()[1]  # will be used at the end,rename
    sk.send(command.encode())

    data = sk.recv(1024)
    print("response:",data.decode())
    if data.decode() == 'valid':
        sk.send(b'request md5')

        md5_check = sk.recv(1024).decode()
        print("md5 check:",md5_check)
        exist_size = 0
        if md5_check in os.listdir(Home):  # file check，if exist crashed file,continue
            exist_size = os.stat("%s/%s" % (Home, md5_check)).st_size
        sk.send(str(exist_size).encode())  # default, send 0

        file_size = sk.recv(1024).decode()  # recv file total size
        print("file size:%s,tpye:%s" % (file_size, type(file_size)))

        sk.send(b'0') ####
        # recv_size = int(file_size) - exist_size
        with open('%s/%s' % (Home, md5_check), 'ab') as f:
            while int(file_size) > exist_size:
                size = int(file_size) - exist_size
                if size < 1024:  # last data to receive
                    data = sk.recv(size)
                else:
                    data = sk.recv(1024)
                exist_size += len(data)
                f.write(data)
                print("Transfer:{p} %".format(p=int(100*exist_size/int(file_size))),end='\r')
            else:
                print('\033[1;34;1mCompletely! 100%\033[0m')
            ####recv finish
         # self check
        md5 = hashlib.md5()
        with open("%s/%s" % (Home, md5_check), "rb") as f:
            for line in f:
                md5.update(line)
        if md5.hexdigest() == md5_check:  # check passed
            if os.path.exists("%s/%s"%(Home,filename)):
                os.remove("%s/%s"%(Home,filename))
            os.rename("%s/%s" % (Home, md5_check), "%s/%s" % (Home, filename))  # rename filename
            print("\033[1;34;1mfile confirm passes,renamed..\033[0m")
        else:
            # self.request.send(b'file crash!!!')
            os.remove("%s/%s" % (Home, md5_check))
            print("\033[1;31;1mRemove file because check failed...\033[0m")
    else:
        print("\033[1;31;1mInvalid filename!\033[0m")

def cd():
    print("No dirs")

def ls():
    print("\033[1;34;1mitems:\033[0m")
    for file in os.listdir(Home):
        print(file)

def df():
    print("@_@!!!".center(30,'*'))

def interaction():
    '''

    :return:
    '''
    client = socket.socket()  # socket
    client.connect((settings.ADDR, settings.PORT))
    print("\033[1;34;1mConnected to socket!\033[0m", )
    #auth login
    data = client.recv(1024).decode() #auth username
    logging.info('client connect in...')
    print('[server]',data)
    user = input("input:").strip()
    client.send(user.encode())#send username
    data = client.recv(1024).decode()#auth password
    print('[server]', data)
    psd = input("input:").strip()
    md5_psd = hashlib.md5(psd.encode())
    client.send(md5_psd.hexdigest().encode())  # send password
    result = client.recv(1024).decode() #recv result
    print("login response:",result)
    if result == 'success': # pass auth
        print("\033[1;34;1mLogin success to server!\033[0m")
        logging.info('client login to server successfully')
        while True:
            command = input("FTP-Server:>>").strip()
            if not command:
                pass
            else:
                list_command = command.split()
                if list_command[0]=='rz':
                    rz(command,client)
                elif list_command[0]=='sz':
                    sz(command,client)
                elif list_command[0]=='logout':
                    client.send(b'logout')
                    logging.info('client disconnect from server')
                    break #leave server
                else: #common command ,do not need resend
                    client.send(command.encode()) # send command
                    data = client.recv(1024).decode() # recv result
                    print("[server]:\n",data)
    else:
        print("\033[1;31;1mLogin failed!\033[0m")

