import ollama

# Kullanıcı mesaj yazdığında lokal modelden yanıt almak için:
try:
    response_obj = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': prompt},
    ])
    response = response_obj['message']['content']
except Exception as e:
    response = "Lokal model şu an çalışmıyor, lütfen bağlantıyı kontrol edin."
    
