import streamlit as st
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from decimal import Decimal, getcontext
import numpy as np
import math

getcontext().prec = 50

# أول 50 صفر
zeta_zeros = [
    Decimal(str(z)) for z in [
        14.134725141, 21.022039639, 25.010857580, 30.424876126, 32.935061588,
        37.586178159, 40.918719012, 43.327073281, 48.005150881, 49.773832478,
        52.970321477, 56.446247697, 59.347044002, 60.831778525, 65.112544048,
        67.079810529, 69.546401711, 72.067157674, 75.704690699, 77.144840069,
        79.337375020, 82.910380854, 84.735492981, 87.425274613, 88.809111208,
        92.491899271, 94.651344041, 95.870634228, 98.831194218, 101.317851006,
        103.725538040, 105.446623052, 107.168611184, 111.029535543, 111.874659177,
        114.320220915, 116.226680321, 118.790782866, 121.370125002, 122.946829294,
        124.256818554, 127.516683880, 129.578704200, 131.087688531, 133.497737203,
        134.756509753, 138.116042055, 139.736208952, 141.123707404, 143.111845808
    ]
]

SCALE = 10**9
zeta_ints = [int(z * SCALE) for z in zeta_zeros]

st.set_page_config(page_title="ZetaKey Pro Analyzer", layout="centered", page_icon="🔐")
st.title("🔐 تحليل متقدم: أول 50 صفر من زيتا مقابل مفاتيح RSA")

uploaded = st.file_uploader("📎 ارفع مفتاح عام PEM", type=["pem"])

if uploaded:
    try:
        pub = serialization.load_pem_public_key(uploaded.read(), backend=default_backend())
        n = pub.public_numbers().n

        st.success("✅ تم استخراج المفتاح")
        st.write(f"**Bit-length:** {n.bit_length()} بت")

        remainders = []
        for i, z_int in enumerate(zeta_ints, start=1):
            rem = n % z_int
            remainders.append(rem)
            st.write(f"γ{i:02d} → n mod γ{i:02d} = {rem / SCALE:.6f}")

        arr = np.array(remainders, dtype=np.float64)
        sigma = arr.std()
        rel = sigma / math.log2(n)

        st.markdown(f"### 🧠 σ = {sigma:.4f} | مؤشر نسبي = {rel:.6f}")
        st.success("🔍 تحليل كامل بنجاح!")

    except Exception as er:
        st.error(f"❌ خطأ: {er}")
