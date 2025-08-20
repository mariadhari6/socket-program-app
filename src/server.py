import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)  # Bisa handle sampai 5 client dalam queue
print("Server berjalan...")

def handle_client(conn, addr):
    print(f"Terhubung dengan {addr}")
    # Terima data dari client
    while True:
      receive_data = conn.recv(1024)
      if receive_data:
         # check if the response is 1 byte soh
         if len(receive_data) == 1 and receive_data[0] == 1:
            print("\nServer ready to receive data.")
            print("SOH received from client.", receive_data)
            # send 1 byte ack to client
            conn.send(bytes([6]))
            continue
         else:
            print("Raw: ", receive_data)
            decoded_bytes = receive_data.decode("utf-8")
            decoded_text = decoded_bytes.strip(chr(2) + chr(3)).replace(chr(6), "")
            if decoded_text:
              print(f"Pesan dari client: {addr}", decoded_text)
              conn.send(bytes([6])) # send ack to client for next data
while True:
   conn, addr = server_socket.accept()
   try:
      thread = threading.Thread(target=handle_client, args=(conn, addr))
      thread.start()
      print(f"Total koneksi aktif: {threading.active_count() - 1}")
   except Exception as e:
      print(f"Error handling client {addr}: {e}")
      conn.close()
   except KeyboardInterrupt:
      print("\nServer shutting down.")
      server_socket.close()
      break
