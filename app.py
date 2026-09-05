import streamlit as st

# Sayfa ayarları (Minimalist görünüm)
st.set_page_config(
    page_title="AI Platform",
    page_icon="💬",
    layout="centered"
)

# Streamlit'in kendi standart arayüz kalabalığını gizle
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Oturum durumunda (hafızada) hangi yapay zekanın seçildiğini ve sohbet geçmişini tutalım
if "selected_ai" not in st.session_state:
    st.session_state.selected_ai = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. AŞAMA: Eğer henüz bir yapay zeka seçilmediyse, 3'lü seçim ekranını göster
if st.session_state.selected_ai is None:
    st.markdown("<h2 style='text-align: center; color: #111;'>Bir Yapay Zeka Seçin</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>Sohbet etmek istediğiniz modeli seçerek başlayın</p>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")

    # Yan yana 3 sütun oluşturalım (Görseldeki 1, 2, 3 kutucukları gibi)
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🤖 Model 1\n\nAsistan", use_container_width=True):
            st.session_state.selected_ai = "Model 1"
            st.rerun()

    with col2:
        if st.button("⚡ Model 2\n\nHızlı AI", use_container_width=True):
            st.session_state.selected_ai = "Model 2"
            st.rerun()

    with col3:
        if st.button("💡 Model 3\n\nYaratıcı", use_container_width=True):
            st.session_state.selected_ai = "Model 3"
            st.rerun()

# 2. AŞAMA: Yapay zeka seçildikten sonra açılacak tertemiz WhatsApp tarzı sohbet ekranı
else:
    # Üst kısımda sade bir başlık ve geri dönme butonu
    col_title, col_back = st.columns([4, 1])
    with col_title:
        st.markdown(f"<h4 style='margin: 0; color: #111;'>{st.session_state.selected_ai} ile Sohbet</h4>", unsafe_allow_html=True)
    with col_back:
        if st.button("← Değiştir"):
            st.session_state.selected_ai = None
            st.session_state.messages = []
            st.rerun()

    st.divider()

    # Geçmiş mesajları ekranda tutma
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # En altta WhatsApp tarzı sade mesaj yazma çubuğu (İşaretlediğin gereksiz butonlar yok)
    if prompt := st.chat_input("Mesajınızı yazın..."):
        # Kullanıcı mesajı
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Simülasyon yanıtı (İleride buraya gerçek yapay zeka bağlanacak)
        response = f"{st.session_state.selected_ai}: {prompt} (Yanıt)"
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
            
