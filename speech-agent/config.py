import json
import os

def reset():
    print("preparing to reset...")
    sys_prompt = input("enter a system prompt (leave blank for default): ")
    message_history = open("message_history.txt", "w")
    message_history.write("")
    if sys_prompt == "":
        message = {
                "role": "system",
                "content": "You are a helpful AI assistant. Respond clearly and use the conversation history when appropriate. Respond with no formatting, as your response must be interpretted by text to speech clearly."
            }
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
    os.system("pip install -r requirements.txt")


def main():
    valid = False
    while not valid:
        command = input("Enter a command (reset, install-reqs, exit): ")
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
        else:
            print(f"{command} is not a valid command.")

if __name__ == "__main__":
    main()
