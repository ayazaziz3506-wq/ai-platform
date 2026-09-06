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
    .block-container { padding-bottom: 5rem; }
    </style>
""", unsafe_allow_html=True)

# Oturum hafızası yönetimi
if "selected_ai" not in st.session_state:
    st.session_state.selected_ai = None

# Tüm sohbetleri tutacak yapı: { "chat_id": {"title": "Kodlama Sohbeti", "model": "Model 1", "messages": [...] } }
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

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
            # Yeni bir sohbet ID'si oluştur ve başlat
            new_id = str(uuid.uuid4())[:8]
            st.session_state.all_chats[new_id] = {"title": "Yeni Sohbet", "model": "Model 1", "messages": []}
            st.session_state.current_chat_id = new_id
            st.rerun()

    with col2:
        if st.button("⚡ Model 2\n\nHızlı AI", use_container_width=True):
            st.session_state.selected_ai = "Model 2"
            new_id = str(uuid.uuid4())[:8]
            st.session_state.all_chats[new_id] = {"title": "Yeni Sohbet", "model": "Model 2", "messages": []}
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
    # Aktif sohbet bilgilerini al
    cur_id = st.session_state.current_chat_id
    if cur_id not in st.session_state.all_chats:
        # Güvenlik önlemi: Eğer sohbet silinmişse yeni oluştur
        new_id = str(uuid.uuid4())[:8]
        st.session_state.all_chats[new_id] = {"title": "Yeni Sohbet", "model": st.session_state.selected_ai, "messages": []}
        st.session_state.current_chat_id = new_id
        cur_id = new_id

    current_chat = st.session_state.all_chats[cur_id]

    # Üst kısım: Aktif model göstergesi
    st.markdown(f"<p style='color: #4CAF50; font-weight: bold;'>🟢 {st.session_state.selected_ai} | Sohbet: {current_chat['title']}</p>", unsafe_allow_html=True)
    st.divider()

    # Mevcut sohbetin mesajlarını ekrana yazdır
    for message in current_chat["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Menü Açıldığında Çıkacak Alan (Geçmiş sohbetler, yeni sohbet, model değiştir)
    if st.session_state.menu_open:
        st.markdown("""
            <div style="background-color: #16192b; padding: 15px; border-radius: 10px; border: 1px solid #262d3d; margin-bottom: 10px;">
            <p style="color: #4CAF50; font-weight: bold; margin-bottom: 10px;">⚙️ Kontrol Paneli</p>
        """, unsafe_allow_html=True)
        
        # İşlem Butonları
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            if st.button("➕ Yeni Sohbet", use_container_width=True):
                # Yeni bir sohbet ID'si üret ve aktif yap
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
        
        # Tüm geçmiş sohbetleri listele ve üzerine tıklayınca o sohbete geri dön
        for chat_id, chat_data in list(st.session_state.all_chats.items()):
            active_mark = "👉 " if chat_id == cur_id else ""
            if st.button(f"{active_mark}{chat_data['title']} ({chat_data['model']})", key=f"chat_btn_{chat_id}", use_container_width=True):
                st.session_state.current_chat_id = chat_id
                st.session_state.selected_ai = chat_data['model']
                st.session_state.menu_open = False
                st.rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)

    # Mesaj Kutusunun Hemen Üstündeki ☰ Menü Butonu
    if st.button("☰ Menü", use_container_width=True):
        st.session_state.menu_open = not st.session_state.menu_open
        st.rerun()

    # Mesaj giriş alanı (En altta sabit)
    if prompt := st.chat_input("Mesajınızı yazın..."):
        # Eğer bu ilk mesajsa, sohbet başlığını kullanıcının yazdığı ilk kelimelere göre güncelle
        if current_chat["title"] == "Yeni Sohbet":
            current_chat["title"] = prompt[:22] + ("..." if len(prompt) > 22 else "")

        # Kullanıcı mesajını kaydet
        current_chat["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Yapay zeka yanıtı
        response = f"{st.session_state.selected_ai} yanıtı: {prompt}"
        current_chat["messages"].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        st.rerun()
        
