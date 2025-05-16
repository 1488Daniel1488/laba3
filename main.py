import tkinter as tk
from tkinter import ttk
import pandas as pd

class TemperatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ температуры")
        # Заголовок
        tk.Label(root, text="Температурный анализ", font=("Arial", 14)).pack(pady=10)
        # Таблица
        self.table = ttk.Treeview(root, columns=("День", "Макс", "Мин", "Сред", "Погода"), show="headings")
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
        self.table.pack(pady=10)
        # Загрузка данных
        self.load_data()
        # Placeholder для графиков
        tk.Label(root, text="Место для графиков").pack(pady=10)

    def load_data(self):
        try:
            self.data = pd.read_csv("data/temperature.csv")
            for _, row in self.data.iterrows():
                self.table.insert("", "end", values=(
                    row["Day"], row["MaxTemp"], row["MinTemp"], row["AvgTemp"], row["Weather"]
                ))
        except FileNotFoundError:
            tk.Label(self.root, text="Файл temperature.csv отсутствует").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureApp(root)
    root.mainloop()