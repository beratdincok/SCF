import streamlit as st

st.set_page_config(
page_title="SFC | SCF–IKARUS Rehberi",
page_icon="✈️",
layout="wide",
initial_sidebar_state="expanded"
)

AIRLINES = ["AWG", "AAR", "ABY", "AEE", "AHY", "AZG", "BBT", "CCA", "CES", "CTN", "CSC", "CSN", "DAH", "DHX", "DLH", "ETD", "FAD", "FDX", "GEC", "IAW", "IGT", "KAC", "KAL", "KNE", "KZR", "AYN", "MGH", "SHI", "SVA", "RAM", "UAE", "UBD", "UZB", "BRU", "SKYAIR"]

CATEGORIES = ["Uçuş Bilgileri", "Yolcu Hizmetleri", "Ramp / Apron Hizmetleri", "Uçak Hizmetleri", "Yük Kontrol ve Operasyon", "Kargo ve Posta", "GSE / Ekipman", "Ekstra / Ad-hoc Hizmetler", "İmza ve Kapanış"]

st.markdown(
""" <style>
.stApp {
background:
radial-gradient(
circle at 90% 5%,
rgba(0, 188, 212, 0.12),
transparent 25rem
),
#f5f7fb;
}

```
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #061525 0%,
        #0a2947 100%
    );
}

[data-testid="stSidebar"] * {
    color: white;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}

.hero {
    padding: 2rem;
    border-radius: 24px;
    color: white;
    background: linear-gradient(
        125deg,
        #07182b 0%,
        #0b3a69 55%,
        #08788c 100%
    );
    box-shadow: 0 20px 50px rgba(8, 26, 47, 0.18);
    margin-bottom: 1.2rem;
}

.hero-title {
    margin: 0 0 0.6rem 0;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.1;
}

.hero-subtitle {
    margin: 0;
    opacity: 0.90;
    font-size: 1.05rem;
    line-height: 1.6;
}

.badge {
    display: inline-block;
    margin-top: 1rem;
    margin-right: 0.4rem;
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.20);
    font-size: 0.85rem;
    font-weight: 600;
}

.info-card {
    background: white;
    border: 1px solid rgba(15, 55, 95, 0.13);
    border-radius: 18px;
    padding: 1.2rem;
    box-shadow: 0 8px 26px rgba(12, 39, 69, 0.06);
    margin-bottom: 1rem;
}

.info-card-title {
    color: #0b2542;
    font-size: 1.1rem;
    font-weight: 750;
    margin-bottom: 0.4rem;
}

.info-card-text {
    color: #53657a;
    font-size: 0.94rem;
    line-height: 1.55;
}
</style>
""",
unsafe_allow_html=True
```

)

st.sidebar.title("✈️ SFC")
st.sidebar.caption("SCF–IKARUS Operasyon Rehberi")
st.sidebar.divider()

selected_airline = st.sidebar.selectbox(
"Havayolu seçin",
AIRLINES
)

search_text = st.sidebar.text_input(
"Hizmet ara",
placeholder="Örnek: GPU, merdiven, otobüs"
)

st.sidebar.divider()
st.sidebar.caption("Toplam havayolu: " + str(len(AIRLINES)))
st.sidebar.caption("Havayolu bazlı dijital handbook")

st.markdown(
f""" <div class="hero"> <div class="hero-title">
{selected_airline} Hizmet Rehberi </div>

```
    <div class="hero-subtitle">
        IKARUS'a girilecek hizmetleri, konu başlıklarını,
        giriş kurallarını ve SCF kontrol adımlarını
        havayolu bazında görüntüleyin.
    </div>

    <div>
        <span class="badge">{selected_airline}</span>
        <span class="badge">Toplam {len(AIRLINES)} Havayolu</span>
        <span class="badge">SCF–IKARUS</span>
        <span class="badge">Dijital Handbook</span>
    </div>
</div>
""",
unsafe_allow_html=True
```

)

st.info(
"Gerçek operasyonel hizmet bilgileri gönderildikçe "
"seçilen havayolunun rehberine eklenecektir."
)

st.markdown(
""" <div class="info-card"> <div class="info-card-title">
Havayolu Bazlı Kullanım </div>

```
    <div class="info-card-text">
        Sol menüden havayolu seçildiğinde sayfadaki rehber,
        hizmet şablonu ve kontrol işlemleri seçilen havayoluna
        göre görüntülenir.
    </div>
</div>
""",
unsafe_allow_html=True
```

)

st.subheader("IKARUS Konu Başlıkları")

st.write(" • ".join(CATEGORIES))

st.subheader("Hizmet Giriş Şablonu")

st.dataframe(
[
{
"Havayolu": selected_airline,
"Ana kategori": "Ramp / Apron Hizmetleri",
"Hizmet adı": "Gerçek hizmet adı",
"IKARUS konu başlığı": "Gerçek IKARUS bölümü",
"IKARUS alanı": "Adet / süre / saat",
"Giriş kuralı": "Gerçekleşen değer girilir",
"Birim": "Adet / dakika / kg",
"Zorunlu": "Evet / Hayır",
"Ne zaman girilir?": "Hizmet gerçekleştiğinde",
"Kontrol kaynağı": "Operasyon kaydı",
"Not": "Havayolu özel kuralı"
}
],
use_container_width=True,
hide_index=True
)

st.subheader("Seçilen Havayolu")

st.success(
"Aktif havayolu: " + selected_airline
)

st.subheader("SCF Kapanış Kontrolü")

st.checkbox(
"Doğru uçuş ve tarih seçildi.",
key="check_1"
)

st.checkbox(
"Arrival / Departure ayrımı kontrol edildi.",
key="check_2"
)

st.checkbox(
"Uçak tipi ve tescili doğrulandı.",
key="check_3"
)

st.checkbox(
"Gerçekleşen bütün hizmetler girildi.",
key="check_4"
)

st.checkbox(
"Gerçekleşmeyen hizmetler eklenmedi.",
key="check_5"
)

st.checkbox(
"Saat, adet, süre ve birimler kontrol edildi.",
key="check_6"
)

st.checkbox(
"Mükerrer hizmet bulunmadığı kontrol edildi.",
key="check_7"
)

st.checkbox(
"Ekstra hizmet açıklamaları eklendi.",
key="check_8"
)

st.checkbox(
"Havayolu özel kuralları kontrol edildi.",
key="check_9"
)

st.checkbox(
"İmza ve kapanış işlemleri tamamlandı.",
key="check_10"
)

st.divider()

st.caption(
"SFC • SCF–IKARUS Dijital Operasyon Rehberi"
)
