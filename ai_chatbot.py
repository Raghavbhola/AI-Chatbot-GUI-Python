import tkinter as tk
from tkinter import scrolledtext, font
from fpdf import FPDF

import random
import datetime
import json
                               
from groq import Groq
# import os
client = Groq(api_key=("GROQ_API_KEY"))

import pyttsx3
import speech_recognition as sr

# TTS Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed
engine.setProperty('volume', 1)  # Volume

# STT
recognizer = sr.Recognizer()

speak_enabled = False  # Default OFF

listen_enabled = False  # Default OFF

# ─────────────────────────────────────────
#           CHATBOT LOGIC
# ─────────────────────────────────────────

bot_name = "Buddy"
user_name = None
history = []

def get_response(user_input):
    global bot_name, user_name, history

    text = user_input.strip().lower()

    if not text:
        return "Please type something! 😊"

    # Exit
    if any(w in text for w in ["bye", "exit", "quit", "alvida", "goodbye", "see you", "chalte hai","chalo thik hai", "chalo chalte hai"]):
        save_history()
        return f"Goodbye! Have a great day! 😊 - {bot_name}"

    # Name change
    if any(w in text for w in [
        "change name", "naam badlo", "rename", "apna naam badlo",
        "change your name", "new name", "different name",
        "kya m apka koi name rakhu", "kya m apko kisi hoor name se bulau",
        "kya m tuze kisi hoor naam se bualu", "kya m tuze koi hoor name du"
    ]):
        return "CHANGE_NAME"

    # Date + Time dono saath — SABSE PEHLE
    if (any(t in text for t in ["time", "waqt", "baj", "ghante"]) and
            any(d in text for d in ["date", "aaj", "aj", "today", "din"])):
        today = datetime.datetime.now().strftime("%d %B %Y")
        now   = datetime.datetime.now().strftime("%H:%M:%S")
        return f"📅 Date: {today}  |  ⏰ Time: {now}"

    # Time only
    if any(w in text for w in ["time", "waqt", "kitne baje", "kitne baj gaye", "time kya", "time bata"]):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        return f"Current time is ⏰ {now}"

    # Date only
    if any(w in text for w in [
        "date", "aaj", "aj", "today", "din kya", "din kya hai", "din kya aj", "din kya hai aj",
        "din bataio", "what day", "which date","date kya hai aj"
    ]):
        today = datetime.datetime.now().strftime("%A, %d-%B-%Y")
        return f"Aaj 📅 {today}"

    # Sad — greetings se PEHLE (warna "thik" mein "hi" match hoga)
    if any(w in text for w in [
        "sad", "upset", "dukhi", "depressed", "rona",
        "hurt", "lonely", "stressed", "tension", "pareshan", "cry",
        "mood thik nhi", "mood acha nhi", "dukhi hu", "tension hori"
    ]):
        return random.choice([
            "I'm really sorry to hear that 😔\nWant to talk about it?",
            "Hey, it's okay. Things will get better! 💪",
            f"I'm here for you. What's bothering you? - {bot_name}"
        ])

    # Happy
    if any(w in text for w in [
        "happy", "khush",  "zabardast", "awesome",
        "excited", "wonderful", "fantastic", "amazing", "feeling good", "khush hu"
    ]):
        return random.choice([
            "That's amazing! Keep smiling! 😊",
            "Yayy! So happy for you! 🎉",
            "Wonderful! Spread that happiness! ✨"
        ])


    # User name save
    if any(p in text for p in ["my name is", "mera naam", "main hun", "i am", "call me", "i'm"]):
        for phrase in ["my name is", "mera naam", "main hun", "i am", "call me", "i'm"]:
            if phrase in text:
                user_name = text.split(phrase)[-1].strip().title()
                break
        return f"Nice to meet you, {user_name}! 😊" if user_name else "Cool! What's your name?"

    # Bot name
    if any(w in text for w in [
        "your name", "tera naam", "tera name", "tumhara naam", "naam bataio", "naam kya hai",
        "who are you", "kaun ho", "tum kaun", "tu kon hai", "introduce yourself"
    ]):
        return f"I'm {bot_name}, your friendly AI assistant! 🤖"

    # Joke
    if any(w in text for w in [
        "joke", "funny", "hasao", "hasa", "mazak", "comedy",
        "laugh", "lol", "haha"
    ]):
        jokes = [
            "Why do programmers prefer dark mode?\nBecause light attracts bugs! 🐛",
            "Why did Python programmer wear glasses?\nBecause they couldn't C#! 😂",
            "I told my computer I needed a break...\nNow it won't stop sending me Kit-Kat ads! 🍫",
            "Why is 6 afraid of 7?\nBecause 7 8 9! 😄"
        ]
        return random.choice(jokes)

    
    # Small talk
    if any(w in text.split() for w in ["ok", "okay", "oke", "hmm", "hm", "achha", "accha", "han", "haan", "yep", "yup"]) \
       or any(p in text for p in ["kuch or", "kuch aur", "aur kya", "phir kya","or kya"]):
        return random.choice([
            "Batao! Main sun raha hun 👂",
            "Haan bolo! Kya help chahiye? 😊",
            f"Kya poochna chahte ho? {bot_name} ready hai! 🤖",
            "Kuch aur poochho! 😄"
        ])
