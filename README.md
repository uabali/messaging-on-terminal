# Simple TCP/IP Messaging Application

A simple TCP/IP-based messaging system that enables communication between different computers using a relay server architecture.

## Features

- Real-time messaging between multiple clients
- Relay server architecture for handling multiple connections
- Support for usernames and basic chat functionality
- Cross-platform compatibility (Windows, macOS, Linux)
- Ngrok integration for easy remote access

## Prerequisites

### System Requirements
- Python 3.x
- Internet connection
- Ngrok (for server-side)

### Python Libraries
- socket (built-in)
- threading (built-in)
- json (built-in)
- colorama (optional, for colored terminal output)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/messaging-app.git
   cd messaging-app
   ```

2. **Install required Python packages**
   ```bash
   pip install colorama==0.4.6
   ```

3. **Install Ngrok**
   - Download from [https://ngrok.com/download](https://ngrok.com/download)
   - Or install via package managers:
     ```bash
     # macOS (using Homebrew)
     brew install ngrok

     # Windows (using Chocolatey)
     choco install ngrok
     ```

## Usage

### Server Side Setup

1. **Start the relay server:**
   ```bash
   python relay_server.py
   ```

2. **Start Ngrok** (in a new terminal):
   ```bash
   ngrok tcp 5003
   ```

3. **Note the Ngrok URL**
   - You'll see a URL like: `tcp://0.tcp.ngrok.io:12345`
   - Share the hostname (e.g., `0.tcp.ngrok.io`) and port number (e.g., `12345`) with clients

### Client Side Setup

1. **Run the client application:**
   ```bash
   python relay_client.py
   ```

2. **When prompted:**
   - Enter the server IP (e.g., `0.tcp.ngrok.io` - without `tcp://`)
   - Enter the port number (e.g., `12345`)
   - Enter your username

## Project Structure

```
messaging-app/
├── relay_server.py    # Server application
├── relay_client.py    # Client application
└── README.md         # Documentation
```

## Important Notes

### For Server Operators
- The server must be running before clients can connect
- Ngrok URL changes each time you restart Ngrok
- Share the new Ngrok URL and port with clients each time you restart
- Default server port is 5003

### For Clients
- Ensure you have the correct Ngrok URL and port
- Don't include `tcp://` when entering the server IP
- Make sure Python and required libraries are installed

## Troubleshooting

### Common Issues and Solutions

1. **Connection Error**
   - Verify the server is running
   - Check if Ngrok is running
   - Ensure correct IP and port
   - Don't include `tcp://` in the server IP

2. **Port Already in Use**
   - Change the port in `relay_server.py`
   - Check for other applications using port 5003
   - Kill existing processes using the port

3. **Ngrok Issues**
   - Ensure Ngrok is properly installed
   - Check your internet connection
   - Verify Ngrok authentication (if required)

### Error Messages

- "Could not connect to server": Check if server is running and Ngrok URL is correct
- "Port already in use": Choose a different port or close competing applications
- "Connection refused": Verify firewall settings and server availability

## Security Considerations

- This is a basic implementation without encryption
- Use only in trusted networks
- Don't share sensitive information
- For educational purposes only

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request


## Acknowledgments

- Built with Python's socket programming
- Uses Ngrok for tunnel creation
- Inspired by basic chat applications