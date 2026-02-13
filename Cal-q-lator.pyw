import customtkinter as ctk
import math

# --- Settings ---
MAIN_FONT = ("Comic Sans MS", 18, "bold")
DISPLAY_FONT = ("Comic Sans MS", 32, "bold")
SMALL_FONT = ("Comic Sans MS", 14, "bold")

# --- Global Variables ---
current_input = "0"
first_operand = None
operator = None
waiting_for_second_operand = False
memory_value = 0
history_list = []

# --- Logic Functions ---
def update_display():
    display_var.set(current_input)

def button_click(char):
    global current_input, waiting_for_second_operand
    if waiting_for_second_operand:
        current_input = char
        waiting_for_second_operand = False
    else:
        if current_input == "0" and char != ".":
            current_input = char
        elif char == "." and "." in current_input:
            pass 
        else:
            current_input += char
    update_display()

def operator_click(op):
    global first_operand, operator, current_input, waiting_for_second_operand
    if first_operand is not None and operator is not None and not waiting_for_second_operand:
        calculate_result()
    try:
        first_operand = float(current_input)
        operator = op
        waiting_for_second_operand = True
    except:
        current_input = "Error"
    update_display()

def calculate_result():
    global current_input, first_operand, operator, waiting_for_second_operand
    if first_operand is None or operator is None: return
    try:
        val = float(current_input)
        res = 0
        if operator == "+": res = first_operand + val
        elif operator == "-": res = first_operand - val
        elif operator == "*": res = first_operand * val
        elif operator == "/": res = first_operand / val if val != 0 else "Error"
        elif operator == "%": res = (first_operand / 100) * val
        elif operator == "^": res = first_operand ** val
        
        if res == "Error":
            current_input = "Error"
        else:
            rounded = round(res, 12)
            current_input = str(int(rounded)) if rounded == int(rounded) else str(rounded)
            history_list.append(f"{first_operand} {operator} {val} = {current_input}")
    except:
        current_input = "Error"
    finally:
        update_display()
        first_operand = None
        operator = None
        waiting_for_second_operand = True

def all_clear():
    global current_input, first_operand, operator, waiting_for_second_operand
    current_input, first_operand, operator, waiting_for_second_operand = "0", None, None, False
    update_display()

def backspace():
    global current_input
    if current_input == "Error": all_clear(); return
    current_input = current_input[:-1] if len(current_input) > 1 and current_input != "0" else "0"
    update_display()

def single_op(mode):
    global current_input, waiting_for_second_operand, memory_value
    try:
        num = float(current_input)
        if mode == "sqrt": res = math.sqrt(num) if num >= 0 else "Error"
        elif mode == "sq": res = num ** 2
        elif mode == "fact": res = math.factorial(int(num)) if num >= 0 else "Error"
        elif mode == "M+": memory_value += num; return
        elif mode == "M-": memory_value -= num; return
        elif mode == "MR": current_input = str(round(memory_value, 12)); update_display(); return
        elif mode == "MC": memory_value = 0; return
        
        if res == "Error": current_input = "Error"
        else:
            rounded = round(res, 12)
            current_input = str(int(rounded)) if rounded == int(rounded) else str(rounded)
    except: current_input = "Error"
    finally: update_display(); waiting_for_second_operand = True

def show_history():
    history_win = ctk.CTkToplevel(root)
    history_win.title("History")
    history_win.geometry("300x400")
    history_win.attributes("-topmost", True)
    txt = ctk.CTkTextbox(history_win, font=("Arial", 14), width=280, height=350)
    txt.pack(padx=10, pady=10)
    for item in history_list:
        txt.insert("end", item + "\n")

# --- UI Setup ---
ctk.set_appearance_mode("light")
root = ctk.CTk()
root.title("Comic Sans-lator")
root.geometry("380x580") 
root.configure(fg_color="#e0f7f4") 

