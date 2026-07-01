# SFC MODERN CARD BUILD FIXED MENU 2026-07-01

import json
import uuid
from pathlib import Path
from datetime import datetime

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
    "Hizmet Kartları",
    "Yeni Hizmet Ekle",
    "Hizmet Düzenle / Sil",
    "Tüm Hizmetlerde Ara",
    "SCF Kontrol",
    "Veri Yönetimi",
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


REQUIRED_OPTIONS = [
    "Evet",
    "Hayır",
    "Duruma Bağlı",
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
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: rgba(255, 255, 255, 0.10) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.20) !important;
        border-radius: 12px !important;
        padding: 0.65rem 0.85rem !important;
        margin-bottom: 0.25rem !important;
        font-weight: 700 !important;
        text-align: left !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(41, 194, 209, 0.22) !important;
        border-color: rgba(41, 194, 209, 0.70) !important;
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: #29c2d1 !important;
        color: #061b2e !important;
        border: 1px solid #29c2d1 !important;
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
        border-radius: 16px;
        padding: 0.9rem 1rem;
        box-shadow: 0 6px 18px rgba(14, 38, 62, 0.05);
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] div {
        color: #10233c !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border-radius: 18px;
        box-shadow: 0 8px 22px rgba(14, 38, 62, 0.05);
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


def safe_text(value):
    if value is None:
        return ""
    return str(value)


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
                        fixed_row = {
                            "id": safe_text(row.get("id")) or str(uuid.uuid4()),
                            "Havayolu": code,
                            "Ana Kategori": safe_text(row.get("Ana Kategori")),
                            "Hizmet Adı": safe_text(row.get("Hizmet Adı")),
                            "IKARUS Konu Başlığı": safe_text(row.get("IKARUS Konu Başlığı")),
                            "IKARUS Alanı": safe_text(row.get("IKARUS Alanı")),
                            "Giriş Kuralı": safe_text(row.get("Giriş Kuralı")),
                            "Birim": safe_text(row.get("Birim")),
                            "Zorunlu": safe_text(row.get("Zorunlu")),
                            "Ne Zaman Girilir?": safe_text(row.get("Ne Zaman Girilir?")),
                            "Kontrol Kaynağı": safe_text(row.get("Kontrol Kaynağı")),
                            "Havayolu Özel Notu": safe_text(row.get("Havayolu Özel Notu")),
                            "Son Güncelleme": safe_text(row.get("Son Güncelleme")),
                        }

                        if fixed_row["Hizmet Adı"].strip():
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
        "Hizmet Adı": service_name.strip(),
        "IKARUS Konu Başlığı": section.strip(),
        "IKARUS Alanı": field.strip(),
        "Giriş Kuralı": rule.strip(),
        "Birim": unit.strip(),
        "Zorunlu": required,
        "Ne Zaman Girilir?": when_to_enter.strip(),
        "Kontrol Kaynağı": source.strip(),
        "Havayolu Özel Notu": note.strip(),
        "Son Güncelleme": datetime.now().strftime("%d.%m.%Y %H:%M"),
    }


def services_for_airline(data, airline):
    rows = data.get(airline, [])

    return [
        row
        for row in rows
        if row.get("Havayolu") == airline
    ]


def find_service(data, airline, service_id):
    for row in services_for_airline(data, airline):
        if row.get("id") == service_id:
            return row

    return None


def update_service(data, airline, service_id, updated_row):
    rows = data.get(airline, [])
    new_rows = []

    for row in rows:
        if row.get("id") == service_id:
            new_rows.append(updated_row)
        else:
            new_rows.append(row)

    data[airline] = new_rows

    return data


def delete_service(data, airline, service_id):
    data[airline] = [
        row
        for row in data.get(airline, [])
        if row.get("id") != service_id
    ]

    return data


def filter_services(rows, search, category, required):
    filtered = []

    for row in rows:
        row_text = " ".join(
            safe_text(value).lower()
            for value in row.values()
        )

        if search and search.lower() not in row_text:
            continue

        if category != "Tümü" and row.get("Ana Kategori") != category:
            continue

        if required != "Tümü" and row.get("Zorunlu") != required:
            continue

        filtered.append(row)

    return filtered


def service_title(row):
    if not isinstance(row, dict):
        return "Hizmet bulunamadı"

    name = row.get("Hizmet Adı", "").strip()
    category = row.get("Ana Kategori", "").strip()

    if name and category:
        return name + " • " + category

    if name:
        return name

    return "İsimsiz Hizmet"


