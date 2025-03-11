import socket
import threading
import json

class RelayServer:
    def __init__(self, host='0.0.0.0', port=5003):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = {}  # {client_id: (connection, username)}
        self.client_id_counter = 0
        
    def broadcast(self, message, sender_id):
        print(f"\nMesaj yayinlaniyor: {message}")
        print(f"Aktif kullanicilar: {len(self.clients)}")
        
        for client_id, (client, username) in self.clients.items():
            if client_id != sender_id:
                try:
                    client.send(message.encode('utf-8'))
                    print(f"Mesaj {username} kullanicisina gonderildi")
                except Exception as e:
                    print(f"Mesaj gonderilemedi ({username}): {e}")
                    self.remove_client(client_id)
            else:
                print(f"Mesaj gonderici kullaniciya ({username}) gonderilmedi")
    
    def remove_client(self, client_id):
        if client_id in self.clients:
            client, username = self.clients[client_id]
            client.close()
            del self.clients[client_id]
            print(f"Kullanici silindi: {username} (ID: {client_id})")
    
    def handle_client(self, client, client_id):
        try:
            # İlk mesaj kullanıcı adı olacak
            username = client.recv(1024).decode('utf-8')
            self.clients[client_id] = (client, username)
            print(f"\nYeni kullanici baglandi: {username} (ID: {client_id})")
            print(f"Aktif kullanici sayisi: {len(self.clients)}")
            
            while True:
                message = client.recv(1024).decode('utf-8')
                if not message:
                    break
                    
                # Mesajı diğer kullanıcılara ilet
                formatted_message = f"{username}: {message}"
                self.broadcast(formatted_message, client_id)
                
        except Exception as e:
            print(f"Kullanici hatasi ({username}): {e}")
        finally:
            print(f"\nKullanici ayrildi: {username} (ID: {client_id})")
            self.remove_client(client_id)
            print(f"Kalan kullanici sayisi: {len(self.clients)}")
    
    def start(self):
        print("\n=== Relay Sunucusu Baslatildi ===")
        print(f"Yerel IP: {socket.gethostbyname(socket.gethostname())}")
        print(f"Port: 5003")
        print("================================\n")
        
        while True:
            client, addr = self.server.accept()
            print(f"\nYeni baglanti: {addr}")
            
            # Her bağlantı için yeni bir thread başlat
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client, self.client_id_counter)
            )
            client_thread.start()
            
            self.client_id_counter += 1

if __name__ == "__main__":
    try:
        server = RelayServer()
        server.start()
    except Exception as e:
        print(f"Hata olustu: {e}") 