# 1. Pehle speak() ✅
def speak(text):
    if speak_enabled:
        engine.say(text)
        engine.runAndWait()

def get_response(user_input):
    text = user_input.strip().lower()
    
    if not text:
        return "Please type something! 😊"
    
    # Exit
    if any(w in text for w in ["bye", "exit"]):
        pass

    else:
        try:
            ai_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": text}]
            )
            return ai_response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return "Sorry! AI se connect nahi ho paya 😔"


def save_history():
    with open("chat_history.json", "w") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────
#           GUI
# ─────────────────────────────────────────

BG_DARK    = "#000000"
BG_CARD    = "#000000"
BG_INPUT   = "#000000"
ACCENT     = "#e94560"
ACCENT2    = "#0f3460"
USER_CLR   = "#00d4ff"
BOT_CLR    = "#e4425d"
TEXT_CLR   = "#ffffff"
MUTED      = "#aaaaaa"
SEND_HOVER = "#ff6b81"


root = tk.Tk()
root.title(f"{bot_name} — AI Chatbot")
root.geometry("480x780")
root.resizable(True, True) #this is for drag the window
root.configure(bg=BG_DARK)

# ── Fonts ──
try:
    title_font  = font.Font(family="Consolas", size=15, weight="bold")
    chat_font   = font.Font(family="Consolas", size=11)
    input_font  = font.Font(family="Consolas", size=11)
    btn_font    = font.Font(family="Consolas", size=11, weight="bold")
    status_font = font.Font(family="Consolas", size=9)
except:
    title_font  = font.Font(size=15, weight="bold")
    chat_font   = font.Font(size=11)
    input_font  = font.Font(size=11)
    btn_font    = font.Font(size=11, weight="bold")
    status_font = font.Font(size=9)

# ── Header ──
header = tk.Frame(root, bg=BG_CARD, pady=12)
header.pack(fill=tk.X)

tk.Label(header, text="🤖", font=font.Font(size=20),
         bg=BG_CARD, fg=ACCENT).pack(side=tk.LEFT, padx=(18, 6))

head_text = tk.Frame(header, bg=BG_CARD)
head_text.pack(side=tk.LEFT)

name_label = tk.Label(head_text, text=bot_name, font=title_font,
                      bg=BG_CARD, fg=TEXT_CLR)
name_label.pack(anchor="w")

tk.Label(head_text, text="● Online", font=status_font,
         bg=BG_CARD, fg="#44ff88").pack(anchor="w")

# ── Divider ──
tk.Frame(root, bg=ACCENT, height=2).pack(fill=tk.X)

# ── Chat Window ──
chat_frame = tk.Frame(root, bg=BG_DARK)
chat_frame.pack(padx=12, pady=10, fill=tk.BOTH, expand=True)

chat_window = scrolledtext.ScrolledText(
    chat_frame,
    wrap=tk.WORD,
    font=chat_font,
    bg=BG_CARD,
    fg=TEXT_CLR,
    insertbackground=ACCENT,
    relief=tk.FLAT,
    padx=12,
    pady=10,
    spacing3=4,
    state=tk.DISABLED,
    cursor="arrow"
)
chat_window.pack(fill=tk.BOTH, expand=True)

# Tags for coloring
chat_window.tag_config("user",    foreground=USER_CLR, font=font.Font(family="Consolas", size=11, weight="bold"))
chat_window.tag_config("bot",     foreground=BOT_CLR,  font=font.Font(family="Consolas", size=11, weight="bold"))
chat_window.tag_config("msg",     foreground=TEXT_CLR)
chat_window.tag_config("time",    foreground=MUTED,    font=status_font)
chat_window.tag_config("divider", foreground=ACCENT2)

# New tags 
chat_window.tag_config("heading",  foreground="#FFD700", font=font.Font(family="Consolas", size=11, weight="bold"))
chat_window.tag_config("bullet",   foreground="#00FF99")
chat_window.tag_config("emoji",    foreground="#FF6B6B")

# ── Input Area ──
tk.Frame(root, bg=ACCENT, height=2).pack(fill=tk.X)