def option_index(options, value):
    if value in options:
        return options.index(value)

    return 0


if "data" not in st.session_state:
    st.session_state["data"] = load_data()


if "editing_id" not in st.session_state:
    st.session_state["editing_id"] = None


if "view" not in st.session_state:
    st.session_state["view"] = "Hizmet Kartları"


st.sidebar.markdown("# ✈️ SFC")
st.sidebar.caption("SCF–IKARUS Operasyon Rehberi")
st.sidebar.divider()


st.sidebar.markdown("### Menü")

for menu_item in MENU_ITEMS:
    button_type = "primary" if st.session_state["view"] == menu_item else "secondary"

    clicked = st.sidebar.button(
        menu_item,
        use_container_width=True,
        type=button_type,
        key="nav_" + menu_item,
    )

    if clicked:
        st.session_state["view"] = menu_item
        st.rerun()


page = st.session_state["view"]


st.sidebar.divider()


selected_airline = st.sidebar.selectbox(
    "Havayolu seç",
    AIRLINES,
)


st.sidebar.caption("Aktif havayolu: " + selected_airline)
st.sidebar.caption("Bu sayfada sadece seçili havayolu verisi görünür.")


current_rows = services_for_airline(
    st.session_state["data"],
    selected_airline,
)


total_services = sum(
    len(services_for_airline(st.session_state["data"], code))
    for code in AIRLINES
)


filled_airlines = sum(
    1
    for code in AIRLINES
    if len(services_for_airline(st.session_state["data"], code)) > 0
)


st.title(selected_airline + " Hizmet Rehberi")


st.info(
    selected_airline
    + " için eklenen hizmetler sadece bu havayolunda görünür. "
    + "Başka havayoluna geçtiğinde bu kayıtlar karışmaz."
)


m1, m2, m3, m4 = st.columns(4)

m1.metric("Seçili Havayolu", selected_airline)
m2.metric("Bu Havayolundaki Hizmet", len(current_rows))
m3.metric("Toplam Hizmet", total_services)
m4.metric("Dolu Havayolu", filled_airlines)

st.divider()


if page == "Hizmet Kartları":
    st.subheader("Hizmet Kartları")

    col_filter_1, col_filter_2, col_filter_3 = st.columns(3)

    with col_filter_1:
        search_text = st.text_input(
            "Ara",
            placeholder="GPU, merdiven, süre, not...",
            key="card_search_" + selected_airline,
        )

    with col_filter_2:
        category_filter = st.selectbox(
            "Kategori",
            ["Tümü"] + CATEGORIES,
            key="card_category_" + selected_airline,
        )

    with col_filter_3:
        required_filter = st.selectbox(
            "Zorunluluk",
            ["Tümü"] + REQUIRED_OPTIONS,
            key="card_required_" + selected_airline,
        )

    filtered_rows = filter_services(
        current_rows,
        search_text,
        category_filter,
        required_filter,
    )

    if not filtered_rows:
        st.warning(
            selected_airline
            + " için gösterilecek hizmet bulunamadı. "
            + "Yeni hizmet eklemek için sol menüden 'Yeni Hizmet Ekle' sayfasına geç."
        )

    for row in filtered_rows:
        with st.container(border=True):
            top_1, top_2, top_3 = st.columns([3, 1, 1])

            with top_1:
                st.subheader(row.get("Hizmet Adı", "İsimsiz Hizmet"))
                st.caption(
                    row.get("Ana Kategori", "")
                    + " • "
                    + row.get("Zorunlu", "")
                )

            with top_2:
                edit_clicked = st.button(
                    "Düzenle",
                    key="edit_card_" + row["id"],
                    use_container_width=True,
                )

                if edit_clicked:
                    st.session_state["editing_id"] = row["id"]
                    st.session_state["view"] = "Hizmet Düzenle / Sil"
                    st.rerun()

            with top_3:
                delete_clicked = st.button(
                    "Sil",
                    key="delete_card_" + row["id"],
                    use_container_width=True,
                )

                if delete_clicked:
                    st.session_state["data"] = delete_service(
                        st.session_state["data"],
                        selected_airline,
                        row["id"],
                    )

                    save_data(st.session_state["data"])

                    st.success("Hizmet silindi.")

                    st.rerun()

            detail_1, detail_2, detail_3 = st.columns(3)

            with detail_1:
                st.write("**IKARUS Konu Başlığı**")
                st.write(row.get("IKARUS Konu Başlığı", "-"))

                st.write("**IKARUS Alanı**")
                st.write(row.get("IKARUS Alanı", "-"))

            with detail_2:
                st.write("**Birim**")
                st.write(row.get("Birim", "-"))

                st.write("**Ne Zaman Girilir?**")
                st.write(row.get("Ne Zaman Girilir?", "-"))

            with detail_3:
                st.write("**Kontrol Kaynağı**")
                st.write(row.get("Kontrol Kaynağı", "-"))

                st.write("**Son Güncelleme**")
                st.write(row.get("Son Güncelleme", "-"))

            st.write("**Giriş Kuralı**")
            st.write(row.get("Giriş Kuralı", "-"))

            if row.get("Havayolu Özel Notu", "").strip():
                st.write("**Havayolu Özel Notu**")
                st.write(row.get("Havayolu Özel Notu", "-"))


