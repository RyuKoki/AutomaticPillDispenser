import mysql.connector as mysql

class Medicine():

    def __init__( self ):
        # class attributes
        self.HOST = "localhost"
        self.DATABASE = "medtest01"
        self.USER = "root"
        self.PASSWORD = "123456"
        self.all_name = []
        self.all_slot = []
        self.all_amount = []
        # self.all_med = []
        # connecting to database
        self.mydb = mysql.connect( host=self.HOST, 
                              database=self.DATABASE, 
                              user=self.USER, 
                              password=self.PASSWORD )
        # print( "Connected to:", mydb.get_server_info() )
        cursor = self.mydb.cursor()
        cursor.execute( """SELECT slot , generic_name , amount
                                FROM medtest01.medapp_infomed ;""")
        rows = cursor.fetchall()
        for x in rows:
            self.all_name.append(x[1])
            self.all_slot.append(x[0])
            self.all_amount.append(x[2])
        # print(self.all_name,self.all_slot,self.all_amount)

    def check_pill(self,medi):
        # print(medi)     # [['metformin', '1'], ['Paracetamol_500mg', '2']]
        status = []
        dispense = {}
        for m in medi :
            id_med = self.all_name.index(m[0])
            if self.all_amount[id_med] >= int(m[1]):
                status.append("ok")# มียาเพียงพอ
                dispense[self.all_slot[id_med]] = int(m[1])
            else:   
                status.append("not")# ยาไม่พอ
        # print(status)
        # print(dispense)
        if "not" not in status :
            # print("จ่ายยา")
            # update pill amount
            for pill in medi:
                id_pill = self.all_name.index(pill[0])
                amount = self.all_amount[id_pill] - int(pill[1])
                slot = self.all_slot[id_pill]
                # print(amount)
                # print(slot)
                cursor = self.mydb.cursor()
                cursor.execute( """UPDATE medtest01.medapp_infomed 
                                        SET amount = %s 
                                        WHERE slot = %s ;""", (amount,slot,))
                self.mydb.commit()
            return(dispense)
        else :
            # print("ไม่จ่ายยา")
            return("not")
