# ************************** first way **************************

# from playsound import playsound
# import os
# from gtts import gTTS
# import time

# tts = gTTS('สวัสดีค่ะ คุณสุภิญญา วันนี้ไม่มียาที่ต้องรับประทานนะคะ', lang='th')
# tts.save('name2.mp3')
# playsound('name2.mp3')
# time.sleep(20)
# os.remove('name2.mp3')


# ************************** second way **************************
from gtts import gTTS
from io import BytesIO
from pygame import mixer
import time

# ---------------------------- status eat med ---------------------------------
def speakno():
    bt = BytesIO()
    tts = gTTS('ขณะนี้ไม่มียาที่ต้องรับประทานค่ะ', lang='th')
    tts.write_to_fp(bt)
    return (bt)

def speakbefore():
    bt = BytesIO()
    tts = gTTS('ขณะนี้มียาก่อนอาหาร กรุณารอรับยาก่อนอาหารด้วยค่ะ', lang='th')
    tts.write_to_fp(bt)
    return (bt)

def speakafter():
    bt = BytesIO()
    tts = gTTS('ขณะนี้มียาหลังอาหาร กรุณารอรับยาหลังอาหารด้วยค่ะ', lang='th')
    tts.write_to_fp(bt)
    return (bt)

def run(status):
    mixer.init()
    if status == "before":
        sound = speakbefore()
    elif status == "after":
        sound = speakafter()
    else:
        sound = speakno()
    
    sound.seek(0)
    mixer.music.load(sound)
    mixer.music.play()

# ---------------------------- camera ---------------------------------
def speakcam():
    bt = BytesIO()
    tts = gTTS('ยินดีต้อนรับสู่ Doctor med กรุณามองกล้องเพื่อประมวลผล', lang='th')
    tts.write_to_fp(bt)
    return (bt)

def opencamera():
    mixer.init()
    sound = speakcam()
    sound.seek(0)
    mixer.music.load(sound)
    mixer.music.play()

# ---------------------------- id card ---------------------------------

def speakcard():
    bt = BytesIO()
    tts = gTTS('กรุณาเสียบบัตรประชาชน', lang='th')
    tts.write_to_fp(bt)
    return (bt)

def speakerror():
    bt = BytesIO()
    tts = gTTS('ขออภัยค่ะ ข้อมูลของท่านไม่ถูกต้องกรุณาลองใหม่อีกครั้ง', lang='th')
    tts.write_to_fp(bt)
    return (bt)

def start(x):
    mixer.init()
    if x == "card":
        sound = speakcard()
    else:
        sound = speakerror()
    sound.seek(0)
    mixer.music.load(sound)
    mixer.music.play()

# ---------------------------- hello ---------------------------------

def speakwelcome(name):
    bt = BytesIO()
    tts = gTTS('สวัสดีค่ะ คุณ {} กรุณารอสักครู่ระบบกำลังประมวลผล'.format(name), lang='th')
    tts.write_to_fp(bt)
    return (bt)

def welcome(y):
    mixer.init()
    sound = speakwelcome(y["first_name"])
    sound.seek(0)
    mixer.music.load(sound)
    mixer.music.play()
    # time.sleep(10)
# --------------------------- custom ------------------------

def speakcustom(data):
    bt = BytesIO()
    tts = gTTS('{}'.format(data), lang='th')
    tts.write_to_fp(bt)
    return (bt)

def custom(data):
    mixer.init()
    sound = speakcustom(data)
    sound.seek(0)
    mixer.music.load(sound)
    mixer.music.play()
