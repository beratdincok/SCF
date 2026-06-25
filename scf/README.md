# SFC — SCF–IKARUS Operasyon Rehberi

SFC; havayolu bazında IKARUS'a girilecek hizmetleri, hizmetin hangi konu başlığı/alan altında yer aldığını, giriş kuralını ve SCF kapanış kontrollerini gösteren Streamlit uygulamasıdır.

## Kapsamdaki havayolları

AWG, AAR, ABY, AEE, AHY, AZG, BBT, CCA, CES, CTN, CSC, CSN, DAH, DHX, DLH, ETD, FAD, FDX, GEC, IAW, IGT, KAC, KAL, KNE, KZR, AYN, MGH, SHI, SVA, RAM, UAE, UBD, UZB, BRU ve SKYAIR.

Her kod sol menüde ayrı bir sayfadır.

## Proje yapısı

```text
SFC_IKARUS_REHBERI/
├── app.py
├── requirements.txt
├── validate_data.py
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
└── data/
    ├── airlines.csv
    └── services.csv
```

## Bilgisayarda çalıştırma

Terminali proje klasöründe açın:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Hizmetleri ekleme

Gerçek içerik `data/services.csv` dosyasına eklenir. Dosyanın sütunları:

- `airline_code`: Üçlü kod
- `category`: SFC ana konu başlığı
- `service_name`: Hizmet adı
- `ikarus_section`: IKARUS ana bölümü
- `ikarus_field`: IKARUS alanı
- `entry_rule`: Nasıl girileceği
- `unit`: Adet, dakika, saat, kg vb.
- `required`: Evet/Hayır
- `when_to_enter`: Hangi durumda girileceği
- `verification_source`: Doğrulama kaynağı
- `notes`: Özel not/istisna
- `sort_order`: Sayfadaki sıra

Excel'de düzenlerken dosyayı **CSV UTF-8 (virgülle ayrılmış)** olarak kaydedin.

Veriyi kontrol etmek için:

```bash
python validate_data.py
```

## GitHub'a yükleme

1. GitHub'da yeni bir repository oluşturun.
2. Bu klasörün içindeki tüm dosyaları repository'nin köküne yükleyin.
3. Commit işlemini tamamlayın.

Git komutlarıyla:

```bash
git init
git add .
git commit -m "SFC ilk sürüm"
git branch -M main
git remote add origin GITHUB_REPOSITORY_ADRESI
git push -u origin main
```

## Streamlit Community Cloud'da yayınlama

1. Streamlit Community Cloud'a GitHub hesabınızla giriş yapın.
2. **Create app / Deploy an app** seçeneğini açın.
3. Repository, branch olarak `main`, main file path olarak `app.py` seçin.
4. Uygulama adresini belirleyip deploy edin.

GitHub'a gönderilen sonraki değişiklikler uygulamaya otomatik yansır.

## Gizlilik ve operasyon onayı

- Sözleşme ücretleri, yolcu/çalışan kişisel verileri ve şirket içi gizli dokümanlar kamuya açık repository'ye eklenmemelidir.
- Gerekirse private repository ve erişim kısıtlamalı Streamlit paylaşımı kullanılmalıdır.
- Uygulamadaki hizmet eşleştirmeleri yayından önce ilgili operasyon/yetkili birim tarafından doğrulanmalıdır.
- Bu uygulama resmi prosedürün veya havayolu sözleşmesinin yerine geçmez.


## Önemli GitHub yükleme kontrolü

GitHub repository ana dizinindeki `app.py` dosyasının ilk satırı şu olmalıdır:

```python
# SFC – SCF/IKARUS Rehberi | Streamlit başlangıç dosyası
```

`app.py` içinde `airline_code,category,service_name...` şeklinde başlayan bir CSV satırı görürseniz yanlış dosya yüklenmiştir. Bu satır yalnızca `data/services.csv` dosyasında bulunmalıdır.

ZIP bu sürümde klasör katmanı olmadan hazırlanmıştır. ZIP içeriğini açtıktan sonra `app.py`, `requirements.txt`, `data` ve `.streamlit` öğelerini repository ana dizinine birlikte yükleyin. Streamlit Main file path: `app.py`.
