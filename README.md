# Python ile Gelişmiş Port Tarayıcı

Bu proje, Python kullanılarak geliştirilmiş, komut satırından çalışan bir ağ port tarayıcı aracıdır. Belirtilen bir hedefteki açık portları hızlı bir şekilde tespit etmek, servis bilgilerini almak ve sonuçları kaydetmek için tasarlanmıştır.

## Özellikler

- **Hızlı Tarama:** `threading` kullanarak birden fazla portu aynı anda tarar.
- **Servis Tespiti:** Yaygın port numaralarına göre (HTTP, FTP, SSH vb.) servis adlarını gösterir.
- **Banner Grabbing:** Açık portlardan gelen başlık (banner) bilgilerini alarak servis versiyonu hakkında fikir verir.
- **Otomatik Kayıt:** Tarama sonuçlarını, tarama zamanını ve hedefi içeren bir `.csv` dosyasına otomatik olarak kaydeder.
- **Kullanıcı Dostu Arayüz:** Program, kullanıcıdan alacağı bilgileri interaktif olarak sorar.

## Nasıl Kullanılır?

1.  Depoyu klonlayın veya `port_scanner.py` dosyasını indirin.
2.  Terminali açıp dosyanın bulunduğu dizine gidin.
3.  Aşağıdaki komut ile programı çalıştırın:
    ```bash
    python port_scanner.py
    ```
4.  Programın sorduğu hedef IP adresi ve port aralığı gibi bilgileri girin.

Tarama tamamlandığında, sonuçlar `scan_HEDEFIP_TARIH_SAAT.csv` formatında bir dosyaya kaydedilecektir.

## ⚠️ Etik Kullanım Uyarısı

Bu araç yalnızca eğitim ve yasal test amaçlı geliştirilmiştir. Bu aracı **asla** size ait olmayan veya test etme izninizin bulunmadığı sistemler üzerinde kullanmayın. İzin alınmadan yapılan tarama işlemleri yasa dışıdır ve siber suç teşkil edebilir.