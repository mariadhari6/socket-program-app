import socket
import threading


def handle_client(conn, addr):
    print(f"Terhubung dengan {addr}")
    # Terima data dari client
    while True:    
      encoded_text = conn.recv(1024)
      print("Raw: ", encoded_text)
      soh_byte = bytes([1])  # SOH as byte
      # Check if encoded text had SOH
      contains_soh_bytes = soh_byte in encoded_text
      print(f"encoded_text bytes contains SOH (\\x01): {contains_soh_bytes}")
      decoded_bytes = encoded_text.decode("utf-8")
      if not decoded_bytes:
         break
      decoded_text = decoded_bytes.replace(chr(1), "")
      print(f"Pesan dari client: {addr}", decoded_text)
      if contains_soh_bytes:
         print("Send to client")
         resp_encoded_text = chr(2).encode("utf-8") + chr(6).join(decoded_text).encode("utf-8") + chr(3).encode("utf-8")
         conn.send(resp_encoded_text)
    conn.close()
    

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)  # Bisa handle sampai 5 client dalam queue
print("Server berjalan...")


while True:
  conn, addr = server_socket.accept()
  thread = threading.Thread(target=handle_client, args=(conn, addr))
  thread.start()
  print(f"Total koneksi aktif: {threading.active_count() - 1}")
