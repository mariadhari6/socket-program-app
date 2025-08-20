import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))
allowSend = True

state = [
  'ready',
  'waiting_for_ack',
  'waiting_for_input'
]
current_state = state[0]

def handle_receive_ack(socket):
  while True:
    try:
      resp_acx = socket.recv(1024)
      if resp_acx:
        # check if the response is 1 byte ack
        if len(resp_acx) == 1 and resp_acx[0] == 6:
          print("\nServer ready to receive data.")
          print("ACK received from server.", resp_acx)
          global current_state
          current_state = state[2]
          # return
    except:
      print("\nKoneksi terputus dari server")
      break

thread_ack = threading.Thread(target=handle_receive_ack, args=(client_socket,))
thread_ack.daemon = True
thread_ack.start()

while True:
  try:
    if allowSend:
      soh_byte = bytes([1])
      client_socket.send(soh_byte)
      current_state = state[1]
      allowSend = False
    elif current_state == state[2]:
      text = input("Input your text: ")
      # Send ACK to server
      encoded_text = chr(2).encode("utf-8") + chr(6).join(text).encode("utf-8") + chr(3).encode("utf-8")
      client_socket.send(encoded_text)
      current_state = state[1]

  except:
    print("\nKoneksi terputus dari server")
    break

client_socket.close()
