import tkinter as tk

BG = "#0D0D0D"
ACCENT = "#00FF41"
DARK = "#1A1A1A"

class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔢 Calculator")
        self.root.configure(bg=BG)
        self.root.geometry("320x480")
        self.root.resizable(False, False)
        self.expr = ""
        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(self.root, text="🔢 Calculator",
                bg=BG, fg=ACCENT,
                font=("monospace", 12, "bold")).pack(pady=5)

        self.display = tk.Entry(
            self.root, bg=DARK, fg=ACCENT,
            font=("monospace", 20),
            justify=tk.RIGHT,
            insertbackground=ACCENT,
            relief=tk.FLAT)
        self.display.pack(fill=tk.X, padx=10, pady=5)

        buttons = [
            ['C','±','%','÷'],
            ['7','8','9','×'],
            ['4','5','6','-'],
            ['1','2','3','+'],
            ['0','.','⌫','='],
        ]

        for row in buttons:
            f = tk.Frame(self.root, bg=BG)
            f.pack(fill=tk.X, padx=10, pady=2)
            for b in row:
                bg = ACCENT if b=='=' else DARK
                fg = BG if b=='=' else ACCENT
                tk.Button(f, text=b,
                         bg=bg, fg=fg,
                         font=("monospace", 14),
                         relief=tk.FLAT,
                         command=lambda x=b: self.press(x),
                         cursor="hand2").pack(
                             side=tk.LEFT,
                             expand=True,
                             fill=tk.X,
                             padx=2, pady=2,
                             ipady=10)

    def press(self, b):
        if b == 'C':
            self.expr = ""
        elif b == '=':
            try:
                e = self.expr.replace(
                    '×','*').replace('÷','/')
                self.expr = str(eval(e))
            except:
                self.expr = "Error"
        elif b == '⌫':
            self.expr = self.expr[:-1]
        elif b == '±':
            if self.expr:
                self.expr = self.expr[1:] \
                    if self.expr[0]=='-' \
                    else '-'+self.expr
        else:
            self.expr += b
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expr)

if __name__ == "__main__":
    Calculator()
