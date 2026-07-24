# SFC AIRLINE RULES FIXED BUILD 2026-07-24

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
    "SELÇUK",
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
DEFAULTS_VERSION = "2026-07-24-v3"


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

    div[data-testid="stExpander"] {
        background: #f8fafc !important;
        border: 1px solid #e1e8ef !important;
        border-radius: 10px !important;
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


def safe_text(value):
    if value is None:
        return ""

    return str(value)


def empty_data():
    data = {
        code: []
        for code in AIRLINES
    }

    data["__defaults_version__"] = ""

    return data


def create_rule(
    rule_id,
    airline,
    category,
    title,
    summary,
    details="",
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
        "Son Güncelleme": datetime.now().strftime(
            "%d.%m.%Y %H:%M"
        ),
    }


def default_rows():
    return [
        {
            "airline": "CSN",
            "category": "Kontuar Hizmeti",
            "title": "CSN kontuar hakkı",
            "summary": "Her 40 yolcu için 1 Economy ve 2 Business kontuarı.",
            "details": "Kontuar kullanım süresi 120 dakikadır.",
            "ikarus": "Kontuar / ilgili form",
            "service": "Kontuar",
            "unit": "120 dakika",
            "note": "CSN, China Southern Airlines kodudur.",
            "requirement": "Zorunlu",
        },
        {
            "airline": "CSN",
            "category": "GROUND Form",
            "title": "CSN kontuar hizmeti",
            "summary": "Kontuar hizmeti uçuş formunda bulunmaz.",
            "details": "IKARUS masaüstünde EXTRA FORM olarak girilir.",
            "ikarus": "IKARUS Masaüstü / EXTRA FORM",
            "service": "Kontuar",
            "requirement": "Zorunlu",
        },
        {
            "airline": "CSN",
            "category": "CMA / VIP / VPS",
            "title": "CSN CMA işlemi",
            "summary": "CMA hizmetine ayrı form açılmaz.",
            "details": "OPS girer. VIP varsa EXTRA FORM düzenlenir.",
            "ikarus": "VIP varsa EXTRA FORM",
            "note": "CZ kodu ile de belirtilir.",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "CSN",
            "category": "OBH",
            "title": "CSN OBH",
            "summary": "OBH her zaman 1 girilir.",
            "service": "OBH",
            "unit": "1",
            "requirement": "Zorunlu",
        },
        {
            "airline": "BRU",
            "category": "Kontuar Hizmeti",
            "title": "BRU kontuar hakkı",
            "summary": "Her 50 yolcu için 1 Economy ve Business kontuarı.",
            "details": "Kontuar kullanım süresi 120 dakikadır.",
            "ikarus": "Kontuar / ilgili form",
            "service": "Kontuar",
            "unit": "120 dakika",
            "note": "Business kontuar adedi ayrıca doğrulanmalıdır.",
            "requirement": "Zorunlu",
        },
        {
            "airline": "BRU",
            "category": "CMA / VIP / VPS",
            "title": "BRU CMA/VIP",
            "summary": "CMA/VIP hizmeti uçuş formuna eklenir.",
            "details": "Not kısmına hizmet detayları yazılır.",
            "ikarus": "Uçuş Formu",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "CSC",
            "category": "Kontuar Hizmeti",
            "title": "CSC kontuar hakkı",
            "summary": "Her 60 yolcu için 1 Economy ve 1 Business kontuarı.",
            "details": "Kontuar kullanım süresi 120 dakikadır.",
            "ikarus": "Kontuar / ilgili form",
            "service": "Kontuar",
            "unit": "120 dakika",
            "requirement": "Zorunlu",
        },
        {
            "airline": "CSC",
            "category": "GROUND Form",
            "title": "CSC kontuar hizmeti",
            "summary": "Kontuar hizmeti EXTRA FORM olarak girilir.",
            "details": "IKARUS masaüstü kullanılır.",
            "ikarus": "IKARUS Masaüstü / EXTRA FORM",
            "service": "Kontuar",
            "requirement": "Zorunlu",
        },
        {
            "airline": "CSC",
            "category": "CMA / VIP / VPS",
            "title": "CSC CMA",
            "summary": "CSC için CMA hizmeti girilir.",
            "details": "CSC, 3U kodu ile belirtilir.",
            "ikarus": "İlgili uçuş veya hizmet formu",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "CSC",
            "category": "OBH",
            "title": "CSC OBH",
            "summary": "OBH her zaman 1 girilir.",
            "service": "OBH",
            "unit": "1",
            "requirement": "Zorunlu",
        },
        {
            "airline": "CES",
            "category": "Kontuar Hizmeti",
            "title": "CES kontuar hakkı",
            "summary": "240 yolcu ve üzeri uçuşlarda 8 kontuar hakkı vardır.",
            "details": (
                "B777 için 7, A350 için 7, B787 için 7 ve "
                "A330 için 6 kontuar açılır."
            ),
            "ikarus": "IKARUS Masaüstü / EXTRA FORM",
            "service": "Kontuar",
            "unit": "6-8 kontuar",
            "requirement": "Zorunlu",
        },
        {
            "airline": "CES",
            "category": "GROUND Form",
            "title": "CES kontuar hizmeti",
            "summary": "Kontuar hizmeti EXTRA FORM olarak girilir.",
            "details": "CES, China Eastern Airlines havayoludur.",
            "ikarus": "IKARUS Masaüstü / EXTRA FORM",
            "service": "Kontuar",
            "requirement": "Zorunlu",
        },
        {
            "airline": "CES",
            "category": "CMA / VIP / VPS",
            "title": "CES CMA/VIP",
            "summary": "CMA için ayrı form açılmaz.",
            "details": "VIP varsa EXTRA FORM açılır.",
            "ikarus": "VIP varsa EXTRA FORM",
            "note": "MU kodu ile de belirtilir.",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "CCA",
            "category": "Kontuar Hizmeti",
            "title": "CCA kontuar hakkı",
            "summary": "En az 6 kontuar açılır.",
            "details": (
                "B747 ve B777 için 1 First, 1 Business ve 6 Economy; "
                "A330, A350 ve B787 için 2 Business ve 4 Economy açılır."
            ),
            "ikarus": "Kontuar / ilgili form",
            "service": "Kontuar",
            "unit": "En az 6",
            "requirement": "Zorunlu",
        },
        {
            "airline": "CCA",
            "category": "CMA / VIP / VPS",
            "title": "CCA CMA/VIP",
            "summary": "CMA için ayrı form açılmaz.",
            "details": "VIP varsa EXTRA FORM açılır.",
            "ikarus": "VIP varsa EXTRA FORM",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "CCA",
            "category": "Temsilci",
            "title": "CCA temsilci istisnası",
            "summary": "China uçuşlarının Gözen temsilci kuralına istisnadır.",
            "details": "CCA temsilcisi ayrıca kontrol edilmelidir.",
            "requirement": "Bilgilendirme",
        },
        {
            "airline": "KAC",
            "category": "Kontuar Hizmeti",
            "title": "KAC kontuar hakkı",
            "summary": "1 Royal ve 1 Business kontuarı sabittir.",
            "details": (
                "B777 için 1 Online + 5 Economy; A330 için "
                "1 Online + 3 Economy; A320 için 1 Online + "
                "2 Economy kontuarı açılır."
            ),
            "ikarus": "IKARUS Masaüstü / GROUND FORM",
            "service": "Kontuar",
            "unit": "Uçak tipine göre",
            "note": "KAC için GROUND FORM açılır.",
            "requirement": "Zorunlu",
        },
        {
            "airline": "KAC",
            "category": "GROUND Form",
            "title": "KAC GROUND formu",
            "summary": "KAC için GROUND FORM açılır.",
            "details": (
                "GROUND listesindeki diğer havayollarından farklı olarak "
                "KAC için GROUND FORM açılır."
            ),
            "ikarus": "IKARUS Masaüstü / GROUND FORM",
            "requirement": "Zorunlu",
        },
        {
            "airline": "KAC",
            "category": "OBH",
            "title": "KAC OBH",
            "summary": "OBH her zaman 1 girilir.",
            "service": "OBH",
            "unit": "1",
            "requirement": "Zorunlu",
        },
        {
            "airline": "KAL",
            "category": "Kontuar Hizmeti",
            "title": "KAL kontuar hakkı",
            "summary": "Büyük gövdeli uçaklarda 9 kontuar açılır.",
            "details": "Diğer uçak tiplerinde 7 veya 8 kontuar açılır.",
            "ikarus": "IKARUS Masaüstü / EXTRA FORM",
            "service": "Kontuar",
            "unit": "7-9 kontuar",
            "requirement": "Zorunlu",
        },
        {
            "airline": "KAL",
            "category": "GROUND Form",
            "title": "KAL kontuar hizmeti",
            "summary": "Kontuar hizmeti EXTRA FORM olarak girilir.",
            "ikarus": "IKARUS Masaüstü / EXTRA FORM",
            "service": "Kontuar",
            "requirement": "Zorunlu",
        },
        {
            "airline": "KAL",
            "category": "Temsilci",
            "title": "KAL temsilcisi",
            "summary": "Temsilci kodu 13, firma Gözen.",
            "service": "Temsilci",
            "unit": "13",
            "note": "KE kodu ile de belirtilir.",
            "requirement": "Bilgilendirme",
        },
        {
            "airline": "KAL",
            "category": "OBH",
            "title": "KAL OBH",
            "summary": "OBH her zaman 1 girilir.",
            "service": "OBH",
            "unit": "1",
            "requirement": "Zorunlu",
        },
        {
            "airline": "UZB",
            "category": "INAD / NOREC",
            "title": "UZB INAD/NOREC",
            "summary": "NOREC ve INAD aynı formda olmaz.",
            "details": "İkisi birlikte bulunuyorsa NOREC silinir.",
            "requirement": "Zorunlu",
        },
        {
            "airline": "UZB",
            "category": "CMA / VIP / VPS",
            "title": "UZB VIP/CMA",
            "summary": "VIP/CMA hizmeti uçuş formuna eklenir.",
            "details": "Not kısmına hizmet detayları yazılır.",
            "ikarus": "Uçuş Formu",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "ETD",
            "category": "CMA / VIP / VPS",
            "title": "ETD VIP/CMA",
            "summary": "VIP/CMA hizmeti uçuş formuna eklenir.",
            "details": "Not kısmına hizmet detayları yazılır.",
            "ikarus": "Uçuş Formu",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "ETD",
            "category": "OBH",
            "title": "ETD OBH",
            "summary": "OBH her zaman 1 girilir.",
            "service": "OBH",
            "unit": "1",
            "requirement": "Zorunlu",
        },
        {
            "airline": "DLH",
            "category": "CMA / VIP / VPS",
            "title": "DLH CMA/VIP",
            "summary": "CMA/VIP hizmeti uçuş formuna eklenir.",
            "details": "Not kısmına hizmet detayları yazılır.",
            "ikarus": "Uçuş Formu",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "KNE",
            "category": "CMA / VIP / VPS",
            "title": "KNE CMA/VIP",
            "summary": "CMA/VIP hizmeti uçuş formuna eklenir.",
            "details": "Not kısmına hizmet detayları yazılır.",
            "ikarus": "Uçuş Formu",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "KNE",
            "category": "Temsilci",
            "title": "KNE temsilcisi",
            "summary": "Temsilci kodu 15, firma Adriyatik.",
            "unit": "15",
            "requirement": "Bilgilendirme",
        },
        {
            "airline": "UAE",
            "category": "INAD / NOREC",
            "title": "Emirates INAD",
            "summary": "Emirates için INAD girilmez.",
            "requirement": "Zorunlu",
        },
        {
            "airline": "UAE",
            "category": "CMA / VIP / VPS",
            "title": "Emirates VIP/VPS/CMA",
            "summary": "IKARUS masaüstünden EXTRA FORM düzenlenir.",
            "details": (
                "1 UNIT VIP ve 1 UNIT VPS girilir. Not kısmına "
                "yolcu adı, uçuş numarası ve eşlik eden kişi yazılır."
            ),
            "ikarus": "IKARUS Masaüstü / EXTRA FORM",
            "service": "VIP + VPS",
            "unit": "1 VIP + 1 VPS",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "DAH",
            "category": "Fatura",
            "title": "DAH fatura kuralı",
            "summary": "DAH faturalarına EXT hizmeti girilmez.",
            "requirement": "Zorunlu",
        },
        {
            "airline": "DAH",
            "category": "Gökkuşağı",
            "title": "DAH Gökkuşağı faturası",
            "summary": "Servis adı HTL, REFRESHMENT veya CRM olur.",
            "details": "EXT kullanılmaz.",
            "ikarus": "GROUND Form",
            "service": "HTL / REFRESHMENT / CRM",
            "requirement": "Zorunlu",
        },
        {
            "airline": "DAH",
            "category": "Ay Sonu Excess",
            "title": "DAH ay sonu excess",
            "summary": "Müşteri adı DAHEXC olarak girilir.",
            "details": "Excess mailinde belirtilen tutar kullanılır.",
            "service": "DAHEXC",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "DAH",
            "category": "OBH",
            "title": "DAH OBH",
            "summary": "OBH her zaman 1 girilir.",
            "service": "OBH",
            "unit": "1",
            "requirement": "Zorunlu",
        },
        {
            "airline": "RAM",
            "category": "Yemek / Otel",
            "title": "RAM yemek faturası",
            "summary": "Müşteri adı RAMEXC olarak girilir.",
            "service": "RAMEXC",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "RAM",
            "category": "CMA / VIP / VPS",
            "title": "RAM ekip eşlik",
            "summary": "Müşteri adı RAMCRW olarak girilir.",
            "service": "RAMCRW",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "RAM",
            "category": "Ay Sonu Excess",
            "title": "RAM ay sonu excess",
            "summary": "Müşteri adı RAMEXC olarak girilir.",
            "details": "Excess mailinde belirtilen tutar kullanılır.",
            "service": "RAMEXC",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "RAM",
            "category": "Genel Operasyon",
            "title": "Royal Air Maroc kodu",
            "summary": "Üçlü kod RAM'dir.",
            "unit": "RAM",
            "requirement": "Bilgilendirme",
        },
        {
            "airline": "RAM",
            "category": "OBH",
            "title": "RAM OBH",
            "summary": "OBH her zaman 1 girilir.",
            "service": "OBH",
            "unit": "1",
            "requirement": "Zorunlu",
        },
        {
            "airline": "AEE",
            "category": "Ay Sonu Excess",
            "title": "AEE ay sonu excess",
            "summary": "Müşteri adı AEEEXC olarak girilir.",
            "details": "Excess mailinde belirtilen tutar kullanılır.",
            "service": "AEEEXC",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "SVA",
            "category": "GROUND Form",
            "title": "SVA kontuar kuralı",
            "summary": "SVA için ekstra kontuar yansıtılmaz.",
            "requirement": "Zorunlu",
        },
        {
            "airline": "SVA",
            "category": "Ay Sonu Excess",
            "title": "SVA ay sonu excess",
            "summary": "Müşteri adı SVAEXC olarak girilir.",
            "details": "Excess mailinde belirtilen tutar kullanılır.",
            "service": "SVAEXC",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "FAD",
            "category": "Ay Sonu Excess",
            "title": "FAD ay sonu excess",
            "summary": "Müşteri adı FADEXC olarak girilir.",
            "details": "Excess mailinde belirtilen tutar kullanılır.",
            "service": "FADEXC",
            "requirement": "Duruma Bağlı",
        },
        {
            "airline": "FAD",
            "category": "OBH",
            "title": "FAD OBH",
            "summary": "OBH her zaman 1 girilir.",
            "service": "OBH",
            "unit": "1",
            "requirement": "Zorunlu",
        },
        {
            "airline": "ABY",
            "category": "Temsilci",
            "title": "ABY temsilci kodu",
            "summary": "G9/ABY temsilci kodu 75'tir.",
            "details": "Temsilci firma adı belirtilmemiştir.",
            "service": "Temsilci",
            "unit": "75",
            "requirement": "Bilgilendirme",
        },
        {
            "airline": "ABY",
            "category": "Genel Operasyon",
            "title": "Air Arabia kodu",
            "summary": "Üçlü kod ABY'dir.",
            "unit": "ABY",
            "requirement": "Bilgilendirme",
        },
        {
            "airline": "ABY",
            "category": "OBH",
            "title": "ABY OBH",
            "summary": "OBH her zaman 1 girilir.",
            "service": "OBH",
            "unit": "1",
            "requirement": "Zorunlu",
        },
        {
            "airline": "UBD",
            "category": "Temsilci",
            "title": "UBD temsilci kodu",
            "summary": "UD/UBD temsilci kodu 03'tür.",
            "details": "Temsilci firma adı belirtilmemiştir.",
            "service": "Temsilci",
            "unit": "03",
            "requirement": "Bilgilendirme",
        },
        {
            "airline": "UBD",
            "category": "OBH",
            "title": "UBD OBH",
            "summary": "OBH her zaman 1 girilir.",
            "service": "OBH",
            "unit": "1",
            "requirement": "Zorunlu",
        },
        {
            "airline": "SHI",
            "category": "Temsilci",
            "title": "SHI temsilcisi",
            "summary": "Temsilci kodu 04, firma Bilen.",
            "service": "Temsilci",
            "unit": "04",
            "requirement": "Bilgilendirme",
        },
        {
            "airline": "IAW",
            "category": "OBH",
            "title": "IAW OBH",
            "summary": "OBH her zaman 1 girilir.",
            "service": "OBH",
            "unit": "1",
            "requirement": "Zorunlu",
        },
        {
            "airline": "MGH",
            "category": "OBH",
            "title": "MGH OBH",
            "summary": "OBH her zaman 1 girilir.",
            "service": "OBH",
            "unit": "1",
            "requirement": "Zorunlu",
        },
    ]


def default_data():
    data = empty_data()

    for index, row in enumerate(
        default_rows(),
        start=1,
    ):
        airline = row.get("airline", "")

        if airline not in AIRLINES:
            continue

        data[airline].append(
            create_rule(
                rule_id="default-" + str(index),
                airline=airline,
                category=row.get("category", "Diğer"),
                title=row.get("title", "Başlıksız"),
                summary=row.get("summary", ""),
                details=row.get("details", ""),
                ikarus_location=row.get("ikarus", ""),
                service_name=row.get("service", ""),
                unit=row.get("unit", ""),
                note=row.get("note", ""),
                requirement=row.get(
                    "requirement",
                    "Bilgilendirme",
                ),
            )
        )

    data["__defaults_version__"] = DEFAULTS_VERSION

    return data


def normalize_rule(row, airline):
    return create_rule(
        rule_id=safe_text(
            row.get("id")
        ) or "custom-" + str(uuid.uuid4()),
        airline=airline,
        category=safe_text(
            row.get("Kategori")
        ) or "Diğer",
        title=safe_text(
            row.get("Başlık")
        ) or "Başlıksız",
        summary=safe_text(
            row.get("Kısa Bilgi")
        ),
        details=safe_text(
            row.get("Detay")
        ),
        ikarus_location=safe_text(
            row.get("IKARUS Yeri")
        ),
        service_name=safe_text(
            row.get("Servis Adı")
        ),
        unit=safe_text(
            row.get("Unit / Değer")
        ),
        note=safe_text(
            row.get("Not")
        ),
        requirement=safe_text(
            row.get("Durum")
        ) or "Bilgilendirme",
    )


def normalize_data(data):
    normalized = empty_data()

    if not isinstance(data, dict):
        return normalized

    for code in AIRLINES:
        rows = data.get(code, [])

        if not isinstance(rows, list):
            continue

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
    existing = normalize_data(existing_data)
    defaults = default_data()

    if (
        existing.get("__defaults_version__")
        == DEFAULTS_VERSION
    ):
        return existing

    for code in AIRLINES:
        existing_keys = {
            (
                row.get("Kategori"),
                row.get("Başlık"),
            )
            for row in existing.get(code, [])
        }

        for rule in defaults.get(code, []):
            rule_key = (
                rule.get("Kategori"),
                rule.get("Başlık"),
            )

            if rule_key not in existing_keys:
                existing[code].append(rule)

    existing["__defaults_version__"] = DEFAULTS_VERSION

    return existing


def save_data(data):
    DATA_FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def load_data():
    if DATA_FILE.exists():
        try:
            loaded = json.loads(
                DATA_FILE.read_text(
                    encoding="utf-8"
                )
            )

            merged = merge_default_rules(loaded)
            save_data(merged)

            return merged

        except Exception:
            pass

    data = default_data()
    save_data(data)

    return data


def rules_for_airline(data, airline):
    return [
        row
        for row in data.get(airline, [])
        if row.get("Havayolu") == airline
    ]


def find_rule(data, airline, rule_id):
    for row in rules_for_airline(
        data,
        airline,
    ):
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


def update_rule(
    data,
    airline,
    rule_id,
    updated_rule,
):
    data[airline] = [
        updated_rule
        if row.get("id") == rule_id
        else row
        for row in data.get(airline, [])
    ]

    return data


def option_index(options, value):
    if value in options:
        return options.index(value)

    return 0


GENERAL_RULES = [
    {
        "category": "INAD / NOREC",
        "title": "INAD yolcu formu",
        "detail": (
            "Servis adı EXT-CZA olarak girilir. 1 UNIT girilir. "
            "Not kısmına idari para cezası ve şirket adı yazılır."
        ),
    },
    {
        "category": "CMA / VIP / VPS",
        "title": "China teknisyen eşlik",
        "detail": (
            "Mailde yalnızca teknisyen eşlik varsa uçuş formuna "
            "+1 CMA eklenir ve not kısmına detay yazılır."
        ),
    },
    {
        "category": "CMA / VIP / VPS",
        "title": "CMA/VIP uçuş formu",
        "detail": (
            "DLH, UZB, ETD, CCA, KNE ve BRU için CMA/VIP "
            "hizmetleri uçuş formuna eklenir."
        ),
    },
    {
        "category": "Yemek / Otel",
        "title": "MENÜ-3",
        "detail": (
            "INAD/DELAY MENU için Tumiçtur'dan VOUCHER alınır."
        ),
    },
    {
        "category": "Fatura",
        "title": "Fatura dönemi",
        "detail": (
            "Dönem dışı açılan faturalar değerlendirilmez ve "
            "ödeme talep edilemez."
        ),
    },
    {
        "category": "Fatura",
        "title": "KDV'siz tutar",
        "detail": "Faturalarda her zaman KDV'siz tutar yazılır.",
    },
    {
        "category": "Yemek / Otel",
        "title": "Yemek faturası ekleri",
        "detail": (
            "Fatura, Transfer Excel detay tablosu ve "
            "Muhasebe detayı eklenir."
        ),
    },
    {
        "category": "Yemek / Otel",
        "title": "Otel faturaları",
        "detail": (
            "Konaklama vergisi KDV'siz tutara eklenir. "
            "Vergi oranı işlem öncesinde doğrulanmalıdır."
        ),
    },
    {
        "category": "GROUND Form",
        "title": "Kontuar giriş yeri",
        "detail": (
            "Kontuar hizmetleri IKARUS masaüstünde EXTRA FORM "
            "olarak girilir."
        ),
    },
    {
        "category": "GROUND Form",
        "title": "TPL kuralı",
        "detail": (
            "KAC hariç GROUND listesindeki havayollarına TPL girilmez."
        ),
    },
    {
        "category": "GROUND Form",
        "title": "GROUND listesi",
        "detail": "CES, CSN, CSC, KAC, KAL ve SVA.",
    },
    {
        "category": "CMA / VIP / VPS",
        "title": "Emirates mutabakatı",
        "detail": (
            "Haftalık Excel tablo Şefliğe gönderilir. "
            "Mutabakat sonrasında formlar hazırlanır."
        ),
    },
    {
        "category": "Sizer",
        "title": "Sizer kullanımı",
        "detail": (
            "GROUND FORM açılır. 1 UNIT EXT-SZR girilir. "
            "Fatura tarihi ayın son günüdür. Notta havayolu ve ay yazılır."
        ),
    },
    {
        "category": "ABS",
        "title": "ABS faturaları",
        "detail": (
            "Servis adı EXT. SCF dosyası Web IKARUS'tan ground "
            "olarak indirilip masaüstüne eklenir."
        ),
    },
    {
        "category": "Gökkuşağı",
        "title": "Gökkuşağı faturaları",
        "detail": (
            "GROUND FORM açılır. Genel servis adı EXT; "
            "DAH için HTL, REFRESHMENT veya CRM kullanılır."
        ),
    },
    {
        "category": "Ay Sonu Excess",
        "title": "Ay sonu müşteri adları",
        "detail": (
            "RAMEXC, AEEEXC, SVAEXC, FADEXC ve DAHEXC."
        ),
    },
    {
        "category": "OBH",
        "title": "OBH her zaman 1",
        "detail": (
            "CSC, FAD, AZV, ANKA, CSN, DAH, BRQ, IAW, ETD, "
            "GMS, KAC, MGH, IRB, KAL, AAW, IRC, RAM, ABY, "
            "TVP, VSV, ASL ve UBD."
        ),
    },
]


REPRESENTATIVES = [
    {
        "code": "KAL / KE",
        "representative_code": "13",
        "company": "GÖZEN",
    },
    {
        "code": "MAC / 3O",
        "representative_code": "75",
        "company": "SHARK",
    },
    {
        "code": "VSV / DV",
        "representative_code": "02",
        "company": "CASIO",
    },
    {
        "code": "ABY / G9",
        "representative_code": "75",
        "company": "Firma belirtilmedi",
    },
    {
        "code": "UBD / UD",
        "representative_code": "03",
        "company": "Firma belirtilmedi",
    },
    {
        "code": "SHI",
        "representative_code": "04",
        "company": "BİLEN",
    },
    {
        "code": "CHINA",
        "representative_code": "13",
        "company": "GÖZEN — CCA hariç",
    },
    {
        "code": "KNE",
        "representative_code": "15",
        "company": "ADRİYATİK",
    },
    {
        "code": "BELAVIA",
        "representative_code": "15",
        "company": "ADRİYATİK",
    },
]


TRIPLE_CODES = [
    {
        "airline": "Royal Air Maroc",
        "code": "RAM",
    },
    {
        "airline": "Air Arabia Maroc",
        "code": "MAC",
    },
    {
        "airline": "Air Arabia",
        "code": "ABY",
    },
]


if "data" not in st.session_state:
    st.session_state["data"] = load_data()


if "view" not in st.session_state:
    st.session_state["view"] = "Havayolu Rehberi"


if "editing_id" not in st.session_state:
    st.session_state["editing_id"] = None


st.sidebar.markdown("# ✈️ SFC")
st.sidebar.caption("SCF–IKARUS Operasyon Rehberi")
st.sidebar.divider()
st.sidebar.markdown("### Menü")


for menu_item in MENU_ITEMS:
    menu_clicked = st.sidebar.button(
        menu_item,
        use_container_width=True,
        type=(
            "primary"
            if st.session_state["view"] == menu_item
            else "secondary"
        ),
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
    "Aktif havayolu: "
    + selected_airline
)


current_rules = rules_for_airline(
    st.session_state["data"],
    selected_airline,
)


total_rules = sum(
    len(
        rules_for_airline(
            st.session_state["data"],
            airline_code,
        )
    )
    for airline_code in AIRLINES
)


filled_airlines = sum(
    1
    for airline_code in AIRLINES
    if rules_for_airline(
        st.session_state["data"],
        airline_code,
    )
)


st.title(
    selected_airline
    + " Operasyon Rehberi"
)


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


if page == "Havayolu Rehberi":
    st.subheader("Havayolu Bilgi Kartları")

    filter_1, filter_2, filter_3 = st.columns(3)

    with filter_1:
        search_text = st.text_input(
            "Bilgi ara",
            placeholder="Kontuar, CMA, OBH, fatura...",
            key="search-" + selected_airline,
        )

    with filter_2:
        category_filter = st.selectbox(
            "Kategori",
            ["Tümü"] + CATEGORIES,
            key="category-" + selected_airline,
        )

    with filter_3:
        status_filter = st.selectbox(
            "Kural durumu",
            ["Tümü"] + REQUIRED_OPTIONS,
            key="status-" + selected_airline,
        )

    filtered_rules = []

    for rule in current_rules:
        combined_text = " ".join(
            safe_text(value).lower()
            for value in rule.values()
        )

        if (
            search_text
            and search_text.lower() not in combined_text
        ):
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
            "Seçilen kriterlere uygun bilgi bulunamadı."
        )

    card_columns = st.columns(3)

    for index, rule in enumerate(filtered_rules):
        with card_columns[index % 3]:
            with st.container(border=True):
                st.markdown(
                    "#### "
                    + (
                        rule.get("Başlık")
                        or "Başlıksız"
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

                with st.expander(
                    "Detayları göster"
                ):
                    st.write(
                        rule.get("Detay")
                        or "-"
                    )

                    if rule.get("Not"):
                        st.markdown("**Not**")
                        st.write(rule.get("Not"))

                edit_column, delete_column = st.columns(2)

                with edit_column:
                    edit_clicked = st.button(
                        "Düzenle",
                        key="edit-" + rule["id"],
                        use_container_width=True,
                    )

                    if edit_clicked:
                        st.session_state["editing_id"] = rule["id"]
                        st.session_state["view"] = "Bilgi Düzenle / Sil"
                        st.rerun()

                with delete_column:
                    delete_clicked = st.button(
                        "Sil",
                        key="delete-" + rule["id"],
                        use_container_width=True,
                    )

                    if delete_clicked:
                        st.session_state["data"] = delete_rule(
                            st.session_state["data"],
                            selected_airline,
                            rule["id"],
                        )

                        save_data(
                            st.session_state["data"]
                        )

                        st.rerun()


if page == "Yeni Bilgi Ekle":
    st.subheader(
        selected_airline
        + " İçin Yeni Bilgi Ekle"
    )

    with st.form(
        "add-rule-form",
        clear_on_submit=True,
    ):
        form_column_1, form_column_2 = st.columns(2)

        with form_column_1:
            new_category = st.selectbox(
                "Kategori",
                CATEGORIES,
            )

            new_title = st.text_input(
                "Başlık",
            )

            new_summary = st.text_area(
                "Kısa bilgi",
                height=90,
            )

            new_status = st.selectbox(
                "Kural durumu",
                REQUIRED_OPTIONS,
            )

        with form_column_2:
            new_ikarus = st.text_input(
                "IKARUS yeri",
            )

            new_service = st.text_input(
                "Servis adı",
            )

            new_unit = st.text_input(
                "Unit / değer",
            )

            new_note = st.text_area(
                "Not",
                height=90,
            )

        new_details = st.text_area(
            "Detaylı açıklama",
            height=170,
        )

        add_submitted = st.form_submit_button(
            "Bilgiyi Kaydet",
            type="primary",
        )

        if add_submitted:
            if not new_title.strip():
                st.error(
                    "Başlık boş bırakılamaz."
                )

            else:
                new_rule = create_rule(
                    rule_id=(
                        "custom-"
                        + str(uuid.uuid4())
                    ),
                    airline=selected_airline,
                    category=new_category,
                    title=new_title,
                    summary=new_summary,
                    details=new_details,
                    ikarus_location=new_ikarus,
                    service_name=new_service,
                    unit=new_unit,
                    note=new_note,
                    requirement=new_status,
                )

                st.session_state[
                    "data"
                ][selected_airline].append(
                    new_rule
                )

                save_data(
                    st.session_state["data"]
                )

                st.session_state["view"] = "Havayolu Rehberi"
                st.rerun()


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
            "Düzenlenecek bilgi bulunmuyor."
        )

    else:
        rule_ids = [
            rule["id"]
            for rule in current_rules
        ]

        selected_index = 0

        if (
            st.session_state["editing_id"]
            in rule_ids
        ):
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
                ) or {}
            ).get(
                "Başlık",
                "Başlıksız",
            ),
        )

        selected_rule = find_rule(
            st.session_state["data"],
            selected_airline,
            selected_rule_id,
        )

        with st.form("edit-rule-form"):
            form_column_1, form_column_2 = st.columns(2)

            with form_column_1:
                edit_category = st.selectbox(
                    "Kategori",
                    CATEGORIES,
                    index=option_index(
                        CATEGORIES,
                        selected_rule.get(
                            "Kategori"
                        ),
                    ),
                )

                edit_title = st.text_input(
                    "Başlık",
                    value=selected_rule.get(
                        "Başlık",
                        "",
                    ),
                )

                edit_summary = st.text_area(
                    "Kısa bilgi",
                    value=selected_rule.get(
                        "Kısa Bilgi",
                        "",
                    ),
                    height=90,
                )

                edit_status = st.selectbox(
                    "Kural durumu",
                    REQUIRED_OPTIONS,
                    index=option_index(
                        REQUIRED_OPTIONS,
                        selected_rule.get(
                            "Durum"
                        ),
                    ),
                )

            with form_column_2:
                edit_ikarus = st.text_input(
                    "IKARUS yeri",
                    value=selected_rule.get(
                        "IKARUS Yeri",
                        "",
                    ),
                )

                edit_service = st.text_input(
                    "Servis adı",
                    value=selected_rule.get(
                        "Servis Adı",
                        "",
                    ),
                )

                edit_unit = st.text_input(
                    "Unit / değer",
                    value=selected_rule.get(
                        "Unit / Değer",
                        "",
                    ),
                )

                edit_note = st.text_area(
                    "Not",
                    value=selected_rule.get(
                        "Not",
                        "",
                    ),
                    height=90,
                )

            edit_details = st.text_area(
                "Detaylı açıklama",
                value=selected_rule.get(
                    "Detay",
                    "",
                ),
                height=170,
            )

            edit_submitted = st.form_submit_button(
                "Değişiklikleri Kaydet",
                type="primary",
            )

            if edit_submitted:
                if not edit_title.strip():
                    st.error(
                        "Başlık boş bırakılamaz."
                    )

                else:
                    edited_rule = create_rule(
                        rule_id=selected_rule_id,
                        airline=selected_airline,
                        category=edit_category,
                        title=edit_title,
                        summary=edit_summary,
                        details=edit_details,
                        ikarus_location=edit_ikarus,
                        service_name=edit_service,
                        unit=edit_unit,
                        note=edit_note,
                        requirement=edit_status,
                    )

                    st.session_state["data"] = update_rule(
                        st.session_state["data"],
                        selected_airline,
                        selected_rule_id,
                        edited_rule,
                    )

                    save_data(
                        st.session_state["data"]
                    )

                    st.session_state["view"] = "Havayolu Rehberi"
                    st.rerun()

        delete_selected = st.button(
            "Seçili Bilgiyi Sil",
            use_container_width=True,
        )

        if delete_selected:
            st.session_state["data"] = delete_rule(
                st.session_state["data"],
                selected_airline,
                selected_rule_id,
            )

            save_data(
                st.session_state["data"]
            )

            st.session_state["editing_id"] = None
            st.session_state["view"] = "Havayolu Rehberi"
            st.rerun()


