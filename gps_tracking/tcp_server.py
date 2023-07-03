import threading
import socket

# IMEI length offset
IMEI_LENGTH_OFFSET = 2

class TCPThread(threading.Thread):
    def __init__(self, client_sock, client_addr):
        super().__init__()
        self.client_sock = client_sock
        self.client_addr = client_addr

    def run(self):
        print(f"Client connected: {self.client_addr}")

        # Receive the IMEI packet from the client
        imei_packet = self.client_sock.recv(IMEI_LENGTH_OFFSET + 15)  # Adjust the buffer size as per the IMEI length

        # Extract IMEI length
        imei_length = int.from_bytes(imei_packet[:IMEI_LENGTH_OFFSET], 'big')

        # Extract IMEI as text
        imei = imei_packet[IMEI_LENGTH_OFFSET:].decode()

        print("Received IMEI:", imei)

        # Determine if the server accepts data from this module
        if should_accept_data(imei):  # Implement your logic to determine acceptance
            # Send acceptance confirmation (01)
            self.client_sock.sendall(b'\x01')
            print("Data accepted from the module")
        else:
            # Send rejection confirmation (00)
            self.client_sock.sendall(b'\x00')
            print("Data rejected from the module")
            self.client_sock.close()
            return

        while True:
            # Receive the AVL data packet from the client
            avl_packet = self.client_sock.recv(1024)  # Adjust the buffer size as per your requirements

            # Parse the AVL packet
            # ...
            # Implement your AVL packet parsing logic here
            # ...

            # Get the number of data received
            received_data_num = 0  # Implement your logic to calculate the number of received data

            # Report the number of data received back to the module
            self.client_sock.sendall(received_data_num.to_bytes(4, 'big'))

            self.client_sock.close()

# Start the TCP server
def start_tcp_server():
    server_ip = '192.96.200.93'  # Use '0.0.0.0' to listen on all network interfaces
    server_port = 8000  # Choose a port number to listen on

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((server_ip, server_port))
    server_sock.listen(1)

    print("Server started, waiting for connections...")

    while True:
        client_sock, client_addr = server_sock.accept()

        tcp_thread = TCPThread(client_sock, client_addr)
        tcp_thread.start()

def should_accept_data(imei):
    # Implement your logic to determine acceptance
    return True  # Accept all data for now, customize as needed
