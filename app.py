# SFC CRUD BUILD 2026-07-01
import json
import uuid
from pathlib import Path
from datetime import datetime

import pandas as pd
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

SERVICE_COLUMNS = [
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
    "Son Güncelleme",
]

DATA_FILE = Path("services.json")


st.markdown(
    """
    <style>
    .stApp {
        background: #f3f6fa;
        color: #10233c;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #07192b 0%, #123452 100%);
        border-right: 1px solid rgba(255,255,255,0.12);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    .hero {
        background: linear-gradient(125deg, #081a2d 0%, #0e527c 58%, #12899b 100%);
        color: #ffffff;
        border-radius: 24px;
        padding: 2rem 2.2rem;
        box-shadow: 0 18px 45px rgba(9,30,50,0.18);
        margin-bottom: 1.25rem;
    }

    .hero-title {
        color: #ffffff;
        font-size: clamp(2.1rem, 4vw, 3.5rem);
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
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.24);
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
        box-shadow: 0 7px 22px rgba(14,38,62,0.06);
        min-height: 132px;
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

    .success-note {
        background: #eafaf2;
        border: 1px solid #9dddbd;
        color: #155b36;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-bottom: 1rem;
        line-height: 1.55;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #d9e3ec;
        border-radius: 15px;
        padding: 0.85rem 1rem;
        box-shadow: 0 6px 18px rgba(14,38,62,0.05);
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] div {
        color: #10233c !important;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    textarea {
        background: #ffffff !important;
        color: #10233c !important;
        border-color: #ccd8e4 !important;
    }

    input {
        color: #10233c !important;
        background: #ffffff !important;
    }

    h1, h2, h3, h4, p, label {
        color: #10233c;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def empty_data():
    return {code: [] for code in AIRLINES}


def normalize_data(data):
    normalized = empty_data()

    if isinstance(data, dict):
        for code in AIRLINES:
            rows = data.get(code, [])
            if isinstance(rows, list):
                normalized[code] = rows

    return normalized


def load_data():
    if DATA_FILE.exists():
        try:
            loaded = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            return normalize_data(loaded)
        except Exception:
            return empty_data()

    return empty_data()


def save_data(data):
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def make_row(
    airline,
    category,
    service_name,
    section,
    field,
    rule,
    unit,
    required,
    when_to_enter,
    source,
    note,
):
    return {
        "id": str(uuid.uuid4()),
        "Havayolu": airline,
        "Ana Kategori": category,
        "Hizmet Adı": service_name,
        "IKARUS Konu Başlığı": section,
        "IKARUS Alanı": field,
        "Giriş Kuralı": rule,
        "Birim": unit,
        "Zorunlu": required,
        "Ne Zaman Girilir?": when_to_enter,
        "Kontrol Kaynağı": source,
        "Havayolu Özel Notu": note,
        "Son Güncelleme": datetime.now().strftime("%d.%m.%Y %H:%M"),
    }


def rows_to_df(rows):
    display_rows = []

    for row in rows:
        new_row = {"Sil": False}

        for col in SERVICE_COLUMNS:
            new_row[col] = row.get(col, "")

        new_row["id"] = row.get("id", str(uuid.uuid4()))
        display_rows.append(new_row)

    if not display_rows:
        return pd.DataFrame(columns=["Sil"] + SERVICE_COLUMNS + ["id"])

    return pd.DataFrame(display_rows)


def df_to_rows(df, airline):
    saved_rows = []

    for _, row in df.iterrows():
        delete_value = bool(row.get("Sil", False))

        if delete_value:
            continue

        service_name = str(row.get("Hizmet Adı", "")).strip()

        if not service_name:
            continue

        saved_row = {}
        current_id = str(row.get("id", "")).strip()

        if current_id:
            saved_row["id"] = current_id
        else:
            saved_row["id"] = str(uuid.uuid4())

        saved_row["Havayolu"] = airline

        for col in SERVICE_COLUMNS:
            if col == "Havayolu":
                continue

            saved_row[col] = str(row.get(col, "")).strip()

        saved_row["Son Güncelleme"] = datetime.now().strftime("%d.%m.%Y %H:%M")
        saved_rows.append(saved_row)

    return saved_rows


if "data" not in st.session_state:
    st.session_state["data"] = load_data()


st.sidebar.markdown("# ✈️ SFC")
st.sidebar.caption("SCF–IKARUS Operasyon Rehberi")
st.sidebar.divider()

page = st.sidebar.radio(
    "MENÜ",
    [
        "Havayolu Yönetimi",
        "Tüm Hizmetler",
        "Veri Yönetimi",
    ],
)

selected_airline = st.sidebar.selectbox(
    "Havayolu seç",
    AIRLINES,
)

st.sidebar.divider()
st.sidebar.caption("Aktif havayolu: " + selected_airline)
st.sidebar.caption("Veri dosyası: services.json")


st.markdown(
    f"""
    <section class="hero">
        <div style="font-size:0.78rem;font-weight:800;letter-spacing:0.15em;text-transform:uppercase;opacity:0.82;margin-bottom:0.55rem;">
            SFC • SCF–IKARUS DİJİTAL HANDBOOK
        </div>

        <div class="hero-title">
            {selected_airline} Hizmet Rehberi
        </div>

        <div class="hero-text">
            Bu ekranda {selected_airline} havayolu için IKARUS'a girilecek hizmetleri
            ekleyebilir, silebilir, düzenleyebilir ve SCF kontrol akışını yönetebilirsin.
        </div>

        <div>
            <span class="badge">{selected_airline}</span>
            <span class="badge">Ekle / Düzenle / Sil</span>
            <span class="badge">SCF–IKARUS</span>
            <span class="badge">CRUD Sürümü</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)


