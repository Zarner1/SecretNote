#Zarner
import customtkinter as ctk
import os
import tkinter as tk
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import urllib.request

app = ctk.CTk()
app.title('Secret Note')
app.minsize(600, 600)
app.config(bg='grey')
i = 0

id_dictionary = {}
Note_Dictionary = {}

if os.path.exists("SecretNote/passwords.txt"):
    pass
else:
    os.mkdir("SecretNote")
    open(os.path.join(('SecretNote/'), ("passwords.txt")), "w")

if os.path.exists("SecretNote/text.txt"):
    pass
else:
    open(os.path.join(('SecretNote/'), ("text.txt")), "w")

dosya_boyutu = os.path.getsize("SecretNote/passwords.txt")

with open('SecretNote/passwords.txt', 'r') as file:  # get file dict
    if dosya_boyutu > 0:
        for line in file:
            key, value = line.strip().split(': ')
            Note_Dictionary[key] = value
    else:
        pass
dosya_boyutu = os.path.getsize("SecretNote/text.txt")
with open('SecretNote/text.txt', 'rb') as file:  # get file dict

    if dosya_boyutu > 2:
        for line in file:
            key, value = line.strip().decode().split(': ')
            id_dictionary[key] = value
    else:
        pass


def SaveEndEncrypt():
    global Note_Dictionary
    global id_dictionary
    global i
    global fernet

    if isimEntry.get() in Note_Dictionary.keys():
        tk.messagebox.showerror("ERROR", "Benzer ID bulunmaktadır lütfen ID değiştiriniz!!!")
    elif len(isimEntry.get()) == 0 or len(password.get()) == 0 or len(text1.get("1.0", ctk.END).strip()) == 0:
        tk.messagebox.showerror("ERROR1", "Lütfen tüm bilgileri giriniz!!!")
    else:
          #password add dict
        keys = Fernet.generate_key()
        keys1 = Fernet.generate_key()
        fernet1 = Fernet(keys1)
        passwordx = fernet1.encrypt(password.get().encode("utf-8"))
        Note_Dictionary[isimEntry.get()] = passwordx #password şifreliyorum
        i += 1

        with open('SecretNote/passwords.txt', 'w') as file:  #update txt file
            for key, value in Note_Dictionary.items():
                file.write(f'{key}: {value}\n')

        fernet = Fernet(keys)
        # text
        mesaj = text1.get(0.0, tk.END)

        # text password
        sifreli_mesaj = fernet.encrypt(mesaj.encode('utf-8'))
        isim = isimEntry.get().encode()
        id_dictionary[isim] = (sifreli_mesaj, keys)
        with open("SecretNote/text.txt", "wb") as file:
            for key, value in id_dictionary.items():
                file.write(f'{key}: {value}\n'.encode("utf-8"))

        isimEntry.delete(0, tk.END)
        password.delete(0, tk.END)
        text1.delete(1.0, tk.END)


def Decrypt():
    global id_dictionary
    isim = isimEntry.get().encode()

    if isimEntry.get() in Note_Dictionary and Note_Dictionary[isimEntry.get()] == password.get():

        mesaj = text1.get(1.0, tk.END)

        fernet = Fernet(id_dictionary[isim][1])
        cozulmus_mesaj = fernet.decrypt(mesaj)
        cozulmus_mesaj = cozulmus_mesaj.decode()
        text1.delete(1.0, tk.END)
        text1.insert(tk.END, cozulmus_mesaj)

    else:
        isimEntry.delete(0, tk.END)
        password.delete(0, tk.END)
        text1.delete(1.0, tk.END)

urllib.request.urlretrieve("https://images.fineartamerica.com/images/artworkimages/medium/3/top-secret-stamp-thp-creative-transparent.png", "topSecret.png")
image = Image.open("topSecret.png")
image = image.resize((100, 100))
photo = ImageTk.PhotoImage(image)

label = tk.Label(app, image=photo)
label.place(x=255, y=0)

#Notun ismini burda yazariz
isimEntry = ctk.CTkEntry(app, width=190, border_color="orange", border_width=4, bg_color="grey")
isimEntry.place(x=210, y=150)
isimLabel = tk.Label(text='Note ID', bg='grey', fg='white', font=("Helvetica", 12))
isimLabel.place(x=275, y=120)
#Not edeceğimiz yazıyı yazacağımız kısım
text1 = ctk.CTkTextbox(app, scrollbar_button_color="yellow", corner_radius=16, border_color="orange", border_width=4,
                       bg_color="grey")
text1.place(x=205, y=210)
text1Label = tk.Label(app, text='Note', bg='grey', fg='white', font=("Helvetica", 12))
text1Label.place(x=285, y=180)
#Notu şifrelemek veya şifre gireceğimiz kısım
password = ctk.CTkEntry(app, width=190, border_color="orange", border_width=4, bg_color="grey", show='*')
password.place(x=210, y=440)
passwordLabel = tk.Label(app, text='Password', bg='grey', fg='white', font=("Helvetica", 12))
passwordLabel.place(x=265, y=410)

#Kaydetme ve şifreleme buttonu
button = ctk.CTkButton(app, text="Save & Encrypt", width=190, border_width=4, bg_color="grey", command=SaveEndEncrypt)
button.place(x=210, y=480)
#Şifre çözme buttonu
button = ctk.CTkButton(app, text="Decrypt", width=190, border_width=4, bg_color="grey", command=Decrypt)
button.place(x=210, y=510)
app.mainloop()
