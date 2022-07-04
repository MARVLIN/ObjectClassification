
# ----- A simple TCP client program in Python using send() function -----

import socket



# Create a client socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);



# Connect to the server

clientSocket.connect(("23.254.176.188" ,8000));



# Send data to server

data = "Hello Server!";

clientSocket.send(data.encode());



# Receive data from server

dataFromServer = clientSocket.recv(1024);



# Print to the console

print(dataFromServer.decode());

