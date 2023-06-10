import mysql.connector as mysql
from datetime import datetime

class Schedule():

    def __init__( self ):
        # class attributes
        self.HOST = "localhost"
        self.DATABASE = "medtest01"
        self.USER = "root"
        self.PASSWORD = "123456"
        self.all_schedule={}
        # connecting to database
        mydb = mysql.connect( host=self.HOST, 
                              database=self.DATABASE, 
                              user=self.USER, 
                              password=self.PASSWORD )
        print( "Connected to:", mydb.get_server_info() )
        self.cursor = mydb.cursor()
        self.cursor.execute( """SELECT medapp_elder.IDN, 
                                    medapp_schedule.breakfast, 
                                    medapp_schedule.lunch, 
                                    medapp_schedule.dinner, 
                                    medapp_schedule.night 
                                FROM medtest01.medapp_schedule 
                                INNER JOIN medtest01.medapp_elder 
                                WHERE medapp_elder.id=medapp_schedule.elder_id_id;""")
        rows = self.cursor.fetchall()
        for x in rows:
            timetable_list = []
            timetable_list.append(x[1])
            timetable_list.append(x[2])
            timetable_list.append(x[3])
            timetable_list.append(x[4])
            self.all_schedule[x[0]] = timetable_list
        # print(self.all_schedule)  # see all data
        # print(type(self.all_schedule))
        # print(self.all_schedule["1160101720685"][0])  #can be {} or {"time": "07:00", "after": {"metformin": "2"}, "before": {}}
     

    def check_data(self , idn):
        if idn in self.all_schedule.keys():
            print("have data")
            # เช็คเวลาว่าควรเป็นมื้อเช้ากลางวันหรือเย็น แล้วมาเทียบว่ามีข้อมูลไหมในตารางทานยา
            now_time = datetime.now()
            # print(now_time)
            breakfast_time = now_time.replace(hour=10, minute=30, second=0, microsecond=0) #ก่อน 10.30   # ตี5-10โมงครึ่ง +5.3
            lunch_time = now_time.replace(hour=14, minute=0, second=0, microsecond=0) #ก่อน 14.00        # 11โมง - บ่ายสอง +2.3
            dinner_time = now_time.replace(hour=20, minute=00, second=0, microsecond=0) #ก่อน 20.00       # 4โมงเย็น - 1 หุ่มครึ่ง +3.3
            # night_time = now_time.replace(hour=23, minute=0, second=0, microsecond=0) #ก่อน 23.00        # 2ทุ่ม - 5 ทุ่ม +3
            # z = now_time.replace(hour=20, minute=00, second=0, microsecond=0) # for test
            if now_time <= breakfast_time :
                print("breakfast time")
                return(0)
            elif now_time <= lunch_time :
                print("lunch time")
                return(1)
            elif now_time <= dinner_time :
                print("dinner time")
                return(2)
            elif now_time > dinner_time :
                print("night time")
                return(3)
            else :
                print("not time")
                return("no")
        else:
            print("no data")
            return("no")
        
    def check_meal(self, idn,  meal):
        if len(self.all_schedule[idn][meal]) > 2 :
            print(self.all_schedule[idn][meal])
            # a = self.all_schedule[idn][meal]
            # b = eval(a)  
            # print(b, type(b))
            return eval(self.all_schedule[idn][meal])
        else:
            print("no meal")
            return("no meal")
        
