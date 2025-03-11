# Kreş Kayıt Sistemi (Kindergarten Registration System)

Bu proje, Atakum Belediyesi için geliştirilmiş bir kreş kayıt ve öğrenci yerleştirme sistemidir.

## Özellikler

- Öğrenci kayıt sistemi
- Otomatik puan hesaplama
- Kreş ve sınıf yönetimi
- Otomatik öğrenci yerleştirme
- Çok kriterli değerlendirme sistemi
- Türkçe arayüz

## Kurulum

### Gereksinimler

- Python 3.8 veya üstü
- pip (Python paket yöneticisi)
- SQLite3

### Adımlar

1. Projeyi klonlayın:
```bash
git clone [repository-url]
cd KresKayit
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Çevresel değişkenleri ayarlayın:
```bash
# Windows
copy .env.example .env

# Linux/MacOS
cp .env.example .env
```

5. `.env` dosyasını düzenleyin:
```
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

6. Veritabanını oluşturun:
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

7. (Opsiyonel) Test verilerini ekleyin:
```bash
python add_test_data.py
```

8. Uygulamayı başlatın:
```bash
python app.py
```

Uygulama varsayılan olarak http://localhost:5000 adresinde çalışacaktır.

## Admin Hesabı Oluşturma

İlk çalıştırmada otomatik olarak aşağıdaki admin hesabı oluşturulur:
- Kullanıcı adı: admin
- Şifre: admin

**Önemli:** Canlı ortamda bu şifreyi değiştirmeyi unutmayın!

## Puan Hesaplama Kriterleri

Öğrenci puanları aşağıdaki kriterlere göre hesaplanır:

1. Yaş kontrolü (3-6 yaş arası kabul edilir)
2. Adres puanı (Atakum'da ikamet +5 puan)
3. Tuvalet eğitimi (zorunlu)
4. Kardeş sayısı (her kardeş için +1 puan)
5. Okul deneyimi (devlet okulu +5 puan)
6. Ebeveyn çalışma yeri (Atakum Belediyesi +5 puan)
7. Ebeveyn durumu (vefat durumunda +5 puan)
8. Ev sahipliği (kiracı +5 puan)
9. Medeni durum (ayrı +5 puan)
10. Gelir düzeyi:
    - 17.000 TL altı: +20 puan
    - 17.000-35.000 TL: +15 puan
    - 35.000-53.000 TL: +10 puan
    - 53.000-67.000 TL: +5 puan

## Yerleştirme Süreci

1. Öğrenciler puan ve kayıt tarihine göre sıralanır
2. Her öğrenci için tercih sırasına göre kreşler kontrol edilir
3. Uygun kontenjanı olan sınıfa yerleştirilir
4. Yerleştirme sonuçları anlık olarak görüntülenebilir

## Güvenlik

- Flask-Login ile oturum yönetimi
- Şifrelerin güvenli saklanması (Werkzeug)
- CSRF koruması
- Yetkilendirme kontrolleri

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

## Project Structure

```
flask_kindergarten/
├── app.py              # Main application file
├── forms.py            # Form definitions
├── requirements.txt    # Project dependencies
├── static/            # Static files (CSS, JS)
├── templates/         # HTML templates
└── instance/          # Instance-specific files (database)
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 