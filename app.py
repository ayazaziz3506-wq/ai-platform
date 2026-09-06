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

# Oturum hafızası
if "selected_ai" not in st.session_state:
    st.session_state.selected_ai = None

if "chats" not in st.session_state:
    st.session_state.chats = {"Model 1": [], "Model 2": [], "Model 3": []}

if "show_menu" not in st.session_state:
    st.session_state.show_menu = False

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
    # Aktif model adı
    st.markdown(f"<p style='color: #4CAF50; font-weight: bold; margin-bottom: 5px;'>🟢 Aktif: {st.session_state.selected_ai}</p>", unsafe_allow_html=True)

    # İSTEDİĞİN YER: Mesaj kutusunun hemen üstünde duran menü açma tuşu
    if st.button("☰ Menü (Yeni, Değiş, Geçmiş)", use_container_width=True):
        st.session_state.show_menu = not st.session_state.show_menu
        st.rerun()

    # Menü açıldığında görünecek panel
    if st.session_state.show_menu:
        st.markdown("""
            <div style="background-color: #16192b; padding: 12px; border-radius: 8px; border: 1px solid #262d3d; margin: 10px 0;">
            <p style="color: #4CAF50; font-weight: bold; margin-bottom: 8px;">⚙️ Kontrol Paneli</p>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("➕ Yeni Sohbet", use_container_width=True):
                st.session_state.chats[st.session_state.selected_ai] = []
                st.session_state.show_menu = False
                st.rerun()
        with col_btn2:
            if st.button("🔄 Model Değiştir", use_container_width=True):
                st.session_state.selected_ai = None
                st.session_state.show_menu = False
                st.rerun()

        st.markdown("<hr style='margin: 10px 0; border-color: #262d3d;'>", unsafe_allow_html=True)
        st.markdown("<b>📜 Sohbet Geçmişi</b>", unsafe_allow_html=True)
        
        messages = st.session_state.chats.get(st.session_state.selected_ai, [])
        if not messages:
            st.write("Henüz mesaj yok.")
        else:
            for msg in messages:
                icon = "👤" if msg["role"] == "user" else "🤖"
                st.text(f"{icon} {msg['content'][:30]}...")
                
        st.markdown("</div>", unsafe_allow_html=True)

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
        
