# טוענים את ספריית Tkinter ליצירת חלונות וכפתורים.
import tkinter as tk


# יוצרים ומעצבים את החלון הראשי של המחשבון.
window = tk.Tk()
window.title("מחשבון")
window.geometry("320x460")
window.resizable(False, False)
window.configure(bg="#111827")

# משתנים שמחוברים לצג ולפעולה שמופיעה לידו.
display = tk.StringVar(value="0")
operation_display = tk.StringVar(value="")

# משתנים ששומרים את מצב החישוב הנוכחי.
first_number = None
operation = None
waiting_for_second_number = False


# מוסיפים ספרה לצג כאשר המשתמש לוחץ על כפתור מספר.
def press_number(value):
    global waiting_for_second_number
    current = display.get()

    # אחרי בחירת פעולה, הספרה הראשונה מחליפה את המספר הקודם בצג.
    if waiting_for_second_number or current in ("0", "שגיאה"):
        display.set(value)
        waiting_for_second_number = False

    # אחרת מוסיפים את הספרה לסוף המספר שכבר מופיע.
    else:
        display.set(current + value)


# מוסיפים נקודה עשרונית למספר, אם עדיין אין בו נקודה.
def press_decimal():
    global waiting_for_second_number

    # אם מתחילים מספר חדש, מתחילים אותו בצורה 0 נקודה.
    if waiting_for_second_number:
        display.set("0.")
        waiting_for_second_number = False
        return

    # לא מאפשרים להוסיף יותר מנקודה עשרונית אחת.
    if "." not in display.get():
        display.set(display.get() + ".")


# שומרים את המספר הראשון ואת הפעולה שנבחרה.
def press_operator(symbol):
    global first_number, operation, waiting_for_second_number
    first_number = float(display.get())
    operation = symbol
    operation_display.set(symbol)

    # מסמנים שהמספר הבא יהיה המספר השני בחישוב.
    waiting_for_second_number = True


# מבצעים את פעולת החשבון ומציגים את התוצאה.
def calculate():
    global first_number, operation, waiting_for_second_number

    # אם לא נבחרו מספר ופעולה, אין עדיין מה לחשב.
    if first_number is None or operation is None:
        return

    second_number = float(display.get())

    # בוחרים את פעולת החשבון לפי הסימן שנשמר.
    if operation == "+":
        result = first_number + second_number
    elif operation == "-":
        result = first_number - second_number
    elif operation == "*":
        result = first_number * second_number
    elif operation == "/":

        # מונעים שגיאה מתמטית כאשר מנסים לחלק באפס.
        if second_number == 0:
            display.set("שגיאה")
            first_number = None
            operation = None
            operation_display.set("")
            waiting_for_second_number = False
            return
        result = first_number / second_number

    # מציגים את התוצאה ומנקים את מצב החישוב הקודם.
    display.set(f"{result:g}")
    first_number = None
    operation = None
    operation_display.set("")
    waiting_for_second_number = False


# מאפס את הצג ואת כל הנתונים של החישוב.
def clear():
    global first_number, operation, waiting_for_second_number
    display.set("0")
    operation_display.set("")
    first_number = None
    operation = None
    waiting_for_second_number = False


# אזור שמחזיק את המספר ואת סימן הפעולה.
display_area = tk.Frame(window, bg="#111827")
display_area.pack(fill="x", pady=(14, 0))

operation_label = tk.Label(
    display_area,
    textvariable=operation_display,
    font=("Segoe UI", 16, "bold"),
    fg="#38BDF8",
    bg="#111827",
    padx=8,
)
operation_label.pack(side="left", pady=28)


# הצג הגדול שמציג את המספר הנוכחי או את התוצאה.
display_label = tk.Label(
    display_area,
    textvariable=display,
    font=("Segoe UI", 30),
    fg="#F9FAFB",
    bg="#111827",
    anchor="e",
    padx=18,
)
display_label.pack(side="right", expand=True, fill="x", ipady=28)

# אזור שמחזיק את כל כפתורי המחשבון.
button_area = tk.Frame(window, bg="#111827")
button_area.pack(expand=True, fill="both", padx=14, pady=14)

# צבעים שונים לסוגים השונים של כפתורים.
button_colors = {
    "number": {"bg": "#1F2937", "activebackground": "#374151"},
    "operator": {"bg": "#0EA5E9", "activebackground": "#38BDF8"},
    "clear": {"bg": "#EF4444", "activebackground": "#F87171"},
    "equals": {"bg": "#10B981", "activebackground": "#34D399"},
}


# פונקציה שיוצרת כפתור וממקמת אותו בשורה ובעמודה המתאימות.
def add_button(text, row, column, command, button_type="number"):
    colors = button_colors[button_type]
    button = tk.Button(
        button_area,
        text=text,
        command=command,
        font=("Segoe UI", 16, "bold"),
        fg="#FFFFFF",
        relief="flat",
        bd=0,
        **colors,
    )
    button.grid(row=row, column=column, sticky="nsew", padx=4, pady=4)


# גורמים לשורות ולעמודות להתרחב באופן שווה בתוך החלון.
for row in range(4):
    button_area.rowconfigure(row, weight=1)
for column in range(4):
    button_area.columnconfigure(column, weight=1)

# יוצרים את כפתורי הפעולות.
add_button("נקה", 0, 0, clear, "clear")
add_button("/", 0, 1, lambda: press_operator("/"), "operator")
add_button("*", 0, 2, lambda: press_operator("*"), "operator")
add_button("-", 0, 3, lambda: press_operator("-"), "operator")

# יוצרים את כפתורי הספרות ואת פעולת החיבור.
add_button("7", 1, 0, lambda: press_number("7"))
add_button("8", 1, 1, lambda: press_number("8"))
add_button("9", 1, 2, lambda: press_number("9"))
add_button("+", 1, 3, lambda: press_operator("+"), "operator")
add_button("4", 2, 0, lambda: press_number("4"))
add_button("5", 2, 1, lambda: press_number("5"))
add_button("6", 2, 2, lambda: press_number("6"))
add_button("=", 2, 3, calculate, "equals")

# יוצרים את שאר כפתורי הספרות.
add_button("1", 3, 0, lambda: press_number("1"))
add_button("2", 3, 1, lambda: press_number("2"))
add_button("3", 3, 2, lambda: press_number("3"))
add_button("0", 3, 3, lambda: press_number("0"))

# יוצרים את כפתור הנקודה ומגדירים את השורה החמישית.
add_button(".", 4, 0, press_decimal)
button_area.rowconfigure(4, weight=1)

# מפעילים את החלון ומחכים ללחיצות של המשתמש.
window.mainloop()
