import streamlit as st
import os

# Sayfa yapılandırması (Mobil uyumlu ve sade)
st.set_page_config(
    page_title="Yapay Zeka Platformu",
    page_icon="🤖",
    layout="centered"
)

# Groq API anahtarını kontrol et
groq_api_key = None
try:
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

if not groq_api_key:
    groq_api_key = os.getenv("GROQ_API_KEY")

# Groq kütüphanesini yüklemeyi dene
client = None
if groq_api_key:
    try:
        from groq import Groq
        client = Groq(api_key=groq_api_key)
    except Exception as e:
        pass

# Oturum geçmişi (Sohbet hafızası)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Üst Menü / Kenar Çubuğu
with st.sidebar:
    st.title("⚙️ Menü")
    
    # Mod seçimi
    st.subheader("🔄 Mod Seçimi")
    mode = st.radio(
        "Çalışma Modu:",
        ["Internetsiz (Offline)", "Normal", "Kodlama"],
        index=0
    )
    
    st.markdown("---")
    if st.button("🧹 Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# Ana Ekran Başlığı
if mode == "Internetsiz (Offline)":
    st.success("🟢 Mod: Internetsiz | Yerel mod aktif.")
elif mode == "Normal":
    st.info("⚡ Mod: Normal (Llama 3.1 - 8B)")
else:
    st.warning("💻 Mod: Kodlama (Llama 3.3 - 70B)")

st.markdown("---")

# Geçmiş mesajları ekrana yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan girdi al
if prompt := st.chat_input("Mesajınızı yazın..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Asistan yanıtı
    with st.chat_message("assistant"):
        response_content = ""
        
        if mode == "Internetsiz (Offline)":
            response_content = f"[Internetsiz (Offline) Mod]: '{prompt}' yerel önbellek üzerinden işlendi. İnternet bağlantısı gerektirmez."
            st.markdown(response_content)
            
        elif client is None:
            response_content = "⚠️ Groq API anahtarı bulunamadı veya geçersiz! Lütfen Streamlit Secrets ayarlarına geçerli bir API anahtarı ekleyin."
            st.error(response_content)
            
        else:
            try:
                # Modlara göre güncel Groq modelleri
                if mode == "Normal":
                    model_name = "llama-3.1-8b-instant"
                else:
                    model_name = "llama-3.3-70b-versatile"
                
                # API çağrısı
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    model=model_name,
                )
                response_content = chat_completion.choices[0].message.content
                st.markdown(response_content)
                
            except Exception as e:
                response_content = f"Bağlantı hatası oluştu: {e}"
                st.error(response_content)
        
        # Asistan yanıtını hafızaya kaydet
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        
