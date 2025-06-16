import streamlit as st
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from decimal import Decimal, getcontext
import numpy as np
import math

getcontext().prec = 50
zeta_ints = [int(Decimal(str(z)) * 10**9) for z in zeta_values]

st.set_page_config(page_title="ZetaKey 100 Analyzer", layout="centered", page_icon="🔐")
st.title("🔐 تحليل أول 100 صفر من زيتا مقابل مفاتيح RSA")

uploaded = st.file_uploader("📎 ارفع مفتاح عام PEM", type=["pem"])
if uploaded:
    pub = serialization.load_pem_public_key(uploaded.read(), default_backend())
    n = pub.public_numbers().n
    st.write(f"Bit-length: {n.bit_length()}")

    remainders = [n % z for z in zeta_ints]
    for i, r in enumerate(remainders, start=1):
        st.write(f"γ{i:03d} → {float(r)/1e9:.6f}")

    arr = np.array(remainders, dtype=np.float64)
    sigma = arr.std()
    rel = sigma / math.log2(n)
    st.write(f"σ = {sigma:.4f}, مؤشر نسبي = {rel:.6f}")
    st.success("تم التحليل أول 100 صفر.")
