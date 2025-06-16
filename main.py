import streamlit as st
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import numpy as np
import math

# 1) اقرأ الأصفار من ملف JSON
with open("zeta_zeros_300.json") as f:
    zeta_values = json.load(f)

# 2) حضّرها كأعداد صحيحة
SCALE = 10**9
zeta_ints = [int(val * SCALE) for val in zeta_values]

st.set_page_config(page_title="ZetaKey 300", layout="centered")
st.title("🔐 تحليل RSA باستخدام أول 300 صفر من زيتا")

uploaded = st.file_uploader("📎 ارفع PEM", type=["pem"])
if not uploaded:
    st.info("ارفع مفتاح PEM لبدء التحليل.")
    st.stop()

pub = serialization.load_pem_public_key(uploaded.read(), backend=default_backend())
n = pub.public_numbers().n

# حساب النسب بسرعة
ratios = [(n % z) / z for z in zeta_ints]

# إحصائيات كما قبل
hist, _ = np.histogram(ratios, bins=20, range=(0.0,1.0))
total = hist.sum()
expected = total/20
chi_sq = float(((hist-expected)**2/expected).sum())
entropy = -float((hist/total * np.log2(hist/total + 1e-16)).sum())

st.write(f"χ² = {chi_sq:.2f}, Entropy = {entropy:.3f}")
st.bar_chart(hist)
if chi_sq>30 or entropy<3.5:
    st.error("❌ مفتاح ضعيف التوليد")
else:
    st.success("✅ مفتاح جيد التوليد")
