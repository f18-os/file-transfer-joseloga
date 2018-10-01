# nets-tcp-framed-echo
tcp echo with framing

Directory `file-transfer-lab` includes a tcp echo server & client

*  `fileClient.py` and `fileServer.py` are a demonstration TCP client and server which exchange frames consisting of byte arrays in the form payload_length:payload where payload_length is in decimal.

* `fileServer` also uses `fork()` to handle multiple simultaneous clients.    

*  The -? (usage) option prints parameters and default values.

*  `framedSock.py` holds the common code used in the client and server including framed send and receive.
