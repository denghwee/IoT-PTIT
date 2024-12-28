import datetime
import speech_recognition as sr
import pyfirmata2
import time
import datetime
import io
import webbrowser as wb
import subprocess
import pyjokes
import pygame
from gtts import gTTS

board = pyfirmata2.Arduino('COM3')

def speak(audio):
    tts = gTTS(text=audio, lang='vi')
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_fp, 'mp3')
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        continue


def time():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(time)


def date():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    date = datetime.datetime.now().day

    speak("the current date is")
    speak(date)
    speak(month)
    speak(year)

def open_chrome():
    speak('mở chrome')
    url = "https://www.google.co.in/"
    chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe %s"
    wb.get(chrome_path).open(url)

def open_portfolio():
    speak('mở portfolio')
    url = "https://sureshkonar.github.io/suresh-portfolio-heroku/"
    chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe %s"
    wb.get(chrome_path).open(url)

def wishme():
    speak("welcome back sir")
    hour = datetime.datetime.now().hour

    if hour >= 6 and hour <= 12:
        speak("Chào buổi sáng")
    elif hour >= 12 and hour <= 18:
        speak("Chào buổi chiều")
    elif hour >= 18 and hour <= 21:
        speak("Chào buổi tối")
    else:
        speak("Chào buổi đêm")

    speak("Trợ lý ảo Jarvis sẵn sàng phục vụ. Tôi có thể giúp gì cho chủ nhân ạ?")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        # r.pause_threshold = 1
        audio=r.listen(source,timeout=10)
        # audio = r.listen(source)
    try:
        print("Recognising...")
        query = r.recognize_google(audio)
    except Exception as e:
        print(e)
        print("---Say that Again---")

        return "None"
    return query

def start():
    # board.digital[3].write(1)
    # board.digital[8].write(1)
    # board.digital[6].write(1)
    # board.digital[5].write(1) 
    # board.digital[4].write(1)
    # board.digital[9].write(1)
    # board.digital[13].write(0)
    wishme()

    while True:
        query = takeCommand().lower()  
        print(query)

        if "thời gian" in query:  
            time()           
        elif "ngày" in query:  
            date()  

        elif'portfolio' in query:
            open_portfolio()

        elif 'chrome' in query:
            open_chrome()

        elif "tìm kiếm" in query:
            speak("Tôi có thể tìm kiếm gì?")
            chromepath = "C:\Program Files\Google\Chrome\Application\chrome.exe %s"  
            search = takeCommand().lower()
            wb.get(chromepath).open_new_tab(search + ".com")  
        
        elif "mở ghi chú" in query:
            speak("Mở ghi chú")
            location = "C:/WINDOWS/system32/notepad.exe"
            notepad = subprocess.Popen(location)

        elif "đóng ghi chú" in query:
                speak("Đóng ghi chú")
                notepad.terminate()

        elif "đùa" in query:
                speak(pyjokes.get_jokes())

        elif 'bật đèn xanh dương' in query:
            speak('Đèn đang được bật....')
            #time.sleep(0.1)
            board.digital[3].write(0)

        elif 'tắt đèn xanh dương' in query:
            speak('Đèn đang được tắt....')
            # time.sleep(0.1)
            board.digital[3].write(1)

        elif 'bật đèn đỏ' in query:
            speak('Đèn đang được bật....')
            #time.sleep(0.1)
            board.digital[4].write(0)

        elif 'tắt đèn đỏ' in query:
            speak('Đèn đang được tắt....')
            # time.sleep(0.1)
            board.digital[4].write(1)

        elif 'bật đèn xanh lá cây' in query:
            speak('Đèn đang được bật....')
            #time.sleep(1)
            board.digital[5].write(0)

        elif 'tắt đèn xanh lá cây' in query:
            speak('Đèn đang được tắt....')
            # time.sleep(0.1)
            board.digital[5].write(1) 

        elif 'bật quạt' in query:
            speak('Quạt đang được bật....')
            #time.sleep(0.1)
            board.digital[6].write(0)

        elif 'tắt quạt' in query:
            speak('Quạt đang được tắt....')
            # time.sleep(0.1)
            board.digital[6].write(1)

        # elif 'security' in query:
        #     speak('Entering Security Mode')
        #     suresh=board.analog[1].read()
        #     # pratish=float(suresh)
        #     # print(pratish)
        #     print(suresh)
        #     # speak(pratish)
        #     if suresh==1:
        #         speak('threat Detected')
        #         break
        #     else:
        #         speak('all good outside no threat detected')
        #         break

        elif 'bật báo thức' in  query:
            board.digital[13].write(1)
            speak('Báo thức đã được bật....')

        elif 'tắt báo thức' in  query:
            board.digital[13].write(0)
            speak('Báo thức đã được tắt....')
        
        elif 'tắt hệ thống' in query:
            speak('Hệ thống đang được tắt, tạm biệt chủ nhân....')
            board.digital[3].write(1)
            board.digital[8].write(1)
            board.digital[6].write(1)
            board.digital[5].write(1) 
            board.digital[4].write(1)
            board.digital[9].write(1)
            board.digital[13].write(0)
            quit()
            

if __name__ == "__main__":
    start()
