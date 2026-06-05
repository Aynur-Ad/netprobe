import socket
import time
from config import (
    SERVER_HOST,
    SERVER_PORT,
    CHUNK_SIZE,
    BUFFER_SIZE,
    TIMEOUT,
    MAX_RETRIES
)

from checksum import calculate_sha256
from logger import log_event

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

file_path = "input_files/test.txt"
sequence_number = 0

with open(file_path, "rb") as file:
    while True:
        chunk = file.read(CHUNK_SIZE)

        if not chunk:
            break

        packet = f"DATA|{sequence_number}|".encode("utf-8") + chunk

        success = False
        retry_count = 0

        while not success and retry_count < MAX_RETRIES:
            client_socket.sendto(packet, (SERVER_HOST, SERVER_PORT))
            log_event(f"PACKET_SENT seq={sequence_number} attempt={retry_count + 1}")
            print(f"Paket gönderildi. Sequence: {sequence_number}, Deneme: {retry_count + 1}")

            try:
                ack, _ = client_socket.recvfrom(BUFFER_SIZE)
                ack_message = ack.decode("utf-8")

                if ack_message == f"ACK|{sequence_number}":
                    print(f"ACK alındı. Sequence: {sequence_number}")
                    log_event(f"ACK_RECEIVED seq={sequence_number}")
                    success = True
                    sequence_number += 1
                else:
                    print("Beklenmeyen ACK:", ack_message)

            except socket.timeout:
                retry_count += 1
                print(f"Timeout oluştu. Sequence {sequence_number} tekrar gönderilecek.")
                log_event(f"TIMEOUT seq={sequence_number}")
                log_event(f"RETRANSMISSION seq={sequence_number}")

        if not success:
            print(f"Sequence {sequence_number} paketi {MAX_RETRIES} denemeye rağmen gönderilemedi.")
            print("Dosya aktarımı başarısız.")
            client_socket.close()
            exit()

        time.sleep(0.01)

file_hash = calculate_sha256(file_path)
end_message = f"END|{file_hash}"
client_socket.sendto(end_message.encode("utf-8"), (SERVER_HOST, SERVER_PORT))

print("Orijinal dosya hash değeri:", file_hash)
client_socket.close()

print("Dosya gönderimi tamamlandı.")
log_event("TRANSFER_COMPLETED")