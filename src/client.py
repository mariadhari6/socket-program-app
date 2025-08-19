import socket
import threading

def handle_response(socket):
  while True:
    try:
      resp_encoded_text = socket.recv(1024)
      if resp_encoded_text:
        print("\nRaw: ", resp_encoded_text)
        decoded_bytes = resp_encoded_text.decode("utf-8")
        decoded_text = decoded_bytes.strip(chr(2) + chr(3)).replace(chr(6), "")
        if decoded_text:
          print("\nDari server:", decoded_text)
    except:
      print("\nKoneksi terbutus dari server")
      break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

thread = threading.Thread(target=handle_response, args=(client_socket,))
thread.daemon = True
thread.start()

while True:
  try:
    text = input("Input your text: ")
    encoded_text = chr(1).join(text).encode("utf-8")
    client_socket.send(encoded_text)
  except KeyboardInterrupt:
    print("\nExit")
    client_socket.close()
    break
