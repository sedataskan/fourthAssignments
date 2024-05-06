from ftplib import FTP
import getpass
from tkinter import Tk, Button, Entry, Label

# FTP bağlantısı kurma
ftp = FTP('ftp.dlptest.com')
ftp.login(user='dlpuser', passwd='rNrKYTX9g7z3RgJRmxWuGHbeu')

class Genel:
    def dosya_yukle(self, dosya_adi):
        with open(filename, 'rb') as file:
            try:
                ftp.storbinary(f'STOR {filename}', file)
            except Exception as e:
                print(f"Error occurred while uploading file: {e}")

    def dosya_indir(self, dosya_adi):
        local_filename = 'indirilen_ornek.txt'
        with open(local_filename, 'wb') as file:
            try:
                ftp.retrbinary(f'RETR {filename}', file.write)
            except Exception as e:
                print(f"Error occurred while downloading file: {e}")

class Local:
    def dizinOlustur(self):
        try:
            ftp.mkd('yeni_dizin')
        except Exception as e:
            print(f"Error occurred while creating directory: {e}")

    def dizinSil(self):
        try:
            ftp.rmd('silinecek_dizin')
        except Exception as e:
            print(f"Error occurred while deleting directory: {e}")

    def dizinDegistir(self):
        try:
            ftp.cwd('yeni_dizin')
        except Exception as e:
            print(f"Error occurred while changing directory: {e}")

    def dosyaAdiDegistir(self):
        try:
            ftp.rename('eski_dosya_adi.txt', 'yeni_dosya_adi.txt')
        except Exception as e:
            print(f"Error occurred while renaming file: {e}")

    def dosyaSil(self):
        try:
            ftp.delete('silinecek_dosya.txt')
        except Exception as e:
            print(f"Error occurred while deleting file: {e}")

    def dosyaListele(self):
        try:
            files = ftp.nlst()
            for file in files:
                text.insert(tk.END, file + "\n")
            # Bağlantıyı kapat
            ftp.quit()
        except Exception as e:
            print(f"Error occurred while listing directories/files: {e}")

class Remote():
    def baglan(self):
        try:
            url = input("Sunucu Adresi: ")
            port = input("Sunucu Portu: ")
            ftp.connect(url, int(port))
            
        except Exception as e:
            print(f"Error occurred while connecting to server: {e}")

    def giris(self):
        try:
            name = input("Kullanıcı Adı: ")
            password = getpass.getpass("Şifre: ")
            ftp.login(name,password)
            
        except Exception as e:
            print(f"Error occurred while logging in: {e}")

    def dizinOlustur(self):
        try:
            ftp.mkd('yeni_dizin')
        except Exception as e:
            print(f"Error occurred while creating directory: {e}")

    def dizinSil(self):
        try:
            ftp.rmd('silinecek_dizin')
        except Exception as e:
            print(f"Error occurred while deleting directory: {e}")

    def dizinDegistir(self):
        try:
            ftp.cwd('yeni_dizin')
        except Exception as e:
            print(f"Error occurred while changing directory: {e}")

    def dosyaAdiDegistir(self):
        try:
            ftp.rename('eski_dosya_adi.txt', 'yeni_dosya_adi.txt')
        except Exception as e:
            print(f"Error occurred while renaming file: {e}")

    def dosyaSil(self):
        try:
            ftp.delete('silinecek_dosya.txt')
        except Exception as e:
            print(f"Error occurred while deleting file: {e}")

    def dosyaListele(self):
        try:
            files = ftp.nlst()
            for file in files:
                text.insert(tk.END, file + "\n")
            # Bağlantıyı kapat
            ftp.quit()
        except Exception as e:
            print(f"Error occurred while listing directories/files: {e}")


import tkinter as tk

root = tk.Tk()
root.title("FTP APP | Seda Nur Taşkan - 201180004")
root.geometry("800x600")
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
root.geometry("+{}+{}".format(positionRight, positionDown))

# Sunucu bağlantısı
server_frame = tk.Frame(root)
server_frame.pack(side="top", pady=5)

server_label = tk.Label(server_frame, text="Sunucu Adresi:")
server_label.pack(side="left", padx=5)
server_entry = tk.Entry(server_frame)
server_entry.pack(side="left")

username_label = tk.Label(server_frame, text="Kullanıcı Adı:")
username_label.pack(side="left", padx=5)
username_entry = tk.Entry(server_frame)
username_entry.pack(side="left")

password_label = tk.Label(server_frame, text="Şifre:")
password_label.pack(side="left", padx=5)
password_entry = tk.Entry(server_frame, show="*")
password_entry.pack(side="left")

login_button = tk.Button(server_frame, text="Giriş Yap")
login_button.pack(side="top", padx=5)
login_button.configure(bg="black", border=1, foreground="white", font=("Arial", 10))

## Genel
frame = tk.Frame(root)
frame.pack(pady=10)

genelBasliklar = ["Dosya Yükle", "Dosya İndir"]
genelRenkler = ["pink", "cyan"]
genelFonksiyonlar = [Genel().dosya_yukle, Genel().dosya_indir]

Label(frame, text="Genel İşlemler").grid(row=0, columnspan=2)
for i in range(2):
    button = tk.Button(frame, text=genelBasliklar[i], command=genelFonksiyonlar[i])
    button.grid(row=1, column=i, padx=5)
    button.configure(bg=genelRenkler[i], border=1, font=("Arial", 10))

frame.pack(anchor="center")

### local
frame = tk.Frame(root)
frame.pack(pady=10)

islemler = ["Dizin Oluştur", "Dizin Sil", "Dizin Değiştir", "Dosya Adı Değiştir", "Dosya Sil", "Dosyaları Listele"]
renkler = ["red", "orange",  "yellow", "green", "blue", "purple"]
yerelFonksiyonlar = [Local().dizinOlustur, Local().dizinSil, Local().dizinDegistir, Local().dosyaAdiDegistir, Local().dosyaSil, Local().dosyaListele]

Label(frame, text="Yerel Sunucu İşlemleri").grid(row=0, columnspan=6)
for i in range(6):
    button = tk.Button(frame, text=islemler[i], command=yerelFonksiyonlar[i])
    button.grid(row=1, column=i, padx=5)
    button.configure(bg=renkler[i], border=1, font=("Arial", 10))

frame.pack(anchor="center")

##remote
frame = tk.Frame(root)
frame.pack(pady=10)

uzakFonksiyonlar = [Remote().dizinOlustur, Remote().dizinSil, Remote().dizinDegistir, Remote().dosyaAdiDegistir, Remote().dosyaSil, Remote().dosyaListele]

Label(frame, text="Uzak Sunucu İşlemleri").grid(row=0, columnspan=6)
for i in range(6):
    button = tk.Button(frame, text=islemler[i], command=uzakFonksiyonlar[i])
    button.grid(row=1, column=i, padx=5)
    button.configure(bg=renkler[i], border=1, font=("Arial", 10))

text = tk.Text(root, height=20, width=80)
text.configure(font=("Arial", 10), wrap="word", bg="lightgrey", border=1)
text.pack()


root.mainloop()