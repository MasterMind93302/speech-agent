import pyttsx3
import ollama
import speech_recognition
import json
import winsound

#functions
def create_client(): #create an ollama cloud client
    key = open("speech-agent/api_key.txt", "r").read().strip()
    client = ollama.Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + key}
    )
    return client

def get_client_response(client, input): #get response from an AI agent
    user_message = {
        "role": "user",
        "content": str(input)
    }

    messages = []
    try:
        with open("speech-agent/message_history.txt", "r", encoding="utf-8") as fh:
            data = fh.read().strip()
            if data:
                try:
                    loaded = json.loads(data)
                    if isinstance(loaded, list):
                        messages = loaded
                except Exception:
                    messages = []
    except FileNotFoundError:
        messages = []

    if not messages:
        messages.append({
            "role": "system",
            "content": "You are a helpful AI assistant. Respond clearly and use the conversation history when appropriate. Respond with no formatting, as your response must be interpretted by text to speech clearly."
        })

    messages.append(user_message)

    try:
        with open("speech-agent/message_history.txt", "w", encoding="utf-8") as fh:
            json.dump(messages, fh, ensure_ascii=False, indent=2)
    except Exception:
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        pass

    response = client.chat("gemma4:31b-cloud", messages=messages, stream=True)
    return response

def wake_agent(): #wake the AI agent using the wake phrase 'wake up'
    recogniser = speech_recognition.Recognizer()
    try:
        with speech_recognition.Microphone() as source:
            print("Listening for wake phrase...")
            recogniser.adjust_for_ambient_noise(source, duration=0.2)
            audio = recogniser.listen(source)
            text = recogniser.recognize_google(audio)
            text = text.lower()
            print(f"user said: {text}")
            if text == "wake up":
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                print("Wake phrase detected.")
                engine = pyttsx3.init()
                engine.say("agent awake")
                engine.runAndWait()
                return True
            else:
                return False

    except speech_recognition.UnknownValueError:
        print("unable to understand, please speak again.")
        return False
    except Exception as e:
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        print(e)
        return False


def get_speech_as_text(): #get user speech as text
    recogniser = speech_recognition.Recognizer()
    try:
        with speech_recognition.Microphone() as source:
            print("\nListening...")
            recogniser.adjust_for_ambient_noise(source, duration=0.2)
            audio = recogniser.listen(source)
            text = recogniser.recognize_google(audio)
            text = text.lower()
            print(f"user said: {text}")
            return text

    except speech_recognition.UnknownValueError:
        print("unable to understand, please speak again.")
        return "RETRY"
    except Exception as e:
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        print(e)
        return "RETRY"


def text_to_speech(input): #output inputted text as speech
    engine = pyttsx3.init()

    engine.say(input)
    engine.runAndWait()

#run
def main():
    client = create_client()
    while True:
        text = get_speech_as_text()
        if text == "go to sleep":
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            print("Sleep phrase detected.")
            engine = pyttsx3.init()
            engine.say("agent asleep")
            engine.runAndWait()
            return "SLEEP"
        while text == "RETRY":
            text = get_speech_as_text()
            if text == "go to sleep":
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                print("Sleep phrase detected.")
                engine = pyttsx3.init()
                engine.say("agent asleep")
                engine.runAndWait()
                return "SLEEP"

        response = get_client_response(client, text)
        fulltext = ""
        for part in response:
            content = part['message']['content']
            print(content, end='', flush=True)
            fulltext += content

        history = []
        try:
            with open("message_history.txt", "r", encoding="utf-8") as fh:
                data = fh.read().strip()
                if data:
                    try:
                        loaded = json.loads(data)
                        if isinstance(loaded, list):
                            history = loaded
                    except Exception:
                        history = []
        except FileNotFoundError:
            history = []

        history.append({"role": "bot", "content": fulltext})
        try:
            with open("speech-agent/message_history.txt", "w", encoding="utf-8") as fh:
                json.dump(history, fh, ensure_ascii=False, indent=2)
        except Exception:
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            pass

        text_to_speech(fulltext)

if __name__ == "__main__":
    while True:
        try:
            awake = wake_agent()
            if awake is True:
                print("Agent is awake. Listening for user input...")
                status = main()
                if status == "SLEEP":
                    print("Agent is asleep. Listening for wake phrase...")
                    awake = False   
                    continue
            elif awake is False:
                print("Wake phrase not detected.")
                continue
        except KeyboardInterrupt:
            print("Keyboard interrupt detected, exiting...")
            break
        except Exception as e:
            print(e)