import speech_recognition as sr
from gtts import gTTS
import ollama
import os

r = sr.Recognizer()
mic = sr.Microphone()

print("🎤 Калибрую микрофон...")
with mic as source:
    r.adjust_for_ambient_noise(source)
print("✅ Готов! Говори что хочешь (скажи 'выход' чтобы выйти)\n")

while True:
    print("Слушаю...")
    with mic as source:
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="ru-RU")
        print(f"Вы: {text}")
    except:
        print("❌ Не расслышал, повтори")
        continue

    if text.lower() in ["стоп", "выход", "stop"]:
        print("До свидания!")
        break

    print("🤔 Думаю...")
    try:
        response = ollama.chat(
            model="gpt-oss:20b", messages=[{"role": "user", "content": text}]
        )
        answer = response["message"]["content"]
        print(f"ИИ: {answer}")

        obj = gTTS(text=answer, lang="en")
        obj.save("answer.mp3")
        os.system("start answer.mp3")
    except Exception as e:
        print(f"Ошибка: {e}")