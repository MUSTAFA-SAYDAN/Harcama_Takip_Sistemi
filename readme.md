# 💰 Harcamalar Takip Sistemi (Flask API)

Bu proje, kullanıcıların günlük harcamalarını güvenli bir şekilde kaydedip yönetebilecekleri basit bir RESTful API'dir. Flask, SQLAlchemy, Bcrypt ve JWT teknolojileriyle geliştirilmiştir.

## 🚀 Özellikler

- ✅ Kullanıcı kayıt ve giriş işlemleri (şifreler hash'lenir)
- 🔐 JWT ile kimlik doğrulama
- 📌 Harcama ekleme, listeleme, güncelleme ve silme (CRUD)
- 👤 Her kullanıcı yalnızca kendi harcamalarını yönetebilir
- 🛡️ Hatalı isteklerde açıklayıcı hata mesajları

## 🛠️ Kullanılan Teknolojiler

- Python & Flask
- Flask-SQLAlchemy
- Flask-Bcrypt
- PyJWT
- SQLite (veritabanı)

## 🔧 Kurulum ve Çalıştırma

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/kullaniciadi/Harcama_Takip_Sistemi_.git
cd Harcama_Takip_Sistemi
2. Sanal Ortam Oluşturun ve Aktif Edin
bash
Kopyala
Düzenle
python -m venv venv
venv\Scripts\activate
3. Gerekli Paketleri Yükleyin
bash
Kopyala
Düzenle
pip install -r requirements.txt
4. Uygulamayı Başlatın
bash
Kopyala
Düzenle
python app.py
Uygulama şu adreste çalışır: http://127.0.0.1:5001

📮 API Endpointleri
🔐 Kimlik Doğrulama
POST /kayit
Yeni kullanıcı kaydı oluşturur.

İstek Gövdesi:

json
Kopyala
Düzenle
{
  "kullanici_adi": "mustafa",
  "sifre": "1234"
}
POST /giris
Giriş yapar ve JWT token döner.

İstek Gövdesi:

json
Kopyala
Düzenle
{
  "kullanici_adi": "mustafa",
  "sifre": "1234"
}
Yanıt:

json
Kopyala
Düzenle
{
  "token": "JWT_TOKEN_BURAYA"
}
💸 Harcamalar
⚠️ Authorization: Bearer <token> header'ı gereklidir.

POST /harcamalar
Yeni harcama ekler.

json
Kopyala
Düzenle
{
  "baslik": "Market",
  "miktar": 200,
  "kategori": "Gıda",
  "tarih": "2025-07-21"
}
GET /harcamalar
Tüm harcamaları listeler.

GET /harcamalar/<id>
Belirtilen ID'li harcamayı getirir.

PUT /harcamalar/<id>
Harcamayı günceller.

json
Kopyala
Düzenle
{
  "baslik": "Güncellenmiş Başlık",
  "miktar": 150
}
DELETE /harcamalar/<id>
Harcamayı siler.

📁 Proje Yapısı
bash
Kopyala
Düzenle
harcamalar-api/
├── app.py              # Ana uygulama dosyası
├── models.py           # Veritabanı modelleri
├── requirements.txt    # Gerekli paketler
└── README.md           # Proje açıklaması
🧪 Test Kullanıcı
json
Kopyala
Düzenle
{
  "kullanici_adi": "demo",
  "sifre": "1234"
}
🧠 Notlar
Şifreler bcrypt ile güvenli şekilde saklanır.

JWT token süresi 3 saattir.

Sadece oturum açan kullanıcı kendi harcamalarını değiştirebilir/silebilir.

Geliştirme modunda debug=True ile başlatılır.

🧑‍💻 Geliştirici
Mustafa – Backend öğrenme yolculuğunda ilerleyen, Flask ile sağlam projeler geliştiren bir yazılımcı adayı.

⚖️ Lisans
Bu proje MIT lisansı ile lisanslanmıştır.