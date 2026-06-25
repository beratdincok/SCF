```python
import streamlit as st


# =========================================================
# SAYFA AYARLARI
# =========================================================

st.set_page_config(
    page_title="SFC | SCF–IKARUS Rehberi",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# HAVAYOLU LİSTESİ
# =========================================================

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


# =========================================================
# IKARUS KONU BAŞLIKLARI
# =========================================================

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


# =========================================================
# ÖRNEK HİZMET ŞABLONU
# GERÇEK BİLGİLER DAHA SONRA BURAYA EKLENECEK
# =========================================================

SERVICE_TEMPLATE = [
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
        "Not": "Havayolu özel kuralı",
    }
]


# =========================================================
# SCF KAPANIŞ KONTROL LİSTESİ
# =========================================================

CONTROL_ITEMS = [
    "Doğru uçuş seçildi.",
    "Doğru uçuş tarihi seçildi.",
    "Arrival / Departure ayrımı kontrol edildi.",
    "Uçak tipi doğrulandı.",
    "Uçak tescili doğrulandı.",
    "Gerçekleşen bütün hizmetler girildi.",
    "Gerçekleşmeyen hizmetler eklenmedi.",
    "Başlangıç ve bitiş saatleri kontrol edildi.",
    "Adet, süre ve birimler doğrulandı.",
    "Mükerrer hizmet bulunmadığı kontrol edildi.",
    "Ekstra hizmetlerin açıklamaları eklendi.",
    "Havayolu özel kuralları kontrol edildi.",
    "İmza ve kapanış işlemleri tamamlandı.",
]


# =========================================================
# TASARIM
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 90% 5%,
                rgba(0, 188, 212, 0.12),
                transparent 25rem
            ),
            radial-gradient(
                circle at 10% 0%,
                rgba(33, 100, 255, 0.10),
                transparent 28rem
            ),
            #f5f7fb;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #061525 0%,
            #0a2947 100%
        );
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    [data-testid="stSidebar"] * {
        color: #f7fbff;
    }

    [data-testid="stSidebar"] .stRadio label {
        padding-top: 0.35rem;
        padding-bottom: 0.35rem;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 2rem 2.2rem;
        border-radius: 25px;
        color: white;
        background: linear-gradient(
            125deg,
            #07182b 0%,
            #0b3a69 55%,
            #08788c 100%
        );
        box-shadow: 0 22px 55px rgba(8, 26, 47, 0.18);
        margin-bottom: 1.3rem;
    }

    .hero-title {
        font-size: clamp(2rem, 4vw, 3.5rem);
        font-weight: 800;
        line-height: 1.08;
        margin-top: 0.4rem;
        margin-bottom: 0.7rem;
    }

    .hero-subtitle {
        opacity: 0.90;
        font-size: 1.05rem;
        max-width: 900px;
        line-height: 1.65;
    }

    .hero-top {
        font-size: 0.78rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        opacity: 0.80;
        font-weight: 700;
    }

    .badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        margin-top: 1rem;
        margin-right: 0.4rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.13);
        border: 1px solid rgba(255, 255, 255, 0.18);
        font-size: 0.82rem;
        font-weight: 650;
    }

    .info-card {
        background: rgba(255, 255, 255, 0.96);
        border: 1px solid rgba(15, 55, 95, 0.14);
        border-radius: 18px;
        padding: 1.2rem 1.25rem;
        box-shadow: 0 8px 28px rgba(12, 39, 69, 0.06);
        min-height: 145px;
        margin-bottom: 0.8rem;
    }

    .info-card h3 {
        margin: 0 0 0.45rem;
        color: #0b2542;
        font-size: 1.05rem;
    }

    .info-card p {
        margin: 0;
        color: #53657a;
        font-size: 0.92rem;
        line-height: 1.55;
    }

    .airline-card {
        background: white;
        border: 1px solid rgba(15, 55, 95, 0.14);
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 6px 20px rgba(12, 39, 69, 0.05);
        text-align: center;
        margin-bottom: 0.8rem;
    }

    .airline-code {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0b3a69;
        margin-bottom: 0.25rem;
    }

    .airline-text {
        font-size: 0.82rem;
        color: #66778a;
    }

    .warning-box {
        background: #fff8e6;
        border: 1px solid #f2d28a;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        color: #62490d;
        line-height: 1.6;
        margin-bottom: 1rem;
    }

    .success-box {
        background: #eafaf2;
        border: 1px solid #9dddbd;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        color: #155b36;
        line-height: 1.6;
        margin-bottom: 1rem;
    }

    .section-label {
        color: #53657a;
        font-size: 0.92rem;
        margin-bottom: 0.5rem;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid rgba(15, 55, 95, 0.12);
        padding: 1rem;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(12, 39, 69, 0.05);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# YARDIMCI FONKSİYONLAR
# =========================================================

def show_hero(title, subtitle, badges):
    badge_html = ""

    for badge in badges:
        badge_html += f'<span class="badge">{badge}</span>'

    st.markdown(
        f"""
        <section class="hero">
            <div class="hero-top">
                SFC • SCF–IKARUS
            </div>

            <div class="hero-title">
                {title}
            </div>

            <div class="hero-subtitle">
                {subtitle}
            </div>

            <div>
                {badge_html}
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def show_info_card(title, description):
    st.markdown(
        f"""
        <div class="info-card">
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_airline_card(airline_code):
    st.markdown(
        f"""
        <div class="airline-card">
            <div class="airline-code">{airline_code}</div>
            <div class="airline-text">Havayolu rehberi</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# SOL MENÜ
# =========================================================

with st.sidebar:
    st.markdown("# ✈️ SFC")
    st.caption("SCF–IKARUS Operasyon Rehberi")

    st.divider()

    selected_page = st.radio(
        "Sayfa seçin",
        [
            "Ana Sayfa",
            "Havayolu Rehberi",
            "Tüm Havayolları",
            "SCF Kontrol Listesi",
            "Sistem Hakkında",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.caption("Modern Streamlit sunum sürümü")
    st.caption("Toplam havayolu: " + str(len(AIRLINES)))


# =========================================================
# ANA SAYFA
# =========================================================

if selected_page == "Ana Sayfa":

    show_hero(
        title="Dijital Operasyon Rehberi",
        subtitle=(
            "Havayolu bazında IKARUS'a girilecek hizmetleri, "
            "konu başlıklarını, giriş kurallarını ve SCF kontrol "
            "adımlarını tek bir sistem üzerinden yönetin."
        ),
        badges=[
            str(len(AIRLINES)) + " Havayolu",
            "Mobil Uyumlu",
            "Sunum Modu",
            "Tek Dosyalık Sistem",
        ],
    )

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)

    with metric_1:
        st.metric(
            label="Havayolu",
            value=len(AIRLINES),
        )

    with metric_2:
        st.metric(
            label="Ana Kategori",
            value=len(CATEGORIES),
        )

    with metric_3:
        st.metric(
            label="Kontrol Maddesi",
            value=len(CONTROL_ITEMS),
        )

    with metric_4:
        st.metric(
            label="Sistem Durumu",
            value="Aktif",
        )

    st.write("")

    column_1, column_2, column_3 = st.columns(3)

    with column_1:
        show_info_card(
            "Havayolu Bazlı Yapı",
            (
                "Her havayolu ayrı seçilir. Kullanıcı yalnızca "
                "seçtiği havayoluna ait hizmetleri ve kuralları görür."
            ),
        )

    with column_2:
        show_info_card(
            "IKARUS Eşleştirmesi",
            (
                "Hizmet adı, IKARUS konu başlığı, giriş alanı, "
                "birim, zorunluluk ve kontrol kaynağı birlikte gösterilir."
            ),
        )

    with column_3:
        show_info_card(
            "SCF Kapanış Kontrolü",
            (
                "SCF tamamlanmadan önce uçuş, tescil, saat, adet, "
                "ekstra hizmet ve imza kontrolleri yapılır."
            ),
        )

    st.subheader("Sistemde Bulunan Konu Başlıkları")

    category_columns = st.columns(3)

    for index, category in enumerate(CATEGORIES):
        with category_columns[index % 3]:
            st.info(category)


# =========================================================
# HAVAYOLU REHBERİ
# =========================================================

elif selected_page == "Havayolu Rehberi":

    selected_airline = st.selectbox(
        "Havayolu seçin",
        AIRLINES,
        index=0,
    )

    show_hero(
        title=selected_airline + " Hizmet Rehberi",
        subtitle=(
            "Bu sayfada seçilen havayoluna ait IKARUS hizmetleri, "
            "konu başlıkları, giriş kuralları ve operasyon notları "
            "gösterilecektir."
        ),
        badges=[
            selected_airline,
            "Havayolu Özel Sayfası",
            "IKARUS Rehberi",
        ],
    )

    st.markdown(
        """
        <div class="warning-box">
            <b>Operasyonel hizmet bilgileri henüz eklenmedi.</b>
            <br>
            Gerçek hizmet bilgileri paylaşılmadan sistem tahmini,
            uydurma veya doğrulanmamış operasyon kuralı göstermeyecektir.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Hizmet Bilgisi Şablonu")

    st.dataframe(
        SERVICE_TEMPLATE,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("IKARUS Konu Başlıkları")

    category_tabs = st.tabs(CATEGORIES)

    for category_tab, category in zip(
        category_tabs,
        CATEGORIES,
    ):
        with category_tab:

            st.markdown(
                f"### {selected_airline} • {category}"
            )

            st.info(
                "Bu başlığa ait hizmet bilgileri gönderildiğinde "
                "ilgili hizmetler burada gösterilecektir."
            )

            st.markdown("**Her hizmet için gösterilecek alanlar:**")

            st.write("• Hizmet adı")
            st.write("• IKARUS konu başlığı")
            st.write("• IKARUS giriş alanı")
            st.write("• Giriş kuralı")
            st.write("• Birim")
            st.write("• Zorunlu / isteğe bağlı")
            st.write("• Ne zaman girileceği")
            st.write("• Kontrol kaynağı")
            st.write("• Havayolu özel notu")


# =========================================================
# TÜM HAVAYOLLARI
# =========================================================

elif selected_page == "Tüm Havayolları":

    show_hero(
        title="Havayolu Listesi",
        subtitle=(
            "Sistemde tanımlı tüm havayollarını tek ekranda "
            "görüntüleyin ve havayolu koduna göre arama yapın."
        ),
        badges=[
            "Toplam " + str(len(AIRLINES)) + " Kod",
            "Hızlı Arama",
            "A–Z Görünüm",
        ],
    )

    search_query = st.text_input(
        "Havayolu kodu ara",
        placeholder="Örnek: SVA, UAE, UZB",
    )

    if search_query:
        filtered_airlines = []

        for airline_code in AIRLINES:
            if search_query.upper() in airline_code:
                filtered_airlines.append(airline_code)
    else:
        filtered_airlines = AIRLINES

    st.write(
        "**Gösterilen havayolu sayısı:** "
        + str(len(filtered_airlines))
    )

    if len(filtered_airlines) == 0:
        st.warning("Aradığınız havayolu kodu bulunamadı.")

    else:
        airline_columns = st.columns(5)

        for index, airline_code in enumerate(filtered_airlines):
            with airline_columns[index % 5]:
                show_airline_card(airline_code)


# =========================================================
# SCF KONTROL LİSTESİ
# =========================================================

elif selected_page == "SCF Kontrol Listesi":

    show_hero(
        title="SCF Kapanış Kontrolü",
        subtitle=(
            "SCF tamamlanmadan önce temel operasyon ve hizmet "
            "doğrulama adımlarını işaretleyin."
        ),
        badges=[
            "Operasyon Kontrolü",
            "Eksik Bilgi Önleme",
            "Kapanış Rehberi",
        ],
    )

    selected_control_airline = st.selectbox(
        "Kontrol yapılacak havayolu",
        AIRLINES,
    )

    st.info(
        "Seçilen havayolu: " + selected_control_airline
    )

    completed_count = 0

    for index, control_item in enumerate(CONTROL_ITEMS):

        checkbox_value = st.checkbox(
            control_item,
            key="control_" + str(index),
        )

        if checkbox_value:
            completed_count += 1

    total_items = len(CONTROL_ITEMS)

    if total_items > 0:
        completion_rate = completed_count / total_items
    else:
        completion_rate = 0

    st.progress(completion_rate)

    st.write(
        "**Tamamlanan kontrol:** "
        + str(completed_count)
        + " / "
        + str(total_items)
    )

    if completed_count == total_items:

        st.markdown(
            """
            <div class="success-box">
                <b>Tüm temel kontroller tamamlandı.</b>
                <br>
                SCF kapanış sürecine geçmeden önce havayolu özel
                kurallarının ayrıca doğrulandığından emin olun.
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        remaining_count = total_items - completed_count

        st.warning(
            "Tamamlanması gereken "
            + str(remaining_count)
            + " kontrol maddesi bulunmaktadır."
        )


# =========================================================
# SİSTEM HAKKINDA
# =========================================================

elif selected_page == "Sistem Hakkında":

    show_hero(
        title="SFC Sistemi",
        subtitle=(
            "SFC, SCF ve IKARUS işlemleri için hazırlanmış "
            "havayolu bazlı dijital operasyon handbook sistemidir."
        ),
        badges=[
            "SCF",
            "IKARUS",
            "Dijital Handbook",
        ],
    )

    st.subheader("Sistemin Amacı")

    st.write(
        """
        SFC sisteminin amacı, her havayolu için IKARUS'a girilecek
        hizmetlerin hangi konu başlığı altında bulunduğunu personele
        açık ve anlaşılır şekilde göstermektir.
        """
    )

    st.subheader("Hizmet Kartlarında Bulunacak Bilgiler")

    st.write("• Havayolu kodu")
    st.write("• Ana hizmet kategorisi")
    st.write("• Hizmet adı")
    st.write("• IKARUS konu başlığı")
    st.write("• IKARUS giriş alanı")
    st.write("• Giriş kuralı")
    st.write("• Kullanılan birim")
    st.write("• Zorunluluk durumu")
    st.write("• Hizmetin ne zaman girileceği")
    st.write("• Doğrulama kaynağı")
    st.write("• Havayolu özel açıklaması")

    st.subheader("Tanımlı Havayolları")

    st.write(", ".join(AIRLINES))

    st.divider()

    st.caption(
        "SFC • SCF–IKARUS Operasyon Rehberi"
    )
```
