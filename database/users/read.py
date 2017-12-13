import os,hashlib,json
with open("data.db",'w',encoding='utf-8') as f:
    md5=hashlib.md5('123456'.encode())
    value = md5.hexdigest()
    admin = dict(admin=value)
    json.dump(admin,f)
# os.makedirs("D:/myProject/SimpleFTP/new")
