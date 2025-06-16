import streamlit as st
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from decimal import Decimal, getcontext
import numpy as np
import math

# دقة Decimal
getcontext().prec = 50

zeta_zeros = [
    Decimal("14.134725141"), Decimal("21.022039639"),
    Decimal("25.010857580"), Decimal("30.424876126"),
    Decimal("32.935061588"), Decimal("37.586178159"),
    Decimal("40.918719012"), Decimal("43.327073281"),
    Decimal("48.005150881"), Decimal("49.773832478")
]

SCALE = 10**9
zeta_ints = [int(z * SCALE) for z in zeta_zeros]

st.set_page_config(page_title="ZetaKey Analyzer", layout="centered", page_icon="🔐")
st.title("🔐 تحليل جودة مفاتيح RSA باستخدام أصفار زيتا")

uploaded = st.file_uploader("📎 ارفع مفتاح عام بصيغة PEM", type=["pem"])

if uploaded:
    try:
        pub_key = serialization.load_pem_public_key(
            uploaded.read(), backend=default_backend()
        )
        n = pub_key.public_numbers().n
        e = pub_key.public_numbers().e

        st.success("✅ تم استخراج المفتاح بنجاح")
        st.write(f"**Bit-length (n):** {n.bit_length()} بت")
        st.write(f"**Exponent (e):** {e}")

        remainders = []
        st.subheader("📊 البواقي (n mod γₙ)")
        for i, z_int in enumerate(zeta_ints, start=1):
            rem_int = n % z_int
            rem_float = rem_int / SCALE
            remainders.append(rem_int)
            st.write(f"γ{i} → n mod γ{i} = {rem_float:.6f}")

        arr = np.array(remainders, dtype=np.float64)
        sigma = arr.std()
        relative_score = sigma / math.log(n, 2)

        st.markdown(f"### 🧠 الانحراف المعياري σ = {sigma:.4f}")
        st.markdown(f"### 🔢 مؤشر نسبي = σ / log₂(n) = {relative_score:.8f}")

        if relative_score < 0.01:
            st.error("❌ مؤشر منخفض — المفتاح يحتمل أنه ضعيف")
        else:
            st.success("✅ مؤشر مرتفع — المفتاح يبدو جيد التوليد")

    except Exception as err:
        st.error(f"❌ خطأ: {err}")
