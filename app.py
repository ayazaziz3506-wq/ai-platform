import streamlit as st

# Sayfa ayarları
st.set_page_config(
    page_title="AI Platform",
    page_icon="💬",
    layout="centered"
)

# Arayüzü sadeleştiren stiller
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0e1117; color: #fafafa; }
    .block-container { padding-bottom: 5rem; }
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
    # Aktif model göstergesi
    st.markdown(f"<p style='color: #4CAF50; font-weight: bold;'>🟢 {st.session_state.selected_ai}</p>", unsafe_allow_html=True)
    st.divider()

    # Sohbet mesajları listesi
    current_messages = st.session_state.chats[st.session_state.selected_ai]
    for message in current_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Menü Açıldığında Çıkacak Alan (Butonun hemen üstünde panel açılır)
    if st.session_state.menu_open:
        st.markdown("""
            <div style="background-color: #16192b; padding: 15px; border-radius: 10px; border: 1px solid #262d3d; margin-bottom: 10px;">
            <p style="color: #4CAF50; font-weight: bold; margin-bottom: 10px;">⚙️ Kontrol Paneli</p>
        """, unsafe_allow_html=True)
        
        # İşlem Butonları (Yan yana iki buton)
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            if st.button("➕ Yeni Sohbet", use_container_width=True):
                st.session_state.chats[st.session_state.selected_ai] = []
                st.session_state.menu_open = False
                st.rerun()
        with col_m2:
            if st.button("🔄 Model Değiştir", use_container_width=True):
                st.session_state.selected_ai = None
                st.session_state.menu_open = False
                st.rerun()

        st.markdown("<hr style='margin: 15px 0; border-color: #262d3d;'>", unsafe_allow_html=True)
        st.markdown("<b style='color: #fafafa;'>📜 Sohbet Geçmişi</b>", unsafe_allow_html=True)
        
        # Geçmiş Mesajların Listesi
        if not current_messages:
            st.markdown("<p style='color: gray; font-size: 13px;'>Bu modelle henüz sohbet geçmişi yok.</p>", unsafe_allow_html=True)
        else:
            for idx, msg in enumerate(current_messages):
                icon = "👤" if msg["role"] == "user" else "🤖"
                st.markdown(f"<p style='font-size: 13px; color: #ccc; margin: 4px 0;'>{icon} {msg['content'][:35]}...</p>", unsafe_allow_html=True)
                
        st.markdown("</div>", unsafe_allow_html=True)

    # Mesaj Kutusunun Hemen Üstündeki ☰ Menü Butonu
    if st.button("☰ Menü", use_container_width=True):
        st.session_state.menu_open = not st.session_state.menu_open
        st.rerun()

    # Mesaj giriş alanı (En altta sabit)
    if prompt := st.chat_input("Mesajınızı yazın..."):
        current_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = f"{st.session_state.selected_ai} yanıtı: {prompt}"
        current_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        st.rerun()
        
