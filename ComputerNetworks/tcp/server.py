import socket
import threading
import json
from colorama import init, Fore, Style

init(autoreset=True)  # Colorama'yı başlat ve renkleri otomatik sıfırla

# server
class ChatServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = {}  # Kullanıcı adını ve bağlantıyı saklamak için
        

    def handle_client(self, client, addr):
        kullanici_adi = None
        while True:
            try:
                mesaj = client.recv(1024).decode('utf-8')
                # dict olarak gelen mesajı parse ediyoruz
                msg_data = json.loads(mesaj)
                kullanici_adi = msg_data['kullanici_adi']
                # kullanici_ekle komutu, sisteme kullanıcı eklemek için 
                if msg_data['command'] == 'kullanici_ekle':
                    if kullanici_adi in self.clients:
                        client.send(json.dumps({'command': 'kullanici_ekle', 'status': 'FAIL'}).encode('utf-8')) # kullanıcı adı zaten varsa
                        print(Fore.RED + f"{kullanici_adi} zaten bağlı.")
                    else:
                        self.clients[kullanici_adi] = {'connection': client, 'groups': []}
                        print(Fore.GREEN + f"{kullanici_adi} bağlandı.")
                        client.send(json.dumps({'command': 'kullanici_ekle', 'status': 'OK'}).encode('utf-8'))

                else: 
                    # kullanici_ekle dışındaki mesajlar, mesaj işleme fonksiyonuna gönderiliyor
                    self.process_mesaj(msg_data)

            except Exception as e:
                print(Fore.RED + f"Error: {e}")
                client.close()
                if kullanici_adi:
                    del self.clients[kullanici_adi]
                    print(Fore.YELLOW + f"- {kullanici_adi} bağlantı listesinden çıkarıldı.")
                break

    def process_mesaj(self, msg_data):
        kullanici_adi = msg_data['kullanici_adi']
        mesaj = msg_data.get('mesaj', None)
        hedef_kisi = msg_data.get('hedef_kisi', None)
        command = msg_data.get('command', None)

        print(Fore.BLUE + str(msg_data))

        # sisteme giriş yapan kullanıcılar, bu komut ile diğer kullanıcıları görebilir
        if command == "list_kullanicilar":
            self.kullanici_listesi_yolla(kullanici_adi)
            return
        # mesaj göndermek için
        if command == 'msg':
            self.kullaniciya_yolla(mesaj, hedef_kisi, kullanici_adi)

            with open('messages.txt', 'a') as f:
                f.write(f"{kullanici_adi}: {hedef_kisi}: {mesaj}\n")

            
    # clienta mesaj göndermek için
    def kullaniciya_yolla(self, mesaj, hedef_kisi, sender):
        if hedef_kisi in self.clients:
            answer = {'command': 'mesaj', 'mesaj': mesaj, 'sender': sender}
            target_client = self.clients[hedef_kisi]['connection']
            target_client.send(json.dumps(answer).encode('utf-8'))
            print(Fore.MAGENTA + f"Mesaj gönderildi: {sender} to {hedef_kisi}: {mesaj}")
        else:
            print(Fore.RED + f"Kullanıcı {hedef_kisi} bulunamadı.")
    
    # sisteme giriş yapan kullanıcılar, bu komut ile diğer kullanıcıları görebilir
    def kullanici_listesi_yolla(self, kullanici_adi):
        user_list = list(self.clients.keys())
        user_list.remove(kullanici_adi)
        answer = {'command': 'list_kullanicilar', 'kullanicilar': user_list}
        target_client = self.clients[kullanici_adi]['connection']
        target_client.send(json.dumps(answer).encode('utf-8'))
        print(Fore.GREEN + f"Kullanıcı listesi gönderildi {kullanici_adi}")

    # serverı başlat
    def start(self):
        print(Fore.CYAN + "Server başlatıldı...")
        while True:
            client, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client, addr))
            thread.start()
            print(Fore.CYAN + f"Yeni bağlantı: {addr}")

def main():
    # Server'ı başlat
    server = ChatServer(host='localhost', port=12345)
    server.start()

main()
