
import speech_recognition as sr
import pyttsx3
import langid
import langdetect
import threading
from PIL import Image

#interfaccia
import tkinter as tk
from PIL import ImageTk
from tkinter import Tk, Button, Label
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename

########################################################
#                                                      #
#               FUNZIONI          GENERICHE            #
#                                                      #
# ######################################################
            
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


########################################################
#                                                      #
#       INIZIO THREAD PRINCIPALE AUDIO RECOGNITION     #
#                                                      #
# ######################################################

def recognizer(window):
    r = sr.Recognizer()

    while(1):   #infinite loop to iteratively look for new audio
           
        with sr.Microphone() as source2: #si sceglie qua il microfono come input
                
            r.adjust_for_ambient_noise(source2, duration=0.2) #sensibilita microfono
                
            audio2 = r.listen(source2) 
        
        # Speech recognition in Italian
        try: #per gestire gli errori se qualcosa va storto

            MyText=r.recognize_google(audio2, language='it-IT') #prende audio e lo converte in testo, presupponendo sia italiano
            MyText = MyText.lower() #mette testo minuscolo
            print("You said: " + MyText) #appare sul terminale il testo
            
            language= langid.classify(MyText)[0] #identifica la lingua
            
            language2= langdetect.detect(MyText) #altra funzione di un altra libreria per la lingua

            # Print the detected language
            print("Detected languages:", language )
            print("Detected languages numero 2:", language )

            if(language=="it"):
                #SpeakText("Buongiorno caro amico, ti auguro una buona giornata!")
                # Open the image file
                image = Image.open("./test.jpg") #qua ci va il path dell'immagine da mostrare
                # Show the image
                # image.show()
                
                photo_image= open_image("./test.jpg")

                # Crea una label per visualizzare l'immagine
                label1 = tk.Label(image=photo_image)
                label1.image = photo_image

                label1.place(x=0, y=0)
      
            elif(language == "es" or language == "eo"):
                #SpeakText("Hola amigooooooo como to estas")
                image = Image.open("./test.jpg")



        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said, the language is not in my dictionary")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
                                        
  
########################################################
#                                                      #
#       INIZIO THREAD VIDEO                            #
#                                                      #
# ######################################################

if __name__ =="__main__":
    # Crea una finestra
        window = tk.Tk()
        window.geometry("1920x1080")
        window.resizable(True, True)

        # Create a separate thread to perform the task
        task_thread = threading.Thread(target=recognizer, args=(window,))
        task_thread.start()


        # Start the Tkinter event loop
        window.mainloop()




