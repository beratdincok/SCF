# SFC – SCF/IKARUS Rehberi | Streamlit başlangıç dosyası
from __future__ import annotations

import html
from pathlib import Path
from typing import Callable

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
AIRLINES_FILE = DATA_DIR / "airlines.csv"
SERVICES_FILE = DATA_DIR / "services.csv"

REQUIRED_SERVICE_COLUMNS = [
    "airline_code",
    "category",
    "service_name",
    "ikarus_section",
    "ikarus_field",
    "entry_rule",
    "unit",
    "required",
    "when_to_enter",
    "verification_source",
    "notes",
    "sort_order",
]

CATEGORY_ICONS = {
    "Uçuş Bilgileri": "🛫",
    "Yolcu Hizmetleri": "👥",
    "Ramp / Apron Hizmetleri": "🦺",
    "Uçak Hizmetleri": "✈️",
    "Yük Kontrol & Operasyon": "⚖️",
    "Kargo & Posta": "📦",
    "GSE / Ekipman": "🛠️",
    "Ekstra / Ad-hoc Hizmetler": "➕",
    "İmza & Kapanış": "✅",
}

DEFAULT_CATEGORIES = list(CATEGORY_ICONS.keys())

st.set_page_config(
    page_title="SFC | SCF–IKARUS Rehberi",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --sfc-navy: #081a2f;
            --sfc-blue: #0b66ff;
            --sfc-cyan: #19c6d4;
            --sfc-soft: #eef5ff;
            --sfc-border: rgba(15, 55, 95, 0.14);
        }
        .stApp {
            background:
                radial-gradient(circle at 88% 4%, rgba(25,198,212,.12), transparent 22rem),
                radial-gradient(circle at 18% 0%, rgba(11,102,255,.10), transparent 25rem),
                #f7f9fc;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #07182b 0%, #0a2440 100%);
            border-right: 1px solid rgba(255,255,255,.08);
        }
        [data-testid="stSidebar"] * { color: #f6fbff; }
        [data-testid="stSidebarNav"] span { font-weight: 600; }
        [data-testid="stSidebarNav"] a:hover { background: rgba(255,255,255,.08); }
        .block-container { max-width: 1480px; padding-top: 1.4rem; padding-bottom: 3rem; }
        .sfc-hero {
            padding: 2rem 2.2rem;
            border-radius: 24px;
            color: white;
            background: linear-gradient(125deg, #07182b 0%, #0b3a69 55%, #08788c 100%);
            box-shadow: 0 22px 55px rgba(8,26,47,.18);
            position: relative;
            overflow: hidden;
            margin-bottom: 1.2rem;
        }
        .sfc-hero:after {
            content: "";
            position: absolute;
            width: 280px; height: 280px;
            border-radius: 50%;
            right: -90px; top: -125px;
            background: rgba(255,255,255,.10);
        }
        .sfc-eyebrow { font-size: .78rem; letter-spacing: .14em; text-transform: uppercase; opacity: .8; font-weight: 700; }
        .sfc-title { font-size: clamp(2rem, 4vw, 3.8rem); line-height: 1.03; margin: .45rem 0 .6rem; font-weight: 850; }
        .sfc-subtitle { font-size: 1.05rem; max-width: 820px; opacity: .88; margin: 0; }
        .sfc-badge {
            display: inline-block; padding: .38rem .72rem; margin-top: 1rem; margin-right: .45rem;
            border-radius: 999px; background: rgba(255,255,255,.13); border: 1px solid rgba(255,255,255,.18);
            font-size: .82rem; font-weight: 650;
        }
        .sfc-card {
            background: rgba(255,255,255,.92);
            border: 1px solid var(--sfc-border);
            border-radius: 18px;
            padding: 1.15rem 1.2rem;
            box-shadow: 0 8px 28px rgba(12,39,69,.06);
            height: 100%;
        }
        .sfc-card h3 { margin: 0 0 .35rem; font-size: 1.05rem; color: #0b2542; }
        .sfc-card p { margin: 0; color: #53657a; font-size: .92rem; }
        .sfc-kpi {
            background: white; border: 1px solid var(--sfc-border); border-radius: 17px;
            padding: 1rem 1.05rem; box-shadow: 0 8px 25px rgba(12,39,69,.05);
        }
        .sfc-kpi-label { color: #65758a; font-size: .78rem; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; }
        .sfc-kpi-value { color: #09213d; font-size: 1.75rem; font-weight: 850; line-height: 1.1; margin-top: .25rem; }
        .sfc-section-title { font-size: 1.45rem; font-weight: 820; color: #09213d; margin: .65rem 0 .2rem; }
        .sfc-muted { color: #6c7b8f; }
        .sfc-service {
            border-left: 4px solid #0b66ff; background: #f8fbff; border-radius: 0 14px 14px 0;
            padding: .9rem 1rem; margin: .55rem 0;
        }
        .sfc-service-title { font-weight: 800; color: #0b2542; margin-bottom: .25rem; }
        .sfc-chip {
            display: inline-block; border-radius: 999px; padding: .2rem .55rem; margin: .15rem .25rem .1rem 0;
            background: #e9f2ff; color: #0a4cae; font-size: .75rem; font-weight: 700;
        }
        .sfc-empty {
            text-align: center; padding: 2.2rem 1.2rem; border-radius: 18px;
            border: 1px dashed #aabbd0; background: rgba(255,255,255,.65); color: #627287;
        }
        .sfc-warning {
            padding: 1rem 1.1rem; border-radius: 14px; background: #fff8e8;
            border: 1px solid #f0d79c; color: #705319;
        }
        div[data-testid="stDataFrame"] { border-radius: 16px; overflow: hidden; border: 1px solid var(--sfc-border); }
        div[data-testid="stTabs"] button { font-weight: 700; }
        .stButton > button, .stDownloadButton > button { border-radius: 12px; font-weight: 750; }
        footer { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_airlines() -> pd.DataFrame:
    df = pd.read_csv(AIRLINES_FILE, dtype=str).fillna("")
    return df


@st.cache_data(show_spinner=False)
def load_services() -> pd.DataFrame:
    try:
        df = pd.read_csv(SERVICES_FILE, dtype=str).fillna("")
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=REQUIRED_SERVICE_COLUMNS)
    for column in REQUIRED_SERVICE_COLUMNS:
        if column not in df.columns:
            df[column] = ""
    df["sort_order_num"] = pd.to_numeric(df["sort_order"], errors="coerce").fillna(9999)
    return df


def safe(value: object) -> str:
    return html.escape(str(value or ""))


def hero(title: str, subtitle: str, eyebrow: str = "SFC • SCF–IKARUS REHBERİ", badges: list[str] | None = None) -> None:
    badge_html = "".join(f'<span class="sfc-badge">{safe(item)}</span>' for item in (badges or []))
    st.markdown(
        f"""
        <div class="sfc-hero">
            <div class="sfc-eyebrow">{safe(eyebrow)}</div>
            <div class="sfc-title">{safe(title)}</div>
            <p class="sfc-subtitle">{safe(subtitle)}</p>
            <div>{badge_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi(label: str, value: str) -> None:
    st.markdown(
        f'<div class="sfc-kpi"><div class="sfc-kpi-label">{safe(label)}</div><div class="sfc-kpi-value">{safe(value)}</div></div>',
        unsafe_allow_html=True,
    )


def info_card(title: str, text: str) -> None:
    st.markdown(
        f'<div class="sfc-card"><h3>{safe(title)}</h3><p>{safe(text)}</p></div>',
        unsafe_allow_html=True,
    )


def render_service_record(row: pd.Series) -> None:
    required_text = "Zorunlu" if str(row.get("required", "")).strip().lower() in {"evet", "yes", "true", "1"} else "Duruma bağlı"
    chips = [
        row.get("ikarus_section", ""),
        row.get("ikarus_field", ""),
        required_text,
        row.get("unit", ""),
    ]
    chips_html = "".join(f'<span class="sfc-chip">{safe(c)}</span>' for c in chips if str(c).strip())
    detail_items = [
        ("Giriş kuralı", row.get("entry_rule", "")),
        ("Ne zaman girilir?", row.get("when_to_enter", "")),
        ("Doğrulama kaynağı", row.get("verification_source", "")),
        ("Not", row.get("notes", "")),
    ]
    details = "".join(
        f'<div style="margin-top:.35rem"><strong>{safe(label)}:</strong> {safe(value)}</div>'
        for label, value in detail_items
        if str(value).strip()
    )
    st.markdown(
        f"""
        <div class="sfc-service">
            <div class="sfc-service-title">{safe(row.get('service_name', ''))}</div>
            <div>{chips_html}</div>
            <div style="color:#4f6277;font-size:.88rem">{details}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def airline_records(code: str) -> pd.DataFrame:
    services = load_services()
    records = services[services["airline_code"].str.upper() == code.upper()].copy()
    return records.sort_values(["sort_order_num", "category", "service_name"], kind="stable")


def render_home() -> None:
    airlines = load_airlines()
    services = load_services()
    active_codes = services.loc[services["service_name"].str.strip() != "", "airline_code"].str.upper().nunique()

    hero(
        "Operasyon bilgisi, tek merkezde.",
        "Her havayolu için IKARUS'a girilecek hizmetleri, doğru konu başlığını, giriş kuralını ve kontrol adımlarını standartlaştıran dijital SCF rehberi.",
        badges=["Havayolu bazlı", "Mobil uyumlu", "Sunuma hazır", "GitHub + Streamlit"],
    )

    cols = st.columns(4)
    with cols[0]:
        kpi("Havayolu", str(len(airlines)))
    with cols[1]:
        kpi("İçeriği girilmiş", str(active_codes))
    with cols[2]:
        kpi("Hizmet kaydı", str((services["service_name"].str.strip() != "").sum()))
    with cols[3]:
        kpi("Konu başlığı", str(services.loc[services["category"].str.strip() != "", "category"].nunique()))

    st.markdown('<div class="sfc-section-title">Hızlı arama</div>', unsafe_allow_html=True)
    query = st.text_input(
        "Hizmet, IKARUS başlığı, alan veya not içinde ara",
        placeholder="Örn. GPU, passenger bus, signature, quantity...",
        label_visibility="collapsed",
    )
    if query.strip():
        haystack = services[REQUIRED_SERVICE_COLUMNS[:-1]].astype(str).agg(" ".join, axis=1)
        result = services[haystack.str.contains(query.strip(), case=False, na=False)]
        if result.empty:
            st.info("Bu ifadeyle eşleşen bir hizmet kaydı bulunamadı.")
        else:
            for _, row in result.head(30).iterrows():
                st.caption(f"{row['airline_code']} • {row['category']}")
                render_service_record(row)

    st.markdown('<div class="sfc-section-title">Sistem nasıl çalışır?</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        info_card("1 • Havayolunu seç", "Sol menüden ilgili üçlü kodu aç. Her havayolu kendi bağımsız sayfasında tutulur.")
    with c2:
        info_card("2 • Hizmeti bul", "Hizmeti kategori, IKARUS bölümü veya arama kutusu üzerinden hızlıca görüntüle.")
    with c3:
        info_card("3 • Giriş kuralını uygula", "Alan, birim, zorunluluk, zamanlama ve doğrulama kaynağını aynı ekranda kontrol et.")
    with c4:
        info_card("4 • SCF'yi kapat", "Kontrol listesini tamamla; eksik, mükerrer veya yanlış başlıkta kayıt bırakma.")

    st.markdown('<div class="sfc-section-title">Havayolu kapsamı</div>', unsafe_allow_html=True)
    groups = airlines.groupby("nav_group", sort=False)
    for group_name, group_df in groups:
        with st.expander(f"{group_name}  •  {len(group_df)} havayolu", expanded=False):
            codes = "  ·  ".join(group_df["code"].tolist())
            st.write(codes)

    st.markdown(
        '<div class="sfc-warning"><strong>Gizlilik:</strong> Sözleşme fiyatları, kişisel veriler veya şirket içi gizli belgeler kamuya açık bir depoda yayınlanmamalıdır. Sunum sürümünde yalnızca yetkilendirilmiş operasyon bilgileri kullanılmalıdır.</div>',
        unsafe_allow_html=True,
    )


def render_airline_page(code: str) -> None:
    airlines = load_airlines()
    match = airlines[airlines["code"].str.upper() == code.upper()]
    if match.empty:
        st.error("Havayolu kaydı bulunamadı.")
        return

    airline = match.iloc[0]
    records = airline_records(code)
    populated = records[records["service_name"].str.strip() != ""]
    categories_used = populated["category"].nunique() if not populated.empty else 0

    hero(
        code,
        airline.get("display_name", code) or code,
        eyebrow="HAVAYOLU OPERASYON SAYFASI",
        badges=[airline.get("status", "Taslak"), f"{len(populated)} hizmet", f"{categories_used} kategori"],
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi("Hizmet kaydı", str(len(populated)))
    with c2:
        kpi("Aktif kategori", str(categories_used))
    with c3:
        mandatory = populated[populated["required"].str.lower().isin(["evet", "yes", "true", "1"])]
        kpi("Zorunlu hizmet", str(len(mandatory)))

    tab_map, tab_flow, tab_check, tab_notes = st.tabs(
        ["Hizmet Haritası", "İşlem Akışı", "Kontrol Listesi", "Havayolu Notları"]
    )

    with tab_map:
        if populated.empty:
            st.markdown(
                """
                <div class="sfc-empty">
                    <div style="font-size:2rem">🗂️</div>
                    <strong>Bu havayolu için hizmet içeriği henüz eklenmedi.</strong><br>
                    İçerik Şablonu sayfasındaki CSV yapısına göre kayıt eklediğinde hizmetler burada otomatik görünecek.
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('<div class="sfc-section-title">Hazır konu başlıkları</div>', unsafe_allow_html=True)
            cols = st.columns(3)
            for index, category in enumerate(DEFAULT_CATEGORIES):
                with cols[index % 3]:
                    info_card(f"{CATEGORY_ICONS.get(category, '•')} {category}", "Hizmetler eklendiğinde bu başlık altında listelenecek.")
        else:
            category_options = ["Tümü"] + list(dict.fromkeys(populated["category"].tolist()))
            selected_category = st.selectbox("Kategori filtresi", category_options)
            visible = populated if selected_category == "Tümü" else populated[populated["category"] == selected_category]
            for category, category_df in visible.groupby("category", sort=False):
                icon = CATEGORY_ICONS.get(category, "📌")
                st.markdown(f'<div class="sfc-section-title">{icon} {safe(category)}</div>', unsafe_allow_html=True)
                for _, row in category_df.iterrows():
                    render_service_record(row)

    with tab_flow:
        st.markdown('<div class="sfc-section-title">Standart kullanım akışı</div>', unsafe_allow_html=True)
        steps = [
            ("01", "Doğru uçuşu aç", "Uçuş numarası, tarih, yön, tescil ve uçak tipini doğrula."),
            ("02", "Hizmeti eşleştir", "Verilen hizmeti bu sayfadaki doğru IKARUS konu başlığı ve alanıyla eşleştir."),
            ("03", "Değeri gir", "Adet, süre, saat veya durum bilgisini belirtilen birim ve kurala göre işle."),
            ("04", "Kaynağı doğrula", "Operasyon kaydı, ekipman formu, gerçek zaman veya yetkili bilgisiyle kontrol et."),
            ("05", "SCF kontrolünü tamamla", "Eksik, mükerrer ve yanlış başlıkta hizmet olmadığından emin ol."),
            ("06", "İmza ve kapanış", "Havayolu özel kuralına göre temsilci onayı/imzası ve kapanış işlemini tamamla."),
        ]
        for number, title, text in steps:
            st.markdown(
                f'<div class="sfc-service"><div class="sfc-service-title">{number} • {safe(title)}</div><div style="color:#53657a">{safe(text)}</div></div>',
                unsafe_allow_html=True,
            )
        st.info("Bu akış genel şablondur. Havayolu özel talimatları hizmet kayıtları ve notlar bölümünde belirtilmelidir.")

    with tab_check:
        st.markdown('<div class="sfc-section-title">SCF kapanış kontrolü</div>', unsafe_allow_html=True)
        checklist = [
            "Doğru havayolu ve uçuş seçildi.",
            "Uçuş tarihi, yönü, tescili ve uçak tipi kontrol edildi.",
            "Gerçekte verilen bütün hizmetler doğru konu başlığına girildi.",
            "Verilmeyen veya iptal edilen hizmetler yanlışlıkla eklenmedi.",
            "Adet, saat, süre ve birimler doğrulandı.",
            "Mükerrer hizmet kaydı bulunmuyor.",
            "Ekstra/ad-hoc hizmetlerde gerekli açıklama ve kanıt bilgisi mevcut.",
            "Havayolu özel notları kontrol edildi.",
            "İmza/onay ve kapanış adımları tamamlandı.",
        ]
        selected = [st.checkbox(item, key=f"{code}_check_{i}") for i, item in enumerate(checklist)]
        progress = sum(selected) / len(checklist)
        st.progress(progress)
        if progress == 1:
            st.success("Kontrol listesi tamamlandı.")
        else:
            st.caption(f"{sum(selected)}/{len(checklist)} kontrol tamamlandı.")

    with tab_notes:
        notes = str(airline.get("notes", "")).strip()
        if notes:
            st.markdown(notes)
        else:
            st.markdown(
                '<div class="sfc-empty">Bu havayolu için özel operasyon notu henüz eklenmedi.</div>',
                unsafe_allow_html=True,
            )
        st.caption(f"İçerik durumu: {airline.get('status', 'Taslak')} • Son güncelleme: {airline.get('last_updated', '-')}")


def render_all_services() -> None:
    services = load_services()
    populated = services[services["service_name"].str.strip() != ""].copy()
    hero(
        "Tüm Hizmetler",
        "Havayollarındaki hizmet kayıtlarını tek tabloda filtrele, karşılaştır ve tutarlılık kontrolü yap.",
        badges=["Filtrelenebilir", "Karşılaştırmalı görünüm", "CSV tabanlı"],
    )

    if populated.empty:
        st.markdown('<div class="sfc-empty">Henüz hizmet kaydı bulunmuyor. İçerik Şablonu sayfasından veri formatını indirebilirsin.</div>', unsafe_allow_html=True)
        return

    c1, c2, c3 = st.columns(3)
    with c1:
        selected_airlines = st.multiselect("Havayolu", sorted(populated["airline_code"].unique()))
    with c2:
        selected_categories = st.multiselect("Kategori", sorted(populated["category"].unique()))
    with c3:
        required_only = st.toggle("Yalnızca zorunlu hizmetler")

    filtered = populated.copy()
    if selected_airlines:
        filtered = filtered[filtered["airline_code"].isin(selected_airlines)]
    if selected_categories:
        filtered = filtered[filtered["category"].isin(selected_categories)]
    if required_only:
        filtered = filtered[filtered["required"].str.lower().isin(["evet", "yes", "true", "1"])]

    shown_columns = [
        "airline_code", "category", "service_name", "ikarus_section", "ikarus_field",
        "entry_rule", "unit", "required", "when_to_enter", "verification_source", "notes"
    ]
    st.dataframe(filtered[shown_columns], use_container_width=True, hide_index=True)
    st.download_button(
        "Filtrelenmiş listeyi indir",
        data=filtered[REQUIRED_SERVICE_COLUMNS].to_csv(index=False).encode("utf-8-sig"),
        file_name="sfc_filtrelenmis_hizmetler.csv",
        mime="text/csv",
    )


def render_demo() -> None:
    hero(
        "Sunum Modu",
        "Gerçek operasyon verisi girmeden, dolu bir havayolu sayfasının nasıl görüneceğini gösteren örnek ekran.",
        badges=["Demo içerik", "Operasyonel kullanım için değildir"],
    )
    st.warning("Aşağıdaki kayıtlar yalnızca arayüz sunumu içindir; gerçek IKARUS başlığı veya operasyon talimatı değildir.")

    demo = pd.DataFrame(
        [
            {
                "service_name": "Örnek Hizmet A",
                "ikarus_section": "Örnek Konu Başlığı",
                "ikarus_field": "Örnek Alan",
                "entry_rule": "Gerçekleşen operasyon değerini yetkili kaynağa göre gir.",
                "unit": "Adet",
                "required": "Evet",
                "when_to_enter": "Hizmet tamamlandıktan sonra",
                "verification_source": "Operasyon kaydı",
                "notes": "Sunum amaçlı örnek kayıttır.",
                "category": "Ramp / Apron Hizmetleri",
            },
            {
                "service_name": "Örnek Hizmet B",
                "ikarus_section": "Örnek Ek Hizmetler",
                "ikarus_field": "Süre",
                "entry_rule": "Başlangıç ve bitiş zamanına göre gerçekleşen süreyi gir.",
                "unit": "Dakika",
                "required": "Hayır",
                "when_to_enter": "Hizmet talep edilip gerçekleştiğinde",
                "verification_source": "Ekipman/operasyon kaydı",
                "notes": "Sunum amaçlı örnek kayıttır.",
                "category": "Ekstra / Ad-hoc Hizmetler",
            },
        ]
    )
    for category, category_df in demo.groupby("category", sort=False):
        st.markdown(f'<div class="sfc-section-title">{CATEGORY_ICONS.get(category, "📌")} {safe(category)}</div>', unsafe_allow_html=True)
        for _, row in category_df.iterrows():
            render_service_record(row)

    c1, c2, c3 = st.columns(3)
    with c1:
        info_card("Hızlı erişim", "Her havayolu sol menüde ayrı sayfa olarak açılır.")
    with c2:
        info_card("Standart görünüm", "Tüm hizmetlerde aynı alan ve kontrol mantığı kullanılır.")
    with c3:
        info_card("Kolay güncelleme", "CSV'de yapılan değişiklik GitHub'a gönderildiğinde site yenilenir.")


def render_content_template() -> None:
    hero(
        "İçerik Şablonu",
        "Hizmetleri hangi havayoluna, hangi IKARUS konu başlığına ve hangi giriş kuralına bağlayacağını belirleyen veri yapısı.",
        badges=["Excel ile düzenlenebilir", "UTF-8 CSV", "Kod değişikliği gerekmez"],
    )

    st.markdown('<div class="sfc-section-title">Sütun açıklamaları</div>', unsafe_allow_html=True)
    definitions = pd.DataFrame(
        [
            ("airline_code", "Havayolunun üçlü kodu", "SVA"),
            ("category", "SFC içinde gösterilecek ana konu başlığı", "Ramp / Apron Hizmetleri"),
            ("service_name", "Personelin arayacağı hizmet adı", "[Gerçek hizmet adı]"),
            ("ikarus_section", "IKARUS içindeki ana bölüm/konu başlığı", "[Gerçek IKARUS başlığı]"),
            ("ikarus_field", "Bilginin girileceği alan", "[Alan adı]"),
            ("entry_rule", "Nasıl ve hangi değerle girileceği", "Gerçekleşen adedi gir"),
            ("unit", "Adet, dakika, saat, kg vb.", "Adet"),
            ("required", "Evet/Hayır", "Evet"),
            ("when_to_enter", "Hangi durumda kayıt yapılacağı", "Hizmet gerçekleştiğinde"),
            ("verification_source", "Değerin hangi kaynaktan doğrulanacağı", "Operasyon kaydı"),
            ("notes", "Havayolu özel notu veya istisna", "Temsilci onayı gerekir"),
            ("sort_order", "Sayfadaki sıralama", "10"),
        ],
        columns=["Sütun", "Açıklama", "Örnek"],
    )
    st.dataframe(definitions, use_container_width=True, hide_index=True)

    template = pd.DataFrame(columns=REQUIRED_SERVICE_COLUMNS)
    st.download_button(
        "Boş hizmet şablonunu indir",
        data=template.to_csv(index=False).encode("utf-8-sig"),
        file_name="services_template.csv",
        mime="text/csv",
    )

    st.markdown('<div class="sfc-section-title">CSV önizleme ve doğrulama</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Doldurduğun services.csv dosyasını yükle", type=["csv"])
    if uploaded is not None:
        try:
            preview = pd.read_csv(uploaded, dtype=str).fillna("")
            missing = [c for c in REQUIRED_SERVICE_COLUMNS if c not in preview.columns]
            unknown_codes = sorted(set(preview.get("airline_code", pd.Series(dtype=str)).str.upper()) - set(load_airlines()["code"].str.upper()))
            if missing:
                st.error("Eksik sütunlar: " + ", ".join(missing))
            elif unknown_codes:
                st.error("airlines.csv içinde bulunmayan kodlar: " + ", ".join(unknown_codes))
            else:
                st.success(f"Dosya yapısı uygun. {len(preview)} kayıt bulundu.")
                st.dataframe(preview, use_container_width=True, hide_index=True)
                st.download_button(
                    "Kontrol edilen dosyayı indir",
                    data=preview[REQUIRED_SERVICE_COLUMNS].to_csv(index=False).encode("utf-8-sig"),
                    file_name="services.csv",
                    mime="text/csv",
                )
        except Exception as exc:
            st.error(f"Dosya okunamadı: {exc}")

    st.info("Kalıcı güncelleme için indirilen services.csv dosyasını projenin data klasöründeki dosyayla değiştirip GitHub'a commit et.")


def render_about() -> None:
    hero(
        "Sistem Hakkında",
        "SFC, personelin havayolu bazlı SCF–IKARUS girişlerini standart, aranabilir ve sunuma uygun bir yapıda görüntülemesi için tasarlanmıştır.",
        badges=["Sürüm 1.0", "Taslak yapı", "Operasyon onayı gerektirir"],
    )
    st.markdown(
        """
        ### Amaç
        - Her havayoluna ayrı bir operasyon sayfası sağlamak.
        - Hizmeti doğru IKARUS konu başlığı ve alanıyla eşleştirmek.
        - Giriş birimi, zorunluluk, zamanlama ve doğrulama kaynağını göstermek.
        - SCF kapanışında standart kontrol listesi sunmak.

        ### İçerik yönetimi
        Uygulamanın gerçek operasyon bilgileri `data/services.csv` dosyasında tutulur. Böylece Python koduna dokunmadan Excel veya Google Sheets üzerinden içerik hazırlanabilir.

        ### Önemli sınır
        Bu sistem karar veren bir faturalama motoru değildir. Havayolu sözleşmesi, güncel istasyon talimatı, yetkili birim ve operasyonel prosedür her zaman esas alınmalıdır.
        """
    )


def build_airline_page(code: str) -> Callable[[], None]:
    def page() -> None:
        render_airline_page(code)
    page.__name__ = f"airline_{code.lower().replace('-', '_')}"
    return page


apply_styles()

# Sidebar brand is shown above the generated navigation.
st.sidebar.markdown(
    """
    <div style="padding:.4rem .35rem 1rem">
        <div style="font-size:1.7rem;font-weight:900;letter-spacing:.08em">SFC</div>
        <div style="font-size:.78rem;opacity:.72">SCF–IKARUS OPERASYON REHBERİ</div>
    </div>
    """,
    unsafe_allow_html=True,
)

home_page = st.Page(render_home, title="Ana Sayfa", icon="🏠", default=True, url_path="home")
all_services_page = st.Page(render_all_services, title="Tüm Hizmetler", icon="🔎", url_path="all-services")
demo_page = st.Page(render_demo, title="Sunum Modu", icon="🎤", url_path="demo")
template_page = st.Page(render_content_template, title="İçerik Şablonu", icon="🧩", url_path="content-template")
about_page = st.Page(render_about, title="Sistem Hakkında", icon="ℹ️", url_path="about")

navigation: dict[str, list[st.Page]] = {
    "SFC": [home_page, all_services_page, demo_page, template_page, about_page]
}

airlines_df = load_airlines()
for group_name, group_df in airlines_df.groupby("nav_group", sort=False):
    navigation[group_name] = [
        st.Page(
            build_airline_page(row["code"]),
            title=row["code"],
            icon="✈️",
            url_path=f"airline-{row['code'].lower()}",
        )
        for _, row in group_df.iterrows()
    ]

selected_page = st.navigation(navigation)
st.sidebar.divider()
st.sidebar.caption("SFC v1.0 • Sunum ve rehber altyapısı")
selected_page.run()
