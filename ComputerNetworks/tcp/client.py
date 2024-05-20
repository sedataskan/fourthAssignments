# import socket
# import threading
# import json
# import os
# from colorama import init, Fore, Style

# init(autoreset=True)  # Colorama'yı başlat ve renkleri otomatik sıfırla

# class ChatClient:
#     def __init__(self, kullanici_adi, host='localhost', port=12345):
#         self.host = host
#         self.port = port
#         self.kullanici_adi = kullanici_adi
#         self.gruplar = [{
#             'title': 'Genel',
#             'kisiler': []
#         }]
#         self.kullanicilar = dict()
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.client.connect((self.host, self.port))
#         self.yolla_kullanici_adi()

#     def yolla_kullanici_adi(self):
#         msg_data = {'kullanici_adi': self.kullanici_adi, 'command': 'kullanici_ekle'}
#         self.client.send(json.dumps(msg_data).encode('utf-8'))

#     def yolla_mesaj(self, mesaj, hedef_kisi):
#         msg_data = {'kullanici_adi': self.kullanici_adi, 'mesaj': mesaj, 'hedef_kisi': hedef_kisi,'command': 'msg'}
#         self.client.send(json.dumps(msg_data).encode('utf-8'))

#     def kullanicilari_listele(self):
#         msg_data = {'kullanici_adi': self.kullanici_adi, 'command': 'list_kullanicilar'}
#         self.client.send(json.dumps(msg_data).encode('utf-8'))

#     def mesajlari_dinle(self):
#         while True:
#             try:
#                 mesaj = self.client.recv(1024).decode('utf-8')
#                 mesaj = json.loads(mesaj)
#                 if mesaj['command'] == 'kullanici_ekle':
#                     if mesaj['status'] == 'OK':
#                         sub_main(self)
#                         continue
#                     else:
#                         print(Fore.RED + " ! Kullanıcı adı zaten kullanılıyor")
#                         self.kullanici_adi = input("Kullanıcı adı: ")
#                         self.yolla_kullanici_adi()
#                         continue
#                 elif mesaj['command'] == "list_kullanicilar":
#                     clear_screen()
#                     print(Fore.YELLOW + "0.Geri")
#                     for i in range(len(mesaj["kullanicilar"])):
#                         print(Fore.GREEN + f"{i+1}. {mesaj['kullanicilar'][i]}")
#                     secim = input("Seçiminiz: ")
#                     if secim == '0':
#                         sub_main(self)
#                         continue
#                     print(Fore.YELLOW + "0.Geri")
#                     print(Fore.YELLOW + "1.Gruba Ekle")
#                     print(Fore.YELLOW + "2.Mesajları Görüntüle")
#                     print(Fore.YELLOW + "3.Mesaj Gönder")
#                     secim2 = input("Seçiminiz: ")
#                     if secim2 == '1':
#                         h_kisi = mesaj["kullanicilar"][int(secim)-1]
#                         print(Fore.YELLOW + "Gruplar")
#                         print(Fore.YELLOW + "0.Geri")
#                         for i in range(len(self.gruplar)):
#                             print(Fore.GREEN + f"{i+1}. {self.gruplar[i]['title']}")
#                         grup_secim = input("Grup seçiniz: ")
#                         if grup_secim == '0':
#                             sub_main(self)
#                             continue
#                         grup = self.gruplar[int(grup_secim)-1]
#                         if h_kisi not in grup['kisiler']:
#                             grup['kisiler'].append(h_kisi)
#                     elif secim2 == '2':
#                         print(Fore.YELLOW + mesaj[i] + " Son 5 Mesajı")
#                         h_kisi = mesaj[int(secim)-1]
#                         if h_kisi in self.kullanicilar:
#                             for mes in self.kullanicilar[h_kisi]['mesajs'][-5:]:
#                                 if mes['is_me']:
#                                     print(Fore.CYAN + f"{self.kullanici_adi}: {mes['mesaj']}")
#                                 else:
#                                     print(Fore.MAGENTA + f"{h_kisi}: {mes['mesaj']}")

