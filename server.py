import socket
import os
from config import SERVER_HOST, SERVER_PORT, BUFFER_SIZE
from checksum import calculate_sha256
from logger import log_event

os.makedirs("received_files", exist_ok=True)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))

print(f"UDP Server başlatıldı: {SERVER_HOST}:{SERVER_PORT}")
print("Dosya bekleniyor...")

file_path = "received_files/received_test.txt"
received_sequences = set()

with open(file_path, "wb") as file:
    while True:
        data, client_address = server_socket.recvfrom(BUFFER_SIZE)

        if data.startswith(b"END|"):
            received_hash = data.decode("utf-8").split("|")[1]
            print("Dosya aktarımı tamamlandı.")
            break

        parts = data.split(b"|", 2)

        packet_type = parts[0].decode("utf-8")
        sequence_number = int(parts[1].decode("utf-8"))
        payload = parts[2]

        if packet_type == "DATA":
            is_duplicate = sequence_number in received_sequences

            if not is_duplicate:
                file.write(payload)
                received_sequences.add(sequence_number)
                print(f"Yeni paket alındı ve dosyaya yazıldı. Sequence: {sequence_number}")
                log_event(f"PACKET_RECEIVED seq={sequence_number}")
            else:
                print(f"Duplicate paket geldi, dosyaya tekrar yazılmadı. Sequence: {sequence_number}")
                log_event(f"DUPLICATE_PACKET seq={sequence_number}")

            ack_message = f"ACK|{sequence_number}"
            server_socket.sendto(ack_message.encode("utf-8"), client_address)
            print(f"ACK gönderildi. Sequence: {sequence_number}")
            log_event(f"ACK_SENT seq={sequence_number}")

server_socket.close()
print(f"Dosya kaydedildi: {file_path}")

calculated_hash = calculate_sha256(file_path)

print("Client tarafından gönderilen hash:", received_hash)
print("Server tarafından hesaplanan hash:", calculated_hash)

if received_hash == calculated_hash:
    print("Dosya bütünlüğü doğrulandı. Aktarım başarılı.")
else:
    print("Dosya bütünlüğü doğrulanamadı. Dosya bozulmuş olabilir.")