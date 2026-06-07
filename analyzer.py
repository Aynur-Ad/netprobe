import os
import re
import matplotlib.pyplot as plt


LOG_FILE = "logs/transfer.log"
TEST_FILE = "input_files/test.txt"


CHUNK_SIZE = 1024  
HEADER_SIZE = 15   # DATA|seq| gibi başlıkların tahmini byte boyutu

def analyze_logs():
    if not os.path.exists(LOG_FILE):
        print(f"Hata: {LOG_FILE} bulunamadı! Önce client ve server'ı çalıştırıp log üretmelisin.")
        return

   
    events = {
        "PACKET_SENT": 0,
        "ACK_RECEIVED": 0,
        "TIMEOUT": 0,
        "RETRANSMISSION": 0
    }
    
    rtt_values = []
    
    print("Log dosyası analiz ediliyor...")
    
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "PACKET_SENT" in line:
                events["PACKET_SENT"] += 1
            elif "ACK_RECEIVED" in line:
                events["ACK_RECEIVED"] += 1
                # RTT değerini regex ile çekiyoruz (Örn: rtt=0.0123)
                match = re.search(r"rtt=([\d\.]+)", line)
                if match:
                    rtt_values.append(float(match.group(1)))
            elif "TIMEOUT" in line:
                events["TIMEOUT"] += 1
            elif "RETRANSMISSION" in line:
                events["RETRANSMISSION"] += 1
    
    # 1. Retransmission Rate
    total_sent = events["PACKET_SENT"]
    retransmissions = events["RETRANSMISSION"]
    retransmission_rate = (retransmissions / total_sent * 100) if total_sent > 0 else 0

    # 2. Ortalama RTT
    avg_rtt = sum(rtt_values) / len(rtt_values) if rtt_values else 0

    # 3. Dosya Boyutları ve Süre
    # Dosyanın gerçek boyutu (Goodput için)
    file_size_bytes = os.path.getsize(TEST_FILE) if os.path.exists(TEST_FILE) else 0
    
    # Ağda taşınan toplam veri (Throughput için - header'lar ve tekrar gönderimler dahil)
    total_bytes_sent = total_sent * (CHUNK_SIZE + HEADER_SIZE)
    
    # Completion Time (Yaklaşık)
    # Eger logger.py dosyasında timestamp (zaman damgası) yoksa, 
    # geçen süreyi RTT'lerin toplamı + timeout bekleme süreleri olarak tahmin edebiliriz.
    # (Not: Eğer logger.py zaman damgası basıyorsa, ilk ve son satırın zaman farkını almak daha kesin olur).
    estimated_completion_time = sum(rtt_values) + (events["TIMEOUT"] * 0.5) # 0.5 = config.TIMEOUT
    
    # 4. Throughput ve Goodput (Byte/Saniye -> KB/Saniye)
    if estimated_completion_time > 0:
        throughput_bps = total_bytes_sent / estimated_completion_time
        goodput_bps = file_size_bytes / estimated_completion_time
    else:
        throughput_bps = 0
        goodput_bps = 0

    print("\n" + "="*40)
    print("AĞ PERFORMANS ANALİZ RAPORU")
    print("="*40)
    print(f"Toplam Gönderilen Paket: {total_sent}")
    print(f"Alınan Başarılı ACK:     {events['ACK_RECEIVED']}")
    print(f"Yaşanan Timeout:         {events['TIMEOUT']}")
    print(f"Retransmission Sayısı:   {retransmissions}")
    print("-" * 40)
    print(f"Retransmission Rate:     %{retransmission_rate:.2f}")
    print(f"Ortalama RTT:            {avg_rtt:.4f} saniye")
    print(f"Tahmini Tamamlanma Süresi: {estimated_completion_time:.4f} saniye")
    print(f"Throughput:              {throughput_bps / 1024:.2f} KB/s")
    print(f"Goodput:                 {goodput_bps / 1024:.2f} KB/s")
    print("="*40 + "\n")

    plot_results(events, rtt_values)

def plot_results(events, rtt_values):
    plt.figure(figsize=(12, 5))

    # 1. Grafik: Olay Dağılımı (Bar Chart)
    plt.subplot(1, 2, 1)
    labels = list(events.keys())
    values = list(events.values())
    colors = ['blue', 'green', 'orange', 'red']
    
    plt.bar(labels, values, color=colors)
    plt.title('Ağ Olayları Dağılımı')
    plt.ylabel('Frekans (Adet)')
    plt.xticks(rotation=15)

    # 2. Grafik: RTT Değişimi (Line Chart)
    plt.subplot(1, 2, 2)
    plt.plot(range(1, len(rtt_values) + 1), rtt_values, marker='o', linestyle='-', color='purple')
    plt.title('Paket Sırasına Göre RTT Değişimi')
    plt.xlabel('Paket Numarası (Sıra)')
    plt.ylabel('Gecikme - RTT (Saniye)')
    plt.grid(True)

    plt.tight_layout()
    # Grafiği ekranda göster ve kaydet
    plt.savefig('results/performance_graphs.png')
    print("Grafikler oluşturuldu ve 'results/performance_graphs.png' olarak kaydedildi.")
    plt.show()

if __name__ == "__main__":
    # results klasörü yoksa oluştur
    if not os.path.exists("results"):
        os.makedirs("results")
        
    analyze_logs()