#                                 # filtre = input(Fore.YELLOW + "Geçmiş Mesajlar Arasından Ara:")
#                                 # print(Fore.YELLOW + "*Bulunan Mesajlar")
#                                 # for mes in self.kullanicilar[h_kisi]['mesajs']:
#                                 #     if filtre in mes['mesaj']:
#                                 #         if mes['is_me']:
#                                 #             print(Fore.CYAN + f"{self.kullanici_adi}: {mes['mesaj']}")
#                                 #         else:
#                                 #             print(Fore.MAGENTA + f"{h_kisi}: {mes['mesaj']}")
#                                 # input(Fore.YELLOW + " - Devam etmek için bir tuşa basınız")
#                         else:
#                             print(Fore.RED + " ! Mesaj yok")
#                     elif secim2 == '3':
#                         h_kisi = mesaj["kullanicilar"][int(secim)-1]
#                         mesaj = input(Fore.YELLOW + "Mesajınız: ")
#                         self.yolla_mesaj(mesaj, h_kisi)
#                         msg = {
#                             'mesaj': mesaj,
#                             'is_me': True
#                         }

#                         if h_kisi not in self.kullanicilar:
#                             self.kullanicilar[h_kisi] = {
#                                 'mesajs': []
#                             }
#                             self.kullanicilar[h_kisi]['mesajs'].append(msg)
#                         else:
#                             self.kullanicilar[h_kisi]['mesajs'].append(msg)
#                     elif secim2 == '0':
#                         sub_main(self)
#                         continue
#                 elif mesaj['command'] == "mesaj":
#                     msg = {
#                         'mesaj': mesaj['mesaj'],
#                         'is_me': False
#                     }

#                     if mesaj['sender'] not in self.kullanicilar:
#                         self.kullanicilar[mesaj['sender']] = {
#                             'mesajs': []
#                         }
#                         self.kullanicilar[mesaj['sender']]['mesajs'].append(msg)
#                     else:
#                         self.kullanicilar[mesaj['sender']]['mesajs'].append(msg)
#                     print(Fore.CYAN + f"{mesaj['sender']}: {mesaj['mesaj']}")
#                     continue
#                 sub_main(self)

#             except Exception as e:
#                 print(Fore.RED + "Error", e)
#                 self.client.close()
#                 break

#     def start(self):
#         thread = threading.Thread(target=self.mesajlari_dinle)
#         thread.start()

# def clear_screen():
#     if os.name == 'nt':
#         os.system('cls')
#     else:
#         os.system('clear')

# def main():
#     kullanici_adi = input(Fore.YELLOW + "Kullanıcı adınızı giriniz: ")
#     client = ChatClient(kullanici_adi, host='localhost', port=12345)
#     client.start()

# def sub_main(client):
#     while True:
#         clear_screen()
#         print(Fore.YELLOW + "0.Çıkış")
#         print(Fore.YELLOW + "1.Kullanıcıları Listele")
#         print(Fore.YELLOW + "2.Gruplar")
#         secim = input(Fore.YELLOW + "Seçiminiz: ")
#         if secim == '0':
#             client.client.close()
#             exit()
#         elif secim == '1':
#             clear_screen()
#             client.kullanicilari_listele()
#             return
#         elif secim == '2':
#             clear_screen()
#             print(Fore.YELLOW + "Gruplar")
#             print(Fore.YELLOW + "0.Geri")
#             print(Fore.YELLOW + "1.Grup Oluştur")
#             print(Fore.YELLOW + "2.Grup Seç")
#             secim = input(Fore.YELLOW + "Seçiminiz: ")

