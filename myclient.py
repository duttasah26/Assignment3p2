import socket, threading, json

def connect(client):
    print('\n' + ("=" * 20) + "\nAssignment 3 - Client\n")

    while True:
        operator = input("Enter desired operation ('ADD', 'SUB', 'MULT', 'DIV', 'MOD', 'SQRT'): ")

        if operator.upper() not in ['ADD', 'SUB', 'MULT', 'DIV', 'MOD', 'SQRT']:
            print("Invalid operation. Please choose from ['ADD', 'SUB', 'MULT', 'DIV', 'MOD', 'SQRT'].\n")
            continue

        try:
            num1 = int(input("Enter the first number for the math operation: "))
            num2 = None

            if operator != "SQRT":
                num2 = int(input("Enter the second number for the math operation: "))

        except ValueError:
            print("Invalid input. Please enter only valid integers.\n")
            continue

        request = json.dumps({ "num1": num1, "num2": num2, "op": operator })
        client.send(request.encode('ascii'))

        response = json.loads(client.recv(1024).decode('ascii'))
        print(f"Result: {response.get('result')}\n")

if __name__ == "__main__":
    """ creating socket and connecting to server """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "mysocketserver"        # connects to mysocketserver on docker on port 8080
    port = 8080
    client.connect((host, port))

    """ running client in thread """
    client_thread = threading.Thread(target=connect, args=(client,))
    client_thread.start()