if page == "Yeni Hizmet Ekle":
    st.subheader("Yeni Hizmet Ekle")

    with st.form("add_service_form", clear_on_submit=True):
        c1, c2 = st.columns(2)

        with c1:
            new_category = st.selectbox(
                "Ana Kategori",
                CATEGORIES,
                key="add_category",
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

            new_unit = st.text_input(
                "Birim",
                placeholder="Adet / dakika / kg / saat",
            )

        with c2:
            new_required = st.selectbox(
                "Zorunlu mu?",
                REQUIRED_OPTIONS,
                key="add_required",
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

            new_rule = st.text_area(
                "Giriş Kuralı",
                placeholder="Nasıl girilecek?",
                height=120,
            )

        new_note = st.text_area(
            "Havayolu Özel Notu",
            placeholder="Özel kural veya açıklama",
            height=90,
        )

        add_clicked = st.form_submit_button(
            "Hizmeti Kaydet",
            type="primary",
        )

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
                    + " için yeni hizmet kaydedildi."
                )

                st.session_state["view"] = "Hizmet Kartları"

                st.rerun()


if page == "Hizmet Düzenle / Sil":
    st.subheader("Hizmet Düzenle / Sil")

    current_rows = services_for_airline(
        st.session_state["data"],
        selected_airline,
    )

    if not current_rows:
        st.warning(
            selected_airline
            + " için düzenlenecek hizmet bulunmuyor."
        )
    else:
        current_ids = [
            row["id"]
            for row in current_rows
        ]

        selected_index = 0

        if st.session_state["editing_id"] in current_ids:
            selected_index = current_ids.index(st.session_state["editing_id"])

        selected_service_id = st.selectbox(
            "Düzenlenecek hizmeti seç",
            current_ids,
            index=selected_index,
            format_func=lambda service_id: service_title(
                find_service(
                    st.session_state["data"],
                    selected_airline,
                    service_id,
                )
            ),
            key="edit_service_selector_" + selected_airline,
        )

        selected_row = find_service(
            st.session_state["data"],
            selected_airline,
            selected_service_id,
        )

        st.session_state["editing_id"] = selected_service_id

        with st.form("edit_service_form"):
            c1, c2 = st.columns(2)

            with c1:
                edit_category = st.selectbox(
                    "Ana Kategori",
                    CATEGORIES,
                    index=option_index(
                        CATEGORIES,
                        selected_row.get("Ana Kategori", ""),
                    ),
                    key="edit_category_" + selected_service_id,
                )

                edit_service = st.text_input(
                    "Hizmet Adı",
                    value=selected_row.get("Hizmet Adı", ""),
                )

                edit_section = st.text_input(
                    "IKARUS Konu Başlığı",
                    value=selected_row.get("IKARUS Konu Başlığı", ""),
                )

                edit_field = st.text_input(
                    "IKARUS Alanı",
                    value=selected_row.get("IKARUS Alanı", ""),
                )

                edit_unit = st.text_input(
                    "Birim",
                    value=selected_row.get("Birim", ""),
                )

            with c2:
                edit_required = st.selectbox(
                    "Zorunlu mu?",
                    REQUIRED_OPTIONS,
                    index=option_index(
                        REQUIRED_OPTIONS,
                        selected_row.get("Zorunlu", ""),
                    ),
                    key="edit_required_" + selected_service_id,
                )

                edit_when = st.text_area(
                    "Ne Zaman Girilir?",
                    value=selected_row.get("Ne Zaman Girilir?", ""),
                    height=90,
                )

                edit_source = st.text_input(
                    "Kontrol Kaynağı",
                    value=selected_row.get("Kontrol Kaynağı", ""),
                )

                edit_rule = st.text_area(
                    "Giriş Kuralı",
                    value=selected_row.get("Giriş Kuralı", ""),
                    height=120,
                )

            edit_note = st.text_area(
                "Havayolu Özel Notu",
                value=selected_row.get("Havayolu Özel Notu", ""),
                height=90,
            )

            save_edit = st.form_submit_button(
                "Düzenlemeyi Kaydet",
                type="primary",
            )

            if save_edit:
                if not edit_service.strip():
                    st.error("Hizmet adı boş olamaz.")
                else:
                    updated_row = make_row(
                        selected_airline,
                        edit_category,
                        edit_service,
                        edit_section,
                        edit_field,
                        edit_rule,
                        edit_unit,
                        edit_required,
                        edit_when,
                        edit_source,
                        edit_note,
                    )

                    updated_row["id"] = selected_service_id

                    st.session_state["data"] = update_service(
                        st.session_state["data"],
                        selected_airline,
                        selected_service_id,
                        updated_row,
                    )

                    save_data(st.session_state["data"])

                    st.success("Hizmet güncellendi.")

                    st.session_state["view"] = "Hizmet Kartları"

                    st.rerun()

        st.divider()

        delete_col_1, delete_col_2 = st.columns([3, 1])

        with delete_col_1:
            st.warning(
                "Bu işlem yalnızca "
                + selected_airline
                + " içindeki seçili hizmeti siler."
            )

        with delete_col_2:
            delete_selected = st.button(
                "Seçili Hizmeti Sil",
                type="secondary",
                use_container_width=True,
            )

            if delete_selected:
                st.session_state["data"] = delete_service(
                    st.session_state["data"],
                    selected_airline,
                    selected_service_id,
                )

                save_data(st.session_state["data"])

                st.session_state["editing_id"] = None

                st.success("Seçili hizmet silindi.")

                st.session_state["view"] = "Hizmet Kartları"

                st.rerun()


if page == "Tüm Hizmetlerde Ara":
    st.subheader("Tüm Hizmetlerde Ara")

    st.info(
        "Bu bölüm genel arama içindir. Burada tüm havayolları birlikte aranır. "
        "Sadece tek havayolunu görmek için 'Hizmet Kartları' sayfasını kullan."
    )

    search_all = st.text_input(
        "Genel arama",
        placeholder="GPU, merdiven, süre, SVA...",
        key="global_search",
    )

    filter_airline = st.selectbox(
        "Havayolu filtresi",
        ["Tümü"] + AIRLINES,
        key="global_airline_filter",
    )

    filter_category = st.selectbox(
        "Kategori filtresi",
        ["Tümü"] + CATEGORIES,
        key="global_category_filter",
    )

    all_rows = []

    for code in AIRLINES:
        for row in services_for_airline(st.session_state["data"], code):
            all_rows.append(row)

    filtered_all = []

    for row in all_rows:
        text = " ".join(
            safe_text(value).lower()
            for value in row.values()
        )

        if search_all and search_all.lower() not in text:
            continue

        if filter_airline != "Tümü" and row.get("Havayolu") != filter_airline:
            continue

        if filter_category != "Tümü" and row.get("Ana Kategori") != filter_category:
            continue

        filtered_all.append(row)

    if not filtered_all:
        st.warning("Arama kriterine uygun hizmet bulunamadı.")

    for row in filtered_all:
        with st.container(border=True):
            st.subheader(
                row.get("Hizmet Adı", "İsimsiz Hizmet")
                + " — "
                + row.get("Havayolu", "")
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.write("**Kategori**")
                st.write(row.get("Ana Kategori", "-"))

            with c2:
                st.write("**IKARUS Başlığı**")
                st.write(row.get("IKARUS Konu Başlığı", "-"))

            with c3:
                st.write("**Zorunlu**")
                st.write(row.get("Zorunlu", "-"))

            st.write("**Giriş Kuralı**")
            st.write(row.get("Giriş Kuralı", "-"))


if page == "SCF Kontrol":
    st.subheader(selected_airline + " SCF Kapanış Kontrolü")

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

    if completed == len(CHECKLIST):
        st.success("Tüm SCF kontrolleri tamamlandı.")
    else:
        st.warning(
            "Eksik kontrol sayısı: "
            + str(len(CHECKLIST) - completed)
        )


if page == "Veri Yönetimi":
    st.subheader("Veri Yönetimi")

    st.warning(
        "Bu sürüm veriyi services.json dosyasına kaydeder. Streamlit Cloud yeniden "
        "kurulduğunda yerel JSON verisi kaybolabilir. Kalıcı çözüm için Supabase "
        "veya Google Sheets bağlantısı yapılmalıdır."
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
