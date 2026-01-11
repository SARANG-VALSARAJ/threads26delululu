import tkinter as tk
from tkinter import ttk, messagebox
import math
import random

# -------------------- Main Window --------------------
root = tk.Tk()
root.title("AURA FASHION AI")
root.attributes("-fullscreen", True)
root.configure(bg="black")
root.bind("<Escape>", lambda e: root.destroy())

# -------------------- Canvas Background --------------------
canvas = tk.Canvas(root, bg="#050510", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# -------------------- Animated Gradient Stars --------------------
stars = []

def create_stars():
    for _ in range(120):
        x = random.randint(0, root.winfo_screenwidth())
        y = random.randint(0, root.winfo_screenheight())
        r = random.randint(1, 2)
        star = canvas.create_oval(x, y, x+r, y+r, fill="#ffffff", outline="")
        stars.append(star)

def animate_stars():
    for star in stars:
        canvas.move(star, 0, 0.3)
        if canvas.coords(star)[1] > root.winfo_screenheight():
            canvas.move(star, 0, -root.winfo_screenheight())
    root.after(30, animate_stars)

create_stars()
animate_stars()

# -------------------- Wave Animation --------------------
wave_offset = 0

def animate_wave():
    global wave_offset
    canvas.delete("wave")
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    points = []
    for x in range(0, w, 15):
        y = int(80 * math.sin((x + wave_offset) * 0.02) + h * 0.75)
        points.extend([x, y])
    canvas.create_line(points, fill="#ff2fd2", width=3, smooth=True, tag="wave")
    wave_offset += 5
    root.after(40, animate_wave)

animate_wave()

# -------------------- Glass Panel --------------------
panel = tk.Frame(canvas, bg="#111122", bd=0)
panel.place(relx=0.5, rely=0.35, anchor="center", width=650, height=460)

# Glow Border
glow = canvas.create_rectangle(0, 0, 0, 0, outline="#ff2fd2", width=3)
def update_glow():
    x = panel.winfo_x()
    y = panel.winfo_y()
    w = panel.winfo_width()
    h = panel.winfo_height()
    canvas.coords(glow, x-4, y-4, x+w+4, y+h+4)
    root.after(50, update_glow)
update_glow()

# -------------------- Title Animation --------------------
title = tk.Label(
    panel,
    text="AURA FASHION AI",
    font=("Helvetica", 30, "bold"),
    fg="#ff2fd2",
    bg="#111122"
)
title.pack(pady=15)

def animate_title():
    colors = ["#ff2fd2", "#00f5ff", "#ffd700", "#7fff00"]
    title.config(fg=random.choice(colors))
    root.after(600, animate_title)

animate_title()

# -------------------- Inputs --------------------
style = ttk.Style()
style.theme_use("default")
style.configure("TCombobox", font=("Helvetica", 13))

gender_var = tk.StringVar(value="Female")
occasion_var = tk.StringVar(value="Casual")
weather_var = tk.StringVar(value="Sunny")

def field(label, var, values):
    tk.Label(panel, text=label, fg="white", bg="#111122", font=("Helvetica", 14)).pack(pady=(8,2))
    ttk.Combobox(panel, textvariable=var, values=values, state="readonly").pack()

field("Gender", gender_var, ["Female", "Male"])
field("Occasion", occasion_var, ["Casual", "Formal", "Party", "Wedding"])
field("Climate", weather_var, ["Sunny", "Hot", "Rainy", "Cold"])

# -------------------- AI Logic --------------------
def recommend_dress():
    g = gender_var.get().lower()
    o = occasion_var.get().lower()
    w = weather_var.get().lower()

    if not g or not o or not w:
        messagebox.showwarning("Alert", "Select all fields")
        return

    if g == "female":
        data = {
            "sunny": ["Silk Maxi Dress", "Boho Jumpsuit", "Crop Top & Skirt"],
            "hot": ["Linen Co-ord Set", "Sleeveless Midi"],
            "rainy": ["Trench Coat Dress", "Layered Kurti"],
            "cold": ["Wool Sweater Dress", "Long Coat Look"]
        }
        if o == "wedding":
            suggestions = ["Royal Saree", "Designer Lehenga"]
        else:
            suggestions = data[w]
    else:
        data = {
            "sunny": ["Linen Shirt & Chinos", "Resort Wear Set"],
            "hot": ["Cotton Shirt & Shorts"],
            "rainy": ["Stylish Rain Jacket"],
            "cold": ["Overcoat & Boots Look"]
        }
        if o == "wedding":
            suggestions = ["Sherwani", "Indo-Western Suit"]
        else:
            suggestions = data[w]

    show_result(suggestions)

# -------------------- Result Animation --------------------
result = tk.Text(panel, height=5, bg="#1a1a3d", fg="#ffffff",
                 font=("Helvetica", 14), wrap="word", bd=0)
result.pack(pady=15, padx=30, fill="x")
result.config(state="disabled")

def show_result(items):
    result.config(state="normal")
    result.delete("1.0", tk.END)
    def animate(i=0):
        if i < len(items):
            result.insert(tk.END, f"✦ {items[i]}\n")
            result.after(200, animate, i+1)
        else:
            result.config(state="disabled")
    animate()

# -------------------- Button --------------------
btn = tk.Button(
    panel,
    text="✨ STYLE MY AURA ✨",
    command=recommend_dress,
    font=("Helvetica", 16, "bold"),
    bg="#ff2fd2",
    fg="black",
    relief="flat"
)
btn.pack(pady=10)

# -------------------- Bottom Slogan --------------------
slogan = tk.Label(
    canvas,
    text="BE BOLD • BE ICONIC • BE AURA",
    font=("Helvetica", 40, "bold"),
    fg="#ffd700",
    bg="#050510"
)
slogan.place(relx=0.5, rely=0.85, anchor="center")

root.mainloop()
