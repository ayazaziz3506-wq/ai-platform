import streamlit as st

# Sayfa ayarları
st.set_page_config(
    page_title="AI Platform",
    page_icon="💬",
    layout="centered"
)

# Arayüzü şıklaştıran stil kodları
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0e1117; color: #fafafa; }
    </style>
""", unsafe_allow_html=True)

# Oturum hafızasını başlatma
if "selected_ai" not in st.session_state:
    st.session_state.selected_ai = None

if "chats" not in st.session_state:
    st.session_state.chats = {"Model 1": [], "Model 2": [], "Model 3": []}

# --- SOL MENÜ (Geçmiş ve Yeni Sohbet) ---
with st.sidebar:
    st.markdown("### 💬 Menü")
    
    if st.session_state.selected_ai:
        if st.button("🏠 Ana Sayfa (Model Seç)", use_container_width=True):
            st.session_state.selected_ai = None
            st.rerun()
            
        if st.button("➕ Yeni Sohbet", use_container_width=True):
            st.session_state.chats[st.session_state.selected_ai] = []
            st.rerun()

    st.divider()
    st.markdown("#### 📜 Sohbet Geçmişi")
    if st.session_state.selected_ai:
        messages = st.session_state.chats.get(st.session_state.selected_ai, [])
        if not messages:
            st.write("Henüz mesaj yok.")
        else:
            for msg in messages[-5:]:
                icon = "👤" if msg["role"] == "user" else "🤖"
                st.text(f"{icon} {msg['content'][:20]}...")
    else:
        st.write("Model seçilmedi.")

# --- ANA EKRAN ---

# 1. Model Seçim Ekranı
if st.session_state.selected_ai is None:
    st.markdown("<h2 style='text-align: center; color: #fff;'>Yapay Zeka Seçin</h2>", unsafe_allow_html=True)
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

# 2. WhatsApp Tarzı Sohbet Ekranı
else:
    # Üst kısımda hem model adı hem de ana sayfaya dönme butonu
    top_col1, top_col2 = st.columns([3, 1])
    with top_col1:
        st.markdown(f"<h4 style='color: #4CAF50; margin:0;'>🟢 {st.session_state.selected_ai}</h4>", unsafe_allow_html=True)
    with top_col2:
        if st.button("🔄 Değiştir"):
            st.session_state.selected_ai = None
            st.rerun()

    st.divider()

    # Mesajları ekranda tutma
    current_messages = st.session_state.chats[st.session_state.selected_ai]
    for message in current_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Mesajlaşma çubuğu
    if prompt := st.chat_input("Mesajınızı yazın..."):
        current_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = f"{st.session_state.selected_ai} yanıtı: {prompt}"
        current_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
            
