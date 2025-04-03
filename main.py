import socket
import sys
import time


def send_lines(host: str, port: int, filename: str):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                print(f"Listening to {host}:{port}")
            except socket.error as e:
                print(f'Bind failed. Error: {e}.')
                raise
            s.listen()
            conn, ip = s.accept()
            print(f"Connected to {ip}")

            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        conn.sendall(line.encode('utf-8') + b'\n')
                        print(f"Sent: {line}")
                    except (BrokenPipeError, OSError):
                        print("Connection lost, retrying...")
                        break
                    time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <host> <port> <filename>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]

    send_lines(host, port, filename)
