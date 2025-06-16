import streamlit as st
from Crypto.PublicKey import RSA
from math import log2
from statistics import stdev
from zeta_data import zeta_zeros

st.set_page_config(page_title="تحليل المفاتيح باستخدام أصفار زيتا", layout="centered")
st.title("🔐 توليد وتحليل مفاتيح RSA باستخدام أصفار زيتا")

# توليد المفتاح
bit_length = st.selectbox("اختر الطول البتّي للمفتاح:", [512, 1024, 2048, 4096], index=2)

if st.button("🎲 توليد مفتاح وتحليله"):
    key = RSA.generate(bit_length)
    n = key.n
    e = key.e

    st.success("✅ تم توليد المفتاح بنجاح")
    st.code(f"Bit-length (n): {bit_length} بت\nExponent (e): {e}")

    # تحليل البواقي
    remainders = [float(n % int(z * 1e9)) / 1e7 for z in zeta_zeros]  # normalizing
    sigma = stdev(remainders)
    entropy = -sum((1/len(remainders)) * log2(1/len(remainders)) for _ in remainders)
    max_entropy = log2(len(remainders))

    st.subheader("📊 إحصائيات التحليل")
    st.markdown(f"""
    • σ (std): `{sigma:.4f}`  
    • Entropy: `{entropy:.3f}` / max ≈ `{max_entropy:.3f}`  
    • مؤشر نسبي: `{sigma / log2(n):.6f}`
    """)

    if sigma < 1:
        st.error("❌ المفتاح يحتمل أنه ضعيف التوليد")
    else:
        st.success("✅ المفتاح يبدو جيد التوليد")

    # عرض البواقي
    st.subheader("📈 البواقي (n mod γₙ)")
    for i, val in enumerate(remainders):
        st.write(f"γ{i+1:03} → (n mod γ) = {val:.6f}")
