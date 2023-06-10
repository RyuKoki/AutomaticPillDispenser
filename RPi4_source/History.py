import mysql.connector as mysql
from datetime import datetime

class History():

    def __init__(self):
        # class attributes
        self.HOST = "localhost"
        self.DATABASE = "medtest01"
        self.USER = "root"
        self.PASSWORD = "123456"
        # connecting to database
        self.mydb = mysql.connect( host=self.HOST, 
                              database=self.DATABASE, 
                              user=self.USER, 
                              password=self.PASSWORD )
        # print( "Connected to:", mydb.get_server_info() )
        # self.cursor = mydb.cursor(buffered=True)

    def create(self, IDN):
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute("""SELECT id FROM medtest01.medapp_elder WHERE IDN=%s""", (IDN, ))
        elder_id = cursor.fetchone()[0]
        # cursor.close()
        # print(elder_id, type(elder_id))
        cursor.execute("""INSERT INTO medtest01.medapp_history(time,med_picture,elder_id_id)
                            VALUES (%s, %s, %s)""",(datetime.now(),'web_app/file_upload/Pill/Gemfibrozil_300mg.jpg',elder_id))
        self.mydb.commit()
    
    def read(self, IDN):
        cursor = self.mydb.cursor(buffered=True)
        cursor.execute("""SELECT id FROM medtest01.medapp_elder WHERE IDN=%s""", (IDN, ))
        elder_id = cursor.fetchone()[0]

        cursor.execute("""SELECT * FROM medtest01.medapp_history WHERE elder_id_id=%s order by id desc limit 2""", (elder_id, ))
        elder_allhis = cursor.fetchall()
        # print(elder_allhis)
        if elder_allhis == []:
            return False
        else:
            return elder_allhis
