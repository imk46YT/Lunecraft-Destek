import tkinter as tk
from tkinter import scrolledtext, messagebox
from google import genai
import pyperclip
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API")
client = genai.Client(api_key=api_key)

def generate_response():
    user_input = entry.get()
    if user_input.lower() == '!q':
        root.destroy()
        return
    destek_ilkeleri = """
LuneCraft destek ekibi olarak cevap verirken belirli ilkelere ve yapıya göre hareket edilir. Bu yapı, oyunculara karşı nazik, profesyonel ve net bir yaklaşımı temel alır.
Yazının Aşağısına LuneCraft Destek Ekibi yazısı eklemeden.

Her zaman kibar bir giriş yapılır. Örneğin "Merhaba [oyuncu adı]," gibi ifadeler kullanılır. Resmi ama saldırgan olmayan bir üslup tercih edilir. Oyuncunun yaşadığı sorun anlaşılır, ancak yanıtlar tarafsız bir dille verilir. Gerekirse duygusal anlayış gösterilir, ama objektiflik korunur.

Duruma göre cevap yapısı farklılaşır:

Küfür veya hakaret bildirimi:
Bu durum ciddiyetle ele alınır. Oyuncuya üzgün olunduğu ifade edilir. Eğer kanıt varsa işlem yapıldığı belirtilir, yoksa işlem yapılamayacağı açıklanır.
Örnek yanıt:
"Üzgünüz böyle bir durum yaşadığınız için. Kanıtınız incelenmiş, gerekli işlem yapılmıştır."

Eşya kaybı bildirimi:
Eşya iadesi yalnızca şartnamede belirtilen kriterlere göre yapılabilir. Envanter görüntüsü veya görsel kanıt istenir. Eğer kanıt yoksa iade yapılamaz.
Örnek yanıt:
"Eşya iadesi yapılabilmesi için görsel kanıt gereklidir. Elimizde yeterli kanıt olmadığında işlem yapamıyoruz."

Saldırgan veya tehditkâr üslupla yazan oyuncular:
Destek ekibi soğukkanlı kalır, kişisel tartışmalara girilmez. Gerekirse hukuki süreç hatırlatılır.
Örnek yanıt:
"Tarafımıza ilettiğiniz ifadeler kayıt altına alınmıştır. Anayasa ve Türk Ceza Kanunu kapsamında dijital ortamda yapılan hakaret ve tehditler yasal sorumluluk doğurabilir."

Bug veya hata bildirimi:
Bildirim için teşekkür edilir, konu yetkili ekibe iletilir. Oyuncuya doğrudan çözüm süresi verilmez.
Örnek yanıt:
"Geri bildiriminiz için teşekkür ederiz. İlgili ekip bilgilendirilmiştir."

Bedrock PvP ile ilgili durumlar:
Bedrock oyuncularının istemeden PvP açmasına neden olan bug’lar oyuncudan gelen bildirimle kayda alınır. Eşya kaybı varsa, yalnızca geçerli bir kanıtla işlem yapılabilir.
Örnek yanıt:
"Bildirdiğiniz durum için teşekkür ederiz. Bedrock PvP ile ilgili geri bildiriminiz yetkili ekibe iletilmiştir. Eşya iadesi yapılabilmesi için gerekli şartlara uygun kanıt sunulması gerekmektedir."

Genel olarak verilen yanıtlar şu yapıya sahiptir:

Oyuncuya doğrudan hitap edilir.
Oyuncunun yaşadığı durumun farkında olunduğu belirtilir.
Yapılan işlem veya işlem yapılamama nedeni açıklanır.
Gereken bilgi, belge veya şartnameye uygunluk vurgulanır.
Nazik ve olumlu şekilde kapanış yapılır.

Yapılmaması gerekenler:
Küfürlü, alaycı veya küçümseyici ifadeler kullanılmaz.
Oyuncu suçlanmaz, savunmaya geçilmez.
Tartışmaya girilmez.
Polemiğe neden olacak açıklamalardan kaçınılır.
"""
    prompt = f"{destek_ilkeleri}\nOyuncudan gelen mesaj: \"{user_input}\"\nYukarıdaki ilkelere uygun şekilde LuneCraft destek ekibi adına yanıt ver."
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        pyperclip.copy(response.text)
        output_box.config(state='normal')
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, response.text)
        output_box.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Hata", str(e))

root = tk.Tk()
root.title("LuneCraft Destek Yanıt Botu")

tk.Label(root, text="Destek talebini yaz:").pack(pady=5)
entry = tk.Entry(root, width=60)
entry.pack(pady=5)

tk.Button(root, text="Yanıt Oluştur", command=generate_response).pack(pady=5)

output_box = scrolledtext.ScrolledText(root, width=70, height=10, state='disabled')
output_box.pack(pady=10)

root.mainloop()