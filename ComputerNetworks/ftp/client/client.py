from ftplib import FTP
from tkinter import Tk, Button, Entry, Label, messagebox, filedialog, Listbox
from tkinter.simpledialog import askstring
import tkinter as tk
import os
import shutil


class App:
    def __init__(self, root):
        """
        Bu fonksiyon, uygulamanin baslangic ayarlarini yapar.
        Gerekli olan tum widget'lari olusturur ve baslangicta gerekli olan ayarlari yapar.
        """
        self.root = root
        # dosyanin localde bulundugu path
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.local_path = os.path.join(self.path, "./files/")

        root.title("FTP APP | Seda Nur Taşkan - 201180004")
        root.geometry("1000x400")
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()
        positionRight = int(root.winfo_screenwidth()/2 - windowWidth*2)
        positionDown = int(root.winfo_screenheight()/2 -
                           windowHeight)  # merkezde acilmasi icin
        root.geometry("+{}+{}".format(positionRight, positionDown))

        # Sunucu baglantisi icin gerekli olan alanlar
        server_frame = tk.Frame(root)
        server_frame.pack(side="top", pady=5)

        server_label = tk.Label(server_frame, text="Sunucu Adresi:")
        server_label.pack(side="left", padx=5)
        self.server_entry = tk.Entry(server_frame)
        self.server_entry.pack(side="left")

        username_label = tk.Label(server_frame, text="Kullanıcı Adı:")
        username_label.pack(side="left", padx=5)
        self.username_entry = tk.Entry(server_frame)
        self.username_entry.pack(side="left")

        password_label = tk.Label(server_frame, text="Şifre:")
        password_label.pack(side="left", padx=5)
        self.password_entry = tk.Entry(server_frame, show="*")
        self.password_entry.pack(side="left")

        login_button = tk.Button(
            server_frame, text="Giriş Yap", command=self.baglan)  # baglan fonksiyonu cagirilir ve sunucuya baglanilir
        login_button.pack(side="top", padx=5)
        login_button.configure(bg="black", border=1,
                               foreground="white", font=("Arial", 10))

        # local ve remote sunucu islemleri icin gerekli olan alanlar
        frame = tk.Frame(root)
        frame.pack(pady=10)

        frame1 = tk.Frame(frame)
        frame1.pack(side="left", pady=10, padx=0)

        islemler = ["Dizin Oluştur", "Dizin Sil",
                    "Seçili Dizine Gir", "Önceki Dizine Git"]
        renkler = ["green", "blue", "white", "purple"]
        yerelFonksiyonlar = [self.dizinOlustur,
                             self.dizinSil, self.dizinGir, self.dizinDegistir]

        Label(frame1, text="Yerel Sunucu İşlemleri").grid(row=0, columnspan=4)
        for i in range(4):
            button = tk.Button(
                frame1, text=islemler[i], command=yerelFonksiyonlar[i])
            button.grid(row=1, column=i, padx=5)
            button.configure(bg=renkler[i], border=1, font=("Arial", 10))

        frame1.pack(anchor="center")
        frameEmpty = tk.Frame(frame)
        frameEmpty.pack(side="left", pady=10, padx=30)

        frame2 = tk.Frame(frame)
        frame2.pack(side="left", pady=10)

        remoteFonksiyonlar = [self.remoteDizinOlustur, self.dizinSil,
                              self.remote_dizineGir, self.remoteDizinDegistir]

        Label(frame2, text="Uzak Sunucu İşlemleri").grid(row=0, columnspan=14)
        for i in range(4):
            button = tk.Button(
                frame2, text=islemler[i], command=remoteFonksiyonlar[i])
            button.grid(row=1, column=i+5, padx=5)
            button.configure(bg=renkler[i], border=1, font=("Arial", 10))

        frame2.pack(anchor="center")

        # Local ve Remote dosya listeleri
        frame = tk.Frame(root)
        frame.pack(pady=10)

        self.local_file_listbox = tk.Listbox(frame)
        self.local_file_listbox.pack(side="left", padx=10)
        self.local_file_listbox.configure(width=70)

        self.file_listbox = tk.Listbox(frame)
        self.file_listbox.pack(side="left", padx=10)
        self.file_listbox.configure(width=70)

        frame.pack(anchor="center")

        # Genel dosya islemleri icin gerekli olan alanlar
        frame = tk.Frame(root)
        frame.pack(pady=10)

        genelBasliklar = ["Dosya Yükle", "Dosya İndir",
                          "İsim Değiştir", "Dosya Sil"]
        genelRenkler = ["pink", "cyan", "brown", "orange"]
        genelFonksiyonlar = [
            self.dosya_yukle, self.dosya_indir, self.dosyaAdiDegistir, self.dosyaSil]

        for i in range(4):
            button = tk.Button(
                frame, text=genelBasliklar[i], command=genelFonksiyonlar[i])
            button.grid(row=1, column=i, padx=5)
            button.configure(bg=genelRenkler[i], border=1, font=("Arial", 10))

        frame.pack(anchor="center")

    def dizinGir(self):
        """
        Bu fonksiyon, listeden secilen dizine girilmesini saglar.
        Local sunucuda secilen dizine girilir.
        """
        try:
            selected_index = self.local_file_listbox.curselection()
            if selected_index:
                selected_file = self.local_file_listbox.get(selected_index)

                # secilen dosya mi dizin mi oldugunu kontrol eder
                if os.path.isfile(f"{self.local_path}{selected_file}"):
                    self.local_path = self.local_path
                    self.update_file_list_local()
                else:
                    if os.path.isdir(f"{self.local_path}{selected_file}"):
                        self.local_path = f"{self.local_path}{selected_file}/"
                        self.update_file_list_local()
            else:
                messagebox.showwarning("Uyarı", "Lütfen bir dizin seçin.")
        except Exception as e:
            print(f"Error occurred while changing directory: {e}")

    def remote_dizineGir(self):
        """
        Bu fonksiyon, listeden secilen dizine girilmesini saglar. 
        Remote sunucuda secilen dizine girilir.
        """
        try:
            selected_index = self.file_listbox.curselection()
            if selected_index:
                selected_file = self.file_listbox.get(selected_index)
                self.ftp.cwd(selected_file)
                self.update_file_list_remote()
            else:
                messagebox.showwarning("Uyarı", "Lütfen bir dizin seçin.")
        except Exception as e:
            print(f"Error occurred while changing directory: {e}")

    def baglan(self):
        """
        Bu fonksiyon, girilen bilgilerle sunucuya baglanmayi saglar.
        Girilen bilgiler dogruysa, sunucu ile baglanti kurulur ve dosyalar listelenir.
        """
        try:
            server = self.server_entry.get()
            username = self.username_entry.get()
            password = self.password_entry.get()

            # server = "127.0.0.1"
            # username = "seda"   #./server/server.py dosyasinda tanimlanan user
            # password = "6653"

            self.ftp = FTP(server)
            self.ftp.login(username, password)

            self.update_file_list_remote()
            self.update_file_list_local()

        except Exception as e:
            print(f"Error occurred while connecting to server: {e}")

    def update_file_list_remote(self):
        """
        Bu fonksiyon, uzak sunucudaki dosyalari listeler.
        Uzak sunucudaki dosyalar listelenir ve file_listbox'a eklenir.
        """
        self.file_listbox.delete(0, tk.END)
        files = self.ftp.nlst()
        for file in files:
            self.file_listbox.insert(tk.END, file)

    def update_file_list_local(self):
        """
        Bu fonksiyon, local sunucudaki dosyalari listeler.
        Local sunucudaki dosyalar listelenir ve local_file_listbox'a eklenir.
        """
        try:
            self.local_file_listbox.delete(0, tk.END)
            local_files = os.listdir(self.local_path)
            for index in range(len(local_files)):
                self.local_file_listbox.insert(index, local_files[index])

        except Exception as e:
            print(f"Hata oluştu: {e}")

    def dosya_yukle(self):
        """
        Bu fonksiyon, local sunucu listesinden secilen dosyayi uzak sunucuya yukler.
        Secilen dosya, uzak sunucuya yuklenir ve file_listbox guncellenir.
        """
        try:
            selected_index = self.local_file_listbox.curselection()
            if selected_index:
                selected_file = self.local_file_listbox.get(selected_index)
                with open(f"{self.local_path}{selected_file}", "rb") as local_file:
                    self.ftp.storbinary("STOR " + selected_file, local_file)
                self.update_file_list_remote()
                messagebox.showinfo(
                    "Yükleme Başarılı", f"{selected_file} dosyası başarıyla yüklendi.")
            else:
                messagebox.showwarning(
                    "Dosya Seçilmedi", "Lütfen yüklemek istediğiniz dosyayı seçin.")
        except Exception as e:
            messagebox.showerror(
                "Yükleme Hatası", f"Dosya yüklenirken bir hata oluştu: {e}")

    def is_file(self, filename):
        """
        Bu fonksiyon, secilen dosyanin dosya olup olmadigini kontrol eder.
        Secilen dosya bir dosya ise True, degilse False dondurur.
        """
        current = self.ftp.pwd()
        try:
            self.ftp.cwd(filename)
        except:
            self.ftp.cwd(current)
            return True
        self.ftp.cwd(current)
        return False

    def dosya_indir(self):
        """
        Bu fonksiyon, uzak sunucu listesinden secilen dosyayi local sunucuya indirir.
        Secilen dosya, local sunucuya indirilir ve local_file_listbox guncellenir.
        """
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            local_filename = selected_file.split("/")[-1]
            if self.is_file(selected_file):
                try:
                    with open(f"{self.local_path}{local_filename}", "wb") as local_file:
                        self.ftp.retrbinary(
                            "RETR " + selected_file, local_file.write)
                        self.update_file_list_local()
                        messagebox.showinfo(
                            "İndirme Başarılı", f"{selected_file} dosyası başarıyla indirildi ve {local_filename} olarak kaydedildi.")
                except Exception as e:
                    messagebox.showerror(
                        "İndirme Hatası", f"Dosya indirilirken bir hata oluştu: {e}")
            else:
                messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin.")
        else:
            messagebox.showwarning(
                "Dosya Seçilmedi", "Lütfen indirmek istediğiniz dosyayı seçin.")

    def dizinOlustur(self):
        """
        Bu fonksiyon, local sunucuda yeni bir dizin olusturur.
        Local sunucuda yeni bir dizin olusturulur ve local_file_listbox guncellenir.
        """
        try:
            directory_name = askstring("Dizin Oluşturma", "Dizin ismi girin")
            messagebox.showinfo(
                "Dizin Oluşturuldu", f"{directory_name} adlı dizin başarıyla oluşturuldu.")
            os.mkdir(self.local_path+directory_name)
            self.update_file_list_local()
        except Exception as e:
            messagebox.showerror(
                "Hata", f"Dizin oluşturulurken bir hata oluştu: {e}")

    def remoteDizinOlustur(self):
        """
        Bu fonksiyon, uzak sunucuda yeni bir dizin olusturur.
        Uzak sunucuda yeni bir dizin olusturulur ve file_listbox guncellenir.
        """
        try:
            directory_name = askstring("Dizin ismi", "Dizin ismi girin")
            self.ftp.mkd(directory_name)
            self.update_file_list_remote()
            messagebox.showinfo(
                "Dizin Oluşturuldu", f"{directory_name} adlı dizin başarıyla oluşturuldu.")
        except Exception as e:
            messagebox.showerror(
                "Hata", f"Dizin oluşturulurken bir hata oluştu: {e}")

    def dizinSil(self):
        """
        Bu fonksiyon, secilen dizini siler.
        Secilen dizin, local sunucuda veya uzak sunucuda silinir.
        """
        if self.local_file_listbox.curselection():  # local sunucuda secilen dizin silinir
            selected_index = self.local_file_listbox.curselection()
            selected_file = self.local_file_listbox.get(selected_index)
            try:
                shutil.rmtree(self.local_path+selected_file)
                self.update_file_list_local()
                messagebox.showinfo(
                    "Dizin Silindi", f"{selected_file} adlı dizin başarıyla silindi.")
            except Exception as e:
                messagebox.showerror("Hata", str(e))
        elif self.file_listbox.curselection():  # remote sunucuda secilen dizin silinir
            selected_index = self.file_listbox.curselection()
            selected_file = self.file_listbox.get(selected_index)
            try:
                self.ftp.rmd(selected_file)
                self.update_file_list_remote()
                messagebox.showinfo(
                    "Dizin Silindi", f"{selected_file} adlı dizin başarıyla silindi.")
            except Exception as e:
                messagebox.showerror("Hata", str(e))
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir dizin seçin.")

    def dizinDegistir(self):
        """
        Bu fonksiyon, local sunucuda bir onceki dizine gecilmesini saglar.
        Local sunucuda bir onceki dizine gecilir ve local_file_listbox guncellenir.
        """
        newPath = self.local_path.split("/")
        newPath.pop()

        if len(newPath) > 2:
            newPath.pop()
            newPath = "/".join(newPath)
            self.local_path = newPath + "/"
            self.update_file_list_local()

        else:
            self.path = os.path.dirname(os.path.abspath(__file__))
            self.local_path = os.path.join(self.path, "./files/")
            self.update_file_list_local()

    def remoteDizinDegistir(self):
        """
        Bu fonksiyon, uzak sunucuda bir onceki dizine gecilmesini saglar.
        Uzak sunucuda bir onceki dizine gecilir ve file_listbox guncellenir.
        """
        try:
            self.ftp.cwd("..")
            self.update_file_list_remote()
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def dosyaAdiDegistir(self):
        """
        Bu fonksiyon, secilen dosyanin ya da klasorun adini degistirir.
        Secilen dosyanin ya da klasorun adi degistirilir ve file_listbox ya da local_file_listbox guncellenir.
        """
        if self.local_file_listbox.curselection():  # local sunucuda secilen dosyanin ya da klasorun adi degistirilir
            selected_index = self.local_file_listbox.curselection()

            newName = askstring("Yeniden İsimlendir", "Yeni İsmi Girin")
            selected_file = self.local_file_listbox.get(selected_index)
            new_file_name = f"{self.local_path}{newName}"
            try:
                os.rename(self.local_path+selected_file, new_file_name)
                self.update_file_list_local()
                messagebox.showinfo(
                    "Dosya Adı Değiştirildi", f"{selected_file} adlı dosyanın adı başarıyla {new_file_name} olarak değiştirildi.")
            except Exception as e:
                messagebox.showerror("Hata", str(e))

        elif self.file_listbox.curselection():  # remote sunucuda secilen dosyanin ya da klasorun adi degistirilir
            selected_index = self.file_listbox.curselection()
            newName = askstring("Yeniden İsimlendir", "Yeni İsmi Girin")
            selected_file = self.file_listbox.get(selected_index)
            new_file_name = newName
            try:
                self.ftp.rename(selected_file, new_file_name)
                self.update_file_list_remote()
                messagebox.showinfo(
                    "Dosya Adı Değiştirildi", f"{selected_file} adlı dosyanın adı başarıyla {new_file_name} olarak değiştirildi.")
            except Exception as e:
                messagebox.showerror("Hata", str(e))
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin.")

    def dosyaSil(self):
        """
        Bu fonksiyon, secilen dosyayi siler.
        Secilen dosya, local sunucuda veya uzak sunucuda silinir.
        """
        if self.file_listbox.curselection():  # remote sunucuda secilen dosya silinir
            selected_index = self.file_listbox.curselection()
            selected_file = self.file_listbox.get(selected_index)
            try:
                self.ftp.delete(selected_file)
                messagebox.showinfo(
                    "Dosya Silindi", f"{selected_file} adlı dosya başarıyla silindi.")
                self.update_file_list_remote()
            except Exception as e:
                messagebox.showerror("Hata", str(e))
        elif self.local_file_listbox.curselection():  # local sunucuda secilen dosya silinir
            selected_index = self.local_file_listbox.curselection()
            selected_file = self.local_file_listbox.get(selected_index)
            try:
                os.remove(f"{self.local_path}{selected_file}")
                self.update_file_list_local()
                messagebox.showinfo(
                    "Dosya Silindi", f"{selected_file} adlı dosya başarıyla silindi.")
            except Exception as e:
                messagebox.showerror("Hata", str(e))
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin.")


root = tk.Tk()
app = App(root)
root.mainloop()
