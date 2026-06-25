import html
from datetime import date

import streamlit as st

st.set_page_config(
page_title="SFC | SCF–IKARUS Rehberi",
page_icon="✈️",
layout="wide",
initial_sidebar_state="expanded",
)

AIRLINES = [
"AWG", "AAR", "ABY", "AEE", "AHY", "AZG", "BBT", "CCA", "CES",
"CTN", "CSC", "CSN", "DAH", "DHX", "DLH", "ETD", "FAD", "FDX",
"GEC", "IAW", "IGT", "KAC", "KAL", "KNE", "KZR", "AYN", "MGH",
"SHI", "SVA", "RAM", "UAE", "UBD", "UZB", "BRU", "SKYAIR",
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
"Doğru uçuş numarası ve tarih seçildi.",
"Arrival / Departure ayrımı kontrol edildi.",
"Uçak tipi ve tescili doğrulandı.",
"Gerçekleşen bütün hizmetler girildi.",
"Gerçekleşmeyen hizmetler eklenmedi.",
"Başlangıç ve bitiş saatleri kontrol edildi.",
"Adet, süre, ağırlık ve diğer birimler doğrulandı.",
"Mükerrer hizmet bulunmadığı kontrol edildi.",
"Ekstra hizmet açıklamaları eklendi.",
"Havayolu özel kuralları kontrol edildi.",
"İmza ve kapanış işlemleri tamamlandı.",
]

# Gerçek hizmetleri aşağıdaki sözlüğe ekle.

#

# Örnek:

#

# AIRLINE_SERVICES["SVA"] = [

# {

# "category": "Ramp / Apron Hizmetleri",

# "service_name": "Gerçek hizmet adı",

# "ikarus_section": "IKARUS konu başlığı",

# "ikarus_field": "Adet / süre / saat alanı",

# "entry_rule": "Gerçekleşen değer girilir",

# "unit": "Adet",

# "required": "Evet",

# "when_to_enter": "Hizmet gerçekleştiğinde",

# "verification_source": "Operasyon kaydı",

# "notes": "Havayolu özel notu",

# }

# ]

AIRLINE_SERVICES = {
code: []
for code in AIRLINES
}

AIRLINE_INFO = {
code: {
"general_note": (
"Henüz doğrulanmış havayolu özel notu eklenmedi."
),
"source_document": "Kaynak doküman tanımlanmadı.",
"approved_by": "Onaylayan kişi tanımlanmadı.",
"last_update": "Güncelleme bekleniyor.",
"version": "Taslak v0.1",
}
for code in AIRLINES
}

st.markdown(
""" <style>
:root {
--navy: #0b1f33;
--blue: #0b5f8a;
--cyan: #1ea5b8;
--bg: #f4f7fb;
--card: #ffffff;
--text: #10233c;
--muted: #5d6d7e;
--border: #dce5ee;
}

```
.stApp {
    background: var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0b1f33 0%,
        #12324f 100%
    );
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #f8fbff;
}

.hero {
    padding: 2rem 2.2rem;
    border-radius: 24px;
    color: #ffffff;
    background: linear-gradient(
        125deg,
        #0b1f33 0%,
        #0d4b74 58%,
        #11879a 100%
    );
    box-shadow: 0 18px 44px rgba(11, 31, 51, 0.18);
    margin-bottom: 1.2rem;
}

.kicker {
    font-size: 0.78rem;
    font-weight: 750;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    opacity: 0.82;
    margin-bottom: 0.5rem;
}

.title {
    font-size: clamp(2rem, 4vw, 3.4rem);
    line-height: 1.08;
    font-weight: 850;
    margin-bottom: 0.7rem;
}

.subtitle {
    font-size: 1.05rem;
    line-height: 1.65;
    max-width: 980px;
    opacity: 0.92;
}

.badge {
    display: inline-block;
    margin-top: 1rem;
    margin-right: 0.45rem;
    padding: 0.38rem 0.78rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.24);
    color: #ffffff;
    font-size: 0.82rem;
    font-weight: 700;
}

.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.15rem 1.2rem;
    box-shadow: 0 8px 24px rgba(16, 35, 60, 0.06);
    min-height: 140px;
    margin-bottom: 0.9rem;
}

.card-title {
    color: var(--text);
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: 0.45rem;
}

.card-text {
    color: var(--muted);
    font-size: 0.94rem;
    line-height: 1.55;
}

.notice {
    background: #fff8e8;
    border: 1px solid #edd28f;
    color: #6e4d00;
    border-radius: 14px;
    padding: 0.95rem 1rem;
    margin-bottom: 1rem;
}

.step {
    background: #ffffff;
    border: 1px solid var(--border);
    border-left: 5px solid var(--cyan);
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 0.8rem;
    color: var(--text);
}

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 0.85rem 1rem;
    box-shadow: 0 6px 18px rgba(16, 35, 60, 0.05);
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
textarea {
    background: #ffffff !important;
    color: #10233c !important;
}

.stTabs [data-baseweb="tab"] {
    background: #eaf0f6;
    color: #20364f;
    border-radius: 10px 10px 0 0;
    padding-left: 1rem;
    padding-right: 1rem;
}

.stTabs [aria-selected="true"] {
    background: #0b5f8a !important;
    color: #ffffff !important;
}
</style>
""",
unsafe_allow_html=True,

)

