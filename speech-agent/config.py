import json
import os

def reset():
    print("preparing to reset...")
    sys_prompt = input("enter a system prompt (leave blank for default): ")
    message_history = open("speech-agent/message_history.txt", "w")
    message_history.write("")
    if sys_prompt == "":
        message = [{
                "role": "system",
                "content": "You are a helpful AI assistant. Respond clearly and use the conversation history when appropriate. Respond with no formatting, as your response must be interpretted by text to speech clearly."
            }]
    else:
        message = [{
                "role": "system",
                "content": sys_prompt
            }]
    json.dump(message, message_history, ensure_ascii=False, indent=2)
    message_history.close()
    print("reset complete. message history cleared and system prompt set.")

def install_requirements():
    print("preparing to install requirements...")
    os.system("pip install -r speech-agent/requirements.txt")

def customise():
    wake_phrase = input("customise wake phrase (press enter to skip): ")
    if wake_phrase != "":
        with open("wake_phrase.txt", "w") as f:
            f.write(wake_phrase)
        print(f"wake phrase set to: {wake_phrase}")
    sleep_phrase = input("customise sleep phrase (press enter to skip): ")
    if sleep_phrase != "":
        with open("sleep_phrase.txt", "w") as f:
            f.write(sleep_phrase)
        print(f"sleep phrase set to: {sleep_phrase}")
    print("customisation complete.")
    exit()

def fetch_phrases():
    with open("wake_phrase.txt", "r") as f:
        wake_phrase = f.read().strip()

    with open("sleep_phrase.txt", "r") as f:
        sleep_phrase = f.read().strip()

    return wake_phrase, sleep_phrase

def main():
    valid = False
    while not valid:
        command = input("Enter a command (reset, install-reqs, exit, customise): ")
        if command == "reset":
            reset()
            valid = True
        elif command == "install-reqs":
            install_requirements()
            valid = True
        elif command == "exit":
                valid = True
                print("exiting...")
                exit()
        elif command == "customise":
            customise()
            valid = True
        else:
            print(f"{command} is not a valid command.")

if __name__ == "__main__":
    main()
