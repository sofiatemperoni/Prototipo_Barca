
import speech_recognition as sr
import pyttsx3
import langid
import langdetect
import threading
import sys
from PIL import Image
from playsound import playsound


#interfaccia
import tkinter as tk
from PIL import ImageTk
from tkinter import Tk, Button, Label
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename

pause_event = threading.Event()
stop_event = threading.Event()
task_thread = None

button_style = {
    'font': ('Arial', 8),
    'bg': 'grey',
    'fg': 'white',
    'activebackground': 'blue',
    'activeforeground': 'white',
    'relief': 'raised',
    'borderwidth': 2,
    'width': 10,
    'height': 2,
}

            
#funzione per aprire un immagine
def open_image(pathname):
                    image = Image.open(pathname)
                    image = image.resize((400, 400))  # Ridimensiona l'immagine
                    photo = ImageTk.PhotoImage(image)
                    return photo       

 
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


#funzione audio recognizer
def recognizer(window):
    r = sr.Recognizer()

    while not stop_event.is_set():

        while  pause_event.is_set():
            # Wait when the pause event is set
            pass   

        with sr.Microphone() as source2: #si sceglie qua il microfono come input

            print("I'm listeningg")   
            window.title("Listening")
 
            r.adjust_for_ambient_noise(source2, duration=0.2) #sensibilita microfono
                
            audio2 = r.listen(source2) 
        
        try: #per gestire gli errori se qualcosa va storto

           # MyText=r.recognize_google(audio2) #prende audio e lo converte in testo, presupponendo sia italiano
            MyText=r.recognize_google(audio2, language='it-IT') #prende audio e lo converte in testo, presupponendo sia italiano

            MyText = MyText.lower() #mette testo minuscolo
            print("You said: " + MyText) #appare sul terminale il testo
            
            language= langid.classify(MyText)[0] #identifica la lingua
            
            language2= langdetect.detect(MyText) #altra funzione di un altra libreria per la lingua

            # Stampa detected language
            print("Detected languages:", language )
            print("Detected languages numero 2:", language )

            #inserire qui le varie immagini associate alla lingua
            if language == "it":
                image_path = "./test.jpg"
            elif language == "es" or language == "eo":
                image_path = "./test.jpg"
            else:
                # Lingua non riconosciuta, usa l'immagine predefinita
                image_path = "./test2.jpg"

            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            label1.configure(image=photo)
            label1.image = photo

        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said, the language is not in my dictionary")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
                                        

#################------------FUNCTIONS--------#################################

def start_listening():
    global task_thread
    pause_event.clear()
    stop_event.clear()
    task_thread = threading.Thread(target=recognizer, args=(window,))
    task_thread.start()
   
def pause_listening():
    window.title("Paused")
    pause_event.set()

def resume_listening():
    pause_event.clear()

def stop_listening():
    global task_thread
    if task_thread and task_thread.is_alive():
        stop_event.set()
        task_thread.join()
        stop_event.clear()
        sys.exit()  

def play_audio(filename):
    playsound(filename)  

#Funzione che gestisce il click sullo schermo per far partire la voce
def handle_click(event):
    x = event.x
    y = event.y
    #finestra di pixel nella quale deve avvenire il click ->
    if 100 <= x <= 1000 and 100 <= y <= 1000:
        print("Clicked on the specified portion of the screen!")
        #play_audio("./nomefile.mp3")
        SpeakText("Ciao, questa è la storia che dovrei raccontare. Ancora non l'ho imparata quindi mi sembra giusto che qualcuno me la insegni. Sofia dimmi cosa devo direeee") #qui leggo la storia






#################------------MAIN--------#################################

if __name__ =="__main__":
        # Crea una finestra
        window = tk.Tk()
        window.geometry("1080x1920") #formato finestra
        window.resizable(True, True)
        window.state('zoomed')
        window.title("Title for my program") #Inserire il titolo del progetto !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
        photo_image = open_image("./sfondo.jpg")  # Immagine predefinita di sfondo
        label1 = tk.Label(window)
        label1.configure(image=photo_image)
        label1.place(x=0, y=0) #coordinate pixel per immagine di sfondo

        # Create buttons for control
        start_button = tk.Button(window, text="Start", command=start_listening, **button_style)
        start_button.pack
        start_button.place(x=600, y=750) #coordinate button start

        pause_button = tk.Button(window, text="Pause", command=pause_listening, **button_style)
        pause_button.pack
        pause_button.place(x=700, y=750) #coordinate button pause

        resume_button = tk.Button(window, text="Resume", command=resume_listening, **button_style)
        resume_button.pack
        #resume_button.place(x=800, y=750)

        window.bind("<Button-1>", handle_click)

        #stop_button = tk.Button(window, text="Stop", command=stop_listening)
       # stop_button.place(x=400, y=450)

        # Start the Tkinter event loop
        window.mainloop()