if page == "Genel Operasyon Kuralları":
    st.subheader(
        "Genel Operasyon Kuralları"
    )

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
        combined_text = (
            rule["category"]
            + " "
            + rule["title"]
            + " "
            + rule["detail"]
        ).lower()

        if (
            general_search
            and general_search.lower() not in combined_text
        ):
            continue

        if (
            general_category != "Tümü"
            and rule["category"] != general_category
        ):
            continue

        visible_general_rules.append(rule)

    general_columns = st.columns(3)

    for index, rule in enumerate(
        visible_general_rules
    ):
        with general_columns[index % 3]:
            with st.container(border=True):
                st.markdown(
                    "#### "
                    + rule["title"]
                )

                st.caption(
                    rule["category"]
                )

                st.write(
                    rule["detail"]
                )


if page == "Temsilciler ve Kodlar":
    st.subheader("Temsilciler")

    representative_columns = st.columns(3)

    for index, representative in enumerate(
        REPRESENTATIVES
    ):
        with representative_columns[index % 3]:
            with st.container(border=True):
                st.markdown(
                    "#### "
                    + representative["code"]
                )

                st.markdown(
                    "**Temsilci kodu:** "
                    + representative["representative_code"]
                )

                st.markdown(
                    "**Firma:** "
                    + representative["company"]
                )

    st.divider()
    st.subheader("Üçlü Kodlar")

    code_columns = st.columns(3)

    for index, code_info in enumerate(
        TRIPLE_CODES
    ):
        with code_columns[index % 3]:
            with st.container(border=True):
                st.markdown(
                    "#### "
                    + code_info["code"]
                )

                st.write(
                    code_info["airline"]
                )


