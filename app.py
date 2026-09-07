import streamlit as st
import os

# Sayfa yapılandırması (Mobil uyumlu ve sade)
st.set_page_config(
    page_title="Yapay Zeka Platformu",
    page_icon="🤖",
    layout="centered"
)

# Groq API anahtarını kontrol et
groq_api_key = None
try:
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

if not groq_api_key:
    groq_api_key = os.getenv("GROQ_API_KEY")

# Groq kütüphanesini yüklemeyi dene
client = None
if groq_api_key:
    try:
        from groq import Groq
        client = Groq(api_key=groq_api_key)
    except Exception as e:
        pass

# Oturum geçmişi ve sohbet listesi yönetimi
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "sohbet_1"

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {
        "sohbet_1": {"title": "Yeni Sohbet", "messages": []}
    }

# Üst Menü / Kenar Çubuğu (Artı butonu ve dosya yükleme burada)
with st.sidebar:
    st.title("⚙️ Menü")
    
    if st.button("➕ Yeni Sohbet Başlat", use_container_width=True):
        new_id = f"sohbet_{len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[new_id] = {"title": "Yeni Sohbet", "messages": []}
        st.session_state.current_chat_id = new_id
        st.rerun()
        
    st.markdown("---")
    
    # Dosya / Kod / Fotoğraf yükleme alanı sol menüye alındı
    st.subheader("📎 Dosya Yükleme")
    uploaded_file = st.file_uploader("Dosya veya Kod Seç", type=["png", "jpg", "jpeg", "txt", "html", "py", "pdf"])
    
    st.markdown("---")
    
    # Mod seçimi
    st.subheader("🔄 Mod Seçimi")
    mode = st.radio(
        "Çalışma Modu:",
        ["Internetsiz (Offline)", "Normal", "Kodlama"],
        index=0
    )
    
    st.markdown("---")
    
    # Geçmiş sohbetleri listeleme
    st.subheader("💬 Sohbet Geçmişi")
    for chat_id, chat_data in list(st.session_state.all_chats.items()):
        if st.button(chat_data["title"], key=f"btn_{chat_id}", use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()
            
    st.markdown("---")
    if st.button("🧹 Sohbeti Temizle", use_container_width=True):
        st.session_state.all_chats[st.session_state.current_chat_id]["messages"] = []
        st.rerun()

# Aktif sohbetin mesajlarına erişim
current_chat = st.session_state.all_chats[st.session_state.current_chat_id]

# Ana Ekran Başlığı
if mode == "Internetsiz (Offline)":
    st.success("🟢 Mod: Internetsiz | Yerel mod aktif.")
elif mode == "Normal":
    st.info("⚡ Mod: Normal (GPT OSS)")
else:
    st.warning("💻 Mod: Kodlama (GPT OSS)")

st.markdown("---")

# Geçmiş mesajları ekrana yazdır
for message in current_chat["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan girdi al
prompt = st.chat_input("Mesajınızı yazın...")

if prompt or uploaded_file:
    user_message = prompt if prompt else ""
    
    # Eğer dosya yüklendiyse içeriğini okumaya çalış veya adını ekle
    file_content_text = ""
    if uploaded_file is not None:
        try:
            # Metin bazlı dosyaları (html, txt, py vb.) doğrudan okuyabilir
            file_content_text = uploaded_file.read().decode("utf-8", errors="ignore")
            user_message += f"\n\n--- Yüklenen Dosya ({uploaded_file.name}) ---\n```\n{file_content_text[:3000]}\n```"
        except Exception:
            user_message += f"\n\n*(Eklenen dosya: {uploaded_file.name})*"
    
    # Eğer ilk mesajsa sohbet başlığını güncelle
    if len(current_chat["messages"]) == 0 and prompt:
        current_chat["title"] = prompt[:20] + ("..." if len(prompt) > 20 else "")
    elif len(current_chat["messages"]) == 0 and uploaded_file:
        current_chat["title"] = f"Dosya: {uploaded_file.name[:10]}"
        
    # Kullanıcı mesajını ekle
    current_chat["messages"].append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    # Asistan yanıtı
    with st.chat_message("assistant"):
        response_content = ""
        
        if mode == "Internetsiz (Offline)":
            response_content = f"[Internetsiz (Offline) Mod]: Mesajınız ve dosyanız yerel olarak işleme alındı."
            st.markdown(response_content)
            
        elif client is None:
            response_content = "⚠️ Groq API anahtarı bulunamadı veya geçersiz!"
            st.error(response_content)
            
        else:
            try:
                model_name = "openai/gpt-oss-20b"
                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in current_chat["messages"]
                    ],
                    model=model_name,
                )
                response_content = chat_completion.choices[0].message.content
                st.markdown(response_content)
                
            except Exception as e:
                response_content = f"Bağlantı hatası oluştu: {e}"
                st.error(response_content)
        
        # Asistan yanıtını hafızaya kaydet
        current_chat["messages"].append({"role": "assistant", "content": response_content})
        
