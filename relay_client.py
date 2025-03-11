import socket
import threading
import sys

class RelayClient:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        
    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if not message:
                    print("\nSunucu baglantisi kesildi!")
                    sys.exit(1)
                print(f"\n{message}")
            except Exception as e:
                print(f"\nMesaj alma hatasi: {e}")
                sys.exit(1)
    
    def start(self):
        try:
            print(f"\nSunucuya baglaniliyor: {self.host}:{self.port}")
            # Sunucuya bağlan
            self.client.connect((self.host, self.port))
            print("Sunucuya baglandi!")
            
            # Kullanıcı adını gönder
            username = input("\nKullanici adinizi girin: ")
            self.client.send(username.encode('utf-8'))
            print("Kullanici adi gonderildi!")
            
            # Mesaj alma thread'ini başlat
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            print("\nMesajlasmaya baslayabilirsiniz! (Cikmak icin 'q' yazin)")
            print("==================================================\n")
            
            # Mesaj gönderme döngüsü
            while True:
                message = input("")
                if message.lower() == 'q':
                    break
                try:
                    self.client.send(message.encode('utf-8'))
                    print("Mesaj gonderildi!")
                except Exception as e:
                    print(f"Mesaj gonderilemedi: {e}")
                    break
                
        except ConnectionRefusedError:
            print(f"\nHata: {self.host}:{self.port} adresine baglanilamadi!")
            print("Sunucunun calistigindan emin olun.")
            sys.exit(1)
        except Exception as e:
            print(f"\nBaglanti hatasi: {e}")
            sys.exit(1)
        finally:
            print("\nBaglanti kapatiliyor...")
            self.client.close()

if __name__ == "__main__":
    try:
        # Sunucu IP adresini al
        server_ip = input("Sunucu IP adresini girin (ornek: 0.tcp.ngrok.io): ").strip()
        server_port = int(input("Port numarasini girin (ornek: 12345): ").strip())
        
        # İstemciyi başlat
        client = RelayClient(server_ip, server_port)
        client.start()
    except ValueError:
        print("Hata: Gecersiz port numarasi!")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nProgram sonlandirildi.")
        sys.exit(0) 