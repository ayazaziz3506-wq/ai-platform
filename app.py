import streamlit as st

# Sayfa ayarları
st.set_page_config(
    page_title="AI Platform",
    page_icon="💬",
    layout="centered"
)

# Arayüzü sadeleştiren ve şıklaştıran stiller
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0e1117; color: #fafafa; }
    </style>
""", unsafe_allow_html=True)

# Oturum durumu (Hafıza) yönetimi
if "selected_ai" not in st.session_state:
    st.session_state.selected_ai = None

if "chats" not in st.session_state:
    st.session_state.chats = {"Model 1": [], "Model 2": [], "Model 3": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# --- SOL MENÜ (3 Çizgi Menüsü, Yeni Sohbet ve Geçmiş) ---
with st.sidebar:
    st.markdown("### 💬 Sohbet Menüsü")
    
    # Yeni Sohbet Butonu
    if st.button("➕ Yeni Sohbet", use_container_width=True):
        if st.session_state.selected_ai:
            st.session_state.chats[st.session_state.selected_ai] = []
            st.rerun()

    st.divider()
    
    st.markdown("#### 📜 Sohbet Geçmişi")
    if st.session_state.selected_ai:
        messages = st.session_state.chats.get(st.session_state.selected_ai, [])
        if not messages:
            st.write("Henüz mesaj yok.")
        else:
            for i, msg in enumerate(messages[-5:]): # Son 5 mesajın özeti
                role_icon = "👤" if msg["role"] == "user" else "🤖"
                st.text(f"{role_icon} {msg['content'][:25]}...")
    else:
        st.write("Önce bir model seçin.")

    st.divider()
    if st.session_state.selected_ai:
        if st.button("🔄 Model Seçimine Dön", use_container_width=True):
            st.session_state.selected_ai = None
            st.rerun()

# --- ANA EKRAN ---

# 1. AŞAMA: Model Seçim Ekranı
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

# 2. AŞAMA: WhatsApp Tarzı Temiz Sohbet Ekranı
else:
    st.markdown(f"<h4 style='color: #4CAF50;'>🟢 Aktif Model: {st.session_state.selected_ai}</h4>", unsafe_allow_html=True)
    st.divider()

    # Seçilen modelin mesaj geçmişini ekrana yazdır
    current_messages = st.session_state.chats[st.session_state.selected_ai]
    
    for message in current_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Mesaj Giriş Alanı (Sohbeti kaybetmeme garantili hafıza)
    if prompt := st.chat_input("Mesajınızı yazın..."):
        # Kullanıcı mesajını kaydet ve göster
        current_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Yapay zeka yanıt simülasyonu
        response = f"{st.session_state.selected_ai} yanıtı: {prompt}"
        current_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
            