current_rows = st.session_state["data"].get(selected_airline, [])

total_services = sum(len(rows) for rows in st.session_state["data"].values())
filled_airlines = sum(1 for rows in st.session_state["data"].values() if rows)

m1, m2, m3, m4 = st.columns(4)

m1.metric("Seçili Havayolu", selected_airline)
m2.metric("Bu Havayolundaki Hizmet", len(current_rows))
m3.metric("Toplam Hizmet", total_services)
m4.metric("Dolu Havayolu", filled_airlines)


if page == "Havayolu Yönetimi":
    st.subheader("1. Yeni Hizmet Ekle")

    with st.form("add_service_form", clear_on_submit=True):
        c1, c2 = st.columns(2)

        with c1:
            new_category = st.selectbox("Ana Kategori", CATEGORIES)
            new_service = st.text_input("Hizmet Adı", placeholder="Örn: GPU, merdiven, otobüs")
            new_section = st.text_input("IKARUS Konu Başlığı", placeholder="IKARUS'ta açılacak bölüm")
            new_field = st.text_input("IKARUS Alanı", placeholder="Adet / süre / saat / açıklama")

        with c2:
            new_rule = st.text_area("Giriş Kuralı", placeholder="Nasıl girilecek?", height=90)
            new_unit = st.text_input("Birim", placeholder="Adet / dakika / kg / saat")
            new_required = st.selectbox("Zorunlu mu?", ["Evet", "Hayır", "Duruma Bağlı"])
            new_when = st.text_area("Ne Zaman Girilir?", placeholder="Hangi durumda girilecek?", height=90)

        new_source = st.text_input(
            "Kontrol Kaynağı",
            placeholder="Operasyon kaydı / ekipman kaydı / yetkili onayı",
        )

        new_note = st.text_area(
            "Havayolu Özel Notu",
            placeholder="Özel kural veya açıklama",
            height=90,
        )

        add_clicked = st.form_submit_button("Hizmeti Ekle")

        if add_clicked:
            if not new_service.strip():
                st.error("Hizmet adı boş olamaz.")
            else:
                new_row = make_row(
                    selected_airline,
                    new_category,
                    new_service,
                    new_section,
                    new_field,
                    new_rule,
                    new_unit,
                    new_required,
                    new_when,
                    new_source,
                    new_note,
                )

                st.session_state["data"][selected_airline].append(new_row)
                save_data(st.session_state["data"])
                st.success("Hizmet eklendi ve kaydedildi.")
                st.rerun()

    st.subheader("2. Mevcut Hizmetleri Düzenle / Sil")

    st.markdown(
        """
        <div class="notice">
            Hücrelerin içini değiştirerek düzenleme yapabilirsin.
            Satır silmek için en soldaki <strong>Sil</strong> kutusunu işaretleyip
            alttaki <strong>Değişiklikleri Kaydet</strong> butonuna bas.
        </div>
        """,
        unsafe_allow_html=True,
    )

    editor_df = rows_to_df(st.session_state["data"].get(selected_airline, []))

    edited_df = st.data_editor(
        editor_df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "Sil": st.column_config.CheckboxColumn("Sil", default=False),
            "id": None,
            "Ana Kategori": st.column_config.SelectboxColumn(
                "Ana Kategori",
                options=CATEGORIES,
            ),
            "Zorunlu": st.column_config.SelectboxColumn(
                "Zorunlu",
                options=["Evet", "Hayır", "Duruma Bağlı"],
            ),
        },
        key="editor_" + selected_airline,
    )

    save_clicked = st.button("Değişiklikleri Kaydet", type="primary")

    if save_clicked:
        cleaned_rows = df_to_rows(edited_df, selected_airline)
        st.session_state["data"][selected_airline] = cleaned_rows
        save_data(st.session_state["data"])
        st.success("Değişiklikler kaydedildi.")
        st.rerun()

    st.subheader("3. SCF Kapanış Kontrol Listesi")

    checklist = [
        "Doğru uçuş numarası ve tarih seçildi.",
        "Arrival / Departure ayrımı kontrol edildi.",
        "Uçak tipi ve tescili doğrulandı.",
        "Gerçekleşen bütün hizmetler girildi.",
        "Gerçekleşmeyen hizmetler eklenmedi.",
        "Saat, adet, süre ve birimler kontrol edildi.",
        "Mükerrer hizmet bulunmadığı kontrol edildi.",
        "Ekstra hizmet açıklamaları eklendi.",
        "Havayolu özel kuralları kontrol edildi.",
        "İmza ve kapanış işlemleri tamamlandı.",
    ]

    completed = 0

    for index, item in enumerate(checklist):
        checked = st.checkbox(
            item,
            key=selected_airline + "_check_" + str(index),
        )

        if checked:
            completed += 1

    st.progress(completed / len(checklist))
    st.write("Tamamlanan kontrol: **" + str(completed) + "/" + str(len(checklist)) + "**")


