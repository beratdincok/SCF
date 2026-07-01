# SFC CRUD CLEAN BUILD 2026-07-01

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


CHECKLIST = [
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
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
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
    clean_data = empty_data()

    if isinstance(data, dict):
        for code in AIRLINES:
            rows = data.get(code, [])

            if isinstance(rows, list):
                fixed_rows = []

                for row in rows:
                    if isinstance(row, dict):
                        fixed_row = {}

                        fixed_row["id"] = row.get("id", str(uuid.uuid4()))
                        fixed_row["Havayolu"] = code

                        for col in SERVICE_COLUMNS:
                            if col == "Havayolu":
                                fixed_row[col] = code
                            else:
                                fixed_row[col] = row.get(col, "")

                        fixed_rows.append(fixed_row)

                clean_data[code] = fixed_rows

    return clean_data


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


def rows_to_df(rows, airline):
    display_rows = []

    for row in rows:
        if row.get("Havayolu") != airline:
            continue

        new_row = {"Sil": False}

        for col in SERVICE_COLUMNS:
            if col == "Havayolu":
                new_row[col] = airline
            else:
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

        current_id = str(row.get("id", "")).strip()

        if current_id:
            row_id = current_id
        else:
            row_id = str(uuid.uuid4())

        saved_row = {
            "id": row_id,
            "Havayolu": airline,
            "Ana Kategori": str(row.get("Ana Kategori", "")).strip(),
            "Hizmet Adı": service_name,
            "IKARUS Konu Başlığı": str(row.get("IKARUS Konu Başlığı", "")).strip(),
            "IKARUS Alanı": str(row.get("IKARUS Alanı", "")).strip(),
            "Giriş Kuralı": str(row.get("Giriş Kuralı", "")).strip(),
            "Birim": str(row.get("Birim", "")).strip(),
            "Zorunlu": str(row.get("Zorunlu", "")).strip(),
            "Ne Zaman Girilir?": str(row.get("Ne Zaman Girilir?", "")).strip(),
            "Kontrol Kaynağı": str(row.get("Kontrol Kaynağı", "")).strip(),
            "Havayolu Özel Notu": str(row.get("Havayolu Özel Notu", "")).strip(),
            "Son Güncelleme": datetime.now().strftime("%d.%m.%Y %H:%M"),
        }

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


current_rows = [
    row
    for row in st.session_state["data"].get(selected_airline, [])
    if row.get("Havayolu") == selected_airline
]


total_services = sum(
    len(rows)
    for rows in st.session_state["data"].values()
)


filled_airlines = sum(
    1
    for rows in st.session_state["data"].values()
    if len(rows) > 0
)


st.title(selected_airline + " Hizmet Rehberi")


st.info(
    "Bu ekranda "
    + selected_airline
    + " havayolu için IKARUS'a girilecek hizmetleri "
    + "ekleyebilir, silebilir, düzenleyebilir ve SCF kontrol akışını yönetebilirsin. "
    + "Başka havayoluna geçtiğinde bu havayoluna ait hizmetler orada görünmez."
)


m1, m2, m3, m4 = st.columns(4)

m1.metric("Seçili Havayolu", selected_airline)
m2.metric("Bu Havayolundaki Hizmet", len(current_rows))
m3.metric("Toplam Hizmet", total_services)
m4.metric("Dolu Havayolu", filled_airlines)

st.divider()


if page == "Havayolu Yönetimi":
    st.subheader("1. Yeni Hizmet Ekle")

    with st.form("add_service_form", clear_on_submit=True):
        c1, c2 = st.columns(2)

        with c1:
            new_category = st.selectbox(
                "Ana Kategori",
                CATEGORIES,
            )

            new_service = st.text_input(
                "Hizmet Adı",
                placeholder="Örn: GPU, merdiven, otobüs",
            )

            new_section = st.text_input(
                "IKARUS Konu Başlığı",
                placeholder="IKARUS'ta açılacak bölüm",
            )

            new_field = st.text_input(
                "IKARUS Alanı",
                placeholder="Adet / süre / saat / açıklama",
            )

        with c2:
            new_rule = st.text_area(
                "Giriş Kuralı",
                placeholder="Nasıl girilecek?",
                height=90,
            )

            new_unit = st.text_input(
                "Birim",
                placeholder="Adet / dakika / kg / saat",
            )

            new_required = st.selectbox(
                "Zorunlu mu?",
                ["Evet", "Hayır", "Duruma Bağlı"],
            )

            new_when = st.text_area(
                "Ne Zaman Girilir?",
                placeholder="Hangi durumda girilecek?",
                height=90,
            )

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

                st.success(
                    selected_airline
                    + " için hizmet eklendi ve kaydedildi."
                )

                st.rerun()

    st.subheader("2. Mevcut Hizmetleri Düzenle / Sil")

    st.warning(
        "Bu tabloda sadece "
        + selected_airline
        + " havayoluna ait hizmetler gösterilir. "
        + "Başka havayolunun hizmetleri burada görünmez."
    )

    editor_df = rows_to_df(
        st.session_state["data"].get(selected_airline, []),
        selected_airline,
    )

    edited_df = st.data_editor(
        editor_df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "Sil": st.column_config.CheckboxColumn(
                "Sil",
                default=False,
            ),
            "id": None,
            "Havayolu": st.column_config.TextColumn(
                "Havayolu",
                disabled=True,
            ),
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

    save_clicked = st.button(
        "Değişiklikleri Kaydet",
        type="primary",
    )

    if save_clicked:
        cleaned_rows = df_to_rows(
            edited_df,
            selected_airline,
        )

        st.session_state["data"][selected_airline] = cleaned_rows

        save_data(st.session_state["data"])

        st.success(
            selected_airline
            + " hizmetleri güncellendi."
        )

        st.rerun()

    st.subheader("3. SCF Kapanış Kontrol Listesi")

    completed = 0

    for index, item in enumerate(CHECKLIST):
        checked = st.checkbox(
            item,
            key=selected_airline + "_check_" + str(index),
        )

        if checked:
            completed += 1

    st.progress(completed / len(CHECKLIST))

    st.write(
        "Tamamlanan kontrol: **"
        + str(completed)
        + "/"
        + str(len(CHECKLIST))
        + "**"
    )


if page == "Tüm Hizmetler":
    st.subheader("Tüm Havayollarındaki Hizmetler")

    st.info(
        "Bu sayfa genel arama sayfasıdır. Burada bütün havayollarının hizmetleri "
        "bilerek birlikte gösterilir. Sadece seçili havayolunu görmek için "
        "'Havayolu Yönetimi' sayfasını kullan."
    )

    all_rows = []

    for code, rows in st.session_state["data"].items():
        for row in rows:
            fixed_row = dict(row)
            fixed_row["Havayolu"] = code
            all_rows.append(fixed_row)

    search = st.text_input(
        "Genel arama",
        placeholder="GPU, merdiven, süre, SVA...",
    )

    category_filter = st.selectbox(
        "Kategori filtresi",
        ["Tümü"] + CATEGORIES,
    )

    airline_filter = st.selectbox(
        "Havayolu filtresi",
        ["Tümü"] + AIRLINES,
    )

    filtered_rows = []

    for row in all_rows:
        text = " ".join(
            str(value).lower()
            for value in row.values()
        )

        if not search:
            search_match = True
        else:
            search_match = search.lower() in text

        if category_filter == "Tümü":
            category_match = True
        else:
            category_match = row.get("Ana Kategori") == category_filter

        if airline_filter == "Tümü":
            airline_match = True
        else:
            airline_match = row.get("Havayolu") == airline_filter

        if search_match and category_match and airline_match:
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

    st.warning(
        "Bu sürüm veriyi services.json dosyasına yazar. Streamlit Cloud yeniden "
        "kurulduğunda veya dosyalar sıfırlandığında yerel JSON verisi kaybolabilir. "
        "Kalıcı çözüm için sonraki aşamada Supabase veya Google Sheets bağlantısı yapılmalıdır."
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

    uploaded_file = st.file_uploader(
        "JSON yedeği yükle",
        type=["json"],
    )

    if uploaded_file is not None:
        try:
            uploaded_data = json.loads(
                uploaded_file.read().decode("utf-8")
            )

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

st.caption(
    "SFC • SCF–IKARUS Dijital Operasyon Rehberi • "
    + selected_airline
)
