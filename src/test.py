# text = "Helo morasaurus"
# encoded_text = chr(1).join(text).encode("utf-8")

# decoded_bytes = encoded_text.decode("utf-8")
# decoded_text = decoded_bytes.replace(chr(1), "")

# print(encoded_text)
# print(decoded_text)


# soh_byte = bytes([1])  # SOH as byte
# contains_soh_bytes = soh_byte in encoded_text
# print(f"encoded_text bytes contains SOH (\\x01): {contains_soh_bytes}")



text = "Helo morasaurus"
encoded_text = chr(2).encode("utf-8") + chr(6).join(text).encode("utf-8") + chr(3).encode("utf-8")

decoded_bytes = encoded_text.decode("utf-8")
decoded_text = decoded_bytes.strip(chr(2) + chr(3)).replace(chr(6), "")


print(encoded_text)
print(decoded_text)