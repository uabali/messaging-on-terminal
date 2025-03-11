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
                    print("\nServer connection lost!")
                    sys.exit(1)
                print(f"\n{message}")
            except Exception as e:
                print(f"\nError receiving message: {e}")
                sys.exit(1)
    
    def start(self):
        try:
            print(f"\nConnecting to server: {self.host}:{self.port}")
            # Connect to server
            self.client.connect((self.host, self.port))
            print("Connected to server!")
            
            # Send username
            username = input("\nEnter your username: ")
            self.client.send(username.encode('utf-8'))
            print("Username sent!")
            
            # Start message receiving thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            print("\nYou can start messaging! (Type 'q' to quit)")
            print("==================================================\n")
            
            # Message sending loop
            while True:
                message = input("")
                if message.lower() == 'q':
                    break
                try:
                    self.client.send(message.encode('utf-8'))
                    print("Message sent!")
                except Exception as e:
                    print(f"Failed to send message: {e}")
                    break
                
        except ConnectionRefusedError:
            print(f"\nError: Could not connect to {self.host}:{self.port}!")
            print("Make sure the server is running.")
            sys.exit(1)
        except Exception as e:
            print(f"\nConnection error: {e}")
            sys.exit(1)
        finally:
            print("\nClosing connection...")
            self.client.close()

if __name__ == "__main__":
    try:
        # Get server IP address
        server_ip = input("Enter server IP (example: 0.tcp.ngrok.io): ").strip()
        server_port = int(input("Enter port number (example: 12345): ").strip())
        
        # Start client
        client = RelayClient(server_ip, server_port)
        client.start()
    except ValueError:
        print("Error: Invalid port number!")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nProgram terminated.")
        sys.exit(0) 