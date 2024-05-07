from ftplib import FTP
from tkinter import Tk, Button, Entry, Label, messagebox, filedialog, Listbox
import tkinter as tk
import os

class App:
    def __init__(self, root):
        self.root = root
        root.title("FTP APP | Seda Nur Taşkan - 201180004")
        root.geometry("800x400")
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

        login_button = tk.Button(server_frame, text="Giriş Yap", command=self.baglan)
        login_button.pack(side="top", padx=5)
        login_button.configure(bg="black", border=1, foreground="white", font=("Arial", 10))

        ## local
        frame = tk.Frame(root)
        frame.pack(pady=10)

        islemler = ["Dizin Oluştur", "Dizin Sil", "Dizin Değiştir", "Dosya Adı Değiştir", "Dosya Sil"]
        renkler = ["red", "orange",  "yellow", "green", "blue", "purple"]
        yerelFonksiyonlar = [self.dizinOlustur, self.dizinSil, self.dizinDegistir, self.dosyaAdiDegistir, self.dosyaSil]

        Label(frame, text="Yerel Sunucu İşlemleri").grid(row=0, columnspan=5)
        for i in range(5):
            button = tk.Button(frame, text=islemler[i], command=yerelFonksiyonlar[i])
            button.grid(row=1, column=i, padx=5)
            button.configure(bg=renkler[i], border=1, font=("Arial", 10))

        frame.pack(anchor="center")

        ##remote
        frame = tk.Frame(root)
        frame.pack(pady=10)

        uzakFonksiyonlar = [self.dizinOlustur, self.dizinSil, self.dizinDegistir, self.dosyaAdiDegistir, self.dosyaSil]

        Label(frame, text="Uzak Sunucu İşlemleri").grid(row=0, columnspan=5)
        for i in range(5):
            button = tk.Button(frame, text=islemler[i], command=uzakFonksiyonlar[i])
            button.grid(row=1, column=i, padx=5)
            button.configure(bg=renkler[i], border=1, font=("Arial", 10))

        frame.pack(anchor="center")

        ## Liste kutulari
        frame = tk.Frame(root)
        frame.pack(pady=10)

        self.local_file_listbox = tk.Listbox(frame)
        self.local_file_listbox.pack(side="left", padx=10)
        self.local_file_listbox.configure(width=50)

        self.file_listbox = tk.Listbox(frame)
        self.file_listbox.pack(side="left", padx=10)
        self.file_listbox.configure(width=50)

        frame.pack(anchor="center")

        ## Genel
        frame = tk.Frame(root)
        frame.pack(pady=10)

        genelBasliklar = ["Dosya Yükle", "Dosya İndir"]
        genelRenkler = ["pink", "cyan"]
        genelFonksiyonlar = [self.dosya_yukle, self.dosya_indir]

        # Label(frame, text="Genel İşlemler").grid(row=0, columnspan=2)
        for i in range(2):
            button = tk.Button(frame, text=genelBasliklar[i], command=genelFonksiyonlar[i])
            button.grid(row=1, column=i, padx=5)
            button.configure(bg=genelRenkler[i], border=1, font=("Arial", 10))

        frame.pack(anchor="center")
          
    def baglan(self):
        try:
            # server = self.server_entry.get()
            # username = self.username_entry.get()
            # password = self.password_entry.get()

            # server = "ftp.dlptest.com"
            # username = "dlpuser"
            # password = "rNrKYTX9g7z3RgJRmxWuGHbeu"

            server = "127.0.0.1"
            username = "seda"
            password = "6653"

            self.ftp = FTP(server)
            self.ftp.login(username, password)

            self.update_file_list_remote()
            self.update_file_list_local()

        except Exception as e:
            print(f"Error occurred while connecting to server: {e}")

    def update_file_list_remote(self):
        self.file_listbox.delete(0, tk.END)
        files = self.ftp.nlst()
        for file in files:
            self.file_listbox.insert(tk.END, file)
    
    def update_file_list_local(self):
        try:
            self.local_file_listbox.delete(0, tk.END)
            local_files = os.listdir('./ComputerNetworks/ftp/server/folder/')
            for file in local_files:
                self.local_file_listbox.insert(tk.END, file)

        except Exception as e:
            print(f"Hata oluştu: {e}")

    def dosya_yukle(self):
        try:
            local_file_path = filedialog.askopenfilename()
            local_file_name = local_file_path.split("/")[-1]
            with open(local_file_path, "rb") as local_file:
                self.ftp.storbinary("STOR " + local_file_name, local_file)
            self.update_file_list_remote()
            messagebox.showinfo("Yükleme Başarılı", f"{local_file_name} dosyası başarıyla yüklendi.")
        except Exception as e:
            messagebox.showerror("Yükleme Hatası", f"Dosya yüklenirken bir hata oluştu: {e}")

    def dosya_indir(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            local_filename = selected_file.split("/")[-1] 
            try:
                with open(local_filename, "wb") as local_file:
                    self.ftp.retrbinary("RETR " + selected_file, local_file.write)
                messagebox.showinfo("İndirme Başarılı", f"{selected_file} dosyası başarıyla indirildi ve {local_filename} olarak kaydedildi.")
            except Exception as e:
                messagebox.showerror("İndirme Hatası", f"Dosya indirilirken bir hata oluştu: {e}")
        else:
            messagebox.showwarning("Dosya Seçilmedi", "Lütfen indirmek istediğiniz dosyayı seçin.")

    ## Local
    def dizinOlustur(self):
        try:
            directory_name = filedialog.askdirectory()
            os.mkdir(directory_name)
            self.update_file_list_local()
            messagebox.showinfo("Dizin Oluşturuldu", f"{directory_name} adlı dizin başarıyla oluşturuldu.")
        except Exception as e:
            messagebox.showerror("Hata", f"Dizin oluşturulurken bir hata oluştu: {e}")

    def dizinSil(self):
        selected_index = self.local_file_listbox.curselection()
        if selected_index:
            selected_directory = self.local_file_listbox.get(selected_index)
            try:
                os.rmdir(selected_directory)
                self.update_file_list_local()
                messagebox.showinfo("Dizin Silindi", f"{selected_directory} adlı dizin başarıyla silindi.")
            except Exception as e:
                messagebox.showerror("Hata", str(e))
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir dizin seçin.")

    def dizinDegistir(self):
        print("Dizin değiştirme işlemi")

    def dosyaAdiDegistir(self):
        selected_index = self.local_file_listbox.curselection()
        if selected_index:
            selected_file = self.local_file_listbox.get(selected_index)
            new_file_name = filedialog.asksaveasfilename()
            try:
                os.rename(selected_file, new_file_name)
                self.update_file_list_local()
                messagebox.showinfo("Dosya Adı Değiştirildi", f"{selected_file} adlı dosyanın adı başarıyla {new_file_name} olarak değiştirildi.")
            except Exception as e:
                messagebox.showerror("Hata", str(e))
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin.")

    def dosyaSil(self):
        selected_index = self.local_file_listbox.curselection()
        if selected_index:
            selected_file = self.local_file_listbox.get(selected_index)
            try:
                self.ftp.delete(selected_file)
                self.update_file_list_local()
            except Exception as e:
                messagebox.showerror("Hata", str(e))
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin.")

    # ## Remote

    # def dizinOlustur(self):
    #     print("Dizin oluşturma işlemi")

    # def dizinSil(self):
    #     print("Dizin silme işlemi")

    # def dizinDegistir(self):
    #     print("Dizin değiştirme işlemi")

    # def dosyaAdiDegistir(self):
    #     print("Dosya adı değiştirme işlemi")

    # def dosyaSil(self):
    #     selected_index = self.file_listbox.curselection()
    #     if selected_index:
    #         selected_file = self.file_listbox.get(selected_index)
    #         try:
    #             self.ftp.delete(selected_file)
    #             self.update_file_list()
    #         except Exception as e:
    #             messagebox.showerror("Hata", str(e))
    #     else:
    #         messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin.")


root = tk.Tk()
app = App(root)
root.mainloop()