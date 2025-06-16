import streamlit as st
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import numpy as np

# أصفار دالة زيتا (أول 20 تقريباً)
zeta_zeros = np.array([
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005150, 49.773832,
    52.970321, 56.446247, 59.347044, 60.831780, 65.112544,
    67.079811, 69.546401, 72.067158, 75.704690, 77.144840
])

st.set_page_config(page_title="ZetaKey Analyzer", layout="centered", page_icon="🔐")
st.title("🔐 تحليل جودة مفاتيح RSA بأصفار زيتا")

uploaded = st.file_uploader("📎 ارفع مفتاح عام بصيغة PEM", type=["pem"])

if uploaded:
    try:
        pub_key = serialization.load_pem_public_key(
            uploaded.read(), backend=default_backend()
        )
        numbers = pub_key.public_numbers()
        n = numbers.n
        e = numbers.e

        st.success("✅ تم استخراج المفتاح بنجاح")
        st.write(f"**Bit-length (n):** {n.bit_length()} بت")
        st.write(f"**Exponent (e):** {e}")

        # 🧮 التحليل العددي مع أصفار زيتا
        st.subheader("📊 مقارنة n مع أصفار زيتا:")
        remainders = n % zeta_zeros
        for idx, rem in enumerate(remainders, start=1):
            st.write(f"γ{idx} = {zeta_zeros[idx-1]:.6f} → n mod γ{idx} = {rem:.5f}")

        # تقدير مبدئي لجودة المفتاح من بقايا القسمة
        score = np.std(remainders)  # كل ما كان التشتت أعلى، قد يدل على عشوائية أفضل
        st.markdown(f"### 🧠 مؤشر التشتت (σ): `{score:.4f}`")
        if score < 10:
            st.error("❌ تشتت منخفض – قد يشير لعشوائية ضعيفة")
        else:
            st.success("✅ تشتت جيد – المفتاح يبدو عشوائياً بدرجة أفضل")

    except Exception as err:
        st.error(f"خطأ في قراءة المفتاح: {err}")
