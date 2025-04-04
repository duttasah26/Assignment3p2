import math
import Pyro4

@Pyro4.expose
class MathOperations:

    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return a / b
    
    def sqrt(self, a):
        if a < 0:
            raise ValueError("Cannot calculate square root of a negative number.")
        return math.sqrt(a)
    
    def modulus(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Modulus by zero is not allowed.")
        return a % b

def main():
    #pyro server setup
    #'host="pyroserver"' binds the daemon to a hostname inside the Docker network
    #'port=0' lets Pyro pick a random available port
    daemon = Pyro4.Daemon(host="pyroserver", port=0)
    #Connecting to the Pyro name server (running on 'pyronaming', port 9090 inside Docker)
    ns = Pyro4.locateNS(host="pyronaming", port=9090)
    #Register math operations object with the Pyro daemon
    uri= daemon.register(MathOperations)
    # Register the object in the name server under the name "math.operations"
    ns.register("math.operations", uri)
    print("Pyro4 server waiting for requests..")
    # starting request loop
    daemon.requestLoop()

if __name__ == "__main__":
    main()