if page == "Tüm Bilgilerde Ara":
    st.subheader(
        "Tüm Havayollarında Ara"
    )

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
        combined_text = " ".join(
            safe_text(value).lower()
            for value in rule.values()
        )

        if (
            global_search
            and global_search.lower() not in combined_text
        ):
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

    for index, rule in enumerate(
        visible_rules
    ):
        with global_columns[index % 3]:
            with st.container(border=True):
                st.markdown(
                    "#### "
                    + rule.get(
                        "Başlık",
                        "Başlıksız",
                    )
                )

                st.caption(
                    rule.get(
                        "Havayolu",
                        "-",
                    )
                    + " • "
                    + rule.get(
                        "Kategori",
                        "-",
                    )
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


if page == "Veri Yönetimi":
    st.subheader("Veri Yönetimi")

    st.warning(
        "Veriler services.json dosyasına kaydedilir. "
        "Streamlit Cloud yeniden kurulursa yerel dosya "
        "kaybolabilir. Düzenli olarak JSON yedeği indir."
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
                uploaded_json.read().decode(
                    "utf-8"
                )
            )

            st.session_state["data"] = normalize_data(
                uploaded_data
            )

            st.session_state["data"][
                "__defaults_version__"
            ] = DEFAULTS_VERSION

            save_data(
                st.session_state["data"]
            )

            st.success(
                "Yedek başarıyla yüklendi."
            )

            st.rerun()

        except Exception as error:
            st.error(
                "Yedek okunamadı: "
                + str(error)
            )

    reload_defaults = st.button(
        "Hazır Kuralları Yeniden Yükle",
        use_container_width=True,
    )

    if reload_defaults:
        st.session_state["data"] = default_data()

        save_data(
            st.session_state["data"]
        )

        st.rerun()


st.divider()

st.caption(
    "SFC • SCF–IKARUS Dijital Operasyon Rehberi • "
    + selected_airline
)
