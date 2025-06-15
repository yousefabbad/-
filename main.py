import streamlit as st
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from sympy import factorint
import math

st.set_page_config(page_title="Zeta Key Analyzer", layout="centered")

st.title("🔐 تحليل جودة مفاتيح RSA باستخدام أصفار زيتا")
uploaded_file = st.file_uploader("📎 ارفع مفتاح عام بصيغة PEM", type=["pem"])

if uploaded_file is not None:
    try:
        public_key = serialization.load_pem_public_key(
            uploaded_file.read(),
            backend=default_backend()
        )
        public_numbers = public_key.public_numbers()
        n = public_numbers.n
        e = public_numbers.e

        st.success("✅ تم استخراج المفتاح بنجاح")
        st.write(f"**Modulus (n):** {n}")
        st.write(f"**Exponent (e):** {e}")

        st.subheader("🧮 تحليل العوامل الأولية للمودولوس:")
        factors = factorint(n)
        for prime, count in factors.items():
            st.write(f"{prime} ^ {count}")

        st.subheader("📊 الفروقات بين العوامل:")
        primes = sorted(factors.keys())
        for i in range(1, len(primes)):
            rsa_diff = primes[i] - primes[i - 1]
            zeta_val = round(7 - math.log(i + 1), 6)  # مثال تقريبي
            st.write(f"فرق {i}: RSA = {rsa_diff} ⬄ زيتا = {zeta_val}")

    except Exception as ex:
        st.error(f"❌ خطأ في قراءة المفتاح: {str(ex)}")
