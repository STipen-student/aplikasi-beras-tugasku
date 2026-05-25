"""
================================================================================
APLIKASI PEMBELAJARAN INTERAKTIF
Persamaan Diferensial Orde 1 dalam Ekonomi:
Laju Pertumbuhan Harga Beras dengan Model Dinamis (Permintaan dan Penawaran)
================================================================================
Framework : Streamlit
Metode    : Euler Numerik
Bahasa    : Python 3
================================================================================
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PD Orde 1 — Dinamika Harga Beras",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS KUSTOM — tampilan elegan bertema akademik
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ─── Import Google Fonts ─── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─── Variabel Tema ─── */
:root {
    --hijau-tua   : #1a472a;
    --hijau-muda  : #2d6a4f;
    --emas        : #c9a84c;
    --krem        : #fdf6e3;
    --abu-gelap   : #2c2c2c;
    --abu-terang  : #f5f5f0;
    --putih       : #ffffff;
    --aksen-biru  : #1b4f72;
}

/* ─── Latar Belakang Utama ─── */
.stApp {
    background: linear-gradient(135deg, #f0f4e8 0%, #fdf6e3 50%, #e8f0e8 100%);
    font-family: 'Source Sans 3', sans-serif;
}

/* ─── Header Utama ─── */
.header-utama {
    background: linear-gradient(135deg, var(--hijau-tua) 0%, var(--hijau-muda) 60%, #40916c 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(26,71,42,0.25);
}
.header-utama::before {
    content: "🌾";
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 6rem;
    opacity: 0.15;
}
.header-utama h1 {
    font-family: 'Playfair Display', serif;
    color: #ffffff;
    font-size: 2rem;
    margin: 0 0 0.4rem;
    line-height: 1.3;
}
.header-utama p {
    color: rgba(255,255,255,0.85);
    font-size: 1rem;
    margin: 0;
    font-weight: 300;
}
.badge-menu {
    display: inline-block;
    background: var(--emas);
    color: var(--hijau-tua);
    font-weight: 600;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin-bottom: 0.8rem;
}

/* ─── Kartu Konten ─── */
.kartu {
    background: var(--putih);
    border-radius: 12px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06);
    border-left: 4px solid var(--hijau-muda);
}
.kartu-emas {
    border-left-color: var(--emas);
    background: linear-gradient(135deg, #fffdf5 0%, #fff9e6 100%);
}
.kartu-biru {
    border-left-color: var(--aksen-biru);
    background: linear-gradient(135deg, #f0f4fb 0%, #e8f0f8 100%);
}
.kartu h3 {
    font-family: 'Playfair Display', serif;
    color: var(--hijau-tua);
    margin-top: 0;
    font-size: 1.2rem;
}

/* ─── Judul Seksi ─── */
.judul-seksi {
    font-family: 'Playfair Display', serif;
    color: var(--hijau-tua);
    font-size: 1.5rem;
    border-bottom: 2px solid var(--emas);
    padding-bottom: 0.4rem;
    margin-bottom: 1.2rem;
}

/* ─── Kotak Rumus ─── */
.kotak-rumus {
    background: #1e1e2e;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
    border: 1px solid rgba(201,168,76,0.3);
    font-family: 'JetBrains Mono', monospace;
}

/* ─── Kotak Hasil Numerik ─── */
.hasil-numerik {
    background: linear-gradient(135deg, var(--hijau-tua), var(--hijau-muda));
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    color: white;
    text-align: center;
    font-size: 1.4rem;
    font-family: 'Playfair Display', serif;
    box-shadow: 0 4px 16px rgba(26,71,42,0.3);
}
.hasil-numerik span {
    font-size: 0.85rem;
    font-family: 'Source Sans 3', sans-serif;
    opacity: 0.85;
    display: block;
    margin-bottom: 0.3rem;
}

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--hijau-tua) 0%, #163d21 100%);
}
[data-testid="stSidebar"] * {
    color: #e0f0e0 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
    color: rgba(255,255,255,0.85) !important;
    font-size: 0.85rem !important;
}

/* ─── Tabel DataFrame ─── */
[data-testid="stDataFrame"] {
    border-radius: 8px;
    overflow: hidden;
}

/* ─── Info Box ─── */
.info-box {
    background: linear-gradient(135deg, #e8f4fd, #d6eaf8);
    border: 1px solid #aed6f1;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    color: var(--aksen-biru);
    font-size: 0.92rem;
}
.info-box strong { color: var(--aksen-biru); }

/* ─── Definisi Term ─── */
.term-baris {
    display: flex;
    gap: 1rem;
    padding: 0.5rem 0;
    border-bottom: 1px dashed #d0d0c0;
    align-items: flex-start;
}
.term-label {
    font-family: 'JetBrains Mono', monospace;
    color: var(--emas);
    background: var(--hijau-tua);
    padding: 0.1rem 0.5rem;
    border-radius: 4px;
    font-size: 0.85rem;
    min-width: 50px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — Navigasi & Parameter Input
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌾 Navigasi Menu")
    st.markdown("---")

    menu = st.selectbox(
        "Pilih Menu:",
        options=[
            "📚 Materi & Teori",
            "📐 Representasi Model Matematis",
            "🔢 Simulasi & Solusi Numerik",
            "📊 Grafik Representasi Model",
        ],
    )

    st.markdown("---")
    st.markdown("### ⚙️ Parameter Simulasi")
    st.markdown("*Parameter ini digunakan pada menu Simulasi & Grafik.*")

    # ── Input Parameter ──
    P0 = st.slider(
        "💰 Harga Awal Beras P₀ (Rp/kg)",
        min_value=5000, max_value=25000, value=10000, step=500,
        help="Harga beras pada saat t=0 (kondisi awal)"
    )
    st.markdown("**Fungsi Permintaan D(P) = a − bP**")
    a = st.slider("a — Konstanta Permintaan", 100.0, 2000.0, 800.0, 50.0,
                  help="Permintaan dasar saat harga nol")
    b = st.slider("b — Koefisien Harga Permintaan", 0.01, 0.20, 0.05, 0.005,
                  help="Sensitivitas permintaan terhadap perubahan harga")

    st.markdown("**Fungsi Penawaran S(P) = −c + dP**")
    c = st.slider("c — Konstanta Penawaran", 100.0, 2000.0, 400.0, 50.0,
                  help="Biaya produksi / penawaran minimum")
    d = st.slider("d — Koefisien Harga Penawaran", 0.01, 0.20, 0.03, 0.005,
                  help="Sensitivitas penawaran terhadap perubahan harga")

    st.markdown("**Parameter Dinamika Pasar**")
    k = st.slider("k — Konstanta Kecepatan Penyesuaian", 0.001, 0.10, 0.02, 0.001,
                  help="Seberapa cepat harga bereaksi terhadap kelebihan permintaan")
    t_max = st.slider("⏱ Rentang Waktu Simulasi (hari)", 10, 365, 120, 5)
    dt = st.slider("Δt — Langkah Waktu (hari)", 0.1, 5.0, 1.0, 0.1)

    # ── Hitung Nilai Keseimbangan ──
    Pe = (a + c) / (b + d)
    st.markdown("---")
    st.markdown("### 📌 Harga Keseimbangan")
    st.markdown(f"""
    <div style='background:rgba(201,168,76,0.2);border-radius:8px;
                padding:0.8rem;text-align:center;border:1px solid rgba(201,168,76,0.5)'>
        <span style='font-size:0.8rem;opacity:0.8'>Pe = (a+c)/(b+d)</span><br>
        <strong style='font-size:1.4rem;color:#c9a84c'>Rp {Pe:,.0f}/kg</strong>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# FUNGSI UTILITAS — Metode Euler
