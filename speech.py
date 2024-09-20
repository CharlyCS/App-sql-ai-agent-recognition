import speech_recognition as sr
r = sr.Recognizer()

def transcription():
    with sr.Microphone() as source:
        print("Por favor, hable ahora...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            texto = r.recognize_google(audio, language="es-ES")
            print(texto)
            return texto
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError as e:
            print(f"Error al conectar: {e}")
