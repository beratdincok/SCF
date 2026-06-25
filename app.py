# SFC CLEAN BUILD 2026-06-25

import streamlit as st

st.set_page_config(
page_title="SFC | SCF–IKARUS Rehberi",
page_icon="✈️",
layout="wide",
initial_sidebar_state="expanded",
)

AIRLINES = [
"AWG",
"AAR",
"ABY",
"AEE",
"AHY",
"AZG",
"BBT",
"CCA",
"CES",
"CTN",
"CSC",
"CSN",
"DAH",
"DHX",
"DLH",
"ETD",
"FAD",
"FDX",
"GEC",
"IAW",
"IGT",
"KAC",
"KAL",
"KNE",
"KZR",
"AYN",
"MGH",
"SHI",
"SVA",
"RAM",
"UAE",
"UBD",
"UZB",
"BRU",
"SKYAIR",
]

CATEGORIES = [
"Uçuş Bilgileri",
"Yolcu Hizmetleri",
"Ramp / Apron Hizmetleri",
"Uçak Hizmetleri",
"Yük Kontrol ve Operasyon",
"Kargo ve Posta",
"GSE / Ekipman",
"Ekstra / Ad-hoc Hizmetler",
"İmza ve Kapanış",
]

st.markdown(
""" <style>
:root {
--navy: #0b1f33;
--blue: #0d5f88;
--cyan: #1597a8;
--background: #f3f6fa;
--card: #ffffff;
--text: #10233c;
--muted: #526579;
--border: #d9e3ec;
}

```
.stApp {
    background: #f3f6fa;
    color: #10233c;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #07192b 0%,
        #123452 100%
    );
    border-right: 1px solid rgba(255, 255, 255, 0.12);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #ffffff !important;
}

section[data-testid="stSidebar"]
div[role="radiogroup"] label {
    background: rgba(255, 255, 255, 0.06);
    border-radius: 9px;
    padding: 0.25rem 0.45rem;
    margin-bottom: 0.12rem;
}

section[data-testid="stSidebar"]
div[role="radiogroup"] label:hover {
    background: rgba(255, 255, 255, 0.14);
}

.hero {
    background: linear-gradient(
        125deg,
        #081a2d 0%,
        #0e527c 58%,
        #12899b 100%
    );
    color: #ffffff;
    border-radius: 24px;
    padding: 2rem 2.2rem;
    box-shadow: 0 18px 45px rgba(9, 30, 50, 0.18);
    margin-bottom: 1.25rem;
}

.hero-kicker {
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    opacity: 0.82;
    margin-bottom: 0.55rem;
}

.hero-title {
    font-size: clamp(2.2rem, 4vw, 3.6rem);
    font-weight: 850;
    line-height: 1.05;
    margin-bottom: 0.7rem;
}

.hero-text {
    font-size: 1.05rem;
    line-height: 1.65;
    max-width: 960px;
    opacity: 0.92;
}

.badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.24);
    color: #ffffff;
    border-radius: 999px;
    padding: 0.38rem 0.8rem;
    margin-top: 1rem;
    margin-right: 0.45rem;
    font-size: 0.82rem;
    font-weight: 700;
}

.card {
    background: #ffffff;
    border: 1px solid #d9e3ec;
    border-radius: 17px;
    padding: 1.15rem 1.2rem;
    box-shadow: 0 7px 22px rgba(14, 38, 62, 0.06);
    min-height: 138px;
    margin-bottom: 0.9rem;
}

.card-title {
    color: #10233c;
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: 0.45rem;
}

.card-text {
    color: #526579;
    font-size: 0.94rem;
    line-height: 1.55;
}

.notice {
    background: #fff8e7;
    border: 1px solid #edd18c;
    color: #674900;
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
    line-height: 1.55;
}

.step {
    background: #ffffff;
    border: 1px solid #d9e3ec;
    border-left: 5px solid #1597a8;
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.75rem;
    color: #10233c;
}

.section-box {
    background: #ffffff;
    border: 1px solid #d9e3ec;
    border-radius: 16px;
    padding: 1.1rem;
    margin-bottom: 1rem;
}

.section-title {
    color: #10233c;
    font-size: 1.1rem;
    font-weight: 800;
    margin-bottom: 0.45rem;
}

.section-text {
    color: #526579;
    line-height: 1.55;
}

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #d9e3ec;
    border-radius: 15px;
    padding: 0.85rem 1rem;
    box-shadow: 0 6px 18px rgba(14, 38, 62, 0.05);
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] div {
    color: #10233c !important;
}

div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #10233c !important;
    border-color: #ccd8e4 !important;
}

div[data-baseweb="input"] > div {
    background: #ffffff !important;
    color: #10233c !important;
}

input,
textarea {
    color: #10233c !important;
    background: #ffffff !important;
}

.stAlert {
    color: #10233c;
}

h1,
h2,
h3,
h4,
p,
label {
    color: #10233c;
}
</style>
""",
unsafe_allow_html=True,

)

