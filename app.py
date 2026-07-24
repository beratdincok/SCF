# SFC AIRLINE RULES BUILD 2026-07-24

import json
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="SFC | SCF–IKARUS Rehberi",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SABİT LİSTELER
# =========================================================

AIRLINES = [
    "AWG", "AAR", "ABY", "AEE", "AHY", "AZG", "BBT", "CCA", "CES",
    "CTN", "CSC", "CSN", "DAH", "DHX", "DLH", "ETD", "FAD", "FDX",
    "GEC", "IAW", "IGT", "KAC", "KAL", "KNE", "KZR", "AYN", "MGH",
    "SHI", "SVA", "RAM", "UAE", "UBD", "UZB", "BRU", "SKYAIR",
]


MENU_ITEMS = [
    "Havayolu Rehberi",
    "Yeni Bilgi Ekle",
    "Bilgi Düzenle / Sil",
    "Genel Operasyon Kuralları",
    "Temsilciler ve Kodlar",
    "Tüm Bilgilerde Ara",
    "Veri Yönetimi",
]


CATEGORIES = [
    "Kontuar Hizmeti",
    "GROUND Form",
    "INAD / NOREC",
    "CMA / VIP / VPS",
    "OBH",
    "Fatura",
    "Yemek / Otel",
    "Sizer",
    "ABS",
    "Gökkuşağı",
    "Ay Sonu Excess",
    "Temsilci",
    "Genel Operasyon",
    "Diğer",
]


REQUIRED_OPTIONS = [
    "Zorunlu",
    "Duruma Bağlı",
    "Bilgilendirme",
]


DATA_FILE = Path("services.json")
DEFAULTS_VERSION = "2026-07-24-v1"


