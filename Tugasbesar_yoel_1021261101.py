"""
Tugas Besar - Aplikasi Biaya Laundry Kiloan (Python + Streamlit)
Nama : Yoel Christman Tambunan
NIM  : 1021261101

Jalankan dengan:
    streamlit run Tugasbesar_yoel_1021261101.py
"""

import re

import streamlit as st

# ---------------------------------------------------------------------------
# Konfigurasi halaman
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Laundry Kiloan",
    page_icon="🧺",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Gaya (CSS)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .block-container {max-width: 860px; padding-top: 2rem;}
    .hero {
        background: linear-gradient(135deg, #0b3d91 0%, #1976d2 60%, #42a5f5 100%);
        border-radius: 18px; padding: 26px 30px; color: #fff;
        box-shadow: 0 8px 24px rgba(25, 118, 210, .25); margin-bottom: 22px;
    }
    .hero h1 {margin: 0; font-size: 2rem; color: #fff;}
    .hero p {margin: 6px 0 0 0; opacity: .92; font-size: 1rem;}
    .section-title {
        font-size: 1.1rem; font-weight: 700; color: #0b3d91; margin: 6px 0 10px 0;
    }
    .card {
        border-radius: 14px; padding: 14px 16px; border: 1px solid rgba(0,0,0,.06);
        box-shadow: 0 2px 10px rgba(0,0,0,.05); height: 100%;
    }
    .card .lbl {font-size: .8rem; color: #555; margin-bottom: 2px;}
    .card .val {font-size: 1.25rem; font-weight: 700; color: #111;}
    .c-blue   {background: #e3f2fd;}
    .c-purple {background: #ede7f6;}
    .c-green  {background: #e8f5e9;}
    .c-orange {background: #fff3e0;}
    .c-gray   {background: #eceff1;}
    .total {
        background: linear-gradient(135deg, #2e7d32, #66bb6a); color: #fff;
        border-radius: 16px; padding: 18px 22px; margin-top: 12px;
        display: flex; justify-content: space-between; align-items: center;
        box-shadow: 0 6px 18px rgba(46, 125, 50, .3);
    }
    .total .lbl {font-size: 1rem; font-weight: 600;}
    .total .val {font-size: 1.8rem; font-weight: 800;}
    .footer {text-align: center; color: #888; font-size: .8rem; margin-top: 28px;}
    div.stButton > button {
        width: 100%; border-radius: 10px; font-weight: 600; padding: .55rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Fungsi bantu
# ---------------------------------------------------------------------------
def rupiah(angka: int) -> str:
    """Format angka menjadi 'Rp 85.000'."""
    return "Rp " + f"{angka:,}".replace(",", ".")


def validasi_nim(nim: str):
    """NIM valid jika terdiri dari tepat 10 digit angka (0-9)."""
    nim = nim.strip()
    if not re.fullmatch(r"[0-9]{10}", nim):
        return None, "NIM tidak valid! NIM harus terdiri dari tepat 10 digit angka."
    return nim, None


def validasi_berat(berat):
    """Berat harus bilangan bulat dan lebih dari 0."""
    if berat is None:
        return None, "Berat cucian belum diisi! Masukkan bilangan bulat lebih dari 0."
    if float(berat) != int(berat):
        return None, "Berat cucian harus berupa bilangan bulat!"
    berat = int(berat)
    if berat <= 0:
        return None, "Berat cucian tidak valid! Berat harus lebih dari 0."
    return berat, None


def hitung_biaya(nim: str, berat: int) -> dict:
    """Menghitung seluruh komponen biaya laundry."""
    digit_terakhir = int(nim[-1])
    digit_genap = sum(1 for d in nim if int(d) % 2 == 0)  # 0 termasuk genap

    tarif = 5000 + digit_terakhir * 500
    persen_diskon = digit_genap  # 1% per digit genap
    biaya_normal = berat * tarif
    potongan = biaya_normal * persen_diskon // 100
    total = biaya_normal - potongan

    return {
        "nim": nim,
        "berat": berat,
        "tarif": tarif,
        "digit_genap": digit_genap,
        "persen_diskon": persen_diskon,
        "biaya_normal": biaya_normal,
        "potongan": potongan,
        "total": total,
    }


def on_hitung():
    nim, err_nim = validasi_nim(st.session_state.get("nim", ""))
    berat, err_berat = validasi_berat(st.session_state.get("berat"))

    st.session_state["error"] = [e for e in (err_nim, err_berat) if e]
    if st.session_state["error"]:
        st.session_state["hasil"] = None
    else:
        st.session_state["hasil"] = hitung_biaya(nim, berat)


def on_reset():
    st.session_state["nim"] = ""
    st.session_state["berat"] = None
    st.session_state["hasil"] = None
    st.session_state["error"] = []


# ---------------------------------------------------------------------------
# Inisialisasi state
# ---------------------------------------------------------------------------
st.session_state.setdefault("nim", "")
st.session_state.setdefault("berat", None)
st.session_state.setdefault("hasil", None)
st.session_state.setdefault("error", [])

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🧺 Laundry Kiloan</h1>
        <p>Aplikasi perhitungan biaya laundry cepat, akurat, dan transparan.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Form input
# ---------------------------------------------------------------------------
st.markdown('<div class="section-title">📝 Data Pelanggan</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    st.text_input(
        "NIM (10 digit)",
        key="nim",
        max_chars=30,
        placeholder="contoh: 1021261101",
    )
with col_b:
    st.number_input(
        "Berat Cucian (kg)",
        key="berat",
        value=None,
        step=1,
        placeholder="contoh: 10",
    )

btn1, btn2 = st.columns(2)
with btn1:
    st.button("🧮 Hitung", type="primary", on_click=on_hitung)
with btn2:
    st.button("🔄 Reset", on_click=on_reset)

# ---------------------------------------------------------------------------
# Pesan kesalahan
# ---------------------------------------------------------------------------
for pesan in st.session_state["error"]:
    st.error(pesan, icon="🚫")

# ---------------------------------------------------------------------------
# Hasil perhitungan
# ---------------------------------------------------------------------------
h = st.session_state["hasil"]
if h:
    st.markdown("---")
    st.markdown(
        '<div class="section-title">📊 Rincian Perhitungan</div>',
        unsafe_allow_html=True,
    )

    def kartu(warna, label, nilai):
        return (
            f'<div class="card {warna}"><div class="lbl">{label}</div>'
            f'<div class="val">{nilai}</div></div>'
        )

    r1 = st.columns(3)
    r1[0].markdown(kartu("c-gray", "NIM", h["nim"]), unsafe_allow_html=True)
    r1[1].markdown(kartu("c-gray", "Berat Cucian", f'{h["berat"]} kg'), unsafe_allow_html=True)
    r1[2].markdown(kartu("c-gray", "Jumlah Digit Genap", h["digit_genap"]), unsafe_allow_html=True)

    st.write("")
    r2 = st.columns(2)
    r2[0].markdown(kartu("c-blue", "🏷️ Tarif per kg", rupiah(h["tarif"])), unsafe_allow_html=True)
    r2[1].markdown(kartu("c-purple", "％ Persen Diskon", f'{h["persen_diskon"]} %'), unsafe_allow_html=True)

    st.write("")
    r3 = st.columns(2)
    r3[0].markdown(kartu("c-green", "💰 Biaya Normal", rupiah(h["biaya_normal"])), unsafe_allow_html=True)
    r3[1].markdown(kartu("c-orange", "✂️ Potongan", rupiah(h["potongan"])), unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="total">
            <span class="lbl">💵 Total Bayar</span>
            <span class="val">{rupiah(h["total"])}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Lihat rumus perhitungan"):
        st.markdown(
            f"""
            - Tarif per kg = Rp 5.000 + (digit terakhir NIM × Rp 500) = **{rupiah(h["tarif"])}**
            - Persen diskon = jumlah digit genap × 1 % = **{h["persen_diskon"]} %**
            - Biaya normal = {h["berat"]} × {rupiah(h["tarif"])} = **{rupiah(h["biaya_normal"])}**
            - Potongan = {h["persen_diskon"]} % × {rupiah(h["biaya_normal"])} = **{rupiah(h["potongan"])}**
            - Total bayar = {rupiah(h["biaya_normal"])} − {rupiah(h["potongan"])} = **{rupiah(h["total"])}**
            """
        )

st.markdown(
    '<div class="footer">Tugas Besar · Yoel Christman Tambunan · 1021261101</div>',
    unsafe_allow_html=True,
)