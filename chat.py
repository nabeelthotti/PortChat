import sys
import socket
import threading

class Chat:

    def __init__(self):
        self.connections = []  # List to keep track of (conn, addr, id) tuples
        self.next_id = 1  # Unique identifier for each connection
        self.lock = threading.Lock()
        self.shutdown_event = threading.Event() #Event to signal shutdown

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            #response = requests.get("https://ipinfo.io/ip")
            #ip_addr = response.text
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            s.connect((ip, 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def handle_client(self, conn: socket, addr: str, id: int):
        print(f"New connection from {addr}, id: {id}")
        try:
            while not self.shutdown_event.is_set():
                try: 
                    msg = conn.recv(1024).decode('utf-8')
                    if not msg:
                        break
                    print(f"Message received from {addr[0]}")
                    print(f"Sender's Port: {addr[1]}")
                    print(f"Message: \"{msg}\"")
                except socket.error:
                    break
        except Exception as e:
            print(f"Error with connection id {id}: {e}")
        finally:
            with self.lock:
                self.connections = [(c, a, i) for c, a, i in self.connections if i != id]
            conn.close()
            print(f"Connection id {id} closed.") 

    def accept_connections(self, server_socket):
        server_socket.settimeout(1)  # Allows the accept call to timeout periodically
        while not self.shutdown_event.is_set(): 
            # this prevents the method from blocking indefinitely on recv() and allows threads to exit if a shutdown is signaled.
            try:
                conn, addr = server_socket.accept()
                with self.lock:
                    self.connections.append((conn, addr, self.next_id))
                    thread = threading.Thread(target=self.handle_client, args=(conn, addr, self.next_id))
                    thread.start()
                    self.next_id += 1
            except socket.timeout:
                continue
            except socket.error as e:
                if not self.shutdown_event.is_set():
                    print(f"Socket error: {e}")
                break


    def connect_to_peer(self, dest, port):
        try:
            peer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_sock.connect((dest, port))
            with self.lock:
                self.connections.append((peer_sock, (dest, port), self.next_id))
                thread = threading.Thread(target=self.handle_client, args=(peer_sock, (dest, port), self.next_id))
                thread.start()
                print(f"Connected to {dest}:{port} with connection id {self.next_id}")
                self.next_id += 1
        except Exception as e:
            print(f"Failed to connect to {dest}:{port}: {e}")

def main(port):
    chatter = Chat()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('', port))
        server_socket.listen()
        print(f"Listening on port {port}")
        threading.Thread(target=chatter.accept_connections, args=(server_socket,), daemon=False).start()

    except Exception as e:
        print(f"Failed to bind socket on port {port}: {e}")
        sys.exit()
    
    my_ip = chatter.get_ip()

    while True:
        cmd = input().split()
        if not cmd:
            continue

        if cmd[0] == 'exit':
            print("Closing all connections and terminating process.")
            chatter.shutdown_event.set()  # Signal all threads to shutdown  
            for conn, _, _ in list(chatter.connections): # # Use a list copy for safe iteration
                conn.close()
            server_socket.close()
            # Ensure all threads finish
            main_thread = threading.current_thread()
            for t in threading.enumerate():
                if t is not main_thread:
                    t.join()
            break
        elif cmd[0] == 'help':
            print("Available commands:\nhelp, myip, myport, connect <destination> <port>, list, terminate <id>, send <id> <message>, exit")
        elif cmd[0] == 'myip':
            print(f"My IP address is {my_ip}")
        elif cmd[0] == 'myport':
            print(f"Listening on port {port}")
        elif cmd[0] == 'connect' and len(cmd) == 3:
            has_error = False
            if my_ip == cmd[1] and port == int(cmd[2]):
                print("Error: Connecting to yourself is not allowed.")
                has_error = True
            for connection in chatter.connections:
                if connection[1][0] == cmd[1] and connection[1][1] == int(cmd[2]):
                    print("Error: You are already connected to that peer.")
                    has_error = True
                    break
            if (not has_error):
                chatter.connect_to_peer(cmd[1], int(cmd[2]))
        elif cmd[0] == 'list':
            print("id: IP address Port No.")
            for conn, addr, id in chatter.connections:
                    # Use getsockname to get the local endpoint details
                    local_ip, local_port = conn.getsockname()
                    print(f"{id}: {local_ip} {local_port}")

        elif cmd[0] == 'terminate' and len(cmd) == 2:
            terminate_id = int(cmd[1])
            terminated = False
            with chatter.lock:
                # use list to safely iterate
                for conn, addr, id in list(chatter.connections):
                    if id == terminate_id:
                        conn.close()
                        # connection list is correctly updated without trying to modify it during iteration.
                        chatter.connections = [(c, a, i) for c, a, i in chatter.connections if i != id]
                        terminated = True
                        print(f"Terminated connection {terminate_id}")
                        break
            if not terminated:
                print(f"No connection found with id {terminate_id}")
        elif cmd[0] == 'send' and len(cmd) >= 3:
            send_id = int(cmd[1])
            message = " ".join(cmd[2:])
            print("Sending message: " + message)
            sent = False
            with chatter.lock:
                for conn, addr, id in chatter.connections:
                    if id == send_id:
                        conn.sendall(message.encode('utf-8'))
                        print(f"Message sent to {send_id} Successfully")  # Modified output for success
                        sent = True
                        break
            if not sent:
                print(f"No connection found with id {send_id}")
        else:
            print(f"{cmd} is not a valid option. Type 'help' for more options.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python chat.py <listening_port>")
        sys.exit()
    main(int(sys.argv[1]))
