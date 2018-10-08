# File-transfer
tcp sending files from clients to the server

`fileClient.py` and `fileServer.py` are a demonstration TCP client and server which exchange frames consisting of byte arrays in the form payload_length:payload where payload_length is in decimal.

* `fileServer` also uses `fork()` to handle multiple simultaneous clients.    

*  The -? (usage) option prints parameters and default values.

*  `framedSock.py` holds the common code used in the client and server including framed send and receive.

To run this first run the fileServer.py and then run the fileClient.py in one or multiple command lines
then as a client is a command called "put" where you can send files to the server.
ex. put "test.txt".

* Notice that you can only send 100 bytes long.