# =========================================================
# GÖRSEL TASARIM
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #f3f6fa;
        color: #10233c;
    }

    .block-container {
        max-width: 1650px;
        padding-top: 1rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #07192b 0%,
            #123452 100%
        );
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: rgba(255, 255, 255, 0.09) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        border-radius: 10px !important;
        padding: 0.50rem 0.70rem !important;
        margin-bottom: 0.14rem !important;
        font-size: 0.84rem !important;
        font-weight: 700 !important;
        text-align: left !important;
        justify-content: flex-start !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(41, 194, 209, 0.22) !important;
        border-color: #29c2d1 !important;
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: #29c2d1 !important;
        color: #061b2e !important;
        border-color: #29c2d1 !important;
        font-weight: 900 !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #10233c !important;
        border: 1px solid #ccd8e4 !important;
        border-radius: 10px !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] div[data-baseweb="select"] input,
    section[data-testid="stSidebar"] div[data-baseweb="select"] div {
        color: #10233c !important;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #d9e3ec;
        border-radius: 14px;
        padding: 0.65rem 0.80rem;
        box-shadow: 0 5px 14px rgba(14, 38, 62, 0.05);
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] div {
        color: #10233c !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border: 1px solid #d9e3ec;
        border-radius: 14px;
        box-shadow: 0 5px 14px rgba(14, 38, 62, 0.05);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] h3,
    div[data-testid="stVerticalBlockBorderWrapper"] h4 {
        font-size: 1rem !important;
        line-height: 1.2 !important;
        margin-bottom: 0.10rem !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] p {
        font-size: 0.82rem !important;
        line-height: 1.35 !important;
        margin-bottom: 0.18rem !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button {
        min-height: 2rem !important;
        padding: 0.25rem 0.45rem !important;
        font-size: 0.76rem !important;
        border-radius: 8px !important;
    }

    div[data-testid="stExpander"] {
        background: #f8fafc !important;
        border: 1px solid #e1e8ef !important;
        border-radius: 10px !important;
    }

    div[data-testid="stExpander"] summary {
        font-size: 0.80rem !important;
        font-weight: 700 !important;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    textarea {
        background: #ffffff !important;
        color: #10233c !important;
        border-color: #ccd8e4 !important;
    }

    input {
        background: #ffffff !important;
        color: #10233c !important;
    }

    h1, h2, h3, h4, p, label {
        color: #10233c;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# YARDIMCI FONKSİYONLAR
# =========================================================

def safe_text(value):
    if value is None:
        return ""
    return str(value)


def new_id(prefix="rule"):
    return prefix + "-" + str(uuid.uuid4())


def empty_data():
    data = {code: [] for code in AIRLINES}
    data["__defaults_version__"] = ""
    return data


def create_rule(
    rule_id,
    airline,
    category,
    title,
    summary,
    details,
    ikarus_location="",
    service_name="",
    unit="",
    note="",
    requirement="Bilgilendirme",
):
    return {
        "id": rule_id,
        "Havayolu": airline,
        "Kategori": category,
        "Başlık": title,
        "Kısa Bilgi": summary,
        "Detay": details,
        "IKARUS Yeri": ikarus_location,
        "Servis Adı": service_name,
        "Unit / Değer": unit,
        "Not": note,
        "Durum": requirement,
        "Son Güncelleme": datetime.now().strftime("%d.%m.%Y %H:%M"),
    }


def default_data():
    data = empty_data()
    data["__defaults_version__"] = DEFAULTS_VERSION

    # -----------------------------------------------------
    # CSN
    # -----------------------------------------------------
    data["CSN"].append(
        create_rule(
            "default-csn-counter",
            "CSN",
            "Kontuar Hizmeti",
            "CSN kontuar hakkı",
            "Her 40 yolcu için 1 kontuar + 2 Business kontuarı.",
            (
                "Kontuar planlamasında her 40 yolcu için 1 adet Economy kontuar "
                "hesaplanır. Buna ek olarak 2 adet Business kontuarı açılır. "
                "Kontuar kullanım süresi 120 dakikadır."
            ),
            ikarus_location="Kontuar kullanımı / ilgili form",
            service_name="Kontuar",
            unit="120 dakika",
            note="CSN, China Southern Airlines kodudur.",
            requirement="Zorunlu",
        )
    )

    data["CSN"].append(
        create_rule(
            "default-csn-ground",
            "CSN",
            "GROUND Form",
            "CSN kontuar hizmeti GROUND/Extra form",
            "Kontuar kullanımı uçuş formunda bulunmaz.",
            (
                "Kontuar hizmetleri IKARUS Web uçuş formundan değil, "
                "IKARUS masaüstünde EXTRA FORM olarak girilir."
            ),
            ikarus_location="IKARUS Masaüstü / EXTRA FORM",
            service_name="Kontuar hizmeti",
            requirement="Zorunlu",
        )
    )

    data["CSN"].append(
        create_rule(
            "default-csn-cma",
            "CSN",
            "CMA / VIP / VPS",
            "CSN CMA işlemi",
            "CMA hizmetine ayrıca form açılmaz.",
            (
                "CSN için CMA operasyonu OPS tarafından girilir. "
                "CMA hizmetine ayrı form açılmaz. VIP hizmeti varsa "
                "EXTRA FORM düzenlenir."
            ),
            ikarus_location="VIP varsa IKARUS Masaüstü / EXTRA FORM",
            note="CSN uçuş kodu CZ olarak da belirtilmiştir.",
            requirement="Duruma Bağlı",
        )
    )

    data["CSN"].append(
        create_rule(
            "default-csn-obh",
            "CSN",
            "OBH",
            "CSN OBH kullanımı",
            "OBH her zaman 1 girilir.",
            service_name="OBH",
            unit="1",
            requirement="Zorunlu",
        )
    )

    # -----------------------------------------------------
    # BRU
    # -----------------------------------------------------
    data["BRU"].append(
        create_rule(
            "default-bru-counter",
            "BRU",
            "Kontuar Hizmeti",
            "BRU kontuar hakkı",
            "Her 50 yolcu için 1 kontuar + Business kontuarı.",
            (
                "Kontuar planlamasında her 50 yolcu için 1 adet Economy kontuar "
                "hesaplanır. Buna ek olarak Business kontuarı açılır. "
                "Kontuar kullanım süresi 120 dakikadır."
            ),
            ikarus_location="Kontuar kullanımı / ilgili form",
            service_name="Kontuar",
            unit="120 dakika",
            note=(
                "Kullanıcı notunda Business kontuar adedi 'BU' olarak verilmiştir. "
                "Kesin adet ayrıca doğrulanmalıdır."
            ),
            requirement="Zorunlu",
        )
    )

    data["BRU"].append(
        create_rule(
            "default-bru-cma",
            "BRU",
            "CMA / VIP / VPS",
            "BRU CMA/VIP hizmetleri",
            "CMA/VIP hizmeti uçuş formuna eklenir.",
            (
                "BRU havayoluna ait CMA veya VIP hizmetleri uçuş formuna eklenir. "
                "Not kısmına hizmet detayları yazılır."
            ),
            ikarus_location="Uçuş Formu",
            requirement="Duruma Bağlı",
        )
    )

    # -----------------------------------------------------
    # CSC
    # -----------------------------------------------------
    data["CSC"].append(
        create_rule(
            "default-csc-counter",
            "CSC",
            "Kontuar Hizmeti",
            "CSC kontuar hakkı",
            "Her 60 yolcu için 1 kontuar + 1 Business kontuarı.",
            (
                "Kontuar planlamasında her 60 yolcu için 1 adet Economy kontuar "
                "hesaplanır. Buna ek olarak 1 adet Business kontuarı açılır. "
                "Kontuar kullanım süresi 120 dakikadır."
            ),
            ikarus_location="Kontuar kullanımı / ilgili form",
            service_name="Kontuar",
            unit="120 dakika",
            requirement="Zorunlu",
        )
    )

    data["CSC"].append(
        create_rule(
            "default-csc-ground",
            "CSC",
            "GROUND Form",
            "CSC kontuar hizmeti",
            "Kontuar hizmeti EXTRA FORM olarak girilir.",
            (
                "Kontuar kullanımı uçuş formunda bulunmaz. IKARUS masaüstünde "
                "EXTRA FORM olarak hazırlanır."
            ),
            ikarus_location="IKARUS Masaüstü / EXTRA FORM",
            requirement="Zorunlu",
        )
    )

    data["CSC"].append(
        create_rule(
            "default-csc-cma",
            "CSC",
            "CMA / VIP / VPS",
            "CSC CMA hizmeti",
            "CSC için CMA hizmeti girilir.",
            (
                "CSC, 3U koduyla belirtilen China Sichuan Airlines uçuşudur. "
                "Bu havayolu için CMA hizmeti girilir."
            ),
            ikarus_location="İlgili uçuş veya hizmet formu",
            requirement="Duruma Bağlı",
        )
    )

    data["CSC"].append(
        create_rule(
            "default-csc-obh",
            "CSC",
            "OBH",
            "CSC OBH kullanımı",
            "OBH her zaman 1 girilir.",
            service_name="OBH",
            unit="1",
            requirement="Zorunlu",
        )
    )

    # -----------------------------------------------------
    # CES
    # -----------------------------------------------------
    data["CES"].append(
        create_rule(
            "default-ces-counter",
            "CES",
            "Kontuar Hizmeti",
            "CES uçak tipine göre kontuar hakkı",
            "Kontuar sayısı yolcu sayısı ve uçak tipine göre belirlenir.",
            (
                "240 yolcu ve üzeri uçuşlarda 8 kontuar hakkı bulunur. "
                "B777 için 7, A350 için 7, B787 için 7 ve A330 için "
                "6 kontuar hakkı bulunur."
            ),
            ikarus_location="IKARUS Masaüstü / EXTRA FORM",
            service_name="Kontuar",
            unit="Uçak tipine göre 6–8 kontuar",
            requirement="Zorunlu",
        )
    )

    data["CES"].append(
        create_rule(
            "default-ces-ground",
            "CES",
            "GROUND Form",
            "CES kontuar hizmeti",
            "Kontuar kullanımı EXTRA FORM olarak girilir.",
            (
                "CES, China Eastern Airlines havayoludur. Kontuar hizmetleri "
                "IKARUS Web uçuş formundan değil, IKARUS masaüstünde "
                "EXTRA FORM olarak girilir."
            ),
            ikarus_location="IKARUS Masaüstü / EXTRA FORM",
            requirement="Zorunlu",
        )
    )

    data["CES"].append(
        create_rule(
            "default-ces-cma",
            "CES",
            "CMA / VIP / VPS",
            "CES CMA/VIP işlemi",
            "CMA hizmetine form açılmaz; VIP varsa EXTRA FORM açılır.",
            (
                "CES için CMA hizmetine ayrı form açılmaz. VIP hizmeti varsa "
                "EXTRA FORM düzenlenir."
            ),
            ikarus_location="VIP varsa IKARUS Masaüstü / EXTRA FORM",
            note="CES uçuş kodu MU olarak belirtilmiştir.",
            requirement="Duruma Bağlı",
        )
    )

    # -----------------------------------------------------
    # CCA
    # -----------------------------------------------------
    data["CCA"].append(
        create_rule(
            "default-cca-counter",
            "CCA",
            "Kontuar Hizmeti",
            "CCA uçak tipine göre kontuar hakkı",
            "En az 6 kontuar açılır.",
            (
                "B747 ve B777 uçaklarında 1 First, 1 Business ve 6 Economy "
                "kontuarı açılır. A330, A350 ve B787 uçaklarında "
                "2 Business ve 4 Economy kontuarı açılır."
            ),
            ikarus_location="Kontuar kullanımı / ilgili form",
            service_name="Kontuar",
            unit="En az 6 kontuar",
            requirement="Zorunlu",
        )
    )

    data["CCA"].append(
        create_rule(
            "default-cca-cma",
            "CCA",
            "CMA / VIP / VPS",
            "CCA CMA/VIP işlemi",
            "CMA hizmetine form açılmaz; VIP varsa EXTRA FORM açılır.",
            (
                "CCA için CMA hizmetine ayrıca form açılmaz. VIP hizmeti "
                "varsa EXTRA FORM düzenlenir."
            ),
            ikarus_location="VIP varsa IKARUS Masaüstü / EXTRA FORM",
            requirement="Duruma Bağlı",
        )
    )

    data["CCA"].append(
        create_rule(
            "default-cca-china-rep",
            "CCA",
            "Temsilci",
            "CCA temsilci istisnası",
            "China uçuşlarının Gözen temsilci kuralı CCA için geçerli değildir.",
            (
                "China uçuşlarında genel olarak temsilci kodu 13 Gözen olarak "
                "belirtilmiştir; ancak CCA bu kuralın istisnasıdır."
            ),
            requirement="Bilgilendirme",
        )
    )

    # -----------------------------------------------------
    # KAC
    # -----------------------------------------------------
    data["KAC"].append(
        create_rule(
            "default-kac-counter",
            "KAC",
            "Kontuar Hizmeti",
            "KAC uçak tipine göre kontuar hakkı",
            "1 Royal ve 1 Business kontuarı sabittir.",
            (
                "1 Royal ve 1 Business kontuarı sabit açılır. Diğer kontuarlar "
                "uçak tipine göre belirlenir. B777 için 1 Online ve 5 Economy, "
                "A330 için 1 Online ve 3 Economy, A320 için 1 Online ve "
                "2 Economy kontuarı açılır."
            ),
            ikarus_location="IKARUS Masaüstü / GROUND FORM",
            service_name="Kontuar",
            unit="Uçak tipine göre",
            note="KAC için GROUND FORM açılır.",
            requirement="Zorunlu",
        )
    )

    data["KAC"].append(
        create_rule(
            "default-kac-ground",
            "KAC",
            "GROUND Form",
            "KAC GROUND formu",
            "KAC için GROUND FORM açılır.",
            (
                "GROUND listesindeki diğer havayollarından farklı olarak "
                "KAC için GROUND FORM açılır. KAC hariç diğer listelenen "
                "havayollarında TPL hizmeti girilmez."
            ),
            ikarus_location="IKARUS Masaüstü / GROUND FORM",
            requirement="Zorunlu",
        )
    )

    data["KAC"].append(
        create_rule(
            "default-kac-obh",
            "KAC",
            "OBH",
            "KAC OBH kullanımı",
            "OBH her zaman 1 girilir.",
            service_name="OBH",
            unit="1",
            requirement="Zorunlu",
        )
    )

    # -----------------------------------------------------
    # KAL
    # -----------------------------------------------------
    data["KAL"].append(
        create_rule(
            "default-kal-counter",
            "KAL",
            "Kontuar Hizmeti",
            "KAL uçak tipine göre kontuar hakkı",
            "Büyük gövdeli uçaklarda 9 kontuar açılır.",
            (
                "Büyük gövdeli uçaklarda 9 kontuar açılır. Diğer uçak "
                "tiplerinde operasyon durumuna göre 7 veya 8 kontuar açılır."
            ),
            ikarus_location="IKARUS Masaüstü / EXTRA FORM",
            service_name="Kontuar",
            unit="7–9 kontuar",
            requirement="Zorunlu",
        )
    )

    data["KAL"].append(
        create_rule(
            "default-kal-ground",
            "KAL",
            "GROUND Form",
            "KAL kontuar hizmeti",
            "Kontuar hizmeti EXTRA FORM olarak girilir.",
            (
                "Kontuar kullanımları uçuş formunda bulunmaz. IKARUS "
                "masaüstünde EXTRA FORM olarak girilir."
            ),
            ikarus_location="IKARUS Masaüstü / EXTRA FORM",
            requirement="Zorunlu",
        )
    )

    data["KAL"].append(
        create_rule(
            "default-kal-rep",
            "KAL",
            "Temsilci",
            "KAL temsilcisi",
            "KAL/KE temsilcisi Gözen'dir.",
            "Temsilci kodu 13, firma Gözen.",
            service_name="Temsilci",
            unit="13",
            note="KAL uçuş kodu KE olarak belirtilmiştir.",
            requirement="Bilgilendirme",
        )
    )

    data["KAL"].append(
        create_rule(
            "default-kal-obh",
            "KAL",
            "OBH",
            "KAL OBH kullanımı",
            "OBH her zaman 1 girilir.",
            service_name="OBH",
            unit="1",
            requirement="Zorunlu",
        )
    )

    # -----------------------------------------------------
    # UZB
    # -----------------------------------------------------
    data["UZB"].append(
        create_rule(
            "default-uzb-inad",
            "UZB",
            "INAD / NOREC",
            "UZB INAD ve NOREC kuralı",
            "NOREC ve INAD aynı formda olmaz.",
            (
                "UZB için NOREC ve INAD aynı form içerisinde yer almaz. "
                "İkisi birlikte bulunuyorsa NOREC silinir."
            ),
            requirement="Zorunlu",
        )
    )

    data["UZB"].append(
        create_rule(
            "default-uzb-cma",
            "UZB",
            "CMA / VIP / VPS",
            "UZB VIP/CMA hizmeti",
            "VIP/CMA hizmeti uçuş formuna eklenir.",
            (
                "UZB için VIP veya CMA hizmetleri uçuş formuna eklenir. "
                "Not kısmına hizmet detayları yazılır."
            ),
            ikarus_location="Uçuş Formu",
            requirement="Duruma Bağlı",
        )
    )

    # -----------------------------------------------------
    # ETD
    # -----------------------------------------------------
    data["ETD"].append(
        create_rule(
            "default-etd-cma",
            "ETD",
            "CMA / VIP / VPS",
            "ETD VIP/CMA hizmeti",
            "VIP/CMA hizmeti uçuş formuna eklenir.",
            (
                "ETD için VIP veya CMA hizmetleri uçuş formuna eklenir. "
                "Not kısmına hizmet detayları yazılır."
            ),
            ikarus_location="Uçuş Formu",
            requirement="Duruma Bağlı",
        )
    )

    data["ETD"].append(
        create_rule(
            "default-etd-obh",
            "ETD",
            "OBH",
            "ETD OBH kullanımı",
            "OBH her zaman 1 girilir.",
            service_name="OBH",
            unit="1",
            requirement="Zorunlu",
        )
    )

    # -----------------------------------------------------
    # DLH
    # -----------------------------------------------------
    data["DLH"].append(
        create_rule(
            "default-dlh-cma",
            "DLH",
            "CMA / VIP / VPS",
            "DLH CMA/VIP hizmeti",
            "CMA/VIP hizmeti uçuş formuna eklenir.",
            (
                "DLH havayoluna ait CMA veya VIP hizmetleri uçuş formuna "
                "eklenir ve not kısmına hizmet detayları yazılır."
            ),
            ikarus_location="Uçuş Formu",
            requirement="Duruma Bağlı",
        )
    )

    # -----------------------------------------------------
    # KNE
    # -----------------------------------------------------
    data["KNE"].append(
        create_rule(
            "default-kne-cma",
            "KNE",
            "CMA / VIP / VPS",
            "KNE CMA/VIP hizmeti",
            "CMA/VIP hizmeti uçuş formuna eklenir.",
            (
                "KNE havayoluna ait CMA veya VIP hizmetleri uçuş formuna "
                "eklenir ve not kısmına hizmet detayları yazılır."
            ),
            ikarus_location="Uçuş Formu",
            requirement="Duruma Bağlı",
        )
    )

    data["KNE"].append(
        create_rule(
            "default-kne-rep",
            "KNE",
            "Temsilci",
            "KNE temsilcisi",
            "KNE temsilcisi Adriyatik'tir.",
            "Temsilci kodu 15, firma Adriyatik.",
            unit="15",
            requirement="Bilgilendirme",
        )
    )

    # -----------------------------------------------------
    # UAE / EMIRATES
    # -----------------------------------------------------
    data["UAE"].append(
        create_rule(
            "default-uae-inad",
            "UAE",
            "INAD / NOREC",
            "Emirates INAD kuralı",
            "Emirates için INAD girişi yapılmaz.",
            (
                "Emirates havayolu için INAD hizmeti veya INAD formu girilmez."
            ),
            requirement="Zorunlu",
        )
    )

    data["UAE"].append(
        create_rule(
            "default-uae-vip",
            "UAE",
            "CMA / VIP / VPS",
            "Emirates VIP/VPS/CMA",
            "IKARUS masaüstünden EXTRA FORM hazırlanır.",
            (
                "Emirates VIP, VPS ve CMA hizmetleri IKARUS masaüstünden "
                "EXTRA FORM olarak düzenlenir. Çelebi VIP ve Transfer "
                "Departmanından gelen raporlara göre açılır. VIP hizmetinde "
                "1 UNIT VIP ve 1 UNIT VPS girilir. Not kısmına yolcu adı, "
                "uçuş numarası ve eşlik eden kişi bilgisi yazılır."
            ),
            ikarus_location="IKARUS Masaüstü / EXTRA FORM",
            service_name="VIP + VPS",
            unit="1 VIP + 1 VPS",
            requirement="Duruma Bağlı",
        )
    )

    # -----------------------------------------------------
    # DAH
    # -----------------------------------------------------
    data["DAH"].append(
        create_rule(
            "default-dah-invoice",
            "DAH",
            "Fatura",
            "DAH fatura kuralı",
            "DAH faturalarına EXT hizmeti girilmez.",
            (
                "DAH için açılan faturalarda EXT servis adı kullanılmaz."
            ),
            requirement="Zorunlu",
        )
    )

    data["DAH"].append(
        create_rule(
            "default-dah-rainbow",
            "DAH",
            "Gökkuşağı",
            "DAH Gökkuşağı faturası",
            "Servis detayı ayrıca belirtilir.",
            (
                "DAH için Gökkuşağı faturalarında servis adı EXT olarak değil; "
                "HTL, REFRESHMENT veya CRM şeklinde detaylandırılır."
            ),
            ikarus_location="GROUND Form",
            service_name="HTL / REFRESHMENT / CRM",
            requirement="Zorunlu",
        )
    )

    data["DAH"].append(
        create_rule(
            "default-dah-excess",
            "DAH",
            "Ay Sonu Excess",
            "DAH ay sonu excess",
            "Müşteri adı DAHEXC olarak girilir.",
            (
                "Ay sonu excess mailinde belirtilen tutar kullanılarak hizmet "
                "girişi yapılır."
            ),
            service_name="DAHEXC",
            requirement="Duruma Bağlı",
        )
    )

    data["DAH"].append(
        create_rule(
            "default-dah-obh",
            "DAH",
            "OBH",
            "DAH OBH kullanımı",
            "OBH her zaman 1 girilir.",
            service_name="OBH",
            unit="1",
            requirement="Zorunlu",
        )
    )

    # -----------------------------------------------------
    # RAM
    # -----------------------------------------------------
    data["RAM"].append(
        create_rule(
            "default-ram-meal",
            "RAM",
            "Yemek / Otel",
            "RAM yemek faturası",
            "Müşteri adı RAMEXC olarak girilir.",
            service_name="RAMEXC",
            requirement="Duruma Bağlı",
        )
    )

    data["RAM"].append(
        create_rule(
            "default-ram-crew",
            "RAM",
            "CMA / VIP / VPS",
            "RAM ekip eşlik hizmeti",
            "Müşteri adı RAMCRW olarak girilir.",
            service_name="RAMCRW",
            requirement="Duruma Bağlı",
        )
    )

    data["RAM"].append(
        create_rule(
            "default-ram-excess",
            "RAM",
            "Ay Sonu Excess",
            "RAM ay sonu excess",
            "Müşteri adı RAMEXC olarak girilir.",
            (
                "Ay sonu excess mailinde belirtilen tutar kullanılarak hizmet "
                "girişi yapılır."
            ),
            service_name="RAMEXC",
            requirement="Duruma Bağlı",
        )
    )

    data["RAM"].append(
        create_rule(
            "default-ram-code",
            "RAM",
            "Genel Operasyon",
            "Royal Air Maroc üçlü kodu",
            "Royal Air Maroc üçlü kodu RAM'dir.",
            unit="RAM",
            requirement="Bilgilendirme",
        )
    )

    data["RAM"].append(
        create_rule(
            "default-ram-obh",
            "RAM",
            "OBH",
            "RAM OBH kullanımı",
            "OBH her zaman 1 girilir.",
            service_name="OBH",
            unit="1",
            requirement="Zorunlu",
        )
    )

    # -----------------------------------------------------
    # AEE
    # -----------------------------------------------------
    data["AEE"].append(
        create_rule(
            "default-aee-excess",
            "AEE",
            "Ay Sonu Excess",
            "AEE ay sonu excess",
            "Müşteri adı AEEEXC olarak girilir.",
            (
                "Ay sonu excess mailinde belirtilen tutar kullanılarak hizmet "
                "girişi yapılır."
            ),
            service_name="AEEEXC",
            requirement="Duruma Bağlı",
        )
    )

    # -----------------------------------------------------
    # SVA
    # -----------------------------------------------------
    data["SVA"].append(
        create_rule(
            "default-sva-ground",
            "SVA",
            "GROUND Form",
            "SVA kontuar kuralı",
            "SVA için ekstra kontuar yansıtılmaz.",
            (
                "Saudia Arabian Airlines için EXTRA kontuar hizmeti "
                "yansıtılmaz."
            ),
            requirement="Zorunlu",
        )
    )

    data["SVA"].append(
        create_rule(
            "default-sva-excess",
            "SVA",
            "Ay Sonu Excess",
            "SVA ay sonu excess",
            "Müşteri adı SVAEXC olarak girilir.",
            (
                "Ay sonu excess mailinde belirtilen tutar kullanılarak hizmet "
                "girişi yapılır."
            ),
            service_name="SVAEXC",
            requirement="Duruma Bağlı",
        )
    )

    # -----------------------------------------------------
    # FAD
    # -----------------------------------------------------
    data["FAD"].append(
        create_rule(
            "default-fad-excess",
            "FAD",
            "Ay Sonu Excess",
            "FAD ay sonu excess",
            "Müşteri adı FADEXC olarak girilir.",
            (
                "Ay sonu excess mailinde belirtilen tutar kullanılarak hizmet "
                "girişi yapılır."
            ),
            service_name="FADEXC",
            requirement="Duruma Bağlı",
        )
    )

    data["FAD"].append(
        create_rule(
            "default-fad-obh",
            "FAD",
            "OBH",
            "FAD OBH kullanımı",
            "OBH her zaman 1 girilir.",
            service_name="OBH",
            unit="1",
            requirement="Zorunlu",
        )
    )

    # -----------------------------------------------------
    # ABY
    # -----------------------------------------------------
    data["ABY"].append(
        create_rule(
            "default-aby-rep",
            "ABY",
            "Temsilci",
            "ABY temsilci kodu",
            "G9/ABY için temsilci kodu 75 olarak belirtilmiştir.",
            unit="75",
            note="Temsilci firma adı kullanıcı notunda belirtilmemiştir.",
            requirement="Bilgilendirme",
        )
    )

    data["ABY"].append(
        create_rule(
            "default-aby-code",
            "ABY",
            "Genel Operasyon",
            "Air Arabia üçlü kodu",
            "Air Arabia üçlü kodu ABY'dir.",
            unit="ABY",
            requirement="Bilgilendirme",
        )
    )

    data["ABY"].append(
        create_rule(
            "default-aby-obh",
            "ABY",
            "OBH",
            "ABY OBH kullanımı",
            "OBH her zaman 1 girilir.",
            service_name="OBH",
            unit="1",
            requirement="Zorunlu",
        )
    )

    # -----------------------------------------------------
    # UBD
    # -----------------------------------------------------
    data["UBD"].append(
        create_rule(
            "default-ubd-rep",
            "UBD",
            "Temsilci",
            "UBD temsilci kodu",
            "UD/UBD için temsilci kodu 03 olarak belirtilmiştir.",
            unit="03",
            note="Temsilci firma adı kullanıcı notunda belirtilmemiştir.",
            requirement="Bilgilendirme",
        )
    )

    data["UBD"].append(
        create_rule(
            "default-ubd-obh",
            "UBD",
            "OBH",
            "UBD OBH kullanımı",
            "OBH her zaman 1 girilir.",
            service_name="OBH",
            unit="1",
            requirement="Zorunlu",
        )
    )

    # -----------------------------------------------------
    # SHI
    # -----------------------------------------------------
    data["SHI"].append(
        create_rule(
            "default-shi-rep",
            "SHI",
            "Temsilci",
            "SHI temsilcisi",
            "SHI temsilcisi Bilen'dir.",
            "Temsilci kodu 04, firma Bilen.",
            unit="04",
            requirement="Bilgilendirme",
        )
    )

    # -----------------------------------------------------
    # IAW
    # -----------------------------------------------------
    data["IAW"].append(
        create_rule(
            "default-iaw-obh",
            "IAW",
            "OBH",
            "IAW OBH kullanımı",
            "OBH her zaman 1 girilir.",
            service_name="OBH",
            unit="1",
            requirement="Zorunlu",
        )
    )

    # -----------------------------------------------------
    # MGH
    # -----------------------------------------------------
    data["MGH"].append(
        create_rule(
            "default-mgh-obh",
            "MGH",
            "OBH",
            "MGH OBH kullanımı",
            "OBH her zaman 1 girilir.",
            service_name="OBH",
            unit="1",
            requirement="Zorunlu",
        )
    )

    return data


def normalize_rule(row, airline):
    return {
        "id": safe_text(row.get("id")) or new_id(),
        "Havayolu": airline,
        "Kategori": safe_text(row.get("Kategori")),
        "Başlık": safe_text(row.get("Başlık")),
        "Kısa Bilgi": safe_text(row.get("Kısa Bilgi")),
        "Detay": safe_text(row.get("Detay")),
        "IKARUS Yeri": safe_text(row.get("IKARUS Yeri")),
        "Servis Adı": safe_text(row.get("Servis Adı")),
        "Unit / Değer": safe_text(row.get("Unit / Değer")),
        "Not": safe_text(row.get("Not")),
        "Durum": safe_text(row.get("Durum")) or "Bilgilendirme",
        "Son Güncelleme": safe_text(row.get("Son Güncelleme")),
    }


def normalize_data(data):
    normalized = empty_data()

    if not isinstance(data, dict):
        return normalized

    for code in AIRLINES:
        rows = data.get(code, [])

        if isinstance(rows, list):
            normalized[code] = [
                normalize_rule(row, code)
                for row in rows
                if isinstance(row, dict)
            ]

    normalized["__defaults_version__"] = safe_text(
        data.get("__defaults_version__")
    )

    return normalized


def merge_default_rules(existing_data):
    defaults = default_data()
    existing = normalize_data(existing_data)

    if existing.get("__defaults_version__") == DEFAULTS_VERSION:
        return existing

    for code in AIRLINES:
        existing_ids = {
            row.get("id")
            for row in existing.get(code, [])
        }

        for default_rule in defaults.get(code, []):
            if default_rule.get("id") not in existing_ids:
                existing[code].append(default_rule)

    existing["__defaults_version__"] = DEFAULTS_VERSION

    return existing


def load_data():
    if DATA_FILE.exists():
        try:
            loaded = json.loads(
                DATA_FILE.read_text(encoding="utf-8")
            )

            merged = merge_default_rules(loaded)

            DATA_FILE.write_text(
                json.dumps(
                    merged,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            return merged

        except Exception:
            return default_data()

    data = default_data()

    DATA_FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return data


def save_data(data):
    DATA_FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def rules_for_airline(data, airline):
    return [
        row
        for row in data.get(airline, [])
        if row.get("Havayolu") == airline
    ]


def find_rule(data, airline, rule_id):
    for row in rules_for_airline(data, airline):
        if row.get("id") == rule_id:
            return row

    return None


def delete_rule(data, airline, rule_id):
    data[airline] = [
        row
        for row in data.get(airline, [])
        if row.get("id") != rule_id
    ]

    return data


def update_rule(data, airline, rule_id, new_rule):
    updated = []

    for row in data.get(airline, []):
        if row.get("id") == rule_id:
            updated.append(new_rule)
        else:
            updated.append(row)

    data[airline] = updated

    return data


def option_index(options, value):
    if value in options:
        return options.index(value)

    return 0


# =========================================================
# GENEL OPERASYON KURALLARI
# =========================================================

GENERAL_RULES = [
    {
        "Kategori": "INAD / NOREC",
        "Başlık": "INAD yolcu formu",
        "Detay": (
            "Servis adı EXT-CZA olarak girilir. 1 UNIT girilir. Not kısmında "
            "INAD yolcuya ilişkin idari para cezası ve şirket adı belirtilir."
        ),
    },
    {
        "Kategori": "CMA / VIP / VPS",
        "Başlık": "China teknisyen eşlik işlemi",
        "Detay": (
            "China uçuşları için gelen mailde yalnızca TEKNİSYEN EŞLİK hizmeti "
            "varsa uçuş formuna +1 CMA eklenir ve detaylar not kısmına yazılır."
        ),
    },
    {
        "Kategori": "CMA / VIP / VPS",
        "Başlık": "CMA/VIP form ayrımı",
        "Detay": (
            "DLH, UZB, ETD, CCA, KNE ve BRU için CMA/VIP hizmetleri uçuş "
            "formuna eklenir. Bunların dışındaki havayollarında kural ayrıca "
            "kontrol edilerek EXTRA FORM düzenlenir."
        ),
    },
    {
        "Kategori": "Yemek / Otel",
        "Başlık": "MENÜ-3 yemek faturası",
        "Detay": (
            "Muhasebeden gelen yemek faturası MENÜ-3, yani INAD/DELAY MENU ise "
            "Tumiçtur yemek şirketinden VOUCHER teslim alınır."
        ),
    },
    {
        "Kategori": "Fatura",
        "Başlık": "Fatura dönemi",
        "Detay": (
            "EXTRA formlar ilgili fatura dönemine ait olmalıdır. Dönem dışında "
            "açılan fatura değerlendirmeye alınmaz ve ödeme talep edilemez."
        ),
    },
    {
        "Kategori": "Fatura",
        "Başlık": "KDV'siz tutar",
        "Detay": "Faturalarda her zaman KDV'siz tutar yazılır.",
    },
    {
        "Kategori": "Yemek / Otel",
        "Başlık": "Yemek faturası ekleri",
        "Detay": (
            "Servis eklerine fatura, Transfer departmanından gelen Excel detay "
            "tablosu ve Muhasebe departmanından gelen detay eklenir."
        ),
    },
    {
        "Kategori": "Yemek / Otel",
        "Başlık": "Otel faturaları",
        "Detay": (
            "Kullanıcı notunda konaklama vergisinin KDV'siz tutara eklenmesi "
            "gerektiği belirtilmiştir. Vergi oranı veya metindeki belirsiz ifade "
            "işlem öncesinde doğrulanmalıdır."
        ),
    },
    {
        "Kategori": "GROUND Form",
        "Başlık": "Kontuar hizmeti giriş yeri",
        "Detay": (
            "GROUND listesindeki havayollarında kontuar hizmetleri IKARUS Web "
            "uçuş formundan değil, IKARUS masaüstünde EXTRA FORM olarak girilir."
        ),
    },
    {
        "Kategori": "GROUND Form",
        "Başlık": "TPL kuralı",
        "Detay": (
            "GROUND listesindeki havayollarına KAC hariç TPL hizmeti girilmez."
        ),
    },
    {
        "Kategori": "GROUND Form",
        "Başlık": "GROUND havayolu listesi",
        "Detay": "CES, CSN, CSC, KAC, KAL ve SVA.",
    },
    {
        "Kategori": "CMA / VIP / VPS",
        "Başlık": "Emirates VIP mutabakatı",
        "Detay": (
            "Emirates VIP/VPS/CMA raporları haftalık olarak Çelebi Şeflik "
            "Departmanına Excel tablosu ile mutabakat için gönderilir. "
            "Havayolu ile mutabık kalındıktan sonra formlar hazırlanır."
        ),
    },
    {
        "Kategori": "Sizer",
        "Başlık": "Sizer kullanımları",
        "Detay": (
            "Aylık mutabakat mailine göre GROUND FORM açılır. Servis "
            "1 UNIT EXT-SZR olarak girilir. Fatura tarihi ayın son günüdür. "
            "Not kısmına havayolu ve ait olduğu ay yazılır."
        ),
    },
    {
        "Kategori": "ABS",
        "Başlık": "ABS faturaları",
        "Detay": (
            "Servis adı EXT olarak girilir. SCF dosyası Web IKARUS üzerinden "
            "GROUND olarak indirilip masaüstüne eklenir."
        ),
    },
    {
        "Kategori": "Gökkuşağı",
        "Başlık": "Gökkuşağı faturaları",
        "Detay": (
            "GROUND FORM olarak açılır. Genel servis adı EXT'dir. DAH için "
            "servis adı HTL, REFRESHMENT veya CRM olarak detaylandırılır."
        ),
    },
    {
        "Kategori": "Ay Sonu Excess",
        "Başlık": "Ay sonu excess müşteri adları",
        "Detay": (
            "RAMEXC, AEEEXC, SVAEXC, FADEXC ve DAHEXC müşteri adları kullanılır. "
            "Gelen excess mailinde belirtilen tutar üzerinden hizmet girişi yapılır."
        ),
    },
    {
        "Kategori": "OBH",
        "Başlık": "OBH her zaman 1 girilen havayolları",
        "Detay": (
            "CSC, FAD, AZV, ANKA, CSN, DAH, BRQ, IAW, ETD, GMS, KAC, "
            "MGH, IRB, KAL, AAW, IRC, RAM, ABY, TVP, VSV, ASL ve UBD."
        ),
    },
]


REPRESENTATIVES = [
    {
        "Kod": "KAL / KE",
        "Temsilci Kodu": "13",
        "Temsilci": "GÖZEN",
    },
    {
        "Kod": "MAC / 3O",
        "Temsilci Kodu": "75",
        "Temsilci": "SHARK",
    },
    {
        "Kod": "VSV / DV",
        "Temsilci Kodu": "02",
        "Temsilci": "CASIO",
    },
    {
        "Kod": "ABY / G9",
        "Temsilci Kodu": "75",
        "Temsilci": "Firma adı belirtilmedi",
    },
    {
        "Kod": "UBD / UD",
        "Temsilci Kodu": "03",
        "Temsilci": "Firma adı belirtilmedi",
    },
    {
        "Kod": "SHI",
        "Temsilci Kodu": "04",
        "Temsilci": "BİLEN",
    },
    {
        "Kod": "CHINA",
        "Temsilci Kodu": "13",
        "Temsilci": "GÖZEN — CCA hariç",
    },
    {
        "Kod": "KNE",
        "Temsilci Kodu": "15",
        "Temsilci": "ADRİYATİK",
    },
    {
        "Kod": "BELAVIA",
        "Temsilci Kodu": "15",
        "Temsilci": "ADRİYATİK",
    },
]


TRIPLE_CODES = [
    {
        "Havayolu": "Royal Air Maroc",
        "Üçlü Kod": "RAM",
    },
    {
        "Havayolu": "Air Arabia Maroc",
        "Üçlü Kod": "MAC",
    },
    {
        "Havayolu": "Air Arabia",
        "Üçlü Kod": "ABY",
    },
]


# =========================================================
# OTURUM DURUMU
# =========================================================

if "data" not in st.session_state:
    st.session_state["data"] = load_data()


if "view" not in st.session_state:
    st.session_state["view"] = "Havayolu Rehberi"


if "editing_id" not in st.session_state:
    st.session_state["editing_id"] = None


# =========================================================
# SOL MENÜ
# =========================================================

st.sidebar.markdown("# ✈️ SFC")
st.sidebar.caption("SCF–IKARUS Operasyon Rehberi")
st.sidebar.divider()
st.sidebar.markdown("### Menü")


for menu_item in MENU_ITEMS:
    menu_type = (
        "primary"
        if st.session_state["view"] == menu_item
        else "secondary"
    )

    menu_clicked = st.sidebar.button(
        menu_item,
        use_container_width=True,
        type=menu_type,
        key="menu-" + menu_item,
    )

    if menu_clicked:
        st.session_state["view"] = menu_item
        st.rerun()


page = st.session_state["view"]


st.sidebar.divider()


selected_airline = st.sidebar.selectbox(
    "Havayolu sayfası",
    AIRLINES,
)


st.sidebar.caption(
    "Aktif havayolu: " + selected_airline
)


# =========================================================
# ÜST BİLGİ
# =========================================================

current_rules = rules_for_airline(
    st.session_state["data"],
    selected_airline,
)


total_rules = sum(
    len(rules_for_airline(st.session_state["data"], code))
    for code in AIRLINES
)


filled_airlines = sum(
    1
    for code in AIRLINES
    if rules_for_airline(st.session_state["data"], code)
)


st.title(selected_airline + " Operasyon Rehberi")


st.caption(
    "Bu sayfada yalnızca "
    + selected_airline
    + " havayoluna ait bilgiler gösterilir."
)


metric_1, metric_2, metric_3, metric_4 = st.columns(4)

metric_1.metric(
    "Havayolu",
    selected_airline,
)

metric_2.metric(
    "Bilgi Sayısı",
    len(current_rules),
)

metric_3.metric(
    "Toplam Bilgi",
    total_rules,
)

metric_4.metric(
    "Dolu Havayolu",
    filled_airlines,
)

st.divider()


# =========================================================
# HAVAYOLU REHBERİ
# =========================================================

if page == "Havayolu Rehberi":
    st.subheader("Havayolu Bilgi Kartları")

    filter_1, filter_2, filter_3 = st.columns(3)

    with filter_1:
        search_text = st.text_input(
            "Bilgi ara",
            placeholder="Kontuar, CMA, OBH, fatura...",
            key="airline-search-" + selected_airline,
        )

    with filter_2:
        category_filter = st.selectbox(
            "Kategori",
            ["Tümü"] + CATEGORIES,
            key="airline-category-" + selected_airline,
        )

    with filter_3:
        status_filter = st.selectbox(
            "Kural durumu",
            ["Tümü"] + REQUIRED_OPTIONS,
            key="airline-status-" + selected_airline,
        )

    filtered_rules = []

    for rule in current_rules:
        combined_text = " ".join(
            safe_text(value).lower()
            for value in rule.values()
        )

        if search_text and search_text.lower() not in combined_text:
            continue

        if (
            category_filter != "Tümü"
            and rule.get("Kategori") != category_filter
        ):
            continue

        if (
            status_filter != "Tümü"
            and rule.get("Durum") != status_filter
        ):
            continue

        filtered_rules.append(rule)

    if not filtered_rules:
        st.warning(
            selected_airline
            + " için seçilen kriterlere uygun bilgi bulunamadı."
        )

    card_columns = st.columns(3)

    for index, rule in enumerate(filtered_rules):
        current_column = card_columns[index % 3]

        with current_column:
            with st.container(border=True):
                st.markdown(
                    "#### "
                    + (
                        rule.get("Başlık")
                        or "Başlıksız Bilgi"
                    )
                )

                st.caption(
                    (
                        rule.get("Kategori")
                        or "-"
                    )
                    + " • "
                    + (
                        rule.get("Durum")
                        or "-"
                    )
                )

                st.write(
                    rule.get("Kısa Bilgi")
                    or "-"
                )

                if rule.get("Servis Adı"):
                    st.markdown(
                        "**Servis:** "
                        + rule.get("Servis Adı")
                    )

                if rule.get("Unit / Değer"):
                    st.markdown(
                        "**Değer:** "
                        + rule.get("Unit / Değer")
                    )

                if rule.get("IKARUS Yeri"):
                    st.markdown(
                        "**IKARUS:** "
                        + rule.get("IKARUS Yeri")
                    )

                with st.expander("Detayları göster"):
                    st.write(
                        rule.get("Detay")
                        or "-"
                    )

                    if rule.get("Not"):
                        st.markdown("**Not**")
                        st.write(rule.get("Not"))

                    st.caption(
                        "Son güncelleme: "
                        + (
                            rule.get("Son Güncelleme")
                            or "-"
                        )
                    )

                edit_column, delete_column = st.columns(2)

                with edit_column:
                    if st.button(
                        "Düzenle",
                        key="edit-" + rule["id"],
                        use_container_width=True,
                    ):
                        st.session_state["editing_id"] = rule["id"]
                        st.session_state["view"] = "Bilgi Düzenle / Sil"
                        st.rerun()

                with delete_column:
                    if st.button(
                        "Sil",
                        key="delete-" + rule["id"],
                        use_container_width=True,
                    ):
                        st.session_state["data"] = delete_rule(
                            st.session_state["data"],
                            selected_airline,
                            rule["id"],
                        )

                        save_data(st.session_state["data"])
                        st.rerun()


# =========================================================
# YENİ BİLGİ EKLE
# =========================================================

if page == "Yeni Bilgi Ekle":
    st.subheader(
        selected_airline
        + " İçin Yeni Bilgi Ekle"
    )

    with st.form(
        "add-rule-form",
        clear_on_submit=True,
    ):
        column_1, column_2 = st.columns(2)

        with column_1:
            new_category = st.selectbox(
                "Kategori",
                CATEGORIES,
            )

            new_title = st.text_input(
                "Başlık",
                placeholder="Örnek: B777 kontuar hakkı",
            )

            new_summary = st.text_area(
                "Kısa bilgi",
                placeholder="Kart üzerinde görünecek kısa açıklama",
                height=90,
            )

            new_status = st.selectbox(
                "Kural durumu",
                REQUIRED_OPTIONS,
            )

        with column_2:
            new_ikarus = st.text_input(
                "IKARUS yeri",
                placeholder="Uçuş Formu / EXTRA FORM / GROUND FORM",
            )

            new_service = st.text_input(
                "Servis adı",
                placeholder="EXT-CZA, OBH, RAMEXC...",
            )

            new_unit = st.text_input(
                "Unit / değer",
                placeholder="1 UNIT, 120 dakika, 7 kontuar...",
            )

            new_note = st.text_area(
                "Not",
                height=90,
            )

        new_details = st.text_area(
            "Detaylı açıklama",
            height=170,
        )

        save_new = st.form_submit_button(
            "Bilgiyi Kaydet",
            type="primary",
        )

        if save_new:
            if not new_title.strip():
                st.error("Başlık boş bırakılamaz.")

            else:
                added_rule = create_rule(
                    new_id("custom"),
                    selected_airline,
                    new_category,
                    new_title,
                    new_summary,
                    new_details,
                    new_ikarus,
                    new_service,
                    new_unit,
                    new_note,
                    new_status,
                )

                st.session_state["data"][selected_airline].append(
                    added_rule
                )

                save_data(st.session_state["data"])

                st.session_state["view"] = "Havayolu Rehberi"
                st.rerun()


# =========================================================
# BİLGİ DÜZENLE / SİL
# =========================================================

if page == "Bilgi Düzenle / Sil":
    st.subheader(
        selected_airline
        + " Bilgilerini Düzenle"
    )

    current_rules = rules_for_airline(
        st.session_state["data"],
        selected_airline,
    )

    if not current_rules:
        st.warning(
            selected_airline
            + " için düzenlenecek bilgi bulunmuyor."
        )

    else:
        rule_ids = [
            rule["id"]
            for rule in current_rules
        ]

        selected_index = 0

        if st.session_state["editing_id"] in rule_ids:
            selected_index = rule_ids.index(
                st.session_state["editing_id"]
            )

        selected_rule_id = st.selectbox(
            "Düzenlenecek bilgiyi seç",
            rule_ids,
            index=selected_index,
            format_func=lambda rule_id: (
                find_rule(
                    st.session_state["data"],
                    selected_airline,
                    rule_id,
                ).get("Başlık", "Başlıksız")
            ),
        )

        selected_rule = find_rule(
            st.session_state["data"],
            selected_airline,
            selected_rule_id,
        )

        st.session_state["editing_id"] = selected_rule_id

        with st.form("edit-rule-form"):
            column_1, column_2 = st.columns(2)

            with column_1:
                edit_category = st.selectbox(
                    "Kategori",
                    CATEGORIES,
                    index=option_index(
                        CATEGORIES,
                        selected_rule.get("Kategori"),
                    ),
                )

                edit_title = st.text_input(
                    "Başlık",
                    value=selected_rule.get("Başlık", ""),
                )

                edit_summary = st.text_area(
                    "Kısa bilgi",
                    value=selected_rule.get("Kısa Bilgi", ""),
                    height=90,
                )

                edit_status = st.selectbox(
                    "Kural durumu",
                    REQUIRED_OPTIONS,
                    index=option_index(
                        REQUIRED_OPTIONS,
                        selected_rule.get("Durum"),
                    ),
                )

            with column_2:
                edit_ikarus = st.text_input(
                    "IKARUS yeri",
                    value=selected_rule.get("IKARUS Yeri", ""),
                )

                edit_service = st.text_input(
                    "Servis adı",
                    value=selected_rule.get("Servis Adı", ""),
                )

                edit_unit = st.text_input(
                    "Unit / değer",
                    value=selected_rule.get("Unit / Değer", ""),
                )

                edit_note = st.text_area(
                    "Not",
                    value=selected_rule.get("Not", ""),
                    height=90,
                )

            edit_details = st.text_area(
                "Detaylı açıklama",
                value=selected_rule.get("Detay", ""),
                height=170,
            )

            save_edit = st.form_submit_button(
                "Değişiklikleri Kaydet",
                type="primary",
            )

            if save_edit:
                if not edit_title.strip():
                    st.error("Başlık boş bırakılamaz.")

                else:
                    edited_rule = create_rule(
                        selected_rule_id,
                        selected_airline,
                        edit_category,
                        edit_title,
                        edit_summary,
                        edit_details,
                        edit_ikarus,
                        edit_service,
                        edit_unit,
                        edit_note,
                        edit_status,
                    )

                    st.session_state["data"] = update_rule(
                        st.session_state["data"],
                        selected_airline,
                        selected_rule_id,
                        edited_rule,
                    )

                    save_data(st.session_state["data"])

                    st.session_state["view"] = "Havayolu Rehberi"
                    st.rerun()

        st.divider()

        if st.button(
            "Seçili Bilgiyi Sil",
            use_container_width=True,
        ):
            st.session_state["data"] = delete_rule(
                st.session_state["data"],
                selected_airline,
                selected_rule_id,
            )

            save_data(st.session_state["data"])

            st.session_state["editing_id"] = None
            st.session_state["view"] = "Havayolu Rehberi"
            st.rerun()


# =========================================================
# GENEL OPERASYON KURALLARI
# =========================================================

if page == "Genel Operasyon Kuralları":
    st.subheader("Genel Operasyon Kuralları")

    general_search = st.text_input(
        "Genel kurallarda ara",
        placeholder="INAD, CMA, fatura, Sizer...",
    )

    general_category = st.selectbox(
        "Kategori filtresi",
        ["Tümü"] + CATEGORIES,
        key="general-category",
    )

    visible_general_rules = []

    for rule in GENERAL_RULES:
        combined = (
            rule["Kategori"]
            + " "
            + rule["Başlık"]
            + " "
            + rule["Detay"]
        ).lower()

        if general_search and general_search.lower() not in combined:
            continue

        if (
            general_category != "Tümü"
            and rule["Kategori"] != general_category
        ):
            continue

        visible_general_rules.append(rule)

    general_columns = st.columns(3)

    for index, rule in enumerate(visible_general_rules):
        with general_columns[index % 3]:
            with st.container(border=True):
                st.markdown("#### " + rule["Başlık"])
                st.caption(rule["Kategori"])
                st.write(rule["Detay"])


# =========================================================
# TEMSİLCİLER VE KODLAR
# =========================================================

if page == "Temsilciler ve Kodlar":
    st.subheader("Temsilciler")

    representative_columns = st.columns(3)

    for index, representative in enumerate(REPRESENTATIVES):
        with representative_columns[index % 3]:
            with st.container(border=True):
                st.markdown(
                    "#### " + representative["Kod"]
                )

                st.markdown(
                    "**Temsilci kodu:** "
                    + representative["Temsilci Kodu"]
                )

                st.markdown(
                    "**Firma:** "
                    + representative["Temsilci"]
                )

    st.divider()
    st.subheader("Üçlü Kodlar")

    code_columns = st.columns(3)

    for index, code_info in enumerate(TRIPLE_CODES):
        with code_columns[index % 3]:
            with st.container(border=True):
                st.markdown(
                    "#### " + code_info["Üçlü Kod"]
                )
                st.write(code_info["Havayolu"])


# =========================================================
# TÜM BİLGİLERDE ARA
# =========================================================

if page == "Tüm Bilgilerde Ara":
    st.subheader("Tüm Havayollarında Ara")

    global_search = st.text_input(
        "Arama",
        placeholder="Kontuar, OBH, RAMEXC, CMA...",
    )

    global_airline = st.selectbox(
        "Havayolu filtresi",
        ["Tümü"] + AIRLINES,
    )

    global_category = st.selectbox(
        "Kategori filtresi",
        ["Tümü"] + CATEGORIES,
        key="global-category",
    )

    all_rules = []

    for airline_code in AIRLINES:
        all_rules.extend(
            rules_for_airline(
                st.session_state["data"],
                airline_code,
            )
        )

    visible_rules = []

    for rule in all_rules:
        combined = " ".join(
            safe_text(value).lower()
            for value in rule.values()
        )

        if global_search and global_search.lower() not in combined:
            continue

        if (
            global_airline != "Tümü"
            and rule.get("Havayolu") != global_airline
        ):
            continue

        if (
            global_category != "Tümü"
            and rule.get("Kategori") != global_category
        ):
            continue

        visible_rules.append(rule)

    global_columns = st.columns(3)

    for index, rule in enumerate(visible_rules):
        with global_columns[index % 3]:
            with st.container(border=True):
                st.markdown(
                    "#### "
                    + rule.get("Başlık", "Başlıksız")
                )

                st.caption(
                    rule.get("Havayolu", "-")
                    + " • "
                    + rule.get("Kategori", "-")
                )

                st.write(
                    rule.get("Kısa Bilgi")
                    or "-"
                )

                with st.expander("Detay"):
                    st.write(
                        rule.get("Detay")
                        or "-"
                    )


# =========================================================
# VERİ YÖNETİMİ
# =========================================================

if page == "Veri Yönetimi":
    st.subheader("Veri Yönetimi")

    st.warning(
        "Veriler services.json dosyasına kaydedilir. Streamlit Cloud "
        "yeniden kurulursa yerel dosya kaybolabilir. Düzenli olarak "
        "JSON yedeği indirmen önerilir."
    )

    json_data = json.dumps(
        st.session_state["data"],
        ensure_ascii=False,
        indent=2,
    )

    st.download_button(
        "JSON Yedeğini İndir",
        data=json_data.encode("utf-8"),
        file_name="sfc_services_backup.json",
        mime="application/json",
    )

    uploaded_json = st.file_uploader(
        "JSON yedeği yükle",
        type=["json"],
    )

    if uploaded_json is not None:
        try:
            uploaded_data = json.loads(
                uploaded_json.read().decode("utf-8")
            )

            st.session_state["data"] = normalize_data(
                uploaded_data
            )

            st.session_state["data"][
                "__defaults_version__"
            ] = DEFAULTS_VERSION

            save_data(st.session_state["data"])

            st.success("Yedek başarıyla yüklendi.")
            st.rerun()

        except Exception as error:
            st.error(
                "Yedek okunamadı: "
                + str(error)
            )

    st.divider()

    if st.button(
        "Hazır Kuralları Yeniden Yükle",
        use_container_width=True,
    ):
        st.session_state["data"] = default_data()
        save_data(st.session_state["data"])
        st.rerun()


st.divider()

st.caption(
    "SFC • SCF–IKARUS Dijital Operasyon Rehberi • "
    + selected_airline
)