if page == "Tüm Hizmetler":
    st.subheader("Tüm Havayollarındaki Hizmetler")

    all_rows = []

    for code, rows in st.session_state["data"].items():
        for row in rows:
            all_rows.append(row)

    search = st.text_input(
        "Genel arama",
        placeholder="GPU, merdiven, süre, SVA...",
    )

    category_filter = st.selectbox(
        "Kategori filtresi",
        ["Tümü"] + CATEGORIES,
    )

    filtered_rows = []

    for row in all_rows:
        text = " ".join(str(value).lower() for value in row.values())

        if not search:
            search_match = True
        else:
            search_match = search.lower() in text

        if category_filter == "Tümü":
            category_match = True
        else:
            category_match = row.get("Ana Kategori") == category_filter

        if search_match and category_match:
            filtered_rows.append(row)

    if filtered_rows:
        st.dataframe(
            pd.DataFrame(filtered_rows)[SERVICE_COLUMNS],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Kriterlere uygun hizmet bulunamadı.")


if page == "Veri Yönetimi":
    st.subheader("Veri Yönetimi")

    st.markdown(
        """
        <div class="notice">
            Bu sürüm veriyi <strong>services.json</strong> dosyasına yazar.
            Streamlit Cloud uygulaması yeniden kurulduğunda veya dosyalar sıfırlandığında
            yerel JSON verisi kaybolabilir. Kalıcı çözüm için sonraki aşamada Supabase
            veya Google Sheets bağlantısı yapılmalıdır.
        </div>
        """,
        unsafe_allow_html=True,
    )

    data_as_json = json.dumps(
        st.session_state["data"],
        ensure_ascii=False,
        indent=2,
    )

    st.download_button(
        "Veriyi JSON Olarak İndir",
        data=data_as_json.encode("utf-8"),
        file_name="sfc_services_backup.json",
        mime="application/json",
    )

    uploaded_file = st.file_uploader("JSON yedeği yükle", type=["json"])

    if uploaded_file is not None:
        try:
            uploaded_data = json.loads(uploaded_file.read().decode("utf-8"))
            st.session_state["data"] = normalize_data(uploaded_data)
            save_data(st.session_state["data"])
            st.success("JSON yedeği yüklendi ve kaydedildi.")
            st.rerun()
        except Exception as exc:
            st.error("JSON okunamadı: " + str(exc))

    reset_clicked = st.button("Tüm Veriyi Sıfırla")

    if reset_clicked:
        st.session_state["data"] = empty_data()
        save_data(st.session_state["data"])
        st.warning("Tüm hizmet kayıtları sıfırlandı.")
        st.rerun()


st.divider()
st.caption("SFC • SCF–IKARUS Dijital Operasyon Rehberi • CRUD Yönetim Paneli")
