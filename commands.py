def handle_command(command, profile, chat_history):
    if command == "/help":
        print(
            "\nNeoChat Commands:\n"
            "/help   - Show commands\n"
            "/clear  - Clear memory\n"
            "/whoami - Show saved info\n"
            "exit    - Quit\n"
        )
        return True

    if command == "/clear":
        chat_history.clear()
        profile.clear()
        print("NeoChat: Memory cleared 🧹\n")
        return True

    if command == "/whoami":
        if "full_name" in profile:
            print(f"NeoChat: Your name is {profile['full_name']}\n")
        else:
            print("NeoChat: I don't know your name yet.\n")
        return True

    return False