#             if secim == '0':
#                 continue
#             elif secim == '1':
#                 print(Fore.YELLOW + "Grup Oluştur")
#                 grup_adi = input(Fore.YELLOW + "*Grup adı: ")
#                 client.gruplar.append({
#                     'title': grup_adi,
#                     'kisiler': []
#                 })
#             elif secim == '2':
#                 print(Fore.YELLOW + "Gruplar")
#                 print(Fore.YELLOW + "0.Geri")
#                 for i in range(len(client.gruplar)):
#                     print(Fore.GREEN + f"{i + 1}. {client.gruplar[i]['title']}")
#                 secim2 = input(Fore.YELLOW + "Seçiminiz: ")
#                 if secim2 == '0':
#                     continue
#                 else:
#                     secili_grup = client.gruplar[int(secim2) - 1]
#                     if len(secili_grup['kisiler']) == 0:
#                         print(Fore.RED + " - Grup boş")
#                     else:
#                         print(Fore.YELLOW + "Grup:" + Fore.GREEN + secili_grup["title"])
#                         print(Fore.YELLOW + "0.Geri")
#                         for i in range(len(secili_grup['kisiler'])):
#                             print(Fore.GREEN + f"{i + 1}. {secili_grup['kisiler'][i]}")
#                         secim3 = input(Fore.YELLOW + "Seçiminiz: ")
#                         if secim3 == '0':
#                             continue
#                         elif int(secim3) > len(secili_grup['kisiler']):
#                             print(Fore.RED + " ! Hatalı seçim")
#                         else:
#                             h_kisi = secili_grup['kisiler'][int(secim3) - 1]
#                             print(Fore.YELLOW + "0.Geri")
#                             print(Fore.YELLOW + "1.Mesaj Gönder")
#                             print(Fore.YELLOW + "2.Mesajları Görüntüle")
#                             secim4 = input(Fore.YELLOW + "Seçiminiz: ")
#                             if secim4 == '0':
#                                 continue
#                             elif secim4 == '1':
#                                 inp = input(Fore.YELLOW + "Mesajınız:")
#                                 msg = {
#                                     'mesaj': inp,
#                                     'is_me': True
#                                 }
#                                 client.yolla_mesaj(inp, h_kisi)
#                                 if h_kisi not in client.kullanicilar:
#                                     client.kullanicilar[h_kisi] = {
#                                         'mesajs': []
#                                     }
#                                     client.kullanicilar[h_kisi]['mesajs'].append(msg)
#                                 else:
#                                     client.kullanicilar[h_kisi]['mesajs'].append(msg)
#                             elif secim4 == '2':
#                                 print(Fore.YELLOW + h_kisi + "*Son 5 Mesajı")
#                                 if h_kisi in client.kullanicilar:
#                                     print(Fore.YELLOW + f"{h_kisi} Son 5 Mesajı")
#                                     target_mesajs = client.kullanicilar[h_kisi]['mesajs']
#                                     # Son 5 mesajı alalım ve en yeni mesajı en üstte gösterelim
#                                     for mes in reversed(target_mesajs[-5:]):
#                                         if mes['is_me']:
#                                             print(Fore.CYAN + f"{client.kullanici_adi}: {mes['mesaj']}")
#                                         else:
#                                             print(Fore.MAGENTA + f"{h_kisi}: {mes['mesaj']}")
#                                     filtre = input(Fore.YELLOW + "Geçmiş Mesajlar Arasından Ara:")
#                                     print(Fore.YELLOW + "* Bulunan Mesajlar")
#                                     for mes in client.kullanicilar[h_kisi]['mesajs']:
#                                         if filtre in mes['mesaj']:
#                                             if mes['is_me']:
#                                                 print(Fore.CYAN + f"{client.kullanici_adi}: {mes['mesaj']}")
#                                             else:
#                                                 print(Fore.MAGENTA + f"{h_kisi}: {mes['mesaj']}")
#                                     if not input(Fore.YELLOW + " - Devam etmek için bir tuşa basınız"):
#                                         break
#                                 else:
#                                     print(Fore.RED + "Mesaj yok")
#                             else:
#                                 continue
#             sub_main(client)

