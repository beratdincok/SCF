import csv
import io
from datetime import date

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

CHECKLIST = [
"Doğru uçuş numarası seçildi.",
"Doğru uçuş tarihi seçildi.",
"Arrival / Departure ayrımı kontrol edildi.",
"Uçak tipi doğrulandı.",
"Uçak tescili doğrulandı.",
"Gerçekleşen bütün hizmetler girildi.",
"Gerçekleşmeyen hizmetler eklenmedi.",
"Başlangıç ve bitiş saatleri kontrol edildi.",
"Adet, süre, ağırlık ve diğer birimler doğrulandı.",
"Mükerrer hizmet bulunmadığı kontrol edildi.",
"Ekstra hizmet açıklamaları eklendi.",
"Havayolu özel kuralları kontrol edildi.",
"İmza ve kapanış işlemleri tamamlandı.",
]

SERVICES = {
code: []
for code in AIRLINES
}

AIRLINE_INFO = {
code: {
"version": "Taslak v0.1",
"last_update": "Güncelleme bekleniyor",
"source": "Kaynak doküman tanımlanmadı",
"approved_by": "Onaylayan kişi tanımlanmadı",
"general_note": (
"Bu havayolu için doğrulanmış özel operasyon "
"notları henüz sisteme eklenmedi."
),
}
for code in AIRLINES
}

TEMPLATE_ROWS = [
{
"Ana Kategori": "Ramp / Apron Hizmetleri",
"Hizmet Adı": "Gerçek hizmet adı",
"IKARUS Konu Başlığı": "Gerçek IKARUS bölümü",
"IKARUS Alanı": "Adet / süre / saat",
"Giriş Kuralı": "Gerçekleşen değer girilir",
"Birim": "Adet / dakika / kg",
"Zorunlu": "Evet / Hayır",
"Ne Zaman Girilir?": "Hizmet gerçekleştiğinde",
"Kontrol Kaynağı": "Operasyon kaydı",
"Havayolu Özel Notu": "Doğrulanmış özel kural",
},
{
"Ana Kategori": "Yolcu Hizmetleri",
"Hizmet Adı": "Gerçek yolcu hizmeti",
"IKARUS Konu Başlığı": "Gerçek IKARUS bölümü",
"IKARUS Alanı": "Adet / açıklama",
"Giriş Kuralı": "Onaylı kurala göre girilir",
"Birim": "Adet",
"Zorunlu": "Evet / Hayır",
"Ne Zaman Girilir?": "Operasyon tamamlandığında",
"Kontrol Kaynağı": "Yolcu hizmetleri kaydı",
"Havayolu Özel Notu": "Doğrulanmış özel kural",
},
{
"Ana Kategori": "GSE / Ekipman",
"Hizmet Adı": "Gerçek ekipman hizmeti",
"IKARUS Konu Başlığı": "Gerçek IKARUS bölümü",
"IKARUS Alanı": "Başlangıç / bitiş",
"Giriş Kuralı": "Gerçek kullanım süresi girilir",
"Birim": "Dakika",
"Zorunlu": "Evet / Hayır",
"Ne Zaman Girilir?": "Ekipman kullanıldığında",
"Kontrol Kaynağı": "Ekipman kullanım kaydı",
"Havayolu Özel Notu": "Doğrulanmış özel kural",
},
]