def handle_keypress(event):
    char = event.char
    keysym = event.keysym
    if char.isdigit(): button_click(char)
    elif char == ".": button_click(".")
    elif char in "+-*/^": operator_click(char)
    elif keysym in ["Return", "KP_Enter"]: calculate_result()
    elif keysym == "BackSpace": backspace()
    elif keysym == "Escape": all_clear()

root.bind("<Key>", handle_keypress)

for i in range(4): root.grid_columnconfigure(i, weight=1, pad=5)

top_frame = ctk.CTkFrame(root, fg_color="transparent")
top_frame.grid(row=0, column=0, columnspan=4, padx=15, pady=(15, 5), sticky="nsew")
top_frame.grid_columnconfigure(1, weight=1)

hist_btn = ctk.CTkButton(
    top_frame, text="📜", command=show_history, width=50, height=70, 
    corner_radius=15, font=SMALL_FONT, fg_color="#E6E6FA", text_color="#333333"
)
hist_btn.grid(row=0, column=0, padx=(0, 5))

display_var = ctk.StringVar(value="0")
display_entry = ctk.CTkEntry(
    top_frame, textvariable=display_var, font=DISPLAY_FONT, 
    justify="right", height=70, corner_radius=15, 
    fg_color="#ffffff", text_color="#008080", state="readonly"
)
display_entry.grid(row=0, column=1, sticky="nsew")

colors = {
    "Number": {"fg": "#ffffff", "hover": "#f0fdfa", "text": "#20b2aa"},
    "Operator": {"fg": "#b2ebf2", "hover": "#80deea", "text": "#00838f"},
    "Scientific": {"fg": "#e0f2f1", "hover": "#b2dfdb", "text": "#00695c"},
    "Equals": {"fg": "#4db6ac", "hover": "#26a69a", "text": "#ffffff"}
}

buttons = [
    ("MC", lambda: single_op("MC"), "Scientific"), ("MR", lambda: single_op("MR"), "Scientific"), ("M-", lambda: single_op("M-"), "Scientific"), ("M+", lambda: single_op("M+"), "Scientific"),
    ("π", lambda: button_click(str(round(math.pi, 8))), "Scientific"), ("!", lambda: single_op("fact"), "Scientific"), ("x²", lambda: single_op("sq"), "Scientific"), ("√", lambda: single_op("sqrt"), "Scientific"),
    ("x^y", lambda: operator_click("^"), "Operator"), ("%", lambda: operator_click("%"), "Operator"), ("AC", all_clear, "Operator"), ("÷", lambda: operator_click("/"), "Operator"),
    ("7", lambda: button_click("7"), "Number"), ("8", lambda: button_click("8"), "Number"), ("9", lambda: button_click("9"), "Number"), ("*", lambda: operator_click("*"), "Operator"),
    ("4", lambda: button_click("4"), "Number"), ("5", lambda: button_click("5"), "Number"), ("6", lambda: button_click("6"), "Number"), ("-", lambda: operator_click("-"), "Operator"),
    ("1", lambda: button_click("1"), "Number"), ("2", lambda: button_click("2"), "Number"), ("3", lambda: button_click("3"), "Number"), ("+", lambda: operator_click("+"), "Operator"),
    ("0", lambda: button_click("0"), "Number"), (".", lambda: button_click("."), "Number"), ("->", backspace, "Operator"), ("=", calculate_result, "Equals")
]

row_idx, col_idx = 1, 0
for text, cmd, cat in buttons:
    btn = ctk.CTkButton(
        root, text=text, command=cmd, corner_radius=18, 
        height=48, fg_color=colors[cat]["fg"], hover_color=colors[cat]["hover"], 
        text_color=colors[cat]["text"], font=MAIN_FONT, 
        border_width=2, border_color=colors[cat]["text"]
    )
    btn.grid(row=row_idx, column=col_idx, padx=4, pady=3, sticky="nsew")
    col_idx += 1
    if col_idx >= 4: col_idx = 0; row_idx += 1

for i in range(1, row_idx): root.grid_rowconfigure(i, weight=1)
root.mainloop()
