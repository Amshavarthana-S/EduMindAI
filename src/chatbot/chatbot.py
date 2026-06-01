
from groq import Groq

def get_client(api_key):
    return Groq(api_key=api_key)

def edumind_chat(client, user_message, mode="emotional", chat_history=[]):

    if mode == "emotional":
        system_prompt = """You are EduMind AI, a friendly student companion.
        Keep responses SHORT (3-4 sentences max).
        Be warm and caring like a best friend.
        Never give long lectures.
        Ask one simple question to understand better.
        Use simple everyday language. No formal tone."""

    elif mode == "academic":
        system_prompt = """You are EduMind AI, a helpful study buddy.
        Keep responses SHORT (3-4 sentences max).
        Give 1-2 specific practical tips only.
        Be friendly and encouraging.
        No long explanations.
        Always end with one simple action to take now."""

    elif mode == "career":
        system_prompt = """You are EduMind AI, a friendly career guide.
        Keep responses SHORT (3-4 sentences max).
        Ask about interests first before suggesting careers.
        Be specific and realistic.
        No long explanations.
        Give one clear next step."""

    messages = [{"role": "system", "content": system_prompt}]

    for chat in chat_history:
        messages.append(chat)

    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=150,
        temperature=0.7
    )

    ai_response = response.choices[0].message.content

    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": ai_response})

    return ai_response, chat_history
