# Akıllı Çöp Ayrıştırma Sistemi

## Proje Özeti
Akıllı Çöp Ayrıştırma Sistemi, atıkları plastik, cam, metal ve kağıt gibi türlere sınıflandırmak için makine öğrenimi ve bilgisayarla görme kullanır. Böylece geri dönüşüm oranları artırılır ve çevreye olan olumsuz etkiler azaltılır.

## Çalışma Prensibi
- **Model**: YOLO tabanlı nesne tespiti modeli, 20.000'den fazla görsel ile eğitildi ve farklı atık türlerini sınıflandırmak için kullanılıyor.
- **Teknoloji Yığını**:
  - Python
  - OpenCV
  - YOLOv5
  - Tkinter (grafiksel kullanıcı arayüzü için)
  - PIL (görüntü işleme için)

## Başlangıç
### Gereksinimler
- Python 3.11
- Gerekli kütüphaneler: `opencv-python`, `ultralytics`, `Pillow`, `tkinter`, `threading` vb.

Gerekli kütüphaneleri şu şekilde kurabilirsiniz:
```bash
pip install -r requirements.txt