# ─────────────────────────────────────────────────────────────────────────────
def hitung_euler(P0, a, b, c, d, k, t_max, dt):
    """
    Menyelesaikan PD Orde 1: dP/dt = k*(a+c) - k*(b+d)*P
    menggunakan Metode Euler secara numerik.

    Parameter:
        P0    : Harga awal (kondisi awal)
        a,b   : Parameter fungsi permintaan D(P) = a - b*P
        c,d   : Parameter fungsi penawaran S(P) = -c + d*P
        k     : Konstanta kecepatan penyesuaian pasar
        t_max : Batas waktu simulasi
        dt    : Langkah waktu

    Mengembalikan:
        DataFrame berisi kolom Waktu, Harga Numerik, Harga Keseimbangan
    """
    Pe_val = (a + c) / (b + d)          # Harga keseimbangan (equilibrium)
    n_langkah = int(t_max / dt) + 1      # Jumlah total langkah

    waktu_list   = []
    harga_list   = []
    Pe_list      = []

    P = float(P0)   # Harga awal
    t = 0.0         # Waktu awal

    for _ in range(n_langkah):
        waktu_list.append(round(t, 4))
        harga_list.append(round(P, 4))
        Pe_list.append(round(Pe_val, 4))

        # Turunan dP/dt berdasarkan model: dP/dt = k*(D(P)-S(P))
        # = k*((a-bP) - (-c+dP))
        # = k*(a+c) - k*(b+d)*P
        dP_dt = k * (a + c) - k * (b + d) * P

        # Iterasi Euler: P(t+dt) = P(t) + dP/dt * dt
        P = P + dP_dt * dt
        t = t + dt

    df = pd.DataFrame({
        "Waktu t (hari)": waktu_list,
        "Harga Numerik P(t) (Rp/kg)": harga_list,
        "Harga Keseimbangan Pe (Rp/kg)": Pe_list,
    })
    return df, Pe_val


