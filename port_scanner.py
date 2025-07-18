# Gerekli kütüphaneleri içe aktarıyoruz
import socket
import threading
from queue import Queue
import json      # JSON formatında kayıt için
import csv       # CSV formatında kayıt için
from datetime import datetime

# Yaygın portlar ve karşılık gelen servis adları için bir sözlük
COMMON_PORTS = {
    21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS', 80: 'HTTP',
    110: 'POP3', 143: 'IMAP', 443: 'HTTPS', 445: 'SMB', 993: 'IMAPS',
    995: 'POP3S', 3306: 'MySQL', 3389: 'RDP', 5900: 'VNC', 8080: 'HTTP-Proxy'
}

# Taranacak portları işlemek için bir iş kuyruğu
port_queue = Queue()
# Tarama sonuçlarını saklamak için bir liste
results = []
# Birden fazla thread'in aynı anda ekrana yazmasını engellemek için bir kilit
print_lock = threading.Lock()

def get_service_name(port):
    """Verilen port numarasına göre bilinen servis adını döndürür."""
    return COMMON_PORTS.get(port, 'Bilinmeyen')

def scan_port(target_ip, port):
    """
    Tek bir portu tarar. Açıksa, servis adını ve banner bilgisini almaya çalışır.
    """
    banner = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            service_name = get_service_name(port)
            try:
                s.send(b'HEAD / HTTP/1.0\r\n\r\n')
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            except Exception:
                banner = "Banner çekilemedi."
            
            with print_lock:
                banner_preview = banner.splitlines()[0] if banner else ''
                print(f"[+] Port {port:<5} Açık (Servis: {service_name:<12} Banner: {banner_preview})")
                results.append({"port": port, "service": service_name, "banner": banner})

    except (socket.timeout, ConnectionRefusedError):
        pass
    except Exception:
        pass
    finally:
        s.close()

def worker(target_ip):
    """
    Kuyruktan bir port alır ve boşalana kadar tarama işini yapar.
    """
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(target_ip, port)
        port_queue.task_done()

def save_results_to_csv(filename, target_ip):
    """Sonuçları otomatik olarak CSV dosyasına kaydeder."""
    if not results:
        print("\n[!] Hiç açık port bulunamadı, bu yüzden dosya oluşturulmadı.")
        return

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ["port", "service", "banner"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted(results, key=lambda x: x['port']))
        print(f"\n[+] Sonuçlar başarıyla {filename} dosyasına kaydedildi.")
    except IOError as e:
        print(f"\n[!] Dosya yazma hatası: {e}")

# =================================================================
# ANA PROGRAM BLOĞU - BURASI DEĞİŞTİ
# =================================================================
if __name__ == "__main__":
    # Kullanıcıdan interaktif olarak bilgileri alıyoruz
    target_ip = input("Taranacak Hedef IP Adresini Girin: ")
    
    # Varsayılan değer sunarak port aralığı istiyoruz
    port_range_str = input("Taranacak Port Aralığını Girin [Varsayılan: 1-1024]: ")
    if not port_range_str:
        port_range_str = "1-1024"
        
    # Varsayılan değer sunarak thread sayısı istiyoruz
    thread_count_str = input("Kullanılacak Thread Sayısı [Varsayılan: 100]: ")
    try:
        thread_count = int(thread_count_str) if thread_count_str else 100
    except ValueError:
        print("[!] Geçersiz thread sayısı. Varsayılan olarak 100 kullanılıyor.")
        thread_count = 100

    # Port girdisini parse etme
    try:
        if '-' in port_range_str:
            start, end = map(int, port_range_str.split('-'))
            for port in range(start, end + 1):
                port_queue.put(port)
        else:
            ports = map(int, port_range_str.split(','))
            for port in ports:
                port_queue.put(port)
    except ValueError:
        print("[!] Hatalı port formatı. Lütfen '1-1024' veya '80,443' gibi kullanın. Program sonlandırılıyor.")
        exit()

    print(f"\n[+] {target_ip} adresi {thread_count} thread ile taranıyor...")
    start_time = datetime.now()

    # Thread'leri oluştur ve başlat
    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(target_ip,), daemon=True)
        t.start()
    
    port_queue.join()
    
    end_time = datetime.now()
    print(f"\n[+] Tarama {end_time - start_time} sürede tamamlandı.")

    # Otomatik olarak tarih ve saat içeren bir dosya adı oluştur
    now = datetime.now()
    # IP adresindeki noktaları alt çizgi ile değiştirerek dosya adı için güvenli hale getir
    safe_target_name = target_ip.replace('.', '_')
    filename = f"scan_{safe_target_name}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    
    # Sonuçları otomatik olarak oluşturulan CSV dosyasına kaydet
    save_results_to_csv(filename, target_ip)
