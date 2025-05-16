import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        self.data = None
        self.load_data()
        # Графики
        self.plot_graphs()
        # Перепады температур
        self.calculate_differences()

    def load_data(self):
        try:
            self.data = pd.read_csv("data/temperature.csv")
            for _, row in self.data.iterrows():
                self.table.insert("", "end", values=(
                    row["Day"], row["MaxTemp"], row["MinTemp"], row["AvgTemp"], row["Weather"]
                ))
        except FileNotFoundError:
            tk.Label(self.root, text="Файл temperature.csv отсутствует").pack()

    def plot_graphs(self):
        if self.data is not None:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(self.data["Day"], self.data["MaxTemp"], color="red", label="Макс. темп.")
            ax.plot(self.data["Day"], self.data["MinTemp"], color="blue", label="Мин. темп.")
            ax.set_xlabel("День")
            ax.set_ylabel("Температура (°C)")
            ax.legend()
            ax.grid(True)
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)
        else:
            tk.Label(self.root, text="Данные отсутствуют для графиков").pack()

    def calculate_differences(self):
        if self.data is not None:
            self.data["TempDiff"] = self.data["MaxTemp"] - self.data["MinTemp"]
            max_diff_day = self.data.loc[self.data["TempDiff"].idxmax(), "Day"]
            min_diff_day = self.data.loc[self.data["TempDiff"].idxmin(), "Day"]
            tk.Label(self.root, text=f"Наибольший перепад в день {max_diff_day}: {self.data['TempDiff'].max()}°C").pack()
            tk.Label(self.root, text=f"Наименьший перепад в день {min_diff_day}: {self.data['TempDiff'].min()}°C").pack()
        else:
            tk.Label(self.root, text="Данные отсутствуют для расчёта перепадов").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureApp(root)
    root.mainloop()