query_airline = st.query_params.get("airline", "AWG")

default_index = (
AIRLINES.index(query_airline)
if query_airline in AIRLINES
else 0
)

st.sidebar.markdown("# ✈️ SFC")
st.sidebar.caption("SCF–IKARUS Operasyon Rehberi")
st.sidebar.divider()

selected_airline = st.sidebar.radio(
"HAVAYOLU SAYFALARI",
AIRLINES,
index=default_index,
)

st.query_params["airline"] = selected_airline

st.sidebar.divider()
st.sidebar.caption("Aktif sayfa: " + selected_airline)
st.sidebar.caption("Toplam havayolu: " + str(len(AIRLINES)))
st.sidebar.caption("Her kod bağımsız rehber sayfasıdır.")

st.markdown(
f""" <div class="hero"> <div class="hero-kicker">
SFC • SCF–IKARUS DİJİTAL HANDBOOK </div>

```
    <div class="hero-title">
        {selected_airline} Hizmet Rehberi
    </div>

    <div class="hero-text">
        {selected_airline} havayoluna ait IKARUS hizmet
        girişleri, konu başlıkları, giriş kuralları,
        kontrol kaynakları, özel operasyon notları ve
        SCF kapanış adımları bu sayfada gösterilecektir.
    </div>

    <div>
        <span class="badge">
            {selected_airline}
        </span>

        <span class="badge">
            Havayolu Özel Sayfası
        </span>

        <span class="badge">
            SCF–IKARUS
        </span>

        <span class="badge">
            Taslak v0.1
        </span>
    </div>
</div>
""",
unsafe_allow_html=True,

)

metric_1, metric_2, metric_3, metric_4 = st.columns(4)

metric_1.metric(
"Havayolu Kodu",
selected_airline,
)

metric_2.metric(
"Ana Kategori",
len(CATEGORIES),
)

metric_3.metric(
"Tanımlı Hizmet",
"0",
)

metric_4.metric(
"İçerik Durumu",
"Taslak",
)

st.markdown(
""" <div class="notice"> <strong>
Operasyonel hizmet bilgileri henüz eklenmedi. </strong> <br>
Gerçek ve onaylı bilgiler paylaşılmadan sistem
tahmini veya uydurma hizmet kuralı göstermeyecektir. </div>
""",
unsafe_allow_html=True,
)

st.subheader("1. Havayolu Sayfa Özeti")

summary_1, summary_2, summary_3 = st.columns(3)

