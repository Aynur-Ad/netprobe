import matplotlib.pyplot as plt
import os

# ==============================================================================
# 1. ADIM: DENEY SONUÇLARINI BURAYA GİRİN (analyzer.py'dan alınan değerler)
# ==============================================================================

# --- SENARYO 1: Yapay Paket Kaybı Oranının Etkisi ---
loss_labels = ['%0 Kayıp', '%10 Kayıp', '%20 Kayıp']
loss_throughput       = [951.23, 335.42, 450.95]  # KB/s
loss_goodput          = [21.67, 5.73, 5.14]  # KB/s
loss_completion_time  = [0.0032, 0.0121, 0.0135]  # Saniye
loss_retransmission   = [0.0016, 0.0040, 0.0034]  # Yüzde (%)

# --- SENARYO 2: Paket Boyutunun (Chunk Size) Etkisi ---
size_labels = ['512 Byte', '1024 Byte', '2048 Byte']
size_throughput       = [486.48, 497.99, 513.02]  # KB/s
size_goodput          = [4.75, 4.25, 3.90]  # KB/s
size_completion_time  = [0.0146, 0.0163, 0.0178]  # Saniye
size_retransmission   = [0.0029, 0.0027, 0.0025]  # Yüzde (%)

# --- SENARYO 3: Timeout Değerinin Etkisi ---
timeout_labels = ['0.5 Saniye', '1.0 Saniye', '2.0 Saniye']
timeout_throughput       = [517.68, 536.59, 543.56]  # KB/s
timeout_goodput          = [3.54, 3.33, 3.10]  # KB/s
timeout_completion_time  = [0.0196, 0.0208, 0.0224]  # Saniye
timeout_retransmission   = [0.0024, 0.0023, 0.0022]  # Yüzde (%)


# ==============================================================================
# 2. ADIM: GRAFİK ÇİZİM FONKSİYONU (Aşağıya dokunmana gerek yok)
# ==============================================================================

def ciz_ve_kaydet(baslik, etiketler, throughput, goodput, completion_time, retransmission, dosya_adi):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(baslik, fontsize=16, fontweight='bold')

    # 1. Throughput
    axs[0, 0].bar(etiketler, throughput, color='royalblue', edgecolor='black')
    axs[0, 0].set_title('Throughput Karşılaştırması')
    axs[0, 0].set_ylabel('KB/s')
    axs[0, 0].grid(axis='y', linestyle='--', alpha=0.7)

    # 2. Goodput
    axs[0, 1].bar(etiketler, goodput, color='forestgreen', edgecolor='black')
    axs[0, 1].set_title('Goodput Karşılaştırması')
    axs[0, 1].set_ylabel('KB/s')
    axs[0, 1].grid(axis='y', linestyle='--', alpha=0.7)

    # 3. Completion Time
    axs[1, 0].bar(etiketler, completion_time, color='tomato', edgecolor='black')
    axs[1, 0].set_title('Tamamlanma Süresi (Completion Time)')
    axs[1, 0].set_ylabel('Saniye')
    axs[1, 0].grid(axis='y', linestyle='--', alpha=0.7)

    # 4. Retransmission Rate
    axs[1, 1].plot(etiketler, retransmission, marker='o', color='purple', linewidth=2, markersize=8)
    axs[1, 1].set_title('Yeniden Gönderim Oranı (Retransmission Rate)')
    axs[1, 1].set_ylabel('% (Yüzde)')
    axs[1, 1].grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    kayit_yolu = f"results/{dosya_adi}.png"
    plt.savefig(kayit_yolu)
    print(f"Grafik kaydedildi: {kayit_yolu}")
    plt.close() # Diğer grafiklerle karışmaması için pencereyi kapat

# --- GRAFİKLERİ ÜRET ---

if not os.path.exists("results"):
    os.makedirs("results")

print("Grafikler oluşturuluyor...")

# Senaryo 1 Çizimi
ciz_ve_kaydet('Paket Kayıp Oranının Ağ Performansına Etkisi', 
              loss_labels, loss_throughput, loss_goodput, loss_completion_time, loss_retransmission, 
              'senaryo1_kayip_orani')

# Senaryo 2 Çizimi
ciz_ve_kaydet('Paket Boyutunun Ağ Performansına Etkisi', 
              size_labels, size_throughput, size_goodput, size_completion_time, size_retransmission, 
              'senaryo2_paket_boyutu')

# Senaryo 3 Çizimi
ciz_ve_kaydet('Timeout Değerinin Ağ Performansına Etkisi', 
              timeout_labels, timeout_throughput, timeout_goodput, timeout_completion_time, timeout_retransmission, 
              'senaryo3_timeout')

print("Tüm işlemler tamamlandı! Grafikleri 'results' klasöründe bulabilirsin.")