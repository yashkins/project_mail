from datetime import datetime
import os

class DataBase():
    def __init__(self):
        with open("database.txt","a+") as db:
            db.seek(0,0)
            self.all_db = db.readlines()
    
    def select(self):
       return None if not self.all_db else obj_db.all_db[0].strip()
        
    def insert(self, dict_name_uid):
        new_date = datetime.today().strftime("%d-%m-%Y")
        self.dict_name_len = {}
        d=dict(i.split() for i in self.all_db[1:])
        dict_db = {k:v.split(',') for k,v in d.items()}
        for k,v in dict_name_uid.items():
            dict_db[k] = {*(dict_db.get(k,[])+v)}
        with open("database.txt","w") as db:
            db.write(f"{new_date}\n")
            for k,v in dict_db.items():
                db.write(f"{k} {','.join(v)}\n")
                self.dict_name_len[k] = len(v)
        self.dict_name_len = dict(sorted(self.dict_name_len.items(), key=lambda x:x[1],reverse=True))
        
    def delete(self,dict_keys):
        self.mail = 1
        if not dict_keys: return
        del_uids=[]
        dict_name_len = {}
        with open("db1.txt", "w") as db1:
            db1.write(self.all_db[0])
            for row in self.all_db[1:]:
                list_row = row.split()
                if list_row[0] in dict_keys:
                    del_uids += [i.encode for i in list_row[1].split(",")]
                else:
                    dict_name_len[list_row[0]] = len(list_row[1].split(","))
                    db1.write(row)
        """
        try:
            delete(del_uids)
        except:
           os.remove("db1.txt")
           self.mail = None
           return 
        """
        os.remove("database.txt")
        os.rename("db1.txt","database.txt")
        self.dict_name_len = dict(sorted(dict_name_len.items(),key=lambda x:x[0],reverse=True))

#os.remove("database.txt")       
dict_name = {"мама":["1","2"],"папа":["3","4"],"яша":["5","6"]}
obj_db = DataBase()
date = obj_db.select()
print(date)
obj_db.insert({"f":["1","2"],"a":["3","5"]})
obj_db.delete({"a"})