summary_1.markdown(
""" <div class="card"> <div class="card-title">
Hizmet Haritası </div>

```
    <div class="card-text">
        Hizmet adı, ana kategori, IKARUS konu başlığı,
        giriş alanı, giriş kuralı ve birim bilgileri
        burada yer alır.
    </div>
</div>
""",
unsafe_allow_html=True,
```

)

summary_2.markdown(
""" <div class="card"> <div class="card-title">
Havayolu Özel Kuralları </div>

```
    <div class="card-text">
        Yalnızca seçili havayoluna ait farklı
        uygulamalar, zorunlu açıklamalar ve istasyon
        notları gösterilir.
    </div>
</div>
""",
unsafe_allow_html=True,
```

)

summary_3.markdown(
""" <div class="card"> <div class="card-title">
SCF Kapanış Kontrolü </div>

```
    <div class="card-text">
        Uçuş, tescil, hizmet, süre, adet, açıklama
        ve imza kontrolleri kapanıştan önce tamamlanır.
    </div>
</div>
""",
unsafe_allow_html=True,
```

)

st.subheader("2. Hizmet Arama ve Filtreleme")

search_text = st.text_input(
"Hizmet veya IKARUS alanı ara",
placeholder=(
"Örnek: GPU, merdiven, otobüs, adet, süre"
),
)

selected_category = st.selectbox(
"Ana kategori",
["Tümü"] + CATEGORIES,
)

required_only = st.checkbox(
"Yalnızca zorunlu hizmetleri göster",
key=selected_airline + "_required",
)

st.caption(
"Arama metni: "
+ (
search_text
if search_text
else "Arama yapılmadı"
)
)

st.caption(
"Seçili kategori: "
+ selected_category
)

st.caption(
"Zorunlu filtre: "
+ (
"Açık"
if required_only
else "Kapalı"
)
)

st.subheader("3. IKARUS Hizmet Giriş Tablosu")

service_template = [
{
"Havayolu": selected_airline,
"Ana Kategori": "Ramp / Apron Hizmetleri",
"Hizmet Adı": "Gerçek hizmet adı",
"IKARUS Konu Başlığı": "Gerçek bölüm",
"IKARUS Alanı": "Adet / süre / saat",
"Giriş Kuralı": "Gerçekleşen değer girilir",
"Birim": "Adet / dakika / kg",
"Zorunlu": "Evet / Hayır",
"Ne Zaman Girilir?": "Hizmet gerçekleştiğinde",
"Kontrol Kaynağı": "Operasyon kaydı",
"Özel Not": "Havayolu özel kuralı",
},
{
"Havayolu": selected_airline,
"Ana Kategori": "Yolcu Hizmetleri",
"Hizmet Adı": "İkinci gerçek hizmet",
"IKARUS Konu Başlığı": "Gerçek bölüm",
"IKARUS Alanı": "Adet / açıklama",
"Giriş Kuralı": "Onaylı kurala göre girilir",
"Birim": "Adet",
"Zorunlu": "Evet / Hayır",
"Ne Zaman Girilir?": "Operasyon tamamlandığında",
"Kontrol Kaynağı": "Yolcu hizmetleri kaydı",
"Özel Not": "Doğrulanmış not",
},
{
"Havayolu": selected_airline,
"Ana Kategori": "GSE / Ekipman",
"Hizmet Adı": "Üçüncü gerçek hizmet",
"IKARUS Konu Başlığı": "Gerçek bölüm",
"IKARUS Alanı": "Başlangıç / bitiş",
"Giriş Kuralı": "Gerçek kullanım süresi girilir",
"Birim": "Dakika",
"Zorunlu": "Evet / Hayır",
"Ne Zaman Girilir?": "Ekipman kullanıldığında",
"Kontrol Kaynağı": "Ekipman kaydı",
"Özel Not": "Doğrulanmış not",
},
]

st.dataframe(
service_template,
use_container_width=True,
hide_index=True,
)

st.info(
"Bu tablo şablondur. Gerçek hizmet bilgilerini "
"gönderdiğinde her satırı havayoluna özel olarak "
"dolduracağız."
)

st.subheader("4. IKARUS Konu Başlıkları")

category_1, category_2, category_3 = st.columns(3)

