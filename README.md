# Chat Application

## Overview
This Chat application enables simple network-based text communication between multiple clients using a server-client architecture. Built with Python and utilizing sockets along with threading, the application supports multiple concurrent client connections, sending and receiving messages, and managing connections dynamically.

## Features
- **Listening for Incoming Connections**: The server listens on a specified port and accepts incoming client connections.
- **Handling Multiple Clients**: Multiple clients can connect simultaneously, with each client handled in a separate thread.
- **Sending and Receiving Messages**: Clients can send messages to the server, which then displays the messages.
- **Connection Management**: Clients can be dynamically connected and disconnected.
- **Command-Based Interaction**: Users interact with the server via commands like `connect`, `send`, and `exit`.

## Prerequisites
To run this application, you need:
- Python 3 installed on your system, which you can download from [Python's official site](https://www.python.org/downloads/).

## Installation
No additional libraries are required for the basic operation of this chat application as it uses Python's standard libraries (`sys`, `socket`, `threading`). Simply download the chat application script to your local machine.

## Building the Program
No build process is required for this Python script as it is an interpreted script. Ensure you have Python installed, and you are ready to run the application.

## Running the Application
To start the server:
1. Open your command line interface (CLI).
2. Navigate to the directory containing the `chat.py` script.
3. Run the script with Python and specify a port number for the server to listen on: 
    **python3 chat.py <listening_port>** (Replace `<listening_port>` with the port number you want the server to listen on, for example: python3 chat.py 8080


## Using the Application
Once the server is running, it listens for incoming connections. You can interact with the server using the following commands:

- `help`: Displays the list of available commands.
- `myip`: Displays the IP address of the server.
- `myport`: Displays the port on which the server is listening.
- `connect <destination> <port>`: Connects to another peer (e.g., `connect 192.168.1.5 9090`).
- `list`: Lists all active connections with their IDs, IP addresses, and port numbers.
- `terminate <id>`: Terminates the connection with the specified ID.
- `send <id> <message>`: Sends a message to a specific connection.
- `exit`: Closes all connections and shuts down the server.

## Contributors
- **Nabeel Thotti and Todd Marcus**: 
    - The project was completed through multiple pair-programming and debugging sessions.
    - Both of us had some experience with python programming but had never used the socket or threading modules.
    - We first made sure running the script would handle command line arguments.
    - Then we added cases for each of the features required to our main loop.
    - After that we looked up documentation on how to setup a socket in python.
    - Seeing that a lot potentially simultaneous operations would occur with connecting, sending, and receiving we started looking into threading.
    - We found that having locks around the critical sections seemed to allow for most behavior to work as expected.
    - While trying to resolve an issue with sending we decided it would be easier to reorganize most of the code into a class now that we understood the modules a little better.
    - One of the final issues resolved was some exceptions including a python interpreter exception resulting from worker threads trying to execute after their parent thread had already been joined. This was resolved by using an event handler to stop the run loop condition while the thread was waiting to be joined.
    - After that it seemed like things were working as expected.
    - Nabeel did the majority of the driving since testing the code on his Mac was more convenient for testing Unix behavior. When encountering issues it was mostly divide and conquer and then go with the changes both of us think handled the problem better. Todd tested the code on an Ubuntu VM and Windows once we thought we had completed a requirement.

For further assistance, refer to Python's [official documentation](https://docs.python.org/3/) on sockets and threading.