# ─────────────────────────────────────────────────────────────────────────────
# MENU 1 — MATERI & TEORI
# ─────────────────────────────────────────────────────────────────────────────
if menu == "📚 Materi & Teori":

    st.markdown("""
    <div class="header-utama">
        <div class="badge-menu">Menu 1 — Materi & Teori</div>
        <h1>Persamaan Diferensial Orde 1<br>dalam Ekonomi</h1>
        <p>Model Dinamis Harga Beras: Interaksi Permintaan dan Penawaran</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Bagian A: Konsep Dasar PD Orde 1 ──
    st.markdown('<p class="judul-seksi">A. Konsep Dasar Persamaan Diferensial Orde 1</p>',
                unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        <div class="kartu">
            <h3>Apa itu Persamaan Diferensial?</h3>
            <p>
            <strong>Persamaan Diferensial (PD)</strong> adalah persamaan matematis yang 
            menghubungkan suatu fungsi dengan turunannya. PD digunakan untuk memodelkan 
            fenomena yang berubah secara kontinu terhadap waktu atau variabel lainnya.
            </p>
            <p>
            <strong>PD Orde 1</strong> adalah persamaan diferensial yang hanya melibatkan 
            turunan pertama dari fungsi yang dicari. Bentuk umumnya adalah:
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.latex(r"\frac{dy}{dt} = f(t,\, y)")

        st.markdown("""
        <div class="kartu">
            <h3>Komponen Utama PD Orde 1</h3>
            <div class="term-baris">
                <span class="term-label">y(t)</span>
                <span>Fungsi yang tidak diketahui (variabel dependen terhadap waktu)</span>
            </div>
            <div class="term-baris">
                <span class="term-label">dy/dt</span>
                <span>Laju perubahan fungsi y terhadap waktu t (turunan pertama)</span>
            </div>
            <div class="term-baris">
                <span class="term-label">f(t,y)</span>
                <span>Fungsi yang mendeskripsikan dinamika sistem</span>
            </div>
            <div class="term-baris">
                <span class="term-label">y(0)=y₀</span>
                <span>Kondisi awal: nilai fungsi pada saat t = 0</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="kartu kartu-emas">
            <h3>🎯 PD Orde 1 Linear</h3>
            <p>Bentuk standar PD Orde 1 Linear:</p>
        </div>
        """, unsafe_allow_html=True)

        st.latex(r"\frac{dy}{dt} + P(t)\,y = Q(t)")

        st.markdown("""
        <div class="kartu kartu-emas">
            <h3>📌 Solusi Umum</h3>
            <p>Diselesaikan dengan <em>Faktor Integrasi</em>:</p>
        </div>
        """, unsafe_allow_html=True)

        st.latex(r"\mu(t) = e^{\int P(t)\,dt}")
        st.latex(r"y = \frac{1}{\mu}\int \mu\, Q(t)\, dt + C")

        st.markdown("""
        <div class="info-box">
            <strong>💡 Catatan:</strong> Konstanta <em>C</em> ditentukan dari kondisi awal 
            <em>y(0) = y₀</em>, sehingga solusi menjadi <strong>unik dan spesifik</strong> 
            untuk setiap permasalahan.
        </div>
        """, unsafe_allow_html=True)

    # ── Bagian B: Latar Belakang Model Harga Beras ──
    st.markdown('<p class="judul-seksi">B. Pemodelan Harga Beras di Pasar</p>',
                unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="kartu">
            <h3>🌾 Latar Belakang</h3>
            <p>
            Beras merupakan komoditas pangan strategis di Indonesia. Harga beras di pasar 
            tidak bersifat statis, melainkan <strong>berfluktuasi secara dinamis</strong> 
            dipengaruhi oleh berbagai faktor ekonomi.
            </p>
            <p>
            Untuk memahami pergerakan harga secara ilmiah, kita dapat memodelkan dinamika 
            harga menggunakan <strong>Persamaan Diferensial Orde 1</strong>, yang 
            menggabungkan teori permintaan dan penawaran dengan konsep laju perubahan.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="kartu kartu-biru">
            <h3>⚖️ Hukum Permintaan & Penawaran</h3>
            <ul>
                <li><strong>Hukum Permintaan:</strong> Semakin tinggi harga, semakin 
                rendah jumlah yang diminta konsumen.</li>
                <li><strong>Hukum Penawaran:</strong> Semakin tinggi harga, semakin 
                banyak jumlah yang ditawarkan produsen.</li>
                <li><strong>Harga Keseimbangan:</strong> Titik di mana permintaan dan 
                penawaran bertemu (excess demand = 0).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ── Bagian C: Asumsi Model ──
    st.markdown('<p class="judul-seksi">C. Asumsi Dasar Model</p>', unsafe_allow_html=True)

    asumsi_cols = st.columns(3)
    asumsi_data = [
        ("🏪", "Pasar Kompetitif", "Harga terbentuk melalui mekanisme pasar bebas tanpa intervensi eksternal."),
        ("📈", "Penyesuaian Bertahap", "Harga berubah secara bertahap sebanding dengan kelebihan permintaan (excess demand)."),
        ("🔄", "Konvergensi", "Dalam jangka panjang, harga cenderung menuju titik keseimbangan (equilibrium)."),
    ]
    for col, (ikon, judul, isi) in zip(asumsi_cols, asumsi_data):
        with col:
            st.markdown(f"""
            <div class="kartu" style="text-align:center">
                <div style="font-size:2.5rem">{ikon}</div>
                <h3>{judul}</h3>
                <p style="font-size:0.9rem">{isi}</p>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MENU 2 — REPRESENTASI MODEL MATEMATIS
# ─────────────────────────────────────────────────────────────────────────────
elif menu == "📐 Representasi Model Matematis":

    st.markdown("""
    <div class="header-utama">
        <div class="badge-menu">Menu 2 — Representasi Model Matematis</div>
        <h1>Penurunan Rumus Matematika</h1>
        <p>Dari Konsep Ekonomi ke Persamaan Diferensial Orde 1 Linear</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Langkah 1: Fungsi Permintaan ──
    st.markdown('<p class="judul-seksi">Langkah 1 — Fungsi Permintaan D(P)</p>',
                unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class="kartu">
            <h3>Definisi Fungsi Permintaan</h3>
            <p>Fungsi permintaan menggambarkan jumlah beras yang ingin dibeli konsumen 
            pada berbagai tingkat harga. Sesuai hukum permintaan, fungsi ini bersifat 
            <strong>menurun terhadap harga</strong>.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="kartu kartu-emas">
            <h3>Keterangan Parameter</h3>
            <div class="term-baris">
                <span class="term-label">a > 0</span>
                <span>Permintaan dasar (saat harga = 0)</span>
            </div>
            <div class="term-baris">
                <span class="term-label">b > 0</span>
                <span>Kepekaan permintaan terhadap harga</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.latex(r"D(P) = a - bP \quad (a,\, b > 0)")
    st.markdown("""
    <div class="info-box">
        Interpretasi: Saat harga <em>P</em> naik sebesar 1 satuan, permintaan turun sebesar <em>b</em> satuan.
    </div>
    """, unsafe_allow_html=True)

    # ── Langkah 2: Fungsi Penawaran ──
    st.markdown('<p class="judul-seksi">Langkah 2 — Fungsi Penawaran S(P)</p>',
                unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1])
    with col3:
        st.markdown("""
        <div class="kartu">
            <h3>Definisi Fungsi Penawaran</h3>
            <p>Fungsi penawaran menggambarkan jumlah beras yang bersedia diproduksi dan 
            dijual produsen pada berbagai tingkat harga. Sesuai hukum penawaran, fungsi 
            ini bersifat <strong>meningkat terhadap harga</strong>.</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="kartu kartu-emas">
            <h3>Keterangan Parameter</h3>
            <div class="term-baris">
                <span class="term-label">c > 0</span>
                <span>Biaya tetap produksi (ambang penawaran)</span>
            </div>
            <div class="term-baris">
                <span class="term-label">d > 0</span>
                <span>Kepekaan penawaran terhadap harga</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.latex(r"S(P) = -c + dP \quad (c,\, d > 0)")
    st.markdown("""
    <div class="info-box">
        Interpretasi: Saat harga <em>P</em> naik sebesar 1 satuan, penawaran bertambah sebesar <em>d</em> satuan.
    </div>
    """, unsafe_allow_html=True)

    # ── Langkah 3: Asumsi Dinamika Harga ──
    st.markdown('<p class="judul-seksi">Langkah 3 — Asumsi Dinamika Perubahan Harga</p>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="kartu kartu-biru">
        <h3>Prinsip Penyesuaian Harga</h3>
        <p>Asumsi kunci model ini adalah: <strong>laju perubahan harga sebanding dengan 
        kelebihan permintaan (<em>excess demand</em>)</strong>. Artinya:</p>
        <ul>
            <li>Jika <strong>D(P) > S(P)</strong> → permintaan melebihi penawaran → harga <em>naik</em></li>
            <li>Jika <strong>D(P) < S(P)</strong> → penawaran melebihi permintaan → harga <em>turun</em></li>
            <li>Jika <strong>D(P) = S(P)</strong> → pasar seimbang → harga <em>stabil</em></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.latex(r"\frac{dP}{dt} = k\,\bigl[D(P) - S(P)\bigr], \quad k > 0")

    # ── Langkah 4: Penurunan PD Orde 1 ──
    st.markdown('<p class="judul-seksi">Langkah 4 — Penurunan Persamaan Diferensial</p>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="kartu">
        <h3>Substitusi Fungsi Permintaan dan Penawaran</h3>
    </div>
    """, unsafe_allow_html=True)

    st.latex(r"\frac{dP}{dt} = k\,\bigl[(a - bP) - (-c + dP)\bigr]")
    st.latex(r"\frac{dP}{dt} = k\,\bigl[a - bP + c - dP\bigr]")
    st.latex(r"\frac{dP}{dt} = k\,(a + c) - k\,(b + d)\,P")

    st.markdown("""
    <div class="kartu" style="background:linear-gradient(135deg,#1a472a,#2d6a4f);color:white">
        <h3 style="color:#c9a84c">✅ Bentuk Akhir PD Orde 1 Linear</h3>
        <p style="color:rgba(255,255,255,0.85)">
        Dengan memindahkan suku yang mengandung P ke sisi kiri:
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.latex(r"\boxed{\frac{dP}{dt} + k(b+d)\,P = k(a+c)}")

    st.markdown("""
    <div class="info-box">
        <strong>Identifikasi Bentuk Standar:</strong><br>
        Bandingkan dengan dP/dt + P(t)·P = Q(t), diperoleh:<br>
        • <strong>P(t) = k(b+d)</strong> — koefisien positif, menghasilkan solusi konvergen<br>
        • <strong>Q(t) = k(a+c)</strong> — suku sumber (forcing term), bernilai konstan
    </div>
    """, unsafe_allow_html=True)

    # ── Langkah 5: Solusi Analitik ──
    st.markdown('<p class="judul-seksi">Langkah 5 — Solusi Analitik & Harga Keseimbangan</p>',
                unsafe_allow_html=True)

    col5, col6 = st.columns([3, 2])

    with col5:
        st.markdown("**Faktor integrasi:** μ(t) = e^{k(b+d)t}")
        st.latex(r"\mu(t) = e^{\,k(b+d)\,t}")

        st.markdown("**Solusi umum PD:**")
        st.latex(r"P(t) = \frac{a+c}{b+d} + \left(P_0 - \frac{a+c}{b+d}\right)e^{-k(b+d)\,t}")

        st.markdown("**Sederhanakan dengan Pe = (a+c)/(b+d):**")
        st.latex(r"\boxed{P(t) = P_e + \bigl(P_0 - P_e\bigr)\,e^{-k(b+d)\,t}}")

    with col6:
        st.markdown("""
        <div class="kartu kartu-emas">
            <h3>🎯 Harga Keseimbangan (Ekuilibrium)</h3>
            <p>Diperoleh saat dP/dt = 0 (pasar seimbang, D = S):</p>
        </div>
        """, unsafe_allow_html=True)

        st.latex(r"P_e = \frac{a + c}{b + d}")

        st.markdown(f"""
        <div class="hasil-numerik">
            <span>Dengan parameter saat ini:</span>
            Pe = Rp {Pe:,.0f}/kg
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box" style="margin-top:0.8rem">
            <strong>Konvergensi:</strong> Karena k(b+d) > 0, maka 
            e^{−k(b+d)t} → 0 saat t → ∞, sehingga P(t) → Pe.
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MENU 3 — SIMULASI & SOLUSI NUMERIK
# ─────────────────────────────────────────────────────────────────────────────
elif menu == "🔢 Simulasi & Solusi Numerik":

    st.markdown("""
    <div class="header-utama">
        <div class="badge-menu">Menu 3 — Simulasi & Solusi Numerik</div>
        <h1>Metode Euler untuk PD Orde 1</h1>
        <p>Pendekatan Numerik Iteratif Penyelesaian Dinamika Harga Beras</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Penjelasan Metode Euler ──
    st.markdown('<p class="judul-seksi">A. Prinsip Metode Euler</p>',
                unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        <div class="kartu">
            <h3>Konsep Dasar</h3>
            <p>
            <strong>Metode Euler</strong> adalah metode numerik paling sederhana untuk 
            menyelesaikan persamaan diferensial. Metode ini mengaproksimasi solusi dengan 
            menggunakan garis singgung (tangent line) sebagai pendekatan kurva solusi 
            pada setiap langkah waktu.
            </p>
            <p>
            Ide utamanya: jika kita tahu nilai <em>P</em> dan turunannya <em>dP/dt</em> 
            pada waktu <em>t</em>, kita dapat mengestimasi nilai <em>P</em> pada 
            waktu <em>t + Δt</em>.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="kartu kartu-emas">
            <h3>Rumus Iterasi Euler</h3>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"P_{n+1} = P_n + \Delta t \cdot f(t_n,\, P_n)")
        st.markdown("""
        <div class="term-baris">
            <span class="term-label">Pₙ</span>
            <span>Harga pada langkah ke-n</span>
        </div>
        <div class="term-baris">
            <span class="term-label">Δt</span>
            <span>Langkah waktu (ukuran langkah)</span>
        </div>
        <div class="term-baris">
            <span class="term-label">f(·)</span>
            <span>Fungsi turunan dP/dt dari model</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Terapan pada Model Harga Beras ──
    st.markdown('<p class="judul-seksi">B. Penerapan pada Model Harga Beras</p>',
                unsafe_allow_html=True)

    st.latex(r"\frac{dP}{dt} = k(a+c) - k(b+d)\,P")
    st.latex(r"P_{n+1} = P_n + \Delta t \cdot \bigl[k(a+c) - k(b+d)\,P_n\bigr]")

    # ── Tampilkan Parameter Aktif ──
    st.markdown('<p class="judul-seksi">C. Parameter Simulasi Aktif</p>',
                unsafe_allow_html=True)

    param_cols = st.columns(4)
    params_info = [
        ("P₀", f"Rp {P0:,}", "Harga Awal"),
        ("Pe", f"Rp {Pe:,.0f}", "Harga Ekuilibrium"),
        ("k(b+d)", f"{k*(b+d):.4f}", "Koef. Peluruhan"),
        ("k(a+c)", f"{k*(a+c):.2f}", "Suku Sumber"),
    ]
    for col, (label, nilai, keterangan) in zip(param_cols, params_info):
        with col:
            st.markdown(f"""
            <div class="hasil-numerik" style="padding:1rem">
                <span>{keterangan}</span>
                <strong style="font-size:1.1rem">{nilai}</strong>
                <span style="font-size:0.75rem;margin-top:0.2rem">{label}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Jalankan Simulasi ──
    st.markdown('<p class="judul-seksi">D. Hasil Simulasi Numerik</p>',
                unsafe_allow_html=True)

    df_hasil, Pe_val = hitung_euler(P0, a, b, c, d, k, t_max, dt)

    # Ringkasan statistik
    stat_cols = st.columns(5)
    stats = [
        ("🕐 Waktu Awal", "0 hari"),
        ("🕐 Waktu Akhir", f"{t_max} hari"),
        ("💰 Harga Awal", f"Rp {P0:,}"),
        ("💰 Harga Akhir", f"Rp {df_hasil['Harga Numerik P(t) (Rp/kg)'].iloc[-1]:,.0f}"),
        ("🎯 Konvergensi", f"Rp {Pe_val:,.0f}"),
    ]
    for col, (label, nilai) in zip(stat_cols, stats):
        with col:
            st.metric(label=label, value=nilai)

    # Hitung deviasi akhir dari keseimbangan
    deviasi = abs(df_hasil["Harga Numerik P(t) (Rp/kg)"].iloc[-1] - Pe_val)
    persen_deviasi = (deviasi / Pe_val) * 100

    if persen_deviasi < 1:
        st.success(f"✅ Konvergensi tercapai: Harga akhir hanya menyimpang {persen_deviasi:.2f}% dari harga keseimbangan.")
    elif persen_deviasi < 5:
        st.warning(f"⚠️ Mendekati konvergensi: Harga akhir menyimpang {persen_deviasi:.2f}% dari harga keseimbangan. Pertimbangkan memperpanjang waktu simulasi.")
    else:
        st.info(f"ℹ️ Belum konvergen: Harga akhir masih menyimpang {persen_deviasi:.2f}% dari keseimbangan. Perpanjang t_max untuk melihat konvergensi penuh.")

    # Tampilkan tabel data
    st.markdown("#### 📋 Tabel Data Simulasi Euler")

    # Format kolom untuk tampilan yang lebih baik
    df_tampil = df_hasil.copy()
    df_tampil["Harga Numerik P(t) (Rp/kg)"] = df_tampil["Harga Numerik P(t) (Rp/kg)"].map(
        lambda x: f"Rp {x:,.2f}"
    )
    df_tampil["Harga Keseimbangan Pe (Rp/kg)"] = df_tampil["Harga Keseimbangan Pe (Rp/kg)"].map(
        lambda x: f"Rp {x:,.2f}"
    )

    # Tampilkan maksimal 500 baris (subsample jika terlalu banyak)
    n_baris = len(df_tampil)
    if n_baris > 500:
        langkah_tampil = max(1, n_baris // 500)
        df_tampil = df_tampil.iloc[::langkah_tampil].reset_index(drop=True)
        st.caption(f"*Menampilkan {len(df_tampil)} baris (disaring dari {n_baris} total titik data)*")

    st.dataframe(
        df_tampil,
        use_container_width=True,
        height=400,
    )

    # Tombol unduh CSV
    csv_data = df_hasil.to_csv(index=False, float_format="%.4f").encode("utf-8")
    st.download_button(
        label="⬇️ Unduh Data sebagai CSV",
        data=csv_data,
        file_name="simulasi_harga_beras_euler.csv",
        mime="text/csv",
        help="Unduh seluruh data hasil simulasi dalam format CSV"
    )


# ─────────────────────────────────────────────────────────────────────────────
# MENU 4 — GRAFIK REPRESENTASI MODEL
# ─────────────────────────────────────────────────────────────────────────────
elif menu == "📊 Grafik Representasi Model":

    st.markdown("""
    <div class="header-utama">
        <div class="badge-menu">Menu 4 — Grafik Representasi Model</div>
        <h1>Visualisasi Dinamika Harga Beras</h1>
        <p>Kurva Pergerakan Harga dan Konvergensi menuju Harga Keseimbangan</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Hitung data simulasi ──
    df_hasil, Pe_val = hitung_euler(P0, a, b, c, d, k, t_max, dt)

    t_data  = df_hasil["Waktu t (hari)"].tolist()
    P_data  = df_hasil["Harga Numerik P(t) (Rp/kg)"].tolist()

    # ── Grafik Utama: Dinamika Harga ──
    st.markdown('<p class="judul-seksi">A. Grafik Pergerakan Harga Beras</p>',
                unsafe_allow_html=True)

    # Tentukan rentang Y untuk tampilan yang baik
    P_min = min(min(P_data), Pe_val) * 0.95
    P_max = max(max(P_data), Pe_val) * 1.05

    fig_utama = go.Figure()

    # ── Kurva harga numerik (area shading) ──
    fig_utama.add_trace(go.Scatter(
        x=t_data, y=P_data,
        name="Harga Beras P(t)",
        mode="lines",
        line=dict(color="#2d6a4f", width=3),
        fill="tozeroy",
        fillcolor="rgba(45,106,79,0.08)",
        hovertemplate="<b>t = %{x:.1f} hari</b><br>P(t) = Rp %{y:,.0f}/kg<extra></extra>",
    ))

    # ── Garis keseimbangan ──
    fig_utama.add_trace(go.Scatter(
        x=[t_data[0], t_data[-1]],
        y=[Pe_val, Pe_val],
        name=f"Harga Keseimbangan Pe = Rp {Pe_val:,.0f}/kg",
        mode="lines",
        line=dict(color="#c9a84c", width=2.5, dash="dash"),
        hovertemplate=f"Harga Keseimbangan Pe = Rp {Pe_val:,.0f}/kg<extra></extra>",
    ))

    # ── Titik awal ──
    fig_utama.add_trace(go.Scatter(
        x=[0], y=[P0],
        name=f"Harga Awal P₀ = Rp {P0:,}/kg",
        mode="markers",
        marker=dict(color="#1b4f72", size=12, symbol="circle",
                    line=dict(color="white", width=2)),
        hovertemplate=f"Harga Awal P₀ = Rp {P0:,}/kg<extra></extra>",
    ))

    # ── Anotasi Pe ──
    fig_utama.add_annotation(
        x=t_data[-1] * 0.75, y=Pe_val,
        text=f"  Pe = Rp {Pe_val:,.0f}/kg  ",
        showarrow=False,
        font=dict(color="#c9a84c", size=12, family="JetBrains Mono"),
        bgcolor="rgba(26,71,42,0.85)",
        bordercolor="#c9a84c",
        borderwidth=1,
        borderpad=4,
        yshift=15,
    )

    # ── Layout ──
    fig_utama.update_layout(
        title=dict(
            text="Dinamika Harga Beras P(t) — Metode Euler",
            font=dict(size=18, family="Georgia, serif", color="#1a472a"),
            x=0.5,
        ),
        xaxis=dict(
            title="Waktu (hari)",
            title_font=dict(size=13, color="#555"),
            gridcolor="rgba(0,0,0,0.08)",
            showline=True,
            linecolor="#ccc",
        ),
        yaxis=dict(
            title="Harga Beras P(t) (Rp/kg)",
            title_font=dict(size=13, color="#555"),
            tickformat=",",
            gridcolor="rgba(0,0,0,0.08)",
            range=[P_min, P_max],
            showline=True,
            linecolor="#ccc",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#ddd",
            borderwidth=1,
        ),
        plot_bgcolor="rgba(253,246,227,0.4)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=480,
        hovermode="x unified",
        margin=dict(l=60, r=30, t=80, b=60),
    )

    st.plotly_chart(fig_utama, use_container_width=True)

    # ── Grafik Kedua: Kurva D(P) dan S(P) ──
    st.markdown('<p class="judul-seksi">B. Kurva Permintaan dan Penawaran</p>',
                unsafe_allow_html=True)

    # Rentang harga untuk kurva D dan S
    P_range = np.linspace(max(0, Pe_val * 0.3), Pe_val * 1.7, 300)
    D_vals  = a - b * P_range          # D(P) = a - bP
    S_vals  = -c + d * P_range         # S(P) = -c + dP

    col_kiri, col_kanan = st.columns([3, 2])

    with col_kiri:
        fig_ds = go.Figure()

        # Kurva Permintaan
        fig_ds.add_trace(go.Scatter(
            x=P_range, y=D_vals,
            name="Permintaan D(P) = a − bP",
            mode="lines",
            line=dict(color="#1b4f72", width=2.5),
            hovertemplate="P = Rp %{x:,.0f}<br>D(P) = %{y:.1f}<extra></extra>",
        ))

        # Kurva Penawaran
        fig_ds.add_trace(go.Scatter(
            x=P_range, y=S_vals,
            name="Penawaran S(P) = −c + dP",
            mode="lines",
            line=dict(color="#c0392b", width=2.5),
            hovertemplate="P = Rp %{x:,.0f}<br>S(P) = %{y:.1f}<extra></extra>",
        ))

        # Titik keseimbangan
        De_val = a - b * Pe_val   # = a - b*(a+c)/(b+d)
        fig_ds.add_trace(go.Scatter(
            x=[Pe_val], y=[De_val],
            name=f"Ekuilibrium (Pe = Rp {Pe_val:,.0f})",
            mode="markers",
            marker=dict(color="#c9a84c", size=14, symbol="star",
                        line=dict(color="white", width=2)),
        ))

        fig_ds.add_annotation(
            x=Pe_val, y=De_val,
            text=f"  Ekuilibrium<br>  Pe = Rp {Pe_val:,.0f}",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#c9a84c",
            font=dict(color="#1a472a", size=11),
            bgcolor="rgba(253,246,227,0.9)",
            bordercolor="#c9a84c",
            borderwidth=1,
            ax=60, ay=-40,
        )

        fig_ds.update_layout(
            title=dict(
                text="Kurva Permintaan & Penawaran Beras",
                font=dict(size=15, family="Georgia, serif", color="#1a472a"),
                x=0.5,
            ),
            xaxis=dict(title="Harga P (Rp/kg)", tickformat=",",
                       gridcolor="rgba(0,0,0,0.08)"),
            yaxis=dict(title="Kuantitas (unit)", gridcolor="rgba(0,0,0,0.08)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(253,246,227,0.4)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=380,
            margin=dict(l=60, r=30, t=70, b=60),
        )

        st.plotly_chart(fig_ds, use_container_width=True)

    with col_kanan:
        # ── Panel Analisis ──
        st.markdown("""
        <div class="kartu">
            <h3>📊 Analisis Dinamika</h3>
        </div>
        """, unsafe_allow_html=True)

        D_awal = a - b * P0
        S_awal = -c + d * P0
        excess = D_awal - S_awal

        if P0 > Pe_val:
            arah = "📉 TURUN"
            warna = "#c0392b"
            penjelasan = f"Harga awal LEBIH TINGGI dari keseimbangan. Penawaran melebihi permintaan (excess demand = {excess:,.1f} < 0), sehingga harga cenderung turun."
        elif P0 < Pe_val:
            arah = "📈 NAIK"
            warna = "#27ae60"
            penjelasan = f"Harga awal LEBIH RENDAH dari keseimbangan. Permintaan melebihi penawaran (excess demand = {excess:,.1f} > 0), sehingga harga cenderung naik."
        else:
            arah = "⚖️ STABIL"
            warna = "#c9a84c"
            penjelasan = "Harga awal SAMA dengan harga keseimbangan. Pasar sudah dalam kondisi seimbang."

        st.markdown(f"""
        <div style="background:{warna};color:white;border-radius:10px;
                    padding:1rem;text-align:center;margin-bottom:1rem">
            <span style="font-size:0.8rem;opacity:0.9">Tren Harga</span><br>
            <strong style="font-size:1.6rem">{arah}</strong>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="kartu" style="font-size:0.88rem">
            <p><strong>Analisis:</strong> {penjelasan}</p>
            <hr style="border-color:#eee">
            <div class="term-baris">
                <span class="term-label">D₀</span>
                <span>Permintaan awal = {D_awal:,.1f}</span>
            </div>
            <div class="term-baris">
                <span class="term-label">S₀</span>
                <span>Penawaran awal = {S_awal:,.1f}</span>
            </div>
            <div class="term-baris">
                <span class="term-label">ED</span>
                <span>Excess Demand = {excess:,.1f}</span>
            </div>
            <div class="term-baris">
                <span class="term-label">Pe</span>
                <span>Keseimbangan = Rp {Pe_val:,.0f}/kg</span>
            </div>
            <div class="term-baris">
                <span class="term-label">τ</span>
                <span>Waktu konvergensi ≈ {1/(k*(b+d)):.0f} hari</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Grafik Laju Perubahan ──
    st.markdown('<p class="judul-seksi">C. Laju Perubahan Harga dP/dt</p>',
                unsafe_allow_html=True)

    dPdt_data = [k * (a + c) - k * (b + d) * p for p in P_data]

    fig_laju = go.Figure()

    fig_laju.add_trace(go.Scatter(
        x=t_data, y=dPdt_data,
        name="Laju Perubahan dP/dt",
        mode="lines",
        line=dict(color="#8e44ad", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(142,68,173,0.1)",
        hovertemplate="t = %{x:.1f} hari<br>dP/dt = %{y:.2f} Rp/hari<extra></extra>",
    ))

    # Garis nol
    fig_laju.add_hline(y=0, line_dash="dot", line_color="#c9a84c",
                       annotation_text="dP/dt = 0 (Keseimbangan)",
                       annotation_position="top right")

    fig_laju.update_layout(
        title=dict(
            text="Laju Perubahan Harga Beras dP/dt terhadap Waktu",
            font=dict(size=15, family="Georgia, serif", color="#1a472a"),
            x=0.5,
        ),
        xaxis=dict(title="Waktu (hari)", gridcolor="rgba(0,0,0,0.08)"),
        yaxis=dict(title="dP/dt (Rp/hari)", gridcolor="rgba(0,0,0,0.08)"),
        plot_bgcolor="rgba(253,246,227,0.4)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=320,
        hovermode="x unified",
        margin=dict(l=60, r=30, t=70, b=60),
        showlegend=False,
    )

    st.plotly_chart(fig_laju, use_container_width=True)

    st.markdown("""
    <div class="info-box">
        <strong>📖 Interpretasi Grafik:</strong> Grafik laju perubahan menunjukkan seberapa cepat harga berubah setiap harinya. 
        Saat kurva mendekati nol (garis putus-putus emas), artinya pasar mendekati kondisi keseimbangan dan harga 
        hampir tidak berubah lagi.
    </div>
    """, unsafe_allow_html=True)

    # ── Footer ──
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;font-size:0.85rem;color:#888;padding:1rem 0">
        <strong>Aplikasi Pembelajaran Interaktif PD Orde 1 dalam Ekonomi</strong><br>
        Model Dinamis Harga Beras — Metode Euler Numerik<br>
        <em>Dibuat menggunakan Python · Streamlit · Plotly</em>
    </div>
    """, unsafe_allow_html=True)