category_1.markdown(
""" <div class="section-box"> <div class="section-title">
Uçuş Bilgileri </div>

```
    <div class="section-text">
        Uçuş numarası, tarih, yön, uçak tipi,
        tescil ve operasyon durumunun kontrol
        edildiği bölüm.
    </div>
</div>
""",
unsafe_allow_html=True,
```

)

category_2.markdown(
""" <div class="section-box"> <div class="section-title">
Yolcu Hizmetleri </div>

```
    <div class="section-text">
        Yolcu, transit, özel yolcu, otobüs ve
        ilgili terminal hizmetlerinin
        değerlendirildiği bölüm.
    </div>
</div>
""",
unsafe_allow_html=True,
```

)

category_3.markdown(
""" <div class="section-box"> <div class="section-title">
Ramp / Apron Hizmetleri </div>

```
    <div class="section-text">
        Apronda gerçekleşen ekipman, araç,
        yükleme ve uçak çevresi hizmetlerinin
        bulunduğu bölüm.
    </div>
</div>
""",
unsafe_allow_html=True,
```

)

category_4, category_5, category_6 = st.columns(3)

category_4.markdown(
""" <div class="section-box"> <div class="section-title">
Uçak Hizmetleri </div>

```
    <div class="section-text">
        Su, tuvalet, temizlik, enerji ve uçağa
        doğrudan verilen diğer hizmetlerin
        bulunduğu bölüm.
    </div>
</div>
""",
unsafe_allow_html=True,
```

)

category_5.markdown(
""" <div class="section-box"> <div class="section-title">
Yük Kontrol ve Operasyon </div>

```
    <div class="section-text">
        Yükleme, boşaltma, ağırlık, denge ve
        operasyon kontrol bilgilerinin yer aldığı
        bölüm.
    </div>
</div>
""",
unsafe_allow_html=True,
```

)

category_6.markdown(
""" <div class="section-box"> <div class="section-title">
Kargo ve Posta </div>

```
    <div class="section-text">
        Kargo, posta, özel yük ve ilgili miktar
        bilgilerinin girildiği bölüm.
    </div>
</div>
""",
unsafe_allow_html=True,
```

)

category_7, category_8, category_9 = st.columns(3)

category_7.markdown(
""" <div class="section-box"> <div class="section-title">
GSE / Ekipman </div>

```
    <div class="section-text">
        Kullanılan yer hizmetleri ekipmanlarının
        adet, başlangıç, bitiş ve süre bilgilerinin
        bulunduğu bölüm.
    </div>
</div>
""",
unsafe_allow_html=True,
```

)

category_8.markdown(
""" <div class="section-box"> <div class="section-title">
Ekstra / Ad-hoc Hizmetler </div>

```
    <div class="section-text">
        Standart paket dışında talep edilen veya
        plansız gerçekleşen hizmetlerin bulunduğu
        bölüm.
    </div>
</div>
""",
unsafe_allow_html=True,
```

)

category_9.markdown(
""" <div class="section-box"> <div class="section-title">
İmza ve Kapanış </div>

```
    <div class="section-text">
        Temsilci kontrolü, açıklama, imza, onay
        ve SCF kapanış işlemlerinin tamamlandığı
        bölüm.
    </div>
</div>
""",
unsafe_allow_html=True,
```

)

st.subheader("5. IKARUS İşlem Akışı")

