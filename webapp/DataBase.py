from datetime import datetime
import os
import webapp.request_imap

class DataBase():
    def __init__(self):
        with open("database.txt","a+") as db:
            db.seek(0,0)
            self.all_db = db.readlines()
    
    def select(self):
       return None if not self.all_db else self.all_db[0].strip()
        
    def insert(self, dict_name_uid):
        self.new_date = datetime.today().strftime("%d-%b-%Y")
        self.dict_name_len = {}
        d = dict(i.split() for i in self.all_db[1:])
        self.dict_db = {k:v.split(',') for k,v in d.items()}
        for k,v in dict_name_uid.items():
            self.dict_db[k] = {*(self.dict_db.get(k,[])+v)}
        with open("database.txt","w+") as db:
            db.write(f"{self.new_date}\n")
            for k,v in self.dict_db.items():
                db.write(f"{k} {','.join(v)}\n")
                self.dict_name_len[k] = len(v)
        self.dict_name_len = dict(sorted(self.dict_name_len.items(), key=lambda x:x[1],reverse=True))
        
    def delete(self, dict_keys, mail):
        self.mail = mail
        if not dict_keys: return
        del_uids=[]
        dict_name_len = {}
        with open("db1.txt", "w") as db1:
            db1.write(f"{self.new_date}\n")
            for k,v in self.dict_db.items():
                if k in dict_keys:
                    del_uids += [i.encode() for i in v]
                else:
                    dict_name_len[k] = len(v)
                    db1.write(f"{k} {','.join(v)}\n")
        try:   
            webapp.request_imap.delete(del_uids, mail)
        except:
            os.remove("db1.txt")
            self.mail = None
            return
        [self.dict_db.pop(i) for i in dict_keys]
        os.remove("database.txt")
        os.rename("db1.txt","database.txt")
        self.dict_name_len = dict(sorted(dict_name_len.items(),key=lambda x:x[0],reverse=True))

"""
#os.remove("database.txt")       
dict_name = {"мама":["1","2"],"папа":["3","4"],"яша":["5","6"]}
obj_db = DataBase()
date = obj_db.select()
print(date)
obj_db.insert({"f":["1","2"],"a":["3","5"]})
obj_db.delete({"a"})
"""