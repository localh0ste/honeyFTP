import socket
import threading

# Fake directory structure
FAKE_DIRS = [
    "drwxr-xr-x   2 user ftp 4096 Feb 15 00:00 logs",
    "drwxr-xr-x   2 user ftp 4096 Feb 15 00:00 projects",
    "-rw-r--r--   1 user ftp 1234 Feb 15 00:00 passwords.txt",
    "-rw-r--r--   1 user ftp 5678 Feb 15 00:00 flag.txt"
]

class ActiveModeFTPServer:
    def __init__(self, host="0.0.0.0", port=21):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[FTP] Running on {self.host}:{self.port}")

    def handle_client(self, client_socket, client_addr):
        print(f"[NEW CONNECTION] {client_addr} connected")
        client_socket.send(b"220 Welcome to Fake FTP Server\r\n")

        authenticated = False
        data_conn = None

        while True:
            try:
                command = client_socket.recv(1024).decode().strip()
                if not command:
                    break

                print(f"[{client_addr}] {command}")

                if command.startswith("USER"):
                    client_socket.send(b"331 User OK, need password\r\n")

                elif command.startswith("PASS"):
                    authenticated = True
                    client_socket.send(b"230 Login successful\r\n")

                elif command.startswith("SYST"):
                    client_socket.send(b"215 UNIX Type: L8\r\n")

                elif command.startswith("FEAT"):
                    client_socket.send(b"211 No features available\r\n")

                elif command.startswith("PWD"):
                    client_socket.send(b'257 "/home/user" is the current directory\r\n')

                elif command.startswith("CWD"):
                    client_socket.send(b"250 Directory successfully changed\r\n")

                elif command.startswith("MKD"):
                    client_socket.send(b"257 Directory created\r\n")

                elif command.startswith("RMD"):
                    client_socket.send(b"250 Directory removed\r\n")

                elif command.startswith("PORT"):  # Active Mode Handling
                    parts = command.split(" ")[1].split(",")
                    data_host = ".".join(parts[:4])
                    data_port = int(parts[4]) * 256 + int(parts[5])
                    data_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    data_conn.connect((data_host, data_port))
                    client_socket.send(b"200 PORT command successful\r\n")

                elif command in ["LIST", "LS", "DIR"]:
                    if not data_conn:
                        client_socket.send(b"425 Use PORT first\r\n")
                        continue

                    client_socket.send(b"150 Opening data connection for directory listing\r\n")
                    response = "\r\n".join(FAKE_DIRS) + "\r\n"
                    data_conn.send(response.encode())
                    data_conn.close()
                    client_socket.send(b"226 Directory listing sent successfully\r\n")

                elif command == "QUIT":
                    client_socket.send(b"221 Goodbye!\r\n")
                    break

                else:
                    client_socket.send(b"500 Unknown command\r\n")

            except ConnectionResetError:
                break

        print(f"[DISCONNECTED] {client_addr} disconnected")
        client_socket.close()

    def start(self):
        while True:
            client_socket, client_addr = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_addr))
            client_thread.start()

if __name__ == "__main__":
    ftp_server = ActiveModeFTPServer()
    ftp_server.start()