st.markdown(
""" <div class="step"> <strong>Adım 1 — Uçuşu doğrula:</strong>
Uçuş numarası, tarih, yön, uçak tipi ve
tescili kontrol et. </div>

```
<div class="step">
    <strong>Adım 2 — Doğru kategoriyi aç:</strong>
    Hizmetin rehberde belirtilen IKARUS konu
    başlığına gir.
</div>

<div class="step">
    <strong>Adım 3 — Hizmeti seç:</strong>
    Gerçekleşen hizmeti doğru isim ve doğru
    kod üzerinden aç.
</div>

<div class="step">
    <strong>Adım 4 — Değeri gir:</strong>
    Adet, süre, saat, ağırlık veya açıklama
    alanını kurala göre doldur.
</div>

<div class="step">
    <strong>Adım 5 — Kaynağı kontrol et:</strong>
    Operasyon, ekipman, yükleme veya yetkili
    kayıtlarıyla karşılaştır.
</div>

<div class="step">
    <strong>Adım 6 — Mükerrer kaydı kontrol et:</strong>
    Aynı hizmetin iki kez girilmediğinden emin ol.
</div>

<div class="step">
    <strong>Adım 7 — SCF'yi tamamla:</strong>
    Eksik kayıt olmadığını doğrula ve imza
    sürecini tamamla.
</div>
""",
unsafe_allow_html=True,
```

)

st.subheader("6. SCF Kapanış Kontrol Listesi")

check_1 = st.checkbox(
"Doğru uçuş numarası ve tarih seçildi.",
key=selected_airline + "_check_1",
)

check_2 = st.checkbox(
"Arrival / Departure ayrımı kontrol edildi.",
key=selected_airline + "_check_2",
)

check_3 = st.checkbox(
"Uçak tipi ve tescili doğrulandı.",
key=selected_airline + "_check_3",
)

check_4 = st.checkbox(
"Gerçekleşen bütün hizmetler girildi.",
key=selected_airline + "_check_4",
)

check_5 = st.checkbox(
"Gerçekleşmeyen hizmetler eklenmedi.",
key=selected_airline + "_check_5",
)

check_6 = st.checkbox(
"Başlangıç ve bitiş saatleri kontrol edildi.",
key=selected_airline + "_check_6",
)

check_7 = st.checkbox(
"Adet, süre, ağırlık ve birimler doğrulandı.",
key=selected_airline + "_check_7",
)

check_8 = st.checkbox(
"Mükerrer hizmet bulunmadığı kontrol edildi.",
key=selected_airline + "_check_8",
)

check_9 = st.checkbox(
"Ekstra hizmet açıklamaları eklendi.",
key=selected_airline + "_check_9",
)

check_10 = st.checkbox(
"Havayolu özel kuralları kontrol edildi.",
key=selected_airline + "_check_10",
)

check_11 = st.checkbox(
"İmza ve kapanış işlemleri tamamlandı.",
key=selected_airline + "_check_11",
)

completed = sum(
[
check_1,
check_2,
check_3,
check_4,
check_5,
check_6,
check_7,
check_8,
check_9,
check_10,
check_11,
]
)

st.progress(completed / 11)

st.write(
"Tamamlanan kontrol: **"
+ str(completed)
+ "/11**"
)

st.warning(
"Eksik kontrol sayısı: "
+ str(11 - completed)
)

st.subheader("7. Havayolu Özel Notları")

st.markdown(
f""" <div class="section-box"> <div class="section-title">
{selected_airline} Operasyon Notları </div>

```
    <div class="section-text">
        Bu bölümde yalnızca {selected_airline}
        havayoluna ait özel hizmet kuralları,
        istisnalar, zorunlu açıklamalar ve yetkili
        onay bilgileri gösterilecektir.
    </div>
</div>
""",
unsafe_allow_html=True,
```

)

st.text_area(
"Geçici çalışma notları",
placeholder=(
selected_airline
+ " için not ekleyin..."
),
height=180,
key=selected_airline + "_notes",
)

st.subheader("8. Sürüm ve Onay Bilgileri")

version_1, version_2, version_3, version_4 = st.columns(4)

version_1.info(
"Sürüm\n\nTaslak v0.1"
)

version_2.info(
"Son Güncelleme\n\nBekleniyor"
)

version_3.info(
"Kaynak Doküman\n\nTanımlanmadı"
)

version_4.info(
"Onaylayan\n\nTanımlanmadı"
)

st.divider()

st.caption(
"SFC • "
+ selected_airline
+ " • SCF–IKARUS Dijital Operasyon Rehberi"
)