st.markdown(
""" <style>
:root {
--navy: #081b2d;
--navy-two: #123b5c;
--blue: #0b668f;
--cyan: #1aa5b7;
--background: #f3f6fa;
--card: #ffffff;
--text: #10233c;
--muted: #536579;
--border: #d8e2ec;
--warning-background: #fff8e7;
--warning-border: #ebd08b;
--warning-text: #654900;
}

```
.stApp {
    background: var(--background);
    color: var(--text);
}

.block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            var(--navy) 0%,
            var(--navy-two) 100%
        );
    border-right: 1px solid rgba(255, 255, 255, 0.12);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #ffffff !important;
}

section[data-testid="stSidebar"]
div[role="radiogroup"] label {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 0.25rem 0.5rem;
    margin-bottom: 0.13rem;
}

section[data-testid="stSidebar"]
div[role="radiogroup"] label:hover {
    background: rgba(255, 255, 255, 0.14);
}

.hero {
    background:
        linear-gradient(
            125deg,
            #081b2d 0%,
            #0d527c 57%,
            #118899 100%
        );
    color: #ffffff;
    border-radius: 24px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 18px 45px rgba(9, 30, 50, 0.18);
}

.hero-kicker {
    color: #ffffff;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    opacity: 0.82;
    margin-bottom: 0.55rem;
}

.hero-title {
    color: #ffffff;
    font-size: clamp(2.2rem, 4vw, 3.7rem);
    font-weight: 850;
    line-height: 1.06;
    margin-bottom: 0.7rem;
}

.hero-text {
    color: #ffffff;
    font-size: 1.05rem;
    line-height: 1.65;
    max-width: 1000px;
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
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 1.15rem 1.2rem;
    box-shadow: 0 7px 22px rgba(14, 38, 62, 0.06);
    min-height: 138px;
    margin-bottom: 0.9rem;
}

.card-title {
    color: var(--text);
    font-size: 1.07rem;
    font-weight: 800;
    margin-bottom: 0.45rem;
}

.card-text {
    color: var(--muted);
    font-size: 0.94rem;
    line-height: 1.55;
}

.notice {
    background: var(--warning-background);
    border: 1px solid var(--warning-border);
    color: var(--warning-text);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
    line-height: 1.55;
}

.section-box {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.1rem;
    margin-bottom: 1rem;
    min-height: 150px;
}

.section-title {
    color: var(--text);
    font-size: 1.08rem;
    font-weight: 800;
    margin-bottom: 0.45rem;
}

.section-text {
    color: var(--muted);
    font-size: 0.94rem;
    line-height: 1.55;
}

.step {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 5px solid var(--cyan);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.75rem;
    color: var(--text);
}

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 0.85rem 1rem;
    box-shadow: 0 6px 18px rgba(14, 38, 62, 0.05);
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] div {
    color: var(--text) !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #ffffff !important;
    color: var(--text) !important;
    border-color: #cbd7e3 !important;
}

input,
textarea {
    background: #ffffff !important;
    color: var(--text) !important;
}

h1,
h2,
h3,
h4,
p,
label {
    color: var(--text);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.35rem;
}

.stTabs [data-baseweb="tab"] {
    background: #e8eff5;
    border-radius: 10px 10px 0 0;
    color: #20364f;
    padding-left: 1rem;
    padding-right: 1rem;
}

.stTabs [aria-selected="true"] {
    background: var(--blue) !important;
    color: #ffffff !important;
}
</style>
""",
unsafe_allow_html=True,

)

query_airline = st.query_params.get("airline", "AWG")

default_airline_index = (
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
index=default_airline_index,
)

st.query_params["airline"] = selected_airline

st.sidebar.divider()
st.sidebar.caption("Aktif sayfa: " + selected_airline)
st.sidebar.caption("Toplam havayolu: " + str(len(AIRLINES)))
st.sidebar.caption("Her havayolu ayrı URL ile açılır.")

airline_services = SERVICES.get(
selected_airline,
[],
)

airline_information = AIRLINE_INFO.get(
selected_airline,
{},
)

