import turtle
import random

# صفحه
screen = turtle.Screen()
screen.title("ماشین حساب و ماموریت ریاضی")
screen.setup(width=500, height=500)
screen.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()

expression = ""
mode = "menu"  # حالت: menu / calc / mission
user_input = ""
num1 = num2 = answer = 0
op = "+"

# ------------------- رسم دکمه -------------------
def draw_button(x, y, w, h, text, color="lightgray"):
    pen.goto(x, y)
    pen.color("black", color)
    pen.begin_fill()
    for _ in range(2):
        pen.forward(w)
        pen.right(90)
        pen.forward(h)
        pen.right(90)
    pen.end_fill()
    pen.goto(x + w / 2, y - h / 2 - 8)
    pen.write(text, align="center", font=("Arial", 14, "bold"))

# ------------------- منو -------------------
def draw_menu():
    pen.clear()
    pen.goto(0, 200)
    pen.write("📌 انتخاب کنید:", align="center", font=("Arial", 20, "bold"))
    draw_button(-100, 100, 200, 60, "ماشین حساب ساده")
    draw_button(-100, 0, 200, 60, "ماموریت ریاضی")
    screen.update()

def click_menu(x, y):
    global mode
    if -100 < x < 100 and 40 < y < 100:  # ماشین حساب
        mode = "calc"
        draw_calculator()
    elif -100 < x < 100 and -60 < y < 0:  # ماموریت ریاضی
        mode = "mission"
        new_question()
        show_question()

# ------------------- ماشین حساب -------------------
buttons = [
    ("7", -150, 100), ("8", -50, 100), ("9", 50, 100), ("/", 150, 100),
    ("4", -150, 30), ("5", -50, 30), ("6", 50, 30), ("*", 150, 30),
    ("1", -150, -40), ("2", -50, -40), ("3", 50, -40), ("-", 150, -40),
    ("0", -150, -110), (".", -50, -110), ("=", 50, -110), ("+", 150, -110),
    ("C", -150, 170), ("خروج", 50, 170)
]

def draw_display():
    pen.goto(-180, 200)
    pen.color("black")
    pen.begin_fill()
    for _ in range(2):
        pen.forward(360)
        pen.right(90)
        pen.forward(60)
        pen.right(90)
    pen.end_fill()
    pen.goto(0, 170)
    pen.color("white")
    pen.write(expression, align="center", font=("Arial", 18, "bold"))

def draw_calculator():
    pen.clear()
    draw_display()
    for (text, x, y) in buttons:
        draw_button(x, y, 80, 60, text)
    screen.update()

def click_calc(x, y):
    global expression, mode
    for (text, bx, by) in buttons:
        if bx < x < bx + 80 and by - 60 < y < by:
            if text == "=":
                try:
                    expression = str(eval(expression))
                except:
                    expression = "خطا!"
            elif text == "C":
                expression = ""
            elif text == "خروج":
                mode = "menu"
                draw_menu()
                return
            else:
                expression += text
            draw_calculator()

# ------------------- ماموریت ریاضی -------------------
def new_question():
    global num1, num2, op, answer, user_input
    ops = ["+", "-", "*", "/"]
    op = random.choice(ops)
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)

    if op == "+":
        answer = num1 + num2
    elif op == "-":
        answer = num1 - num2
    elif op == "*":
        answer = num1 * num2
    elif op == "/":
        # تضمین می‌کنیم num1 بر num2 بخش‌پذیر باشه
        num1 = num1 * num2
        answer = num1 // num2

    user_input = ""

def show_question():
    pen.clear()
    pen.goto(0, 150)
    pen.write(f"👨 ماموریت: {num1} {op} {num2} = ?", align="center", font=("Arial", 20, "bold"))
    pen.goto(0, 80)
    pen.write(f"پاسخ شما: {user_input}", align="center", font=("Arial", 16, "normal"))
    draw_button(-80, -150, 160, 60, "خروج")
    screen.update()

def key_input(ch):
    global user_input
    if mode != "mission":
        return
    if ch.isdigit() or (ch == "-" and user_input == ""):  # اجازه عدد منفی
        user_input += ch
    elif ch == "BackSpace":
        user_input = user_input[:-1]
    elif ch == "Return":  # Enter
        check_answer()
    show_question()

def check_answer():
    global user_input
    pen.goto(0, 0)
    try:
        if int(user_input) == answer:
            pen.write("✅ آفرین درست بود!", align="center", font=("Arial", 16, "bold"))
            new_question()
        else:
            pen.write("❌ اشتباهه! دوباره تلاش کن.", align="center", font=("Arial", 16, "bold"))
    except:
        pen.write("⚠️ عدد وارد کن!", align="center", font=("Arial", 16, "bold"))
    user_input = ""

def click_mission(x, y):
    global mode
    if -80 < x < 80 and -210 < y < -150:  # دکمه خروج
        mode = "menu"
        draw_menu()

# ------------------- کنترل کلیک -------------------
def handle_click(x, y):
    if mode == "menu":
        click_menu(x, y)
    elif mode == "calc":
        click_calc(x, y)
    elif mode == "mission":
        click_mission(x, y)

# ------------------- کیبورد -------------------
for key in "0123456789":
    screen.onkey(lambda k=key: key_input(k), key)
screen.onkey(lambda: key_input("BackSpace"), "BackSpace")
screen.onkey(lambda: key_input("Return"), "Return")
screen.onkey(lambda: key_input("-"), "minus")

# ------------------- شروع -------------------
screen.onclick(handle_click)
screen.listen()
draw_menu()
screen.mainloop()
