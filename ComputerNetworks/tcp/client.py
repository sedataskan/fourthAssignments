
import socket
import threading
import json
import os
from colorama import init, Fore

init(autoreset=True)


class ChatClient:
    def __init__(self, username, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.username = username
        self.gruplar = [{
            'title': 'Genel',
            'kisiler': []
        }]
        self.users = dict()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.load_db()
        self.send_username()

    # db.json dosyasına verileri kaydeder ve günceller
    def save_db(self):
        with open('db.json', 'r') as f:
            alldata = json.loads(f.read())
            alldata[self.username] = {
                'users': self.users,
                'gruplar': self.gruplar
            }
        with open('db.json', 'w') as f:
            f.write(json.dumps(alldata))

    # db.json dosyasını yükler ve kullanıcı adına göre verileri alır
    def load_db(self):
        with open('db.json', 'r') as f:
            alldata = json.loads(f.read())
            if self.username in alldata:
                self.users = alldata[self.username]["users"]
                self.gruplar = alldata[self.username]["gruplar"]

    # kullanıcı adını göndermek için
    def send_username(self):
        msg_data = {'username': self.username, 'command': 'add_user'}
        self.client.send(json.dumps(msg_data).encode('utf-8'))

    # mesaj göndermek için
    def send_message(self, message, target_username):
        msg_data = {'username': self.username, 'message': message,
                    'target_username': target_username, 'command': 'msg'}
        self.client.send(json.dumps(msg_data).encode('utf-8'))

    # kullanıcı listesini görmek için
    def kullanicilari_listele(self):
        msg_data = {'username': self.username, 'command': 'list_users'}
        self.client.send(json.dumps(msg_data).encode('utf-8'))

    # gelen mesajları dinlenir
    def listen_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                message = json.loads(message)

                if message['command'] == 'add_user':

                    if message['status'] == 'OK':
                        sub_main(self)
                        continue
                    else:
                        print(Fore.RED + " ! Kullanıcı adı zaten kullanılıyor")
                        self.username = input("Kullanıcı adı: ")
                        self.send_username()
                        continue

                # kullanıcı listesi alındığında
                elif message['command'] == "list_users":
                    clear_screen()

                    print(Fore.GREEN + "Kullanıcılar")
                    print("0.Geri")

                    for i in range(len(message["users"])):
                        print(f"{i+1}. {message['users'][i]}")

                    secim = input("Seçiminiz: ")

                    # geri dönmek için
                    if secim == '0':
                        sub_main(self)
                        continue

                    print("0. Geri")
                    print("1. Gruba Ekle")
                    print("2. Mesajları Görüntüle")
                    print("3. Mesaj Gönder")

                    secim2 = input("Seçiminiz: ")

                    # gruba ekleme işlemi
                    if secim2 == '1':
                        t_user = message["users"][int(secim)-1]

                        print(Fore.GREEN + "Gruplar")
                        print("0. Geri")

                        for i in range(len(self.gruplar)):
                            print(Fore.CYAN +
                                  f"{i+1}. {self.gruplar[i]['title']}")

                        grup_secim = input("Grup seçiniz: ")

                        if grup_secim == '0':
                            sub_main(self)
                            continue

                        grup = self.gruplar[int(grup_secim)-1]

                        if t_user not in grup['kisiler']:
                            grup['kisiler'].append(t_user)

                    # mesajları görmek için
                    elif secim2 == '2':
                        print(
                            Fore.MAGENTA + message["users"][i], " kullanıcısının son 5 mesajı")
                        t_user = message["users"][int(secim)-1]

                        # db.json dosyasından mesajları alıyoruz ve son 5 mesajı gösteriyoruz
                        if t_user in self.users:
                            for mes in self.users[t_user]['messages'][-5:]:
                                if mes['is_me']:
                                    print(Fore.MAGENTA +
                                          f"{self.username}: {mes['message']}")
                                else:
                                    print(Fore.CYAN +
                                          f"{t_user}: {mes['message']}")

                            filtre = input(
                                "\nGeçmiş Mesajlar Arasından Ara:")

                            print(f"\nBulunan Mesajlar")
                            for mes in self.users[t_user]['messages']:
                                if filtre in mes['message']:
                                    if mes['is_me']:
                                        print(Fore.MAGENTA +
                                              f"{self.username}: {mes['message']}")
                                    else:
                                        print(Fore.CYAN +
                                              f"{t_user}: {mes['message']}")

                        else:
                            print(Fore.RED + "! Mesaj yok")

                        input("\n Devam etmek için bir tuşa basınız")
                        sub_main(self)

                    # mesaj göndermek için
                    elif secim2 == '3':
                        t_user = message["users"][int(secim)-1]
                        mesaj = input(Fore.CYAN + "Mesajınız: ")

                        self.send_message(mesaj, t_user)

                        msg = {
                            'message': mesaj,
                            'is_me': True
                        }

                        if t_user not in self.users:
                            self.users[t_user] = {
                                'messages': []
                            }
                            self.users[t_user]['messages'].append(msg)

                        else:
                            self.users[t_user]['messages'].append(msg)

                    else:
                        continue
                # mesaj alındığında
                elif message['command'] == "message":
                    msg = {
                        'message': message['message'],
                        'is_me': False
                    }

                    if message['sender'] not in self.users:
                        self.users[message['sender']] = {
                            'messages': []
                        }
                        self.users[message['sender']]['messages'].append(msg)
                    else:
                        self.users[message['sender']]['messages'].append(msg)

                    continue

                self.save_db()
                sub_main(self)

            except Exception as e:
                print(Fore.RED + "Error", e)
                self.client.close()
                break

    def start(self):
        thread = threading.Thread(target=self.listen_messages)
        thread.start()


def main():
    username = input("Kullanıcı adınızı giriniz: ")
    client = ChatClient(username, host='localhost', port=12345)
    client.start()


def sub_main(client):
    clear_screen()

    print(Fore.GREEN + f"Merhaba {client.username}")
    print("0. Çıkış")
    print("1. Kullanıcıları Listele")
    print("2. Gruplar")

    secim = input(Fore.GREEN + "Seçim: ")

    # cikis yapmak için
    if secim == '0':
        client.client.close()
        exit()

    # kullanıcıları listelemek için
    elif secim == '1':
        clear_screen()
        client.kullanicilari_listele()
        return

    # grup islemleri
    elif secim == '2':
        clear_screen()
        print(Fore.GREEN + "Gruplar")
        print("0. Geri")
        print("1. Grup Oluştur")
        print("2. Grup Seç")

        secim = input("Seçiminiz: ")

        # geri dönmek için
        if secim == '0':
            sub_main(client)

        # grup oluşturmak için
        elif secim == '1':
            print("Grup Oluştur")

            grup_adi = input("Grup adı: ")
            client.gruplar.append({
                'title': grup_adi,
                'kisiler': []
            })

        # grup seçmek için
        elif secim == '2':
            print(Fore.GREEN + "Gruplar")
            print("0. Geri")

            for i in range(len(client.gruplar)):
                print(Fore.LIGHTGREEN_EX +
                      f"{i+1}. {client.gruplar[i]['title']}")

            secim2 = input("Seçiminiz: ")

            # geri dönmek için
            if secim2 == '0':
                sub_main(client)

            # grup seçmek için
            else:
                secili_grup = client.gruplar[int(secim2)-1]
                if len(secili_grup['kisiler']) == 0:
                    print(Fore.RED + " ! Grup boş")
                    input("Devam etmek için bir tuşa basınız")
                    sub_main(client)

                else:
                    print("Grup:", secili_grup["title"])
                    print("0. Geri")

                    for i in range(len(secili_grup['kisiler'])):
                        print(f"{i+1}. {secili_grup['kisiler'][i]}")

                    secim3 = input("Seçiminiz: ")

                    # geri dönmek için
                    if secim3 == '0':
                        sub_main(client)

                    # kullanici sayisindan fazla bir secim yaparsa
                    elif int(secim3) > len(secili_grup['kisiler']):
                        print(Fore.RED + "! Hatalı seçim")
                        input("Devam etmek için bir tuşa basınız")
                        sub_main(client)

                    # kullanıcı ile yapılacak işlemi seçmek için
                    else:
                        t_user = secili_grup['kisiler'][int(secim3)-1]

                        print("0. Geri")
                        print("1. Mesaj Gönder")
                        print("2. Mesajları Görüntüle")

                        secim4 = input("Seçiminiz: ")

                        # geri dönmek için
                        if secim4 == '0':
                            sub_main(client)

                        # mesaj göndermek için
                        elif secim4 == '1':
                            inp = input(Fore.BLUE + "Mesajınız:")
                            msg = {
                                'message': inp,
                                'is_me': True
                            }

                            print("t_user", t_user)

                            client.send_message(inp, t_user)

                            if t_user not in client.users:
                                client.users[t_user] = {
                                    'messages': []
                                }
                                client.users[t_user]['messages'].append(msg)

                            else:
                                client.users[t_user]['messages'].append(msg)

                        # mesajları görmek için
                        elif secim4 == '2':
                            print(t_user,
                                  " kullanıcısının son 5 mesajı")

                            if t_user in client.users:
                                for mes in client.users[t_user]['messages'][-5:]:
                                    if mes['is_me']:
                                        print(Fore.MAGENTA +
                                              f"{client.username}: {mes['message']}")
                                    else:
                                        print(Fore.CYAN +
                                              f"{t_user}: {mes['message']}")

                                # bulunan mesajları filtrelemek için
                                filtre = input(Fore.BLUE +
                                               "\n Geçmiş Mesajlar Arasından Ara:")
                                print(f"\nBulunan Mesajlar")

                                for mes in client.users[t_user]['messages']:
                                    if filtre in mes['message']:
                                        if mes['is_me']:
                                            print(Fore.MAGENTA +
                                                  f"{client.username}: {mes['message']}")
                                        else:
                                            print(Fore.CYAN +
                                                  f"{t_user}: {mes['message']}")
                                input(Fore.YELLOW +
                                      "Devam etmek için bir tuşa basınız")
                            else:
                                print(Fore.RED + " ! Mesaj yok")
                                input(Fore.YELLOW +
                                      "Devam etmek için bir tuşa basınız")
                        else:
                            sub_main(client)
        # kaydedilen verileri güncelle ve alt menüye dön
        client.save_db()
        sub_main(client)


# ekranı temizlemek için
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


main()
