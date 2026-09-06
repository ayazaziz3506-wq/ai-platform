import streamlit as st
import uuid

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
    .block-container { padding-bottom: 6rem; }
    </style>
""", unsafe_allow_html=True)

# Oturum hafızası yönetimi
if "selected_ai" not in st.session_state:
    st.session_state.selected_ai = None

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "menu_open" not in st.session_state:
    st.session_state.menu_open = False

if "attachment_open" not in st.session_state:
    st.session_state.attachment_open = False

# --- 1. MODEL SEÇİM EKRANI ---
if st.session_state.selected_ai is None:
    st.markdown("<h2 style='text-align: center; color: #fff; margin-top: 50px;'>Yapay Zeka Seçin</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>Sohbet etmek istediğiniz modeli seçin</p>", unsafe_allow_html=True)
    
    st.write("")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🤖 Llama 3 8B\n\n(Lokal/Offline)", use_container_width=True):
            st.session_state.selected_ai = "Llama 3 8B"
            new_id = str(uuid.uuid4())[:8]
            st.session_state.all_chats[new_id] = {"title": "Yeni Sohbet", "model": "Llama 3 8B", "messages": []}
            st.session_state.current_chat_id = new_id
            st.rerun()

    with col2:
        if st.button("⚡ Llama 3.2 3B\n\n(Hızlı AI)", use_container_width=True):
            st.session_state.selected_ai = "Llama 3.2 3B"
            new_id = str(uuid.uuid4())[:8]
            st.session_state.all_chats[new_id] = {"title": "Yeni Sohbet", "model": "Llama 3.2 3B", "messages": []}
            st.session_state.current_chat_id = new_id
            st.rerun()

    with col3:
        if st.button("💡 Model 3\n\nYaratıcı", use_container_width=True):
            st.session_state.selected_ai = "Model 3"
            new_id = str(uuid.uuid4())[:8]
            st.session_state.all_chats[new_id] = {"title": "Yeni Sohbet", "model": "Model 3", "messages": []}
            st.session_state.current_chat_id = new_id
            st.rerun()

# --- 2. SOHBET EKRANI ---
else:
    cur_id = st.session_state.current_chat_id
    if cur_id not in st.session_state.all_chats:
        new_id = str(uuid.uuid4())[:8]
        st.session_state.all_chats[new_id] = {"title": "Yeni Sohbet", "model": st.session_state.selected_ai, "messages": []}
        st.session_state.current_chat_id = new_id
        cur_id = new_id

    current_chat = st.session_state.all_chats[cur_id]

    # Üst kısım: Aktif model ve sohbet başlığı
    st.markdown(f"<p style='color: #4CAF50; font-weight: bold;'>🟢 {st.session_state.selected_ai} | Sohbet: {current_chat['title']}</p>", unsafe_allow_html=True)
    st.divider()

    # Mevcut sohbetin mesajlarını ekrana yazdır
    for message in current_chat["messages"]:
        with st.chat_message(message["role"]):
            if message.get("type") == "image":
                st.image(message["content"], caption="Yüklenen Görsel", use_container_width=True)
            else:
                st.markdown(message["content"])

    # ☰ Menü Açıldığında Çıkacak Alan
    if st.session_state.menu_open:
        st.markdown("""
            <div style="background-color: #16192b; padding: 15px; border-radius: 10px; border: 1px solid #262d3d; margin-bottom: 10px;">
            <p style="color: #4CAF50; font-weight: bold; margin-bottom: 10px;">⚙️ Kontrol Paneli</p>
        """, unsafe_allow_html=True)
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            if st.button("➕ Yeni Sohbet", use_container_width=True):
                new_id = str(uuid.uuid4())[:8]
                st.session_state.all_chats[new_id] = {"title": "Yeni Sohbet", "model": st.session_state.selected_ai, "messages": []}
                st.session_state.current_chat_id = new_id
                st.session_state.menu_open = False
                st.rerun()
        with col_m2:
            if st.button("🔄 Model Değiştir", use_container_width=True):
                st.session_state.selected_ai = None
                st.session_state.current_chat_id = None
                st.session_state.menu_open = False
                st.rerun()

        st.markdown("<hr style='margin: 15px 0; border-color: #262d3d;'>", unsafe_allow_html=True)
        st.markdown("<b style='color: #fafafa;'>📜 Geçmiş Sohbetler</b>", unsafe_allow_html=True)
        
        for chat_id, chat_data in list(st.session_state.all_chats.items()):
            active_mark = "👉 " if chat_id == cur_id else ""
            if st.button(f"{active_mark}{chat_data['title']} ({chat_data['model']})", key=f"chat_btn_{chat_id}", use_container_width=True):
                st.session_state.current_chat_id = chat_id
                st.session_state.selected_ai = chat_data['model']
                st.session_state.menu_open = False
                st.rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)

    # ➕ Artı Butonuna Basıldığında Açılan Dosya/Fotoğraf Menüsü
    if st.session_state.attachment_open:
        st.markdown("""
            <div style="background-color: #16192b; padding: 12px; border-radius: 10px; border: 1px solid #262d3d; margin-bottom: 5px;">
            <p style="color: #38bdf8; font-weight: bold; font-size: 14px; margin-bottom: 8px;">📎 Medya ve Dosya Ekle</p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Fotoğraf veya Belge Seç", type=["png", "jpg", "jpeg", "pdf", "txt"], key="file_uploadi")
        if uploaded_file is not None:
            current_chat["messages"].append({"role": "user", "type": "image", "content": uploaded_file})
            current_chat["messages"].append({"role": "assistant", "type": "text", "content": f"Dosyanı aldım! ({uploaded_file.name}) Acil durum için hazır."})
            st.session_state.attachment_open = False
            st.rerun()

    # Mesaj Kutusunun Hemen Üstündeki Butonlar: [ ☰ Menü ] ve [ ➕ Ekle ]
    col_btn_menu, col_btn_plus = st.columns([4, 1])
    with col_btn_menu:
        if st.button("☰ Menü", use_container_width=True):
            st.session_state.menu_open = not st.session_state.menu_open
            st.session_state.attachment_open = False
            st.rerun()
    with col_btn_plus:
        if st.button("➕", use_container_width=True):
            st.session_state.attachment_open = not st.session_state.attachment_open
            st.session_state.menu_open = False
            st.rerun()

    # Mesaj giriş alanı
    if prompt := st.chat_input("Acil durum mesajınızı yazın..."):
        if current_chat["title"] == "Yeni Sohbet":
            current_chat["title"] = prompt[:22] + ("..." if len(prompt) > 22 else "")

        current_chat["messages"].append({"role": "user", "type": "text", "content": prompt})
        
        # Yapay zeka yanıt mekanizması (İleride yerel model bağlandığında burası güncellenecek)
        response = f"[{st.session_state.selected_ai} Yanıtı]: {prompt} (Acil durum modu aktif)"
        
        current_chat["messages"].append({"role": "assistant", "type": "text", "content": response})
        st.session_state.attachment_open = False
        st.rerun()
        
