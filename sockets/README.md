## Sockets

One of the things we touched upon was networking, specifically sockets. We discussed `netc` first and played around with it for a bit, before we ended up discussing how socket works:

* A server listens for connections on a port, and then sets up a socket to maintain connection with clients.
* Server can then receive or send data with this client.
* If you manage connections with clients, you can send data betweeen clients using forwarding.

Afterwards, we were subjected to building our own chat servers. Here's a walkthrough of that, written with no external libraries. It had to meet the following requirements:

- [X] The server should be able to handle multiple clients at once.
- [X] The server should broadcast messages to all clients.
- [ ] The server should send a message to the chatroom when a new client joins the chat room.
- [X] The server should send a message to the chatroom when a client leaves the chat room.
- [X] The client should be able to send messages to the server.
- [ ] The client should be able to receive messages from the server.
- [ ] The client should be able to gracefully exit the chat room.
- [X] The client should have a username, which is sent to the server when the client joins the chat room.
- [X] The server should keep track of all clients in the chat room.
- [X] The client is defined by:
  - [X] Username
  - [X] IP address
  - [X] Password
  - [X] Unique ID
- [X] The server is defined by:
  - [X] IP address
  - [X] Port
- [X] A message in the chat room is defined by:
  - [X] Sender (the client ID)
  - [X] Payload (the message)
  - [X] Timestamp
  - [X] Chatroom ID
  - [X] Unique ID
- [X] The chat room is defined by:
  - [X] Name
  - [X] Unique ID

The code is definitely questionable. (We use files as databases and read them in full every time we need to update them, for one.)

[I](https://jianminchen.com) took this one step further and built [`faceterm`](https://github.com/jianmin-chen/faceterm), which lets you FaceTime in the terminal using sockets! A writeup on how this works can be found [here](https://jianminchen.com).