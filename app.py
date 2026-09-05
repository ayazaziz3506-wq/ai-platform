import streamlit as st

# Sayfa ayarları
st.set_page_config(
    page_title="AI Platform",
    page_icon="💬",
    layout="centered"
)

# Arayüzü tamamen sadeleştiren stil kodları
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0e1117; color: #fafafa; }
    </style>
""", unsafe_allow_html=True)

# Oturum hafızası
if "selected_ai" not in st.session_state:
    st.session_state.selected_ai = None

if "chats" not in st.session_state:
    st.session_state.chats = {"Model 1": [], "Model 2": [], "Model 3": []}

# --- 1. MODEL SEÇİM EKRANI (İlk Açılış) ---
if st.session_state.selected_ai is None:
    st.markdown("<h2 style='text-align: center; color: #fff; margin-top: 50px;'>Yapay Zeka Seçin</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>Sohbet etmek istediğiniz modeli seçin</p>", unsafe_allow_html=True)
    
    st.write("")
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

# --- 2. WHATSAPP TARZI SOHBET EKRANI ---
else:
    # Üst Kısım: Sol tarafta model adı, sağ tarafta küçücük ve şık "Yeni" ve "Değiştir" tuşları
    top_col1, top_col2, top_col3 = st.columns([2, 1, 1])
    
    with top_col1:
        st.markdown(f"<p style='color: #4CAF50; font-weight: bold; margin-top: 10px;'>🟢 {st.session_state.selected_ai}</p>", unsafe_allow_html=True)
    
    with top_col2:
        if st.button("➕ Yeni", use_container_width=True):
            st.session_state.chats[st.session_state.selected_ai] = []
            st.rerun()
            
    with top_col3:
        if st.button("🔄 Değiş", use_container_width=True):
            st.session_state.selected_ai = None
            st.rerun()

    st.divider()

    # Mesaj geçmişini ekranda tutma ve gösterme
    current_messages = st.session_state.chats[st.session_state.selected_ai]
    for message in current_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Mesaj yazma çubuğu (WhatsApp tarzı)
    if prompt := st.chat_input("Mesajınızı yazın..."):
        current_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = f"{st.session_state.selected_ai} yanıtı: {prompt}"
        current_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
            
