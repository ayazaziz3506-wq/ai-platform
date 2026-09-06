import streamlit as st
import uuid

# Sayfa ayarları
st.set_page_config(
    page_title="Acil Durum AI Platformu",
    page_icon="🚨",
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
    st.markdown("<h2 style='text-align: center; color: #fff; margin-top: 50px;'>Mod Seçimi</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>İhtiyacınıza uygun modu seçin</p>", unsafe_allow_html=True)
    
    st.write("")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📴 Internetsiz\n\n(Offline Mod)", use_container_width=True):
            st.session_state.selected_ai = "Internetsiz"
            new_id = str(uuid.uuid4())[:8]
            st.session_state.all_chats[new_id] = {"title": "Yeni Sohbet", "model": "Internetsiz", "messages": []}
            st.session_state.current_chat_id = new_id
            st.rerun()

    with col2:
        if st.button("⚡ Normal\n\n(Günlük Kullanım)", use_container_width=True):
            st.session_state.selected_ai = "Normal"
            new_id = str(uuid.uuid4())[:8]
            st.session_state.all_chats[new_id] = {"title": "Yeni Sohbet", "model": "Normal", "messages": []}
            st.session_state.current_chat_id = new_id
            st.rerun()

    with col3:
        if st.button("💻 Kodlama\n\n(Teknik Destek)", use_container_width=True):
            st.session_state.selected_ai = "Kodlama"
            new_id = str(uuid.uuid4())[:8]
            st.session_state.all_chats[new_id] = {"title": "Yeni Sohbet", "model": "Kodlama", "messages": []}
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

    # Üst kısım: Aktif mod ve sohbet başlığı
    st.markdown(f"<p style='color: #4CAF50; font-weight: bold;'>🟢 Mod: {st.session_state.selected_ai} | Sohbet: {current_chat['title']}</p>", unsafe_allow_html=True)
    st.divider()

    # Mevcut sohbetin mesajlarını ekrana yazdır
    for message in current_chat["messages"]:
        with st.chat_message(message["role"]):
            if message.get("type") == "image":
                st.image(message["content"], caption="Yüklenen Görsel", use_container_width=True)
            else:
                st.markdown(message["content"])

    # ☰ Menü Paneli
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
            if st.button("🔄 Mod Değiştir", use_container_width=True):
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

    # ➕ Dosya/Fotoğraf Menüsü
    if st.session_state.attachment_open:
        st.markdown("""
            <div style="background-color: #16192b; padding: 12px; border-radius: 10px; border: 1px solid #262d3d; margin-bottom: 5px;">
            <p style="color: #38bdf8; font-weight: bold; font-size: 14px; margin-bottom: 8px;">📎 Medya ve Dosya Ekle</p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Fotoğraf veya Belge Seç", type=["png", "jpg", "jpeg", "pdf", "txt"], key="file_uploadi")
        if uploaded_file is not None:
            current_chat["messages"].append({"role": "user", "type": "image", "content": uploaded_file})
            current_chat["messages"].append({"role": "assistant", "type": "text", "content": f"Görsel alındı ({uploaded_file.name}). [{st.session_state.selected_ai}] modu ile işleniyor."})
            st.session_state.attachment_open = False
            st.rerun()

    # Butonlar
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

    # Mesajlaşma Alanı
    if prompt := st.chat_input("Mesajınızı yazın..."):
        if current_chat["title"] == "Yeni Sohbet":
            current_chat["title"] = prompt[:22] + ("..." if len(prompt) > 22 else "")

        current_chat["messages"].append({"role": "user", "type": "text", "content": prompt})
        
        # Seçilen moda göre özel yanıt
        mode = st.session_state.selected_ai
        if mode == "Internetsiz":
            response = f"📴 **[Internetsiz Mod]:** '{prompt}' yerel veritabanında çevrimdışı işlendi."
        elif mode == "Normal":
            response = f"⚡ **[Normal Mod]:** '{prompt}' talebiniz hızla yanıtlandı."
        else:
            response = f"💻 **[Kodlama Modu]:** '{prompt}' için teknik kod yapısı hazırlandı."

        current_chat["messages"].append({"role": "assistant", "type": "text", "content": response})
        st.session_state.attachment_open = False
        st.rerun()
        
