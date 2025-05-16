import tkinter as tk
from tkinter import ttk

class TemperatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ температуры")
        # Заголовок
        tk.Label(root, text="Температурный анализ", font=("Arial", 14)).pack(pady=10)
        # Placeholder для таблицы
        self.table = ttk.Treeview(root, columns=("День", "Макс", "Мин", "Сред", "Погода"), show="headings")
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
        self.table.pack(pady=10)
        # Placeholder для графиков
        tk.Label(root, text="Место для графиков").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureApp(root)
    root.mainloop()