st.markdown(
f""" <section class="hero"> <div class="hero-kicker">
SFC • SCF–IKARUS DİJİTAL HANDBOOK </div>

```
    <div class="hero-title">
        {selected_airline} Hizmet Rehberi
    </div>

    <div class="hero-text">
        {selected_airline} havayoluna ait IKARUS hizmet
        girişleri, konu başlıkları, giriş kuralları,
        kontrol kaynakları, özel operasyon notları ve
        SCF kapanış adımları bu sayfada gösterilir.
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
            {airline_information.get("version", "Taslak")}
        </span>
    </div>
</section>
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
len(airline_services),
)

metric_4.metric(
"İçerik Durumu",
(
"Hazır"
if airline_services
else "Taslak"
),
)

if not airline_services:
st.markdown(
""" <div class="notice"> <strong>
Operasyonel hizmet bilgileri henüz eklenmedi. </strong> <br>
Gerçek ve onaylı bilgiler paylaşılmadan sistem
tahmini veya uydurma hizmet kuralı göstermeyecektir. </div>
""",
unsafe_allow_html=True,
)

tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs(
[
"Hizmet Haritası",
"IKARUS İşlem Akışı",
"SCF Kontrolü",
"Havayolu Özel Notları",
"Sürüm ve Onay",
]
)

with tab_1:
st.subheader(
selected_airline
+ " Hizmet Haritası"
)

summary_1, summary_2, summary_3 = st.columns(3)

with summary_1:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">
                Hizmet Bilgileri
            </div>

            <div class="card-text">
                Hizmet adı, ana kategori, IKARUS konu
                başlığı ve giriş alanı birlikte gösterilir.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with summary_2:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">
                Giriş Kuralları
            </div>

            <div class="card-text">
                Adet, süre, saat, ağırlık, açıklama ve
                zorunluluk bilgileri açıkça belirtilir.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with summary_3:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">
                Kontrol Kaynakları
            </div>

            <div class="card-text">
                Operasyon, ekipman, yükleme veya yetkili
                kayıtlarının hangisinin kullanılacağı gösterilir.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

search_text = st.text_input(
    "Hizmet veya IKARUS alanı ara",
    placeholder=(
        "Örnek: GPU, merdiven, otobüs, adet, süre"
    ),
    key=selected_airline + "_search",
)

selected_category = st.selectbox(
    "Ana kategori",
    ["Tümü"] + CATEGORIES,
    key=selected_airline + "_category",
)

required_only = st.checkbox(
    "Yalnızca zorunlu hizmetleri göster",
    key=selected_airline + "_required",
)

filtered_services = [
    row
    for row in airline_services
    if (
        not search_text
        or search_text.lower()
        in " ".join(
            str(value).lower()
            for value in row.values()
        )
    )
    and (
        selected_category == "Tümü"
        or row.get("Ana Kategori") == selected_category
    )
    and (
        not required_only
        or row.get("Zorunlu") == "Evet"
    )
]

if filtered_services:
    st.dataframe(
        filtered_services,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info(
        "Bu havayolu için doğrulanmış hizmet kaydı "
        "bulunmuyor. Aşağıdaki tablo veri giriş "
        "şablonunu gösterir."
    )

    template_display = [
        {
            "Havayolu": selected_airline,
            **row,
        }
        for row in TEMPLATE_ROWS
    ]

    st.dataframe(
        template_display,
        use_container_width=True,
        hide_index=True,
    )

csv_buffer = io.StringIO()

csv_columns = [
    "Havayolu",
    "Ana Kategori",
    "Hizmet Adı",
    "IKARUS Konu Başlığı",
    "IKARUS Alanı",
    "Giriş Kuralı",
    "Birim",
    "Zorunlu",
    "Ne Zaman Girilir?",
    "Kontrol Kaynağı",
    "Havayolu Özel Notu",
]

csv_writer = csv.DictWriter(
    csv_buffer,
    fieldnames=csv_columns,
)

csv_writer.writeheader()

csv_writer.writerows(
    [
        {
            "Havayolu": selected_airline,
            **row,
        }
        for row in TEMPLATE_ROWS
    ]
)

st.download_button(
    label="Hizmet şablonunu CSV indir",
    data=csv_buffer.getvalue().encode("utf-8-sig"),
    file_name=(
        selected_airline
        + "_hizmet_sablonu.csv"
    ),
    mime="text/csv",
)

st.subheader("IKARUS Konu Başlıkları")

category_1, category_2, category_3 = st.columns(3)

with category_1:
    st.markdown(
        """
        <div class="section-box">
            <div class="section-title">
                Uçuş Bilgileri
            </div>

            <div class="section-text">
                Uçuş numarası, tarih, yön, uçak tipi,
                tescil ve operasyon durumunun kontrol
                edildiği bölüm.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with category_2:
    st.markdown(
        """
        <div class="section-box">
            <div class="section-title">
                Yolcu Hizmetleri
            </div>

            <div class="section-text">
                Yolcu, transit, özel yolcu, otobüs ve
                terminal hizmetlerinin bulunduğu bölüm.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with category_3:
    st.markdown(
        """
        <div class="section-box">
            <div class="section-title">
                Ramp / Apron Hizmetleri
            </div>

            <div class="section-text">
                Apronda gerçekleşen araç, ekipman,
                yükleme ve uçak çevresi hizmetleri.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

category_4, category_5, category_6 = st.columns(3)

with category_4:
    st.markdown(
        """
        <div class="section-box">
            <div class="section-title">
                Uçak Hizmetleri
            </div>

            <div class="section-text">
                Su, tuvalet, temizlik, enerji ve uçağa
                doğrudan verilen diğer hizmetler.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with category_5:
    st.markdown(
        """
        <div class="section-box">
            <div class="section-title">
                Yük Kontrol ve Operasyon
            </div>

            <div class="section-text">
                Yükleme, boşaltma, ağırlık, denge ve
                operasyon kontrol bilgileri.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with category_6:
    st.markdown(
        """
        <div class="section-box">
            <div class="section-title">
                Kargo ve Posta
            </div>

            <div class="section-text">
                Kargo, posta, özel yük ve ilgili miktar
                bilgilerinin girildiği bölüm.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

category_7, category_8, category_9 = st.columns(3)

with category_7:
    st.markdown(
        """
        <div class="section-box">
            <div class="section-title">
                GSE / Ekipman
            </div>

            <div class="section-text">
                Yer hizmetleri ekipmanlarının adet,
                başlangıç, bitiş ve süre bilgileri.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with category_8:
    st.markdown(
        """
        <div class="section-box">
            <div class="section-title">
                Ekstra / Ad-hoc Hizmetler
            </div>

            <div class="section-text">
                Standart paket dışında talep edilen veya
                plansız gerçekleşen hizmetler.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with category_9:
    st.markdown(
        """
        <div class="section-box">
            <div class="section-title">
                İmza ve Kapanış
            </div>

            <div class="section-text">
                Temsilci kontrolü, açıklama, imza, onay
                ve SCF kapanış işlemleri.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_2:
st.subheader("IKARUS İşlem Akışı")

st.markdown(
    """
    <div class="step">
        <strong>Adım 1 — Uçuşu doğrula:</strong>
        Uçuş numarası, tarih, yön, uçak tipi ve tescili
        kontrol et.
    </div>

    <div class="step">
        <strong>Adım 2 — Doğru kategoriyi aç:</strong>
        Hizmetin rehberde belirtilen IKARUS konu başlığına
        gir.
    </div>

    <div class="step">
        <strong>Adım 3 — Hizmeti seç:</strong>
        Gerçekleşen hizmeti doğru isim ve doğru kod
        üzerinden aç.
    </div>

    <div class="step">
        <strong>Adım 4 — Değeri gir:</strong>
        Adet, süre, saat, ağırlık veya açıklama alanını
        belirtilen kurala göre doldur.
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
        Eksik kayıt olmadığını doğrula ve imza sürecini
        tamamla.
    </div>
    """,
    unsafe_allow_html=True,
)

with tab_3:
st.subheader(
selected_airline
+ " SCF Kapanış Kontrolü"
)

checklist_results = [
    st.checkbox(
        item,
        key=(
            selected_airline
            + "_check_"
            + str(index)
        ),
    )
    for index, item in enumerate(CHECKLIST)
]

completed_count = sum(checklist_results)

total_count = len(CHECKLIST)

progress_value = (
    completed_count / total_count
    if total_count
    else 0
)

st.progress(progress_value)

st.write(
    "Tamamlanan kontrol: **"
    + str(completed_count)
    + "/"
    + str(total_count)
    + "**"
)

if completed_count == total_count:
    st.success(
        "Tüm temel SCF kontrolleri tamamlandı."
    )
else:
    st.warning(
        "Tamamlanması gereken "
        + str(total_count - completed_count)
        + " kontrol maddesi bulunuyor."
    )

with tab_4:
st.subheader(
selected_airline
+ " Havayolu Özel Notları"
)

st.info(
    airline_information.get(
        "general_note",
        "Özel not bulunmuyor.",
    )
)

st.text_area(
    "Geçici çalışma notları",
    placeholder=(
        selected_airline
        + " için sunum veya çalışma notu ekleyin..."
    ),
    height=220,
    key=selected_airline + "_notes",
)

st.warning(
    "Bu alana yazılan notlar kalıcı veritabanına "
    "kaydedilmez. Sayfa yenilendiğinde silinebilir."
)

with tab_5:
st.subheader("Sürüm ve Onay Bilgileri")

version_1, version_2 = st.columns(2)

with version_1:
    st.info(
        "Sürüm\n\n"
        + airline_information.get(
            "version",
            "Tanımsız",
        )
    )

    st.info(
        "Son Güncelleme\n\n"
        + airline_information.get(
            "last_update",
            "Tanımsız",
        )
    )

with version_2:
    st.info(
        "Kaynak Doküman\n\n"
        + airline_information.get(
            "source",
            "Tanımsız",
        )
    )

    st.info(
        "Onaylayan\n\n"
        + airline_information.get(
            "approved_by",
            "Tanımsız",
        )
    )

st.caption(
    "Sistem tarihi: "
    + date.today().strftime("%d.%m.%Y")
)

st.divider()

st.caption(
"SFC • "
+ selected_airline
+ " • SCF–IKARUS Dijital Operasyon Rehberi"
)
