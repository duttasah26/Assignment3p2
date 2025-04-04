import socket
import threading
import Pyro4
import json

class Server:
    def __init__(self, host='0.0.0.0', port=8080):
        # Host '0.0.0.0' binds to all interfaces inside the container
        # Port 8080 is the socket server port exposed for client connections
        self.host = host
        self.port = port
        self.is_running = False
        self.socket = None
        # Connecting to the Pyro name server (which gives us access to the remote MathOperations object)
        self.server = Pyro4.Proxy("PYRONAME:math.operations")

    def start_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print(f"Server started on {self.host}:{self.port}")
            self.is_running = True

            while self.is_running:
                client_socket, addr = self.socket.accept()
                print(f"Connected with {addr}")

                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,addr))
                client_thread.daemon = True
                client_thread.start()

        except Exception as e:
            print(f"Server error: {e}")

        finally:
            self.stop_server()

    def handle_client(self, conn, addr):
        with conn:
            while True:
                data = conn.recv(2048).decode('ascii')

                if not data:
                    break

                try:
                    data = json.loads(data)
                    operation = data.get("op")
                    num1 = data.get("num1")
                    num2 = data.get("num2")
                    
                    if not isinstance(num1, (int, float)):
                        raise ValueError("First operand must be a number.")
                    if operation != "SQRT" and not isinstance(num2, (int, float)):
                        raise ValueError("Second operand must be a number.")

                    if operation == "ADD":
                        res = self.server.add(num1, num2)
                    
                    elif operation == "SUB":
                        res = self.server.subtract(num1, num2)

                    elif operation == "MULT":
                        res = self.server.multiply(num1, num2)

                    elif operation == "DIV":
                        if num2 == 0:
                            raise ZeroDivisionError("Cannot divide by zero.")
                        
                        res = self.server.divide(num1, num2)

                    elif operation == "MOD":
                        if num2 == 0:
                            raise ZeroDivisionError("Cannot modulus by zero.")
                        res = self.server.modulus(num1, num2)

                    elif operation == "SQRT":
                        if num1 < 0:
                            raise ValueError("Cannot calculate square root of a negative number.")
                        res = self.server.sqrt(num1)

                    else:
                        res = "Error: Unknown operation"

                    result = {"status": "ok", "result": res}

                except (ValueError, ZeroDivisionError) as e:
                    result = {"status": "error", "result": f"Unexpected error: {str(e)}"}

                conn.sendall(json.dumps(result).encode())  

    def stop_server(self):
        print("Stopping server...")
        self.is_running = False
        if self.socket:
            self.socket.close() 

if __name__ == "__main__":
    server = Server()
    server.start_server()