from **future** import annotations

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
"Yük Kontrol & Operasyon",
"Kargo & Posta",
"GSE / Ekipman",
"Ekstra / Ad-hoc Hizmetler",
"İmza & Kapanış",
]

st.markdown(
""" <style>
.stApp {
background:
radial-gradient(
circle at 88% 4%,
rgba(25, 198, 212, 0.12),
transparent 22rem
),
radial-gradient(
circle at 18% 0%,
rgba(11, 102, 255, 0.10),
transparent 25rem
),
#f7f9fc;
}

```
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #07182b 0%,
        #0a2440 100%
    );
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

[data-testid="stSidebar"] * {
    color: #f6fbff;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.3rem;
    padding-bottom: 3rem;
}

.hero {
    padding: 2rem 2.2rem;
    border-radius: 24px;
    color: white;
    background: linear-gradient(
        125deg,
        #07182b 0%,
        #0b3a69 55%,
        #08788c 100%
    );
    box-shadow: 0 22px 55px rgba(8, 26, 47, 0.18);
    margin-bottom: 1.2rem;
}

.hero h1 {
    font-size: clamp(2rem, 4vw, 3.6rem);
    margin: 0.2rem 0 0.5rem;
}

.hero p {
    opacity: 0.88;
    font-size: 1.05rem;
    margin: 0;
    max-width: 850px;
}

.badge {
    display: inline-block;
    padding: 0.35rem 0.7rem;
    margin-top: 1rem;
    margin-right: 0.4rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.13);
    border: 1px solid rgba(255, 255, 255, 0.18);
    font-size: 0.82rem;
    font-weight: 650;
}

.card {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(15, 55, 95, 0.14);
    border-radius: 18px;
    padding: 1.1rem 1.2rem;
    box-shadow: 0 8px 28px rgba(12, 39, 69, 0.06);
    min-height: 135px;
}

.card h3 {
    margin: 0 0 0.4rem;
    color: #0b2542;
    font-size: 1.05rem;
}

.card p {
    margin: 0;
    color: #53657a;
    font-size: 0.92rem;
}

.warning-box {
    background: #fff8e6;
    border: 1px solid #f2d28a;
    border-radius: 16px;
    padding: 1rem 1.1rem;
    color: #62490d;
}
</style>
""",
unsafe_allow_html=True,
```

)

with st.sidebar:
st.markdown("## ✈️ SFC")
st.caption("SCF–IKARUS Operasyon Rehberi")
st.divider()

```
page = st.radio(
    "Menü",
    [
        "Ana Sayfa",
        "Havayolu Rehberi",
        "Tüm Havayolları",
        "SCF Kontrol Listesi",
    ],
    label_visibility="collapsed",
)

st.divider()
st.caption("Sunum sürümü • Tek dosyalık güvenli yapı")
```

def hero(title: str, subtitle: str, badges: list[str]) -> None:
badge_html = "".join(
f'<span class="badge">{item}</span>'
for item in badges
)

```
st.markdown(
    f"""
    <section class="hero">
        <div style="
            font-size: 0.78rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            opacity: 0.8;
            font-weight: 700;
        ">
            SFC • SCF–IKARUS
        </div>

        <h1>{title}</h1>
        <p>{subtitle}</p>

        <div>
            {badge_html}
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)
```

if page == "Ana Sayfa":
hero(
"Dijital Operasyon Rehberi",
(
"Havayolu bazında IKARUS'a girilecek hizmetleri, "
"konu başlıklarını ve kontrol adımlarını tek noktada yönetin."
),
[
f"{len(AIRLINES)} Havayolu",
"Mobil Uyumlu",
"Sunum Modu",
],
)

```
column_1, column_2, column_3 = st.columns(3)

with column_1:
    st.markdown(
        """
        <div class="card">
            <h3>Havayolu Bazlı Yapı</h3>
            <p>
                Her havayolu kodu ayrı seçilir ve yalnızca
                ilgili hizmetler gösterilir.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with column_2:
    st.markdown(
        """
        <div class="card">
            <h3>IKARUS Eşleştirmesi</h3>
            <p>
                Hizmet adı, konu başlığı, alan, birim ve giriş
                kuralı birlikte gösterilir.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with column_3:
    st.markdown(
        """
        <div class="card">
            <h3>Operasyon Kontrolü</h3>
            <p>
                SCF kapatılmadan önce zorunlu kontroller
                tek listede tamamlanır.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("Kapsam")

category_columns = st.columns(3)

for index, category in enumerate(CATEGORIES):
    with category_columns[index % 3]:
        st.info(category)
```

elif page == "Havayolu Rehberi":
selected_airline = st.selectbox(
"Havayolu seçin",
AIRLINES,
)

```
hero(
    f"{selected_airline} Hizmet Rehberi",
    (
        "Bu sayfada seçilen havayoluna ait hizmetler, "
        "IKARUS konu başlıkları ve giriş kuralları gösterilecektir."
    ),
    [
        selected_airline,
        "Havayolu Özel Sayfası",
        "İçerik Bekleniyor",
    ],
)

st.markdown(
    """
    <div class="warning-box">
        <b>Operasyonel içerik henüz eklenmedi.</b>
        <br>
        Gerçek hizmet bilgileri paylaşılmadan sistem tahmini
        veya uydurma kural göstermeyecektir.
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Hizmet ekleme şablonu")

service_template = [
    {
        "Ana Kategori": "Ramp / Apron Hizmetleri",
        "Hizmet Adı": "Gerçek hizmet adı",
        "IKARUS Konu Başlığı": "Gerçek bölüm",
        "IKARUS Alanı": "Adet / süre / saat",
        "Giriş Kuralı": "Gerçekleşen değer girilir",
        "Birim": "Adet / dakika / kg",
        "Zorunlu": "Evet / Hayır",
        "Ne Zaman Girilir?": "Hizmet gerçekleştiğinde",
        "Kontrol Kaynağı": "Operasyon kaydı",
        "Not": "Havayolu özel kuralı",
    }
]

st.dataframe(
    service_template,
    use_container_width=True,
    hide_index=True,
)

st.subheader("Konu başlıkları")

category_tabs = st.tabs(CATEGORIES)

for category_tab, category in zip(
    category_tabs,
    CATEGORIES,
):
    with category_tab:
        st.caption(
            f"{selected_airline} • {category}"
        )

        st.info(
            "Bu başlığa ait hizmetler gönderildiğinde "
            "buraya eklenecek."
        )
```

elif page == "Tüm Havayolları":
hero(
"Havayolu Listesi",
(
"Sistemde tanımlı tüm havayollarını "
"tek ekranda görüntüleyin."
),
[
f"Toplam {len(AIRLINES)} Kod",
"A–Z Görünüm",
],
)

```
search_query = st.text_input(
    "Kod ara",
    placeholder="Örn. SVA, UAE, UZB",
)

if search_query:
    filtered_airlines = [
        code
        for code in AIRLINES
        if search_query.upper() in code
    ]
else:
    filtered_airlines = AIRLINES

if not filtered_airlines:
    st.warning("Aradığınız kod bulunamadı.")
else:
    airline_columns = st.columns(5)

    for index, airline_code in enumerate(filtered_airlines):
        with airline_columns[index % 5]:
            st.markdown(
                f"""
                <div
                    class="card"
                    style="
                        min-height: auto;
                        text-align: center;
                    "
                >
                    <h3>{airline_code}</h3>
                    <p>Havayolu rehberi</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
```

elif page == "SCF Kontrol Listesi":
hero(
"SCF Kapanış Kontrolü",
(
"SCF tamamlanmadan önce temel doğrulama "
"adımlarını işaretleyin."
),
[
"Operasyon Kontrolü",
"Eksik Bilgi Önleme",
],
)

```
control_items = [
    "Doğru uçuş ve tarih seçildi.",
    "Uçak tipi ve tescil doğrulandı.",
    "Gerçekleşen bütün hizmetler girildi.",
    "Gerçekleşmeyen hizmetler eklenmedi.",
    "Başlangıç ve bitiş saatleri kontrol edildi.",
    "Adet, süre ve birimler doğrulandı.",
    "Mükerrer hizmet bulunmadığı kontrol edildi.",
    "Ekstra hizmetlerin açıklamaları eklendi.",
    "Havayolu özel kuralları kontrol edildi.",
    "İmza ve kapanış işlemleri tamamlandı.",
]

completed_count = 0

for control_item in control_items:
    if st.checkbox(control_item):
        completed_count += 1

completion_rate = completed_count / len(control_items)

st.progress(completion_rate)

st.write(
    f"**Tamamlanan:** "
    f"{completed_count}/{len(control_items)}"
)

if completed_count == len(control_items):
    st.success("Tüm temel kontroller tamamlandı.")
else:
    st.warning(
        "SCF kapatılmadan önce eksik kontrolleri tamamlayın."
    )
```
