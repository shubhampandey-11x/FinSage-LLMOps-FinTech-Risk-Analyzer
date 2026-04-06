from collections import deque

class ConversationMemory:
    def __init__(self, max_len=5):
        self.history = deque(maxlen=max_len)

    def add(self, user_input, response):
        self.history.append({
            "user": user_input,
            "assistant": response
        })

    def get_context(self):
        context = ""
        for chat in self.history:
            context += f"User: {chat['user']}\nAssistant: {chat['assistant']}\n"
        return context