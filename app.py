import streamlit as st

# Sayfa ayarları
st.set_page_config(
    page_title="AI Platform",
    page_icon="💬",
    layout="centered"
)

# Arayüzü sadeleştiren ve butonların düzgün durmasını sağlayan stiller
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

if "menu_open" not in st.session_state:
    st.session_state.menu_open = False

# --- 1. MODEL SEÇİM EKRANI ---
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

# --- 2. SOHBET EKRANI ---
else:
    # Üst kısım: Sol tarafta aktif model, sağ tarafta sorunsuz çalışan 3 çizgi (☰) menü butonu
    col_info, col_menu_btn = st.columns([3, 1])
    
    with col_info:
        st.markdown(f"<p style='color: #4CAF50; font-weight: bold; margin-top: 10px;'>🟢 {st.session_state.selected_ai}</p>", unsafe_allow_html=True)
    
    with col_menu_btn:
        if st.button("☰ Menü", use_container_width=True):
            st.session_state.menu_open = not st.session_state.menu_open
            st.rerun()

    # 3 Çizgiye basıldığında açılan yan menü (İçinde Yeni, Değiş ve Geçmiş var)
    if st.session_state.menu_open:
        with st.sidebar:
            st.markdown(f"### 🟢 {st.session_state.selected_ai}")
            st.divider()
            
            if st.button("➕ Yeni Sohbet", use_container_width=True):
                st.session_state.chats[st.session_state.selected_ai] = []
                st.session_state.menu_open = False
                st.rerun()
                
            if st.button("🔄 Modeli Değiştir", use_container_width=True):
                st.session_state.selected_ai = None
                st.session_state.menu_open = False
                st.rerun()

            st.divider()
            st.markdown("#### 📜 Sohbet Geçmişi")
            messages = st.session_state.chats.get(st.session_state.selected_ai, [])
            if not messages:
                st.write("Henüz mesaj yok.")
            else:
                for msg in messages:
                    icon = "👤" if msg["role"] == "user" else "🤖"
                    st.text(f"{icon} {msg['content'][:22]}...")

    st.divider()

    # Sohbet mesajları listesi
    current_messages = st.session_state.chats[st.session_state.selected_ai]
    for message in current_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Mesaj giriş alanı
    if prompt := st.chat_input("Mesajınızı yazın..."):
        current_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = f"{st.session_state.selected_ai} yanıtı: {prompt}"
        current_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        st.rerun()
        
