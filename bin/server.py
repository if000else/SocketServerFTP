import socketserver, os, sys, json, hashlib,logging
from pathlib import Path
BASEDIR = Path(__file__).parent.parent
sys.path.append(str(BASEDIR))
from conf import settings
from modules.log import *

Bash = {
    'logout': 'self.logout()',
    'cd': 'self.cd()',
    'rz': 'self.rz()',
    'sz': 'self.sz()',
    'useradd': 'self.useradd()',
    'ls': 'self.ls()',
}


class MyTCPHandler(socketserver.BaseRequestHandler):
    '''
    handlle method
    '''

    User = ''
    PATH = settings.HomeOfServer  ### home dir
    Command = []

    def handle(self):
        '''
        judge input from client then response,in a long loop.
        :return:
        '''
        try:
            print("service is on,wait client...")
            print("client [%s] in.." % self.client_address[0])
            while True:
                if not self.User:
                    self.login()
                comm = self.request.recv(1024).decode()
                if comm:
                    self.Command = comm.strip().split()
                    print("recv command:",self.Command[0])
                    if self.Command[0] in Bash.keys():
                        print("Bash[command]:",Bash[self.Command[0]])
                        eval(Bash[self.Command[0]])  # call corresponding functions
                    else:
                        print("Invalid client request")
                        self.request.send(b'Invalid input!')
                else:
                    print("client send blank message!")
                    self.request.close()
        except OSError:
            print("Client [%s] has disconnect!"%self.client_address[0])

    def ls(self):
        '''
        list items of dirs ,client remain receiving...
        :return:
        '''
        dirs = os.listdir(self.PATH)
        data='\n'
        for i in dirs:
            data += "%s\n"%i
        self.request.send(data.encode())

    def cd(self):
        '''
        while 'cd modules' will enter kid dir,'cd ..' will back to parent dir.
        client remain receiving...
        :return:
        '''
        if len(self.Command) == 2:
            dirname = '%s/%s' % (self.PATH, self.Command[1])
            if os.path.isdir(dirname):
                if self.Command[1] == '..': #back <--
                    if self.PATH == settings.HomeOfServer:
                        self.request.send(b'Take no effect!')
                    else:
                        # basename = os.path.basename(self.PATH) # get basename
                        # self.request.send(basename.encode()) # send basename
                        self.PATH = os.path.dirname(self.PATH) # reset PATH
                        self.request.send(self.PATH.encode())
                else:
                    self.request.send(self.Command[1].encode())  # send dir
                    self.PATH = dirname # forward -->
            else:
                self.request.send(b'Please input a valid dirname!')
        else:
            self.request.send(b'Please input dirname!')

    def rz(self):
        """
        upload files to server,like 'rz test.txt'
        :return:
        """
        if os.path.exists("%s/%s" % (self.PATH, self.Command[1])):
            self.request.send(b'file has existed!')
        else:
            self.request.send(b'ready')

            md5_check = self.request.recv(1024).decode()
            print("recv md5:",md5_check)
            exist_size = 0
            if md5_check in os.listdir(self.PATH):  # file check，if exist crashed file,continue
                exist_size = os.stat("%s/%s"%(self.PATH,md5_check)).st_size
            self.request.send(str(exist_size).encode())  # default, send 0

            file_size = self.request.recv(1024).decode() #recv file total size
            self.request.send(b'please start send file')


            with open('%s/%s' % (self.PATH, md5_check), 'ab') as f:
                while exist_size < int(file_size):
                    size = int(file_size) - exist_size
                    if size < 1024:
                        data = self.request.recv(size)
                    else:
                        data = self.request.recv(1024)
                    exist_size += len(data)
                    f.write(data)
                    # print("Transfer:%s%%"%(100*recv_size/file_size),end='\r')
                else:
                    print('recv file completely!')

            # confirm file and reply client
            with open('%s/%s' % (self.PATH, md5_check), 'rb') as f:
                md5 = hashlib.md5()
                for line in f:
                    md5.update(line)
            if md5.hexdigest() == md5_check: # check passed
                if os.path.exists("%s/%s" % (self.PATH, self.Command[1])): # default overwrite
                    os.remove("%s/%s" % (self.PATH, self.Command[1]))
                os.rename("%s/%s" % (self.PATH, md5_check), "%s/%s" % (self.PATH, self.Command[1]))  # rename filename
                self.request.send(b'success,renamed')
            else:
                self.request.send(b'file crash!!!')
                os.remove("%s/%s"%(self.PATH,md5_check))
                print("remove file because check failed...")

    def sz(self):
        """
        download files from server,like 'sz test.txt'
        :return:
        """
        filename = "%s/%s"%(self.PATH,self.Command[1])
        if os.path.isfile(filename):
            self.request.send(b'valid') #respond client

            self.request.recv(1024) # "recv request md5"
            md5_check = hashlib.md5()
            with open(filename,'rb') as f:
                for line in f:
                    md5_check.update(line)
                self.request.send(md5_check.hexdigest().encode()) ####send md5 check

                exist_size = int(self.request.recv(1024).decode())
                file_size = os.stat(filename).st_size
                print("file size:%s,tpye:%s"%(file_size,type(file_size)))
                # sent_size = file_size - exist_size  # how mand bytes to be sent
                self.request.send(str(file_size).encode())  # send file total size

                self.request.recv(1024) #####
            with open(filename, 'rb') as f:
                f.seek(exist_size)  # location to file
                for line in f:
                    self.request.send(line)

            print('send completely!')
            # result = sk.recv(1024).decode()
            # print("transfer result:", result)

        else:
            self.request.send(b'Invalid filename!')

    def useradd(self):
        '''
        like: useradd username password
        encrypt password and save to file
        :return:
        '''
        user = self.Command[1]
        psd = self.Command[2]
        psd = hashlib.md5(psd.encode()).hexdigest()
        print("passwd md5:", psd)
        with open('%s/data.db' % settings.USER_DATA, 'r+') as f:
            data = json.load(f)
            data[user] = str(psd)
            f.seek(0)
            f.truncate(0)  # clear content
            json.dump(data,f)
            print("add user %s successfully!" % user)
            self.request.send(b'successfully!')

    def login(self):
        '''
        interact with user while login,if success,set User
        :return:
        '''
        self.request.send(b'Please input username:')
        user = self.request.recv(1024).decode()
        self.request.send(b'Please input password:')
        psd = self.request.recv(1024).decode()
        with open('%s/data.db' % settings.USER_DATA, 'r') as f:
            date = json.load(f)
            if date.get(user):
                if psd == date[user]:
                    print("client [%s] has login..." % self.client_address[0])
                    self.request.send(b'success')
                    self.User = user
                    logging.info('user [%s] login...'%user)
                    return True
                else:
                    self.request.send(b'Incorrect username or password!')  # failed to login
                    logging.info('user [%s] login failed!'%user)
            else:
                self.request.send(b'Incorrect username or password!')  # failed to login
                logging.info('user [%s] login failed!' % user)
            return False

    def logout(self):
        '''
        request of logout by client,set None User.
        :return:
        '''
        logging.info('user [%s] logout'%self.User)
        self.User = '' #clear user
        # self.request.send(b'logout...')
        self.request.close()


if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer((settings.ADDR, settings.PORT), MyTCPHandler)
    server.serve_forever(poll_interval=0.5)
    server.server_close()
