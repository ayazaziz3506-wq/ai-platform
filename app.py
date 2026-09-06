import streamlit as st

# Sayfa ayarları
st.set_page_config(
    page_title="AI Platform",
    page_icon="💬",
    layout="centered"
)

# Arayüzü gizleyen ve üst barı sabitleyen şık stiller
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0e1117; color: #fafafa; }
    
    /* En üstte sabit kalan modern bar */
    .top-bar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #0e1117;
        padding: 10px 15px;
        z-index: 999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #262d3d;
    }
    .content-spacer {
        margin-top: 60px;
    }
    </style>
""", unsafe_allow_html=True)

# Oturum hafızası
if "selected_ai" not in st.session_state:
    st.session_state.selected_ai = None

if "chats" not in st.session_state:
    st.session_state.chats = {"Model 1": [], "Model 2": [], "Model 3": []}

if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = False

# --- SOL MENÜ (3 Çizgiye Basınca Açılan Geçmiş) ---
if st.session_state.sidebar_open:
    with st.sidebar:
        st.markdown("### 📜 Sohbet Geçmişi")
        if st.session_state.selected_ai:
            messages = st.session_state.chats.get(st.session_state.selected_ai, [])
            if not messages:
                st.write("Henüz mesaj yok.")
            else:
                for msg in messages:
                    icon = "👤" if msg["role"] == "user" else "🤖"
                    st.text(f"{icon} {msg['content'][:20]}...")
        else:
            st.write("Model seçilmedi.")

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

# --- 2. SOHBET EKRANI (Sabit Üst Bar & Yan Yana Butonlar) ---
else:
    # Üst kısım: Sol üstte 3 çizgi (menü), ortada model adı, sağda Yeni (+) ve Değiş butonları
    col_menu, col_title, col_new, col_change = st.columns([0.6, 1.4, 1, 1])
    
    with col_menu:
        if st.button("☰", use_container_width=True):
            st.session_state.sidebar_open = not st.session_state.sidebar_open
            st.rerun()
            
    with col_title:
        st.markdown(f"<p style='color: #4CAF50; font-weight: bold; margin-top: 8px;'>🟢 {st.session_state.selected_ai}</p>", unsafe_allow_html=True)
        
    with col_new:
        if st.button("➕ Yeni", use_container_width=True):
            st.session_state.chats[st.session_state.selected_ai] = []
            st.rerun()
            
    with col_change:
        if st.button("🔄 Değiş", use_container_width=True):
            st.session_state.selected_ai = None
            st.rerun()

    st.markdown("<div class='content-spacer'></div>", unsafe_allow_html=True)

    # Mesajları listeleme
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
            