input_frame = tk.Frame(root, bg=BG_INPUT, pady=10)
input_frame.pack(fill=tk.X, padx=12, pady=(6, 10))

entry = tk.Entry(
    input_frame,
    font=input_font,
    bg=BG_INPUT,
    fg=TEXT_CLR,
    insertbackground=USER_CLR,
    relief=tk.FLAT,
    bd=0
)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0), ipady=6)

send_btn = tk.Button(
    input_frame,
    text="Send ➤",
    font=btn_font,
    bg=ACCENT,
    fg="white",
    activebackground=SEND_HOVER,
    activeforeground="white",
    relief=tk.FLAT,
    bd=0,
    padx=14,
    pady=6,
    cursor="hand2"
)
send_btn.pack(side=tk.RIGHT, padx=(8, 6))


# ─────────────────────────────────────────
#      HELPER: Insert message in chat
# ─────────────────────────────────────────

def insert_message(sender, message, sender_tag):
    chat_window.config(state=tk.NORMAL)
    now = datetime.datetime.now().strftime("%H:%M")

    chat_window.insert(tk.END, f"{sender}  ", sender_tag)
    chat_window.insert(tk.END, f"[{now}]\n", "time")

    for line in message.split("\n"):
        stripped = line.strip()
        if stripped.startswith("•"):
            chat_window.insert(tk.END, f"{line}\n", "bullet")
        elif stripped and stripped[0] in ["📌","🎯","🚀","🌍","🗂️","✅","🐍","💻","📊","🐧","⚡","👨"]:
            chat_window.insert(tk.END, f"{line}\n", "heading")
        else:
            chat_window.insert(tk.END, f"{line}\n", "msg")

    chat_window.insert(tk.END, "\n")
    chat_window.config(state=tk.DISABLED)    
    chat_window.yview(tk.END)              

    if sender != "You":
        speak(message)
# ─────────────────────────────────────────
#      NAME CHANGE FLOW
# ─────────────────────────────────────────

waiting_for_new_name = False

def send_message(event=None):
    global bot_name, waiting_for_new_name

    user_input = entry.get().strip()
    if not user_input:
        return

    entry.delete(0, tk.END)

    # If waiting for new bot name
    if waiting_for_new_name:
        waiting_for_new_name = False
        new_name = user_input.title()
        if new_name:
            old_name = bot_name
            bot_name = new_name
            root.title(f"{bot_name} — AI Chatbot")
            name_label.config(text=bot_name)
            insert_message("You", user_input, "user")
            insert_message(bot_name, f"Done! Now call me {bot_name} instead of {old_name}! 😊🎉", "bot")
        else:
            insert_message(bot_name, f"No input? I'll stay as {bot_name}! 😄", "bot")
        history.append({"user": user_input, "bot": f"Name changed to {bot_name}",
                        "time": datetime.datetime.now().strftime("%H:%M:%S")})
        return

    # Normal flow
    insert_message("You", user_input, "user")

    response = get_response(user_input)

    # Special: name change trigger
    if response == "CHANGE_NAME":
        waiting_for_new_name = True
        insert_message(bot_name, "Sure! What would you like to call me? 😊", "bot")
        history.append({"user": user_input, "bot": "Asked for new name",
                        "time": datetime.datetime.now().strftime("%H:%M:%S")})
        return

    insert_message(bot_name, response, "bot")
    history.append ({
        "user": user_input,
        "bot": response,
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "date": datetime.datetime.now().strftime("%d %B %Y")
    })

    # Auto save on bye
    if any(w in user_input.lower() for w in ["bye", "exit", "quit", "goodbye"]):
        root.after(1500, root.destroy)

def listen():
    if listen_enabled:
        with sr.Microphone() as source:
            insert_message(bot_name, "Listening... 🎤", "bot")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="hi-IN")
            entry.delete(0, tk.END)
            entry.insert(0, text)
            send_message()
        except:
            insert_message(bot_name, "Samajh nahi aaya! 😔 Dobara bolo!", "bot")

#Mic toggle button
def toggle_listen():
    global listen_enabled
    listen_enabled = not listen_enabled
    if listen_enabled:
        mic_btn.config(text="🎤", bg="#227846")  # Green ON
        listen()  # Sunna shuru
    else:
        mic_btn.config(text="🎙️", bg=ACCENT2)   # Default OFF

mic_btn = tk.Button(
    input_frame,
    text="🎙️",        # Default OFF
    font=btn_font,
    bg="#1a1a2e",
    fg="white",
    relief=tk.FLAT,
    bd=0,
    padx=10,
    pady=6,
    cursor="hand2",
    command=toggle_listen
)
mic_btn.pack(side=tk.RIGHT, padx=(4, 0))