# main()



import socket
import threading
import sqlite3

# Veritabanı bağlantısı ve tablo oluşturma
conn = sqlite3.connect('mesajlar.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS mesajlar
             (gonderen TEXT, alici TEXT, mesaj TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS kullanicilar
             (kullanici_adi TEXT, grup TEXT)''')
conn.commit()

# Sunucu ayarları
HOST = '127.0.0.1'
PORT = 65432

# Kullanıcı listesi
kullanicilar = {}

# Grup listesi
gruplar = {"arkadaslar": [], "aile": [], "diger": []}

# Mesaj alma işlevi
def mesaj_al(conn, addr):
    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if data:
                # Mesajı ayrıştır
                gonderen, alici, mesaj = data.split("|")

                # Mesajı veritabanına kaydet
                c.execute("INSERT INTO mesajlar VALUES (?, ?, ?)", (gonderen, alici, mesaj))
                conn.commit()

                # Mesajı alıcıya gönder
                if alici in kullanicilar:
                    kullanicilar[alici].sendall(data.encode('utf-8'))
                else:
                    conn.sendall("Kullanıcı bulunamadı!".encode('utf-8'))
            else:
                # Bağlantı kapatıldı
                print(f"Kullanıcı bağlantısı kesildi: {addr}")
                del kullanicilar[gonderen]
                conn.close()
                break
        except:
            # Hata oluştu
            print(f"Kullanıcı bağlantısı kesildi: {addr}")
            del kullanicilar[gonderen]
            conn.close()
            break

# Yeni kullanıcı kaydı
def kullanici_kaydet(conn, addr):
    kullanici_adi = conn.recv(1024).decode('utf-8')
    if kullanici_adi not in kullanicilar:
        kullanicilar[kullanici_adi] = conn
        print(f"Yeni kullanıcı bağlandı: {kullanici_adi}")
        conn.sendall("Kayıt başarılı!".encode('utf-8'))

        # Kullanıcıyı varsayılan olarak 'diger' grubuna ekle
        gruplar["diger"].append(kullanici_adi)
        c.execute("INSERT INTO kullanicilar VALUES (?, ?)", (kullanici_adi, "diger"))
        conn.commit()
    else:
        conn.sendall("Kullanıcı adı zaten mevcut!".encode('utf-8'))

# Sunucu başlatma
def sunucu_baslat():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Sunucu {HOST}:{PORT} adresinde dinliyor...")

        while True:
            conn, addr = s.accept()
            print(f"Yeni bağlantı: {addr}")

            # Kullanıcı kaydı veya mesaj alma
            islem = conn.recv(1024).decode('utf-8')
            if islem == "KAYIT":
                kullanici_kaydet(conn, addr)
            elif islem == "MESAJ":
                threading.Thread(target=mesaj_al, args=(conn, addr)).start()

# Kullanıcı arayüzü fonksiyonları
def kullanici_listele():
    print("Kullanıcı Listesi:")
    for kullanici in kullanicilar:
        print(kullanici)

def grup_listele():
    print("Grup Listesi:")
    for grup_adi in gruplar:
        print(f"{grup_adi}: {gruplar[grup_adi]}")

# Ana fonksiyon
if __name__ == "__main__":
    # Sunucuyu başlat
    sunucu_thread = threading.Thread(target=sunucu_baslat)
    sunucu_thread.start()

    # Kullanıcı arayüzü döngüsü
    while True:
        print("\nMenü:")
        print("0. Çıkış")
        print("1. Kullanıcıları Listele")
        print("2. Grupları Listele")

        secim = input("Seçiminizi girin: ")

        if secim == "0":
            print("Çıkış yapılıyor...")
            break
        elif secim == "1":
            kullanici_listele()
        elif secim == "2":
            grup_listele()
        else:
            print("Geçersiz seçim!")

    conn.close()