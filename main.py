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
        self.fig, self.ax = None, None
        self.canvas = None
        self.plot_graphs()
        # Перепады температур
        self.calculate_differences()
        # Прогноз
        tk.Label(root, text="Введите число дней для прогноза (N):").pack()
        self.n_entry = tk.Entry(root)
        self.n_entry.pack()
        tk.Button(root, text="Прогнозировать", command=self.forecast_temps).pack(pady=5)

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
            self.fig, self.ax = plt.subplots(figsize=(6, 4))
            self.ax.plot(self.data["Day"], self.data["MaxTemp"], color="red", label="Макс. темп.")
            self.ax.plot(self.data["Day"], self.data["MinTemp"], color="blue", label="Мин. темп.")
            self.ax.set_xlabel("День")
            self.ax.set_ylabel("Температура (°C)")
            self.ax.legend()
            self.ax.grid(True)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(pady=10)
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

    def forecast_temps(self):
        if self.data is not None and self.canvas:
            try:
                n = int(self.n_entry.get())
                if n < 1:
                    raise ValueError("N должно быть положительным")
                # Скользящая средняя
                max_forecast = self.moving_average(self.data["MaxTemp"].tolist(), n, 5)
                min_forecast = self.moving_average(self.data["MinTemp"].tolist(), n, 5)
                forecast_days = list(range(self.data["Day"].max() + 1, self.data["Day"].max() + 6))
                # Обновление графика
                self.ax.plot(forecast_days, max_forecast[-5:], color="red", linestyle="--", label="Прогноз макс.")
                self.ax.plot(forecast_days, min_forecast[-5:], color="blue", linestyle="--", label="Прогноз мин.")
                self.ax.legend()
                self.canvas.draw()
            except ValueError as e:
                tk.Label(self.root, text=f"Ошибка: {e}").pack()
        else:
            tk.Label(self.root, text="Данные отсутствуют для прогноза").pack()

    @staticmethod
    def moving_average(data, n, periods):
        result = data.copy()
        for _ in range(periods):
            result.append(sum(result[-n:]) / n)
        return result

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureApp(root)
    root.mainloop()