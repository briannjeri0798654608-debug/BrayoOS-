import tkinter as tk

BG = "#0D0D0D"
ACCENT = "#00FF41"
TEXT = "#FFFFFF"
DARK = "#1A1A1A"

class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔢 Calculator")
        self.root.configure(bg=BG)
        self.root.geometry("350x500")
        self.root.resizable(False, False)
        self.expression = ""
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root,
                text="🔢 BrayoOS Calculator",
                bg=BG, fg=ACCENT,
                font=("monospace", 12,
                      "bold")).pack(pady=5)

        # Display
        self.display = tk.Entry(
            self.root,
            bg=DARK, fg=ACCENT,
            font=("monospace", 20),
            justify=tk.RIGHT,
            insertbackground=ACCENT,
            relief=tk.FLAT)
        self.display.pack(
            fill=tk.X, padx=10, pady=5)

        # Buttons
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '⌫', '='],
        ]

        for row in buttons:
            frame = tk.Frame(self.root, bg=BG)
            frame.pack(fill=tk.X, padx=10,
                      pady=2)
            for btn in row:
                color = ACCENT \
                    if btn == '=' \
                    else DARK
                fg = BG if btn == '=' else ACCENT
                tk.Button(
                    frame, text=btn,
                    bg=color, fg=fg,
                    font=("monospace", 14),
                    relief=tk.FLAT,
                    command=lambda b=btn:
                    self.press(b),
                    cursor="hand2").pack(
                        side=tk.LEFT,
                        expand=True,
                        fill=tk.X,
                        padx=2, pady=2,
                        ipady=10)

    def press(self, btn):
        if btn == 'C':
            self.expression = ""
        elif btn == '=':
            try:
                expr = self.expression
                expr = expr.replace('×', '*')
                expr = expr.replace('÷', '/')
                result = eval(expr)
                self.expression = str(result)
            except:
                self.expression = "Error"
        elif btn == '⌫':
            self.expression = \
                self.expression[:-1]
        elif btn == '±':
            if self.expression:
                if self.expression[0] == '-':
                    self.expression = \
                        self.expression[1:]
                else:
                    self.expression = \
                        '-' + self.expression
        elif btn == '%':
            try:
                val = float(self.expression)
                self.expression = str(val/100)
            except:
                pass
        else:
            self.expression += btn

        self.display.delete(0, tk.END)
        self.display.insert(
            0, self.expression)

if __name__ == "__main__":
    Calculator()
