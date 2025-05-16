import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ данных")
        self.root.geometry("1000x800")
        # Вкладки
        notebook = ttk.Notebook(root)
        temp_frame = ttk.Frame(notebook)
        currency_frame = ttk.Frame(notebook)
        notebook.add(temp_frame, text="Температуры")
        notebook.add(currency_frame, text="Курс рубля")
        notebook.pack(pady=10, fill="both", expand=True)
        # Инициализация функционала
        TemperatureApp(temp_frame)
        CurrencyAnalyzerApp(currency_frame)

class TemperatureApp:
    def __init__(self, parent):
        self.parent = parent
        self.data = None
        # Заголовок
        tk.Label(parent, text="Анализ температур", font=("Arial", 14)).pack(pady=10)
        # Таблица
        self.table = ttk.Treeview(parent, columns=("День", "Макс", "Мин", "Сред", "Погода"), show="headings")
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
        self.table.pack(pady=10, fill="both", expand=True)
        # Загрузка данных
        self.load_data()
        # Графики
        self.fig, self.ax = None, None
        self.canvas = None
        self.plot_graphs()
        # Перепады температур
        self.calculate_differences()
        # Прогноз
        tk.Label(parent, text="Введите число дней для прогноза (N):").pack()
        self.n_entry = tk.Entry(parent)
        self.n_entry.pack(pady=2)
        tk.Button(parent, text="Прогнозировать", command=self.forecast_temps).pack(pady=5)

    def load_data(self):
        try:
            self.data = pd.read_csv("data/temperature.csv")
            for _, row in self.data.iterrows():
                self.table.insert("", "end", values=(
                    row["Day"], row["MaxTemp"], row["MinTemp"], row["AvgTemp"], row["Weather"]
                ))
        except FileNotFoundError:
            tk.Label(self.parent, text="Файл temperature.csv отсутствует").pack()

    def plot_graphs(self):
        if self.data is not None:
            self.fig, self.ax = plt.subplots(figsize=(6, 4))
            self.ax.plot(self.data["Day"], self.data["MaxTemp"], color="red", label="Макс. темп.")
            self.ax.plot(self.data["Day"], self.data["MinTemp"], color="blue", label="Мин. темп.")
            self.ax.set_xlabel("День")
            self.ax.set_ylabel("Температура (°C)")
            self.ax.legend()
            self.ax.grid(True)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)
        else:
            tk.Label(self.parent, text="Данные отсутствуют для графиков").pack()

    def calculate_differences(self):
        if self.data is not None:
            self.data["TempDiff"] = self.data["MaxTemp"] - self.data["MinTemp"]
            max_diff_day = self.data.loc[self.data["TempDiff"].idxmax(), "Day"]
            min_diff_day = self.data.loc[self.data["TempDiff"].idxmin(), "Day"]
            tk.Label(self.parent, text=f"Наибольший перепад в день {max_diff_day}: {self.data['TempDiff'].max()}°C").pack()
            tk.Label(self.parent, text=f"Наименьший перепад в день {min_diff_day}: {self.data['TempDiff'].min()}°C").pack()
        else:
            tk.Label(self.parent, text="Данные отсутствуют для расчёта перепадов").pack()

    def forecast_temps(self):
        if self.data is not None and self.canvas:
            try:
                n = int(self.n_entry.get())
                if n < 1:
                    raise ValueError("N должно быть положительным")
                max_forecast = self.moving_average(self.data["MaxTemp"].tolist(), n, 5)
                min_forecast = self.moving_average(self.data["MinTemp"].tolist(), n, 5)
                forecast_days = list(range(self.data["Day"].max() + 1, self.data["Day"].max() + 6))
                self.ax.plot(forecast_days, max_forecast[-5:], color="red", linestyle="--", label="Прогноз макс.")
                self.ax.plot(forecast_days, min_forecast[-5:], color="blue", linestyle="--", label="Прогноз мин.")
                self.ax.legend()
                self.canvas.draw()
            except ValueError as e:
                tk.Label(self.parent, text=f"Ошибка: {e}").pack()
        else:
            tk.Label(self.parent, text="Данные отсутствуют для прогноза").pack()

    @staticmethod
    def moving_average(data, n, periods):
        result = data.copy()
        for _ in range(periods):
            result.append(sum(result[-n:]) / n)
        return result