def show_hero(title, subtitle, badges):
badge_html = "".join(
(
'<span class="badge">'
+ html.escape(str(badge))
+ "</span>"
)
for badge in badges
)

st.markdown(
    f"""
    <section class="hero">
        <div class="kicker">
            SFC • SCF–IKARUS
        </div>

        <div class="title">
            {html.escape(title)}
        </div>

        <div class="subtitle">
            {html.escape(subtitle)}
        </div>

        <div>
            {badge_html}
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

def show_card(title, text):
st.markdown(
f""" <div class="card"> <div class="card-title">
{html.escape(title)} </div>

```
        <div class="card-text">
            {html.escape(text)}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

def service_rows(services):
return [
{
"Ana Kategori": item.get("category", ""),
"Hizmet Adı": item.get("service_name", ""),
"IKARUS Konu Başlığı": item.get(
"ikarus_section",
"",
),
"IKARUS Alanı": item.get("ikarus_field", ""),
"Giriş Kuralı": item.get("entry_rule", ""),
"Birim": item.get("unit", ""),
"Zorunlu": item.get("required", ""),
"Ne Zaman Girilir?": item.get(
"when_to_enter",
"",
),
"Kontrol Kaynağı": item.get(
"verification_source",
"",
),
"Not": item.get("notes", ""),
}
for item in services
]

def template_row(code):
return [
{
"Havayolu": code,
"Ana Kategori": "Ramp / Apron Hizmetleri",
"Hizmet Adı": "Gerçek hizmet adı",
"IKARUS Konu Başlığı": (
"Gerçek IKARUS bölümü"
),
"IKARUS Alanı": (
"Adet / süre / saat alanı"
),
"Giriş Kuralı": (
"Gerçekleşen değer girilir"
),
"Birim": "Adet / dakika / kg",
"Zorunlu": "Evet / Hayır",
"Ne Zaman Girilir?": (
"Hizmet gerçekleştiğinde"
),
"Kontrol Kaynağı": "Operasyon kaydı",
"Not": "Havayolu özel kuralı",
}
]

def home_page():
show_hero(
"SFC Dijital Operasyon Rehberi",
(
"Her havayolu için IKARUS'a girilecek "
"hizmetleri, konu başlıklarını, giriş "
"kurallarını ve SCF kapanış kontrollerini "
"ayrı sayfalarda yönetin."
),
[
str(len(AIRLINES)) + " ayrı sayfa",
"Yüksek kontrast",
"Mobil uyumlu",
],
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Havayolu",
    len(AIRLINES),
)

col2.metric(
    "Ana kategori",
    len(CATEGORIES),
)

col3.metric(
    "Kontrol maddesi",
    len(CHECKLIST),
)

col4.metric(
    "Sistem durumu",
    "Aktif",
)

st.write("")

column1, column2, column3 = st.columns(3)

with column1:
    show_card(
        "Her havayolu ayrı sayfa",
        (
            "AWG'den SKYAIR'a kadar bütün kodlar "
            "sol menüde bağımsız sayfa ve bağımsız "
            "URL olarak yer alır."
        ),
    )

with column2:
    show_card(
        "Detaylı hizmet haritası",
        (
            "Her hizmet için IKARUS bölümü, giriş "
            "alanı, kural, birim, zorunluluk ve "
            "kontrol kaynağı gösterilir."
        ),
    )

with column3:
    show_card(
        "Okunabilir tasarım",
        (
            "Açık zemin, koyu metin, beyaz kartlar "
            "ve lacivert menü ile yüksek kontrast "
            "sağlanır."
        ),
    )

st.subheader("Kullanım akışı")

st.markdown(
    """
    <div class="step">
        <strong>1. Havayolunu seç:</strong>
        Sol menüden ilgili üçlü kodu aç.
    </div>

    <div class="step">
        <strong>2. Hizmeti bul:</strong>
        Hizmet adı, IKARUS başlığı veya kategori
        ile filtrele.
    </div>

    <div class="step">
        <strong>3. Giriş kuralını kontrol et:</strong>
        Adet, süre, saat, ağırlık veya açıklama
        alanını doğrula.
    </div>

    <div class="step">
        <strong>4. SCF kontrolünü tamamla:</strong>
        Bütün kapanış maddelerini işaretle.
    </div>
    """,
    unsafe_allow_html=True,
)

def all_airlines_page():
show_hero(
"Tüm Havayolları",
(
"Sistemde tanımlı bütün havayolu kodlarını "
"tek ekranda görüntüleyin."
),
[
"Toplam " + str(len(AIRLINES)) + " kod",
"A–Z görünüm",
"Ayrı sayfalar",
],
)

search = st.text_input(
    "Havayolu kodu ara",
    placeholder="Örnek: SVA, UAE, UZB",
)

if search:
    filtered = [
        code
        for code in AIRLINES
        if search.upper() in code
    ]
else:
    filtered = AIRLINES

st.caption(
    "Gösterilen havayolu sayısı: "
    + str(len(filtered))
)

columns = st.columns(5)

for index, code in enumerate(filtered):
    with columns[index % 5]:
        st.markdown(
            f"""
            <div
                class="card"
                style="
                    min-height: 105px;
                    text-align: center;
                "
            >
                <div
                    class="card-title"
                    style="font-size: 1.35rem;"
                >
                    {html.escape(code)}
                </div>

                <div class="card-text">
                    Ayrı havayolu sayfası
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def global_search_page():
show_hero(
"Genel Hizmet Araması",
(
"Bütün havayollarındaki hizmet kayıtlarını "
"tek ekranda arayın."
),
[
"Hizmet adı",
"IKARUS bölümü",
"Kategori filtresi",
],
)

rows = []

for code, services in AIRLINE_SERVICES.items():
    for service in services:
        row = {
            "Havayolu": code,
        }

        row.update(
            service_rows([service])[0]
        )

        rows.append(row)

query = st.text_input(
    "Arama",
    placeholder=(
        "GPU, merdiven, otobüs, süre..."
    ),
)

category = st.selectbox(
    "Kategori",
    ["Tümü"] + CATEGORIES,
)

filtered = rows

if query:
    query_lower = query.lower()

    filtered = [
        row
        for row in filtered
        if query_lower
        in " ".join(
            str(value).lower()
            for value in row.values()
        )
    ]

if category != "Tümü":
    filtered = [
        row
        for row in filtered
        if row.get("Ana Kategori") == category
    ]

if filtered:
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info(
        "Henüz arama yapılabilecek doğrulanmış "
        "hizmet kaydı bulunmuyor."
    )

def make_airline_page(code):
def airline_page():
services = AIRLINE_SERVICES.get(
code,
[],
)

    info = AIRLINE_INFO.get(
        code,
        {},
    )

    show_hero(
        code + " Hizmet Rehberi",
        (
            "Bu sayfa yalnızca seçilen havayoluna "
            "ait IKARUS hizmetlerini, giriş "
            "kurallarını, özel notları ve SCF "
            "kapanış kontrollerini gösterir."
        ),
        [
            code,
            str(len(services)) + " hizmet",
            info.get(
                "version",
                "Taslak",
            ),
        ],
    )

    metric1, metric2, metric3, metric4 = (
        st.columns(4)
    )

    metric1.metric(
        "Tanımlı hizmet",
        len(services),
    )

    if services:
        category_count = len(
            {
                item.get("category")
                for item in services
            }
        )
    else:
        category_count = 0

    metric2.metric(
        "Kategori",
        category_count,
    )

    required_count = sum(
        1
        for item in services
        if item.get("required") == "Evet"
    )

    metric3.metric(
        "Zorunlu hizmet",
        required_count,
    )

    metric4.metric(
        "Son güncelleme",
        info.get(
            "last_update",
            "Bekleniyor",
        ),
    )

    if not services:
        st.markdown(
            """
            <div class="notice">
                <strong>
                    Doğrulanmış hizmet kaydı henüz
                    eklenmedi.
                </strong>
                <br>
                Sistem tahmini veya uydurma operasyon
                kuralı göstermez.
            </div>
            """,
            unsafe_allow_html=True,
        )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Hizmet Haritası",
            "IKARUS İşlem Akışı",
            "SCF Kontrolü",
            "Özel Notlar",
            "Sürüm ve Onay",
        ]
    )

    with tab1:
        st.subheader(
            code + " hizmet listesi"
        )

        search = st.text_input(
            "Hizmet veya IKARUS alanı ara",
            placeholder=(
                "Örnek: GPU, merdiven, süre, adet"
            ),
            key="search_" + code,
        )

        category = st.selectbox(
            "Kategori filtresi",
            ["Tümü"] + CATEGORIES,
            key="category_" + code,
        )

        required_only = st.checkbox(
            "Yalnızca zorunlu hizmetleri göster",
            key="required_" + code,
        )

        filtered = services

        if search:
            search_lower = search.lower()

            filtered = [
                item
                for item in filtered
                if search_lower
                in " ".join(
                    str(value).lower()
                    for value in item.values()
                )
            ]

        if category != "Tümü":
            filtered = [
                item
                for item in filtered
                if item.get("category") == category
            ]

        if required_only:
            filtered = [
                item
                for item in filtered
                if item.get("required") == "Evet"
            ]

        if filtered:
            st.dataframe(
                service_rows(filtered),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info(
                "Bu filtrelere uygun doğrulanmış "
                "hizmet bulunamadı."
            )

            st.caption(
                "Aşağıdaki tablo, eklenecek "
                "hizmetlerin şablonunu gösterir."
            )

            st.dataframe(
                template_row(code),
                use_container_width=True,
                hide_index=True,
            )

    with tab2:
        st.subheader(
            "IKARUS işlem sırası"
        )

        st.markdown(
            """
            <div class="step">
                <strong>
                    Adım 1 — Uçuşu doğrula:
                </strong>
                Uçuş numarası, tarih, yön, uçak
                tipi ve tescili kontrol et.
            </div>

            <div class="step">
                <strong>
                    Adım 2 — Hizmeti seç:
                </strong>
                Rehberde belirtilen kategori ve
                IKARUS başlığını aç.
            </div>

            <div class="step">
                <strong>
                    Adım 3 — Değeri gir:
                </strong>
                Adet, süre, saat, ağırlık veya
                açıklama alanını kurala göre doldur.
            </div>

            <div class="step">
                <strong>
                    Adım 4 — Kaynağı doğrula:
                </strong>
                Operasyon, ekipman, yükleme veya
                yetkili kayıtlarıyla karşılaştır.
            </div>

            <div class="step">
                <strong>
                    Adım 5 — SCF'yi kapat:
                </strong>
                Eksik ve mükerrer kayıt olmadığını
                kontrol ederek imza sürecini tamamla.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.subheader(
            "IKARUS konu başlıkları"
        )

        columns = st.columns(3)

        for index, category_name in enumerate(
            CATEGORIES
        ):
            with columns[index % 3]:
                st.info(category_name)

    with tab3:
        st.subheader(
            code + " SCF kapanış kontrolü"
        )

        completed = 0

        for index, item in enumerate(CHECKLIST):
            checked = st.checkbox(
                item,
                key=(
                    code
                    + "_check_"
                    + str(index)
                ),
            )

            if checked:
                completed += 1

        total = len(CHECKLIST)

        if total:
            progress = completed / total
        else:
            progress = 0

        st.progress(progress)

        st.write(
            "Tamamlanan kontrol: **"
            + str(completed)
            + "/"
            + str(total)
            + "**"
        )

        if completed == total:
            st.success(
                "Tüm temel kontroller tamamlandı."
            )
        else:
            remaining = total - completed

            st.warning(
                "Tamamlanması gereken "
                + str(remaining)
                + " madde bulunuyor."
            )

    with tab4:
        st.subheader(
            "Havayolu özel notları"
        )

        st.info(
            info.get(
                "general_note",
                "Not bulunmuyor.",
            )
        )

        st.text_area(
            "Sunum / çalışma notları",
            placeholder=(
                "Bu alan geçici not almak içindir."
            ),
            height=180,
            key="notes_" + code,
        )

    with tab5:
        st.subheader(
            "Sürüm ve onay bilgileri"
        )

        left, right = st.columns(2)

        left.info(
            "Sürüm: "
            + info.get(
                "version",
                "Tanımsız",
            )
        )

        left.info(
            "Son güncelleme: "
            + info.get(
                "last_update",
                "Tanımsız",
            )
        )

        right.info(
            "Kaynak doküman: "
            + info.get(
                "source_document",
                "Tanımsız",
            )
        )

        right.info(
            "Onaylayan: "
            + info.get(
                "approved_by",
                "Tanımsız",
            )
        )

        st.caption(
            "Sayfa tarihi: "
            + date.today().strftime(
                "%d.%m.%Y"
            )
        )

return airline_page

st.sidebar.markdown("# ✈️ SFC")

st.sidebar.caption(
"SCF–IKARUS Operasyon Rehberi"
)

st.sidebar.divider()

main_pages = [
st.Page(
home_page,
title="Ana Sayfa",
icon="🏠",
url_path="home",
default=True,
),
st.Page(
all_airlines_page,
title="Tüm Havayolları",
icon="🗂️",
url_path="airlines",
),
st.Page(
global_search_page,
title="Genel Hizmet Araması",
icon="🔎",
url_path="search",
),
]

pages_a_d = [
st.Page(
make_airline_page(code),
title=code,
icon="✈️",
url_path=(
"airline-"
+ code.lower()
),
)
for code in AIRLINES
if code[0] in "ABCD"
]

pages_e_l = [
st.Page(
make_airline_page(code),
title=code,
icon="✈️",
url_path=(
"airline-"
+ code.lower()
),
)
for code in AIRLINES
if code[0] in "EFGHIJKL"
]

pages_m_z = [
st.Page(
make_airline_page(code),
title=code,
icon="✈️",
url_path=(
"airline-"
+ code.lower()
),
)
for code in AIRLINES
if code[0] in "MNOPQRSTUVWXYZ"
]

navigation = st.navigation(
{
"Ana Menü": main_pages,
"Havayolları A–D": pages_a_d,
"Havayolları E–L": pages_e_l,
"Havayolları M–Z": pages_m_z,
},
position="sidebar",
expanded=True,
)

st.sidebar.divider()

st.sidebar.caption(
"Toplam havayolu: "
+ str(len(AIRLINES))
)

st.sidebar.caption(
"Her havayolu ayrı sayfadır."
)

navigation.run()
