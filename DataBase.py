from datetime import datetime
import os

class DateBase():
    def __init__(self):
        with open("database.txt") as db:
            self.date = db.readline()


    def insert(self, dict_name_uid):
        new_date = datetime.today().strftime("%d-%m-%Y")
        self.dict_name_len = {}
        if not self.date:
            with open("database.txt","rw") as db:
                db.write(f"{new_date}\n")
                for k,v in dict_name_uid.items():
                    db.write(f"{k} {','.join(v)}\n")
                    self.dict_name_len[k] = len(v)
        else:
            with open("database.txt","rw") as db:
                with open( "database1.txt", "w") as db1:
                    db = db.readlines()[1:]
                    db1.writte(f"{new_date}\n")
                    for row in db:
                        list_row =row.split()
                        set_uids = {*(dict_name_uid.get(list_row[0],[]) + list_row[1].split(","))}
                        self.dict_name_len[list_row[0]] = len(set_uids)
                        db1.write(f"{row[0]} {','.join(set_uids)}\n")
            os.remove("database.txt")
            os.rename("database1.txt","database.txt")
        self.dict_name_len = {sorted(self.dict_name_len.items(), key=lambda x:x[1],reverse=True)}

    def removed(self, dict_keys):
        if not dict_keys: return
        del_uids=[]
        dict_name_len = {}
        with open("database.txt") as db:
            with open("database1.txt", "w") as db1:
                 db1.write(db.readline())
                 while True:
                    row = db.readline()
                    if not row: break
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
           os.remove("database1.txt")
           self.mail = None
           return
        """
        os.remove("database.txt")
        os.rename("database1.txt","database.txt")
        self.dict_name_len = {sorted(dict_name_len.items(), key=lambda x:x[1],reverse=True)}

obj_db = DateBase()
        