class CurrencyAnalyzerApp:
    def __init__(self, parent):
        self.parent = parent
        self.df = None
        self.fig, self.ax = None, None
        self.canvas = None
        # Заголовок
        tk.Label(parent, text="Анализ курса рубля", font=("Arial", 14)).pack(pady=10)
        # Кнопка загрузки файла
        self.load_button = tk.Button(parent, text="Открыть Excel-файл", command=self.load_file)
        self.load_button.pack(pady=5)
        # Таблица (Text вместо Treeview для упрощения)
        self.text = tk.Text(parent, height=10, width=80)
        self.text.pack(padx=10, pady=10, fill="both", expand=True)
        # Кнопки управления
        self.plot_button = tk.Button(parent, text="Построить график", command=self.plot_graph)
        self.plot_button.pack(pady=5)
        self.analyze_button = tk.Button(parent, text="Анализ курса", command=self.analyze_rates)
        self.analyze_button.pack(pady=5)
        # Прогноз
        tk.Label(parent, text="Прогноз на N дней:").pack()
        self.forecast_entry = tk.Entry(parent)
        self.forecast_entry.insert(0, "5")
        self.forecast_entry.pack(pady=2)
        self.forecast_button = tk.Button(parent, text="Построить прогноз", command=self.forecast_plot)
        self.forecast_button.pack(pady=5)
        # Вывод анализа
        self.analysis_output = tk.Text(parent, height=5, width=80, bg="#f0f0f0")
        self.analysis_output.pack(padx=10, pady=10, fill="both", expand=True)
        # Вывод прогноза
        self.forecast_output = tk.Text(parent, height=5, width=80, bg="#e8f5e9")
        self.forecast_output.pack(padx=10, pady=10, fill="both", expand=True)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите Excel-файл",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not file_path:
            return
        try:
            self.df = pd.read_excel(file_path)
            # Преобразуем столбец 'Дата' в datetime, если он есть
            if 'Дата' in self.df.columns:
                self.df['Дата'] = pd.to_datetime(self.df['Дата'], errors='coerce')
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, self.df.head().to_string(index=False))
            tk.Label(self.parent, text="Файл загружен успешно!").pack()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")

    def plot_graph(self):
        if self.df is None or 'Дата' not in self.df.columns or 'USD' not in self.df.columns or 'EUR' not in self.df.columns:
            messagebox.showwarning("Нет данных", "Сначала загрузите корректный Excel-файл с колонками 'Дата', 'USD', 'EUR'.")
            return
        try:
            df = self.df.copy()
            # Убедимся, что 'Дата' — это datetime
            df['Дата'] = pd.to_datetime(df['Дата'], errors='coerce')
            # Создаём или обновляем график
            if self.canvas:
                self.ax.clear()
            else:
                self.fig, self.ax = plt.subplots(figsize=(6, 4))
            self.ax.plot(df['Дата'], df['USD'], label='USD', marker='o', color='green')
            self.ax.plot(df['Дата'], df['EUR'], label='EUR', marker='x', color='purple')
            self.ax.set_xlabel("Дата")
            self.ax.set_ylabel("Курс рубля")
            self.ax.set_title("Курс рубля к USD и EUR")
            self.ax.legend()
            self.ax.grid(True)
            if not self.canvas:
                self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
                self.canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить график:\n{e}")

    def analyze_rates(self):
        if self.df is None or 'Дата' not in self.df.columns or 'USD' not in self.df.columns or 'EUR' not in self.df.columns:
            messagebox.showwarning("Нет данных", "Сначала загрузите корректный Excel-файл с колонками 'Дата', 'USD', 'EUR'.")
            return
        try:
            df = self.df.copy()
            df['Дата'] = pd.to_datetime(df['Дата'], errors='coerce')
            df['USD_diff'] = df['USD'].diff()
            df['EUR_diff'] = df['EUR'].diff()

            # Находим индексы максимального и минимального изменения
            usd_max_drop_idx = df['USD_diff'].idxmax()
            usd_max_rise_idx = df['USD_diff'].idxmin()
            eur_max_drop_idx = df['EUR_diff'].idxmax()
            eur_max_rise_idx = df['EUR_diff'].idxmin()

            # Получаем даты с учётом возможных NaT
            usd_max_drop_date = df.loc[usd_max_drop_idx, 'Дата'].date() if pd.notna(df.loc[usd_max_drop_idx, 'Дата']) else "Не определено"
            usd_max_rise_date = df.loc[usd_max_rise_idx, 'Дата'].date() if pd.notna(df.loc[usd_max_rise_idx, 'Дата']) else "Не определено"
            eur_max_drop_date = df.loc[eur_max_drop_idx, 'Дата'].date() if pd.notna(df.loc[eur_max_drop_idx, 'Дата']) else "Не определено"
            eur_max_rise_date = df.loc[eur_max_rise_idx, 'Дата'].date() if pd.notna(df.loc[eur_max_rise_idx, 'Дата']) else "Не определено"

            result = f"""📊 Анализ изменений курса рубля:

💵 USD:
- 📉 Макс. укрепление рубля (падение USD): {abs(df.loc[usd_max_rise_idx, 'USD_diff']):.2f} руб. ({usd_max_rise_date})
- 📈 Макс. ослабление рубля (рост USD): {abs(df.loc[usd_max_drop_idx, 'USD_diff']):.2f} руб. ({usd_max_drop_date})

💶 EUR:
- 📉 Макс. укрепление рубля (падение EUR): {abs(df.loc[eur_max_rise_idx, 'EUR_diff']):.2f} руб. ({eur_max_rise_date})
- 📈 Макс. ослабление рубля (рост EUR): {abs(df.loc[eur_max_drop_idx, 'EUR_diff']):.2f} руб. ({eur_max_drop_date})
"""
            self.analysis_output.delete(1.0, tk.END)
            self.analysis_output.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить анализ:\n{e}")

    def forecast_plot(self):
        if self.df is None or 'Дата' not in self.df.columns or 'USD' not in self.df.columns or 'EUR' not in self.df.columns:
            messagebox.showwarning("Нет данных", "Сначала загрузите корректный Excel-файл с колонками 'Дата', 'USD', 'EUR'.")
            return
        try:
            n_str = self.forecast_entry.get()
            if not n_str.strip().isdigit():
                raise ValueError("Введите положительное целое число.")
            N = int(n_str)
            if N < 2 or N >= len(self.df):
                raise ValueError(f"Число должно быть от 2 до {len(self.df) - 1}")
            df = self.df.copy()
            df['Дата'] = pd.to_datetime(df['Дата'], errors='coerce')
            usd_forecast = df['USD'].rolling(window=N).mean().dropna()
            eur_forecast = df['EUR'].rolling(window=N).mean().dropna()
            last_date = df['Дата'].iloc[-1]
            forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=N)
            usd_pred = [round(usd_forecast.iloc[-1], 2)] * N
            eur_pred = [round(eur_forecast.iloc[-1], 2)] * N
            # Обновляем график
            if self.canvas:
                self.ax.clear()
            else:
                self.fig, self.ax = plt.subplots(figsize=(6, 4))
            self.ax.plot(df['Дата'], df['USD'], label='USD', marker='o', color='green')
            self.ax.plot(df['Дата'], df['EUR'], label='EUR', marker='x', color='purple')
            self.ax.plot(forecast_dates, usd_pred, label='USD прогноз', linestyle='--', marker='o', color='darkgreen')
            self.ax.plot(forecast_dates, eur_pred, label='EUR прогноз', linestyle='--', marker='x', color='darkred')
            self.ax.set_xlabel("Дата")
            self.ax.set_ylabel("Курс рубля")
            self.ax.set_title("Курс рубля с прогнозом")
            self.ax.legend()
            self.ax.grid(True)
            if not self.canvas:
                self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
                self.canvas.get_tk_widget().pack(pady=10, fill="both", expand=True)
            self.canvas.draw()
            result = f"📅 Прогноз курса на {N} дней (скользящее среднее):\n\nUSD:\n"
            for date in forecast_dates:
                result += f"{date.date()}: {usd_pred[0]}\n"
            result += "\nEUR:\n"
            for date in forecast_dates:
                result += f"{date.date()}: {eur_pred[0]}\n"
            self.forecast_output.delete(1.0, tk.END)
            self.forecast_output.insert(tk.END, result)
        except ValueError as ve:
            messagebox.showerror("Ошибка ввода", str(ve))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить прогноз:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()