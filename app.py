import streamlit as st

# Sayfa ayarları (Tarayıcı sekmesi için sade bir başlık)
st.set_page_config(
    page_title="AI Platform",
    page_icon="💬",
    layout="centered"
)

# Arayüzdeki gereksiz Streamlit menü ve footer kalabalığını gizleyelim (Minimalist görünüm için)
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Ana Başlık (Tertemiz, sade bir giriş)
st.markdown("<h2 style='text-align: center; color: #111;'>AI Platform</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>Sade ve hızlı sohbet deneyimi</p>", unsafe_allow_html=True)

st.divider()

# Sohbet geçmişi (hafıza) için başlangıç
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekranda tutma ve gösterme
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Alt kısımda yer alan sade mesaj yazma çubuğu (WhatsApp tarzı)
if prompt := st.chat_input("Bir şeyler yazın..."):
    # Kullanıcının yazdığı mesajı ekrana bas
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Şimdilik yapay zeka henüz bağlı olmadığı için test amaçlı sade bir yanıt verelim
    response = f"Mesajın alındı: {prompt}"
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
      
