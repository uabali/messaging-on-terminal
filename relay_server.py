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
        print(f"\nBroadcasting message: {message}")
        print(f"Active users: {len(self.clients)}")
        
        for client_id, (client, username) in self.clients.items():
            if client_id != sender_id:
                try:
                    client.send(message.encode('utf-8'))
                    print(f"Message sent to user {username}")
                except Exception as e:
                    print(f"Failed to send message to {username}: {e}")
                    self.remove_client(client_id)
            else:
                print(f"Message not sent to sender ({username})")
    
    def remove_client(self, client_id):
        if client_id in self.clients:
            client, username = self.clients[client_id]
            client.close()
            del self.clients[client_id]
            print(f"User removed: {username} (ID: {client_id})")
    
    def handle_client(self, client, client_id):
        try:
            # First message will be username
            username = client.recv(1024).decode('utf-8')
            self.clients[client_id] = (client, username)
            print(f"\nNew user connected: {username} (ID: {client_id})")
            print(f"Active user count: {len(self.clients)}")
            
            while True:
                message = client.recv(1024).decode('utf-8')
                if not message:
                    break
                    
                # Forward message to other users
                formatted_message = f"{username}: {message}"
                self.broadcast(formatted_message, client_id)
                
        except Exception as e:
            print(f"User error ({username}): {e}")
        finally:
            print(f"\nUser disconnected: {username} (ID: {client_id})")
            self.remove_client(client_id)
            print(f"Remaining user count: {len(self.clients)}")
    
    def start(self):
        print("\n=== Relay Server Started ===")
        print(f"Local IP: {socket.gethostbyname(socket.gethostname())}")
        print(f"Port: 5003")
        print("================================\n")
        
        while True:
            client, addr = self.server.accept()
            print(f"\nNew connection: {addr}")
            
            # Start a new thread for each connection
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
        print(f"Error occurred: {e}") 