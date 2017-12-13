import re,os,pickle
from conf import settings
from modules import log

def ck_command():
    '''
    check choice ,if it is available ,return command
    :return:
    '''
    while True:
        choice = input("Input:").strip()
        if choice:
            choice = re.sub(" +"," ",choice)
            return choice
        else:
            print("Please input!")
def login():
    '''
    run when user login,return user data
    :return:
    '''
    all_users=os.listdir(settings.USER_DATA)
    while True:
        user=input("Input username:").strip()
        if user == 'q':
            return None
        psd=input("Input password:").strip()

        if user in all_users:
            with open("%s/%s"%(settings.USER_DATA,user),'rb') as f:
                data = pickle.load(f)
            if psd == data["passwd"]:
                log.logger("access").info("User %s login."%user)
                return data
            else:
                print("Incorrect passwd!")
                log.logger("access").info("User %s failed login." % user)
        else:
            print("No such user!")
            log.logger("access").info("Unknown user %s failed login." % user)
def sign_up(name,psd,role):
    '''
    run when sign up
    :param name: username
    :param psd: passwd
    :param role: '1' or '0'
    :return:
    '''
    with open("%s/%s"%(settings.USER_DATA,name),'wb') as f:
        data =dict(name=name,passwd=psd,role=role)
        pickle.dump(data,f)
        log.logger("userEvents").info("Create user :" ,name)
