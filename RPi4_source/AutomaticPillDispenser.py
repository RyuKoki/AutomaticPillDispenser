import tkinter as tk
from FaceRecognition import FaceRecognition
from ThaiSCard import ThaiSCard
from Schedule import Schedule
from History import History
from Medicine import Medicine
from MQTTclient import MQTTclient
from datetime import datetime, timedelta
from detectpill import camera
import tts_sound
import serial
import time
import threading

class PillDispenserGUI():

    def __init__( self ):
        self.win = tk.Tk()
        self.win.geometry("600x400")
        self.win.resizable(0, 0)
        self.win.title('Automatic Pill Dispenser')
        self.GUI = tk.Frame(self.win)
        self.GUI.pack()
        self.IDNumber = ''
        self.face_code = ''
        self.all_id = []
        self.open()
        self.win.mainloop()

    def open( self ):
        for widgets in self.GUI.winfo_children():
            widgets.destroy()
        cam_button = tk.Button( self.GUI, text="Open Camera", command=self.find_IDN, font=("Arial", 16) )
        quit_button = tk.Button( self.GUI, text="Quit", command=self.win.destroy, font=("Arial", 16) )
        cam_button.pack(anchor="center", ipadx=5, ipady=5, pady=10)
        quit_button.pack(anchor="center", ipadx=5, ipady=5)

    def find_IDN( self ):
        face_recog = FaceRecognition()
        self.all_id = face_recog.all_id()
        tts_sound.opencamera()
        msg_fake = ""
        fake_label = tk.Label(self.GUI, text=msg_fake, font=("Arial", 20))
        fake_label.pack(anchor="center", ipadx=5, ipady=5, padx=5, pady=5)
        fake_label.after(5000)
        self.face_code = face_recog.find_facecode()
        self.IDNumber = face_recog.face_detrog(self.face_code)[0]
        if self.IDNumber != '' :
            # have data
            print("have data")
            for widgets in self.GUI.winfo_children():
                widgets.destroy()
            # msg_IDCard = "พบใบหน้าในฐานข้อมูล"
            msg_IDCard = "ยินดีต้อนรับคุณ {}!".format(face_recog.face_detrog(self.face_code)[1])
            msg_label = tk.Label( self.GUI, text=msg_IDCard, font=("Arial", 24), fg='#008000' )
            msg_label.pack(anchor="center", ipadx=5, ipady=5, padx=5, pady=5)
            msg_IDCard2 = "กรุณายืนยันตัวตนด้วยบัตรประชาชนอีกรอบ"
            msg_label2 = tk.Label( self.GUI, text=msg_IDCard2, font=("Arial", 20) )
            msg_label2.pack(anchor="center", ipadx=5, ipady=5, padx=5, pady=5)
            msg_label.after(3000, self.checking_ID)
            # msg_label.after(3000, self.checking_ID("a"))
        else :
            # no data
            print("no data")
            for widgets in self.GUI.winfo_children():
                widgets.destroy()
            msg_IDCard = "ไม่พบใบหน้าในฐานข้อมูล"
            msg_label = tk.Label( self.GUI, text=msg_IDCard, font=("Arial", 20), fg='#ff0000' )
            msg_label.pack(anchor="center", ipadx=5, ipady=5, padx=5, pady=5)
            msg_IDCard2 = "กรุณายืนยันตัวตนผ่านบัตรประชาชน"
            msg_label2 = tk.Label( self.GUI, text=msg_IDCard2, font=("Arial", 20) )
            msg_label2.pack(anchor="center", ipadx=5, ipady=5, padx=5, pady=5)
            msg_label.after(3000, self.checking_ID)
            # msg_label.after(3000, self.checking_ID("b"))

    def checking_ID( self ):
        scard_status = False
        try:
            thai_scard = ThaiSCard()
            scard_status = True
        except:
            pass
        
        if scard_status == True :
            if self.IDNumber != '' :    #  have face in face recog
                # print("1 state")
                if self.IDNumber == thai_scard.ID():
                    for widgets in self.GUI.winfo_children():
                        widgets.destroy()
                    # self.open()
                    tts_sound.welcome(thai_scard.fullname())
                    msg_IDCard = "ข้อมูลใบหน้าและบัตรประชาชนถูกต้อง"
                    msg_label = tk.Label( self.GUI, text=msg_IDCard, font=("Arial", 20), fg='#008000' )
                    msg_label.pack(anchor="center", ipadx=5, ipady=5, padx=5, pady=5)
                    # tts_sound.welcome(thai_scard.fullname())
                    msg_label.after(9000)
                    msg_label.after(1000, self.checking_schedule, self.IDNumber)
                else:
                    for widgets in self.GUI.winfo_children():
                        widgets.destroy()
                    # self.open()
                    msg_IDCard = "ข้อมูลใบหน้าและบัตรประชาชนไม่ถูกต้อง"
                    msg_label = tk.Label( self.GUI, text=msg_IDCard, font=("Arial", 20), fg='#ff0000' )
                    msg_label.pack(anchor="center", ipadx=5, ipady=5, padx=5, pady=5)
                    tts_sound.start("error")
                    msg_label.after(3000, self.open)
            else :        #  no face in face recog
                # print("2 state")
                if thai_scard.ID() in self.all_id :
                    for widgets in self.GUI.winfo_children():
                        widgets.destroy()
                    # self.open()
                    tts_sound.welcome(thai_scard.fullname())
                    msg_IDCard = "พบเลขบัตรประชาชนของท่านในฐานข้อมูล"
                    msg_label = tk.Label( self.GUI, text=msg_IDCard, font=("Arial", 20), fg='#008000' )
                    msg_label.pack(anchor="center", ipadx=5, ipady=5, padx=5, pady=5)
                    # tts_sound.welcome(thai_scard.fullname())
                    msg_label.after(9000)
                    msg_label.after(1000, self.checking_schedule, thai_scard.ID())
                else:
                    for widgets in self.GUI.winfo_children():
                        widgets.destroy()
                    # self.open()
                    msg_IDCard = "ไม่พบข้อมูลของท่านในฐานข้อมูล"
                    msg_label = tk.Label( self.GUI, text=msg_IDCard, font=("Arial", 20), fg='#ff0000' )
                    msg_label.pack(anchor="center", ipadx=5, ipady=5, padx=5, pady=5)
                    tts_sound.start("error")
                    msg_label.after(3000, self.open)
        else:
            for widgets in self.GUI.winfo_children():
                widgets.destroy()
            tts_sound.start("card")
            msg_IDCard = "กรุณาเสียบบัตรประชาชนของท่าน"
            msg_label = tk.Label( self.GUI, text=msg_IDCard, font=("Arial", 20), fg='#ff0000' )
            msg_label.pack(anchor="center", ipadx=5, ipady=5, padx=5, pady=5)
            msg_label.after(5000, self.checking_ID)

    def checking_schedule( self , idn):
        sche = Schedule()
        data = sche.check_data(idn)
        meal = None 
        if data != "no":
            # มีข้อมูลอยู่ใน table
            meal = sche.check_meal(idn, data)
            if meal != "no meal":
                now = datetime.now()
                hour = int(meal['time'][:2])
                mins = int(meal['time'][3:])
                time = now.replace(hour=hour, minute=mins, second=0, microsecond=0)
                history = History()
                time_history = history.read(idn)
                if (len(meal['before'])!=0) and (len(meal['after'])!=0):
                    """กรณีที่ 1 มีตารางการกินยา ก่อน และ หลัง"""
                    if time_history != False:
                        if len(time_history) == 2:
                            """กรณีที่ 1 มีล่าสุด 2 records"""
                            start = time_history[1][1]
                            # print(start)
                            stop = time_history[0][1]
                            # print(stop)
                            # print(time-timedelta(minutes=30))
                            if ((time-timedelta(minutes=30)) <= start <= (time+timedelta(minutes=30))):
                                """1.1 start อยู่ในช่วงมื้ออาหาร"""
                                print("ไม่จ่ายยา1")
                                self.pill_dispense(idn,meal,"none")
                                
                            elif ((time-timedelta(minutes=30)) <= stop <= (time+timedelta(minutes=30))):
                                """1.2.1 start ไม่อยู่ และ stop อยู่ก่อนอาหาร"""
                                # print("ต้องกินยาหลังอาหาร")
                                if ((time+timedelta(minutes=30)) <= now <= (time+timedelta(hours=1,minutes=30))):
                                    print("จ่ายยาหลังอาหาร1")
                                    self.pill_dispense(idn,meal,"after")
                                else:
                                    print("ไม่จ่ายยา2")
                                    self.pill_dispense(idn,meal,"none")
                            elif ((time+timedelta(minutes=30)) <= stop <= (time+timedelta(hours=1,minutes=30))):
                                """1.2.2 start ไม่อยู่ และ stop อยู่หลังอาหาร"""
                                print("ไม่จ่ายยา3")
                                self.pill_dispense(idn,meal,"none")
                            elif ((time-timedelta(minutes=30)) >= stop):
                                """1.3 start และ stop ไม่อยู่"""
                                # print("ต้องกินยาก่อนอาหาร")
                                if ((time-timedelta(minutes=30)) <= now <= (time+timedelta(minutes=30))):
                                    print("จ่ายยาก่อนอาหาร1")
                                    self.pill_dispense(idn,meal,"before")
                                elif ((time+timedelta(minutes=30)) <= now <= (time+timedelta(hours=1,minutes=30))):
                                    print("จ่ายยาหลังอาหาร2")
                                    self.pill_dispense(idn,meal,"after")
                                else:
                                    print("ไม่จ่ายยา4")
                                    self.pill_dispense(idn,meal,"none")
                            else:
                                print('ไม่จ่ายยา5 กรณี stop อยู่ในช่วงมื้ออาหารแต่ไม่อยู่ในเวลาจ่ายยา')
                                self.pill_dispense(idn,meal,"none")
                        else:
                            stop = time_history[0][1]
                            if ((time-timedelta(minutes=30)) <= stop <= (time+timedelta(minutes=30))):
                                """2.1 stop อยู่ในช่วงเวลาก่อนอาหาร"""
                                # print("จ่ายยาหลังอาหาร")
                                if ((time+timedelta(minutes=30)) <= now <= (time+timedelta(hours=1,minutes=30))):
                                    print("จ่ายยาหลังอาหาร3")
                                    self.pill_dispense(idn,meal,"after")
                                else:
                                    print("ไม่จ่ายยา6")
                                    self.pill_dispense(idn,meal,"none")
                            elif ((time+timedelta(minutes=30)) <= stop <= (time+timedelta(hours=1,minutes=30))):
                                """2.3 stop อยู่ในช่วงหลังอาหาร"""
                                print("ไม่จ่ายยา7")
                                self.pill_dispense(idn,meal,"none")
                            elif ((time-timedelta(minutes=30)) >= stop):
                                """2.2 stop ไม่อยู่ในช่วงเวลาก่อนอาหาร"""
                                # print("จ่ายยาก่อนอาหาร")
                                if ((time-timedelta(minutes=30)) <= now <= (time+timedelta(minutes=30))):
                                    print("จ่ายยาก่อนอาหาร2")
                                    self.pill_dispense(idn,meal,"before")
                                elif ((time+timedelta(minutes=30)) <= now <= (time+timedelta(hours=1,minutes=30))):
                                    print("จ่ายยาหลังอาหาร4")
                                    self.pill_dispense(idn,meal,"after")
                                else:
                                    print("ไม่จ่ายยา8")
                                    self.pill_dispense(idn,meal,"none")
                            else:
                                print("ไม่จ่ายยา9 กรณี stop เกินเวลาหลังอาหาร")
                                self.pill_dispense(idn,meal,"none")
                    else:
                        print("ไม่มี record มาก่อน")
                        # คิดกรณีเวลาปัจจุบันกับมื้ออาหาร
                        if ((time-timedelta(minutes=30)) <= now <= (time+timedelta(minutes=30))):
                            print("จ่ายยาก่อนอาหาร3")
                            self.pill_dispense(idn,meal,"before")

                        elif ((time+timedelta(minutes=30)) <= now <= (time+timedelta(hours=1,minutes=30))):
                            print("จ่ายยาหลังอาหาร5")
                            self.pill_dispense(idn,meal,"after")
                        else:
                            print("ไม่จ่ายยา10")
                            self.pill_dispense(idn,meal,"none")

                
                elif len(meal['before']) != 0 :
                    # กรณีมียาก่อนอาหารอย่างเดียว
                    if time_history != False:
                        # have record
                        stop = time_history[0][1]
                        if ((time-timedelta(minutes=30)) <= stop <= (time+timedelta(minutes=30))):
                            print("ไม่จ่ายยา11")
                            self.pill_dispense(idn,meal,"none")
                        elif ((time-timedelta(minutes=30)) <= now <= (time+timedelta(minutes=30))):
                            print("จ่ายยาก่อนอาหาร4")
                            self.pill_dispense(idn,meal,"before")
                        else:
                            print("ไม่จ่ายยา12")
                            self.pill_dispense(idn,meal,"none")
                    else :
                        if ((time-timedelta(minutes=30)) <= now <= (time+timedelta(minutes=30))):
                            print("จ่ายยาก่อนอาหาร5")
                            self.pill_dispense(idn,meal,"before")
                        else:
                            print("ไม่จ่ายยา13")
                            self.pill_dispense(idn,meal,"none")

                elif len(meal['after']) != 0 :
                    # กรณีมียาหลังอาหารอย่างเดียว
                    if time_history != False:
                        # have record
                        stop = time_history[0][1]
                        if ((time+timedelta(minutes=30)) <= stop <= (time+timedelta(hours=1,minutes=30))):
                            print("ไม่จ่ายยา14")
                            self.pill_dispense(idn,meal,"none")
                        elif ((time+timedelta(minutes=30)) <= now <= (time+timedelta(hours=1,minutes=30))):
                            print("จ่ายยาหลังอาหาร6")
                            self.pill_dispense(idn,meal,"after")
                        else:
                            print("ไม่จ่ายยา15")
                            self.pill_dispense(idn,meal,"none")
                    else :
                        if ((time+timedelta(minutes=30)) <= now <= (time+timedelta(hours=1,minutes=30))):
                            print("จ่ายยาหลังอาหาร7")
                            self.pill_dispense(idn,meal,"after")
                        else:
                            print("ไม่จ่ายยา16")
                            self.pill_dispense(idn,meal,"none")
                else:
                    print("ไม่มีมื้อก่อน/หลัง")
                    self.pill_dispense(idn,meal,"none")             
            else :
                # ไม่มีตารางการทานยาในมื้อนั้น ให้แสดงข้อมูล x 
                print("no timetable")
                self.pill_dispense(idn,meal,"none")
        else :
            # ไม่มีข้อมูลตารางการทานยา ให้แสดงข้อมูล x 
            print("no data")
            self.pill_dispense(idn,meal,"none")

    def pill_dispense(self,idn,meal,state):
        med = None
        eat = []
        medicine = Medicine()
        if state == "before":
            # state ก่อนอาหาร
            # print("id : ",idn," meal : ",meal," state : ",state)
            med = meal[state]   # ยาที่ต้องทาน {'metformin': '1'}
            for i in med:
                x = []
                x.append(i)
                x.append(med[i])
                eat.append(x)
            # print(eat)    
            pill = medicine.check_pill(eat)
            if pill != "not":
                print(pill) # { slot : total }  เอาไปสั่งจ่ายยา
                tts_sound.run(state)
                # # คำสั่งจ่ายยา
                all_slots = list(pill.keys())
                for slot in all_slots:
                    if slot == 1:
                        ser = serial.Serial(port='/dev/serial0', baudrate=115200, timeout=1)
                        ser.reset_input_buffer()
                        now = time.time()
                        is_sent = 0
                        while True:
                            # send_dt = str(pill[slot]) + " start\n"
                            # ser.write(send_dt.encode())
                            line = ser.readline().decode('utf-8', errors='ignore')
                            if "recv" in line and is_sent == 1:
                                # กำลังทำการจ่ายยาค่ะ
                                print(line)
                                break
                            elif is_sent == 0:
                                send_dt = str(pill[slot]) + " start\n"
                                ser.write(send_dt.encode())
                                print("pills are sent")
                                is_sent = 1
                            if time.time() > now + 5:
                                print("timeout more than 5 sec")
                                break
                    else:
                        print("send by mqtt")
                self.detect_pill(idn,med)
            else:
                print("ไม่จ่ายยา")
                tts_sound.run("no")
        
        elif state == "after":
            # state หลังอาหาร
            # print("id : ",idn," meal : ",meal," state : ",state)
            med = meal[state]
            for i in med:
                x = []
                x.append(i)
                x.append(med[i])
                eat.append(x)
            # print(eat)    # ยาที่ต้องทาน
            pill = medicine.check_pill(eat)
            if pill != "not":
                print(pill) 
                tts_sound.run(state)
                # # คำสั่งจ่ายยา
                all_slots = list(pill.keys())
                for slot in all_slots:
                    if slot == 1:
                        ser = serial.Serial(port='/dev/serial0', baudrate=115200, timeout=1)
                        ser.reset_input_buffer()
                        now = time.time()
                        is_sent = 0
                        while True:
                            # send_dt = str(pill[slot]) + " start\n"
                            # ser.write(send_dt.encode())
                            line = ser.readline().decode('utf-8', errors='ignore')
                            if "recv" in line and is_sent == 1:
                                # กำลังทำการจ่ายยาค่ะ
                                print(line)
                                break
                            elif is_sent == 0:
                                send_dt = str(pill[slot]) + " start\n"
                                ser.write(send_dt.encode())
                                print("pills are sent")
                                is_sent = 1
                            if time.time() > now + 5:
                                print("timeout more than 5 sec")
                                break
                    else:
                        print("send by mqtt")
                # # จ่ายยาเสร็จแล้ว รอตรวจสอบ
                self.detect_pill(idn,med)
            else:
                print("ไม่จ่ายยา")
                tts_sound.run("no")

        elif state == "none":
            # ไม่มียาต้องทาน
            print("ไม่จ่ายยา")
            tts_sound.run("no")
        else :
            # กรณีเงื่อนไขอื่นๆ ให้ทำเหมือนไม่มียาต้องทาน
            print("ไม่จ่ายยา")
            tts_sound.run("no")
        for widgets in self.GUI.winfo_children():
            widgets.destroy()
        msg = ""
        msg_label = tk.Label( self.GUI, text=msg, font=("Arial", 20) )
        msg_label.pack(anchor="center", ipadx=5, ipady=5, padx=5, pady=5)
        msg_label.after(5000, self.open)


    def detect_pill(self,id,meal):
        d_time = datetime.now().strftime("%Y_%m_%d-%H_%M")
        dispense = camera.verify_pill(id+"/"+d_time)
        if dispense != "X":
            # check meal = dispense ไหม ตามจำนวนสมาชิก dict
            if meal == dispense :
                tts_sound.custom("การจ่ายยาเสร็จสมบูรณ์ กรุณารับยาได้เลยค่ะ")
                # บันทึกประวัติ
                his = History()
                his.create(id,'History/{}/{}/{}'.format(id,d_time,"test.jpg"))
            else:
                tts_sound.custom("การจ่ายยาผิดพลาดกรุณาติดต่อเจ้าหน้าที่")
        else :
            # error for dispense call caretaker
            tts_sound.custom("การจ่ายยาผิดพลาดกรุณาติดต่อเจ้าหน้าที่")


GUI = PillDispenserGUI()
