from tkinter.font import BOLD
from gtts import gTTS
from os import remove
from playsound import playsound
import speech_recognition as sr
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

class Funciones:
    def Conversor(self):
        self.Modo=False
        texto=text1.get(1.0, END)
        try:
            tts1=gTTS(text=texto, lang=self.eleccionidioma2, slow=False)
            guardar=filedialog.asksaveasfilename(title="Guardar", initialfile=".mp3", initialdir="C:",filetypes=(("Ficheros de Audio", "*.mp3*"), ("Todos los Ficheros", "*.*")))
            if guardar=="":
                messagebox.showwarning("Guardar", "Guardado Cancelado")
            else:
                if guardar.endswith(".mp3")==True:
                    try:
                        tts1.save(guardar)
                    except AssertionError:
                        messagebox.showinfo("Guardar", "No ah introducido texto")
                        remove(guardar)
                else:
                    try:
                        tts1.save(guardar + ".mp3")
                    except AssertionError:
                        messagebox.showinfo("Guardar", "No ah introducido texto")
                        remove(guardar)
        except AttributeError:
            messagebox.showinfo("Guardar", "No ah seleccinado un idioma")
                    
    def EscucharAudio(self):
        self.Modo=False
        archivo_temporal= "temporal.mp3"
        texto=text1.get(1.0, END)
        try:
            tts2=gTTS(texto, lang=self.eleccionidioma2, slow=False)
            with open(archivo_temporal, "wb") as archivo:
                tts2.write_to_fp(archivo)
            playsound(archivo_temporal)
            remove(archivo_temporal)
        except AttributeError:
            messagebox.showinfo("Escuchar", "No ah introducido un idioma")
        except AssertionError:
            messagebox.showinfo("Escuchar", "No se ah introducido texto")

    def EleccionCB(self, event): #Debemos pasarle un argumento al combobos para seleccionar
        eleccionidioma=combobox1.get()
        self.eleccionidioma2=""
        if eleccionidioma=="Inglés":
            self.eleccionidioma2="en"
        elif eleccionidioma=="Español":
            self.eleccionidioma2="es"
        elif eleccionidioma=="Frances":
            self.eleccionidioma2="fr"
        elif eleccionidioma=="Portugües":
            self.eleccionidioma2="pt"
        elif eleccionidioma=="Chino":
           self.eleccionidioma2="zh-CN"
        elif eleccionidioma=="Ruso":
            self.eleccionidioma2="ru"
        elif eleccionidioma=="Latín":
            self.eleccionidioma2="la"

    def ModoVoz(self):
        try:
            boton3.config(image=AudioEncendido)
            messagebox.showinfo("Reconocimiendo de Voz", "Activado")
            Recon=sr.Recognizer()
            with sr.Microphone() as source:
                label2.config(text="Escuchando...")
                Recon.pause_threshold=1
                Recon.adjust_for_ambient_noise(source, duration=1)
                audiorecon=Recon.listen(source)
            try:
                label2.config(text="Reconociendo...")
                peticion=Recon.recognize_google(audiorecon, language=self.eleccionidioma2)
                text1.insert(1.0, peticion)
            except Exception as e:
                print(e)
                tts3=gTTS("Repite otra vez", lang=self.eleccionidioma2, slow=False)
                archivo_temporal2="temporal2.mp3"
                with open(archivo_temporal2, "wb") as archivo2:
                    tts3.write_to_fp(archivo2)
                playsound(archivo_temporal2)
                remove(archivo_temporal2)
                boton3.config(image=AudioApagado)
                label2.config(text="Reconocimiento de Voz")
                return "None"
            boton3.config(image=AudioApagado)
            label2.config(text="Reconocimiento de Voz")
            return peticion
        except AttributeError:
            messagebox.showinfo("Voz", "No ah introducido un idioma")
            boton3.config(image=AudioApagado)
            label2.config(text="Reconocimiento de Voz")
                
F=Funciones()
main=Tk()
AudioEncendido=PhotoImage(file=r"C:\Users\diego\Documents\Python\Audio-Encendido.png")
AudioApagado=PhotoImage(file=r"C:\Users\diego\Documents\Python\Audio-Apagado.png")
main.title("Conversor de texto a Voz")
main.geometry("900x570")
main.resizable(1,1)
label1=Label(main, text="Bienvenido", font=BOLD)
label1.pack()
mainFrame=Frame(main)
mainFrame.pack()
label1=Label(mainFrame, text="Introduzca su texto", font=BOLD)
label1.grid(row=0, column=0, pady=5)
text1=Text(mainFrame)
text1.grid(row=0, column=1, pady=5)
BarravertText=Scrollbar(mainFrame, command=text1.yview)
BarravertText.grid(row=0, column=2, padx=0, pady=5, sticky=NSEW)
combobox1=ttk.Combobox(mainFrame, width=20)
combobox1.grid(row=1, column=1, pady=5)
combobox1.config(state="readonly")
combobox1.set("Seleccione un idioma") 
combobox1["values"]=["Inglés", "Español", "Frances", "Portugües", "Chino", "Ruso", "Latín"]
combobox1.bind("<<ComboboxSelected>>", F.EleccionCB)
boton1=Button(mainFrame, text="Escuchar Audio", height=2, command=F.EscucharAudio, cursor="hand2")
boton1.grid(row=3, column=1)
boton2=Button(mainFrame, text="Generar Audio", height=2, command=F.Conversor, cursor="hand2")
boton2.grid(row=4, column=1)
boton3=Button(mainFrame, image=AudioApagado, command=F.ModoVoz, cursor="hand2", border=0)
boton3.grid(row=3, column=0)
label2=Label(mainFrame, text="Reconocimiento de Voz")
label2.grid(row=4, column=0)
main.mainloop()