#Download button
from fpdf import FPDF

def download_pdf():
    if not history:
        insert_message(bot_name, "Koi chat nahi hai abhi! 😔", "bot")
        return
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    
    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"Chat History - {bot_name}", ln=True, align="C")
    pdf.ln(5)
    
    # Messages
    for chat in history:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(0, 150, 255)  # Blue - You
        pdf.cell(0, 8, f"You [{chat.get('date','')} {chat.get('time','')}]", ln=True)
        
        pdf.set_font("Helvetica", size=11)
        pdf.set_text_color(50, 50, 50)  # Dark - Message
        pdf.multi_cell(0, 8, chat['user'])
        pdf.ln(2)
        
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(220, 50, 50)  # Red - Bot
        pdf.cell(0, 8, f"{bot_name}", ln=True)
        
        pdf.set_font("Helvetica", size=11)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 8, chat['bot'])
        pdf.ln(4)
    
    filename = f"chat_{datetime.datetime.now().strftime('%d_%B_%Y_%H_%M')}.pdf"
    pdf.output(filename)
    
    import os
    path = os.path.abspath(filename)
    insert_message(bot_name, f"PDF download ho gayi! 📄\n{path}", "bot")

down_btn = tk.Button(
    input_frame,
    text="⬇️",
    font=btn_font,
    bg=ACCENT2,
    fg="white",
    relief=tk.FLAT,
    bd=0,
    padx=10,
    pady=6,
    cursor="hand2",
    command=download_pdf
)
down_btn.pack(side=tk.RIGHT, padx=(4, 0))

# Tooltip add karo - Button ke baad:
def show_tooltip(event):
    tooltip.place(x=down_btn.winfo_x(), y=down_btn.winfo_y()-25)

def hide_tooltip(event):
    tooltip.place_forget()

tooltip = tk.Label(
    input_frame,
    text="Download Chat",
    bg="#FFD700",
    fg="black",
    font=status_font
)

down_btn.bind("<Enter>", show_tooltip)  # Mouse aaye
down_btn.bind("<Leave>", hide_tooltip)  # Mouse jaye

# chat_window mein right click menu add karo
def right_click_menu(event):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="⬇️ Download This Message", command=lambda: download_selected())
    menu.post(event.x_root, event.y_root)

def download_selected():
    try:
        selected_text = chat_window.get(tk.SEL_FIRST, tk.SEL_LAST)
        if selected_text:
            filename = f"message_{datetime.datetime.now().strftime('%d_%B_%Y_%H_%M')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(selected_text)
            import os
            path = os.path.abspath(filename)
            insert_message(bot_name, f"Message save ho gaya! 💾\n{path}", "bot")
    except:
        insert_message(bot_name, "Pehle message select karo! 😊", "bot")

# chat_window ke baad add karo
chat_window.bind("<Button-3>", right_click_menu)  # Right click

#Toggle button 
def toggle_speak():
    global speak_enabled
    speak_enabled = not speak_enabled
    if speak_enabled:
        speak_btn.config(text="🔊", bg="#228149")  # Green ON
    else:
        speak_btn.config(text="🔇", bg=ACCENT2)    # Default OFF

speak_btn = tk.Button(
    input_frame,
    text="🔇",
    font=btn_font,
    bg="#1a1a2e",
    fg="white",
    relief=tk.FLAT,
    bd=0,
    padx=10,
    pady=6,
    cursor="hand2",
    command=toggle_speak
)
speak_btn.pack(side=tk.RIGHT, padx=(4, 0))

# ── Bind Enter key ──
entry.bind("<Return>", send_message)
send_btn.config(command=send_message)

# ── Welcome message ──
insert_message(bot_name,
               f"Hello! I'm {bot_name}, your AI assistant! 😊\nType 'help' to see what I can do!",
               "bot")

def create_tooltip(widget, text):
    def show(event):
        tooltip = tk.Label(root, text=text, bg="#FFD700", fg="black", font=status_font, padx=4, pady=2)
        tooltip.place(x=event.x_root - root.winfo_x(), y=event.y_root - root.winfo_y() - 30)
        widget._tooltip = tooltip
    def hide(event):
        if hasattr(widget, '_tooltip'):
            widget._tooltip.destroy()
    widget.bind("<Enter>", show)
    widget.bind("<Leave>", hide)

# Buttons ke baad add karo
create_tooltip(send_btn, "Send Message")
create_tooltip(mic_btn,  "Voice Input 🎤")
create_tooltip(speak_btn,"Toggle Voice 🔊")
create_tooltip(down_btn, "Download PDF 💾")

root.focus_force()  
entry.focus_force() 
root.mainloop()
