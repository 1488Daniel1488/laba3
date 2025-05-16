import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

class CurrencyAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ курса рубля")
        self.root.geometry("800x800")

        self.label = tk.Label(root, text="Загрузите Excel-файл с курсами валют")
        self.label.pack(pady=10)

        self.load_button = tk.Button(root, text="Открыть файл", command=self.load_file)
        self.load_button.pack(pady=5)

        self.plot_button = tk.Button(root, text="Построить график", command=self.plot_graph)
        self.plot_button.pack(pady=5)

        self.analyze_button = tk.Button(root, text="Анализ курса", command=self.analyze_rates)
        self.analyze_button.pack(pady=5)

        self.forecast_days_label = tk.Label(root, text="Прогноз на N дней:")
        self.forecast_days_label.pack()
        self.forecast_entry = tk.Entry(root)
        self.forecast_entry.insert(0, "5")
        self.forecast_entry.pack(pady=2)

        self.forecast_button = tk.Button(root, text="Построить прогноз", command=self.forecast_plot)
        self.forecast_button.pack(pady=5)

        self.text = tk.Text(root, height=20, width=100)
        self.text.pack(padx=10, pady=10)

        self.analysis_output = tk.Text(root, height=10, width=100, bg="#f0f0f0")
        self.analysis_output.pack(padx=10, pady=10)

        self.df = None

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите Excel-файл",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not file_path:
            return

        try:
            self.df = pd.read_excel(file_path)
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, self.df.head().to_string(index=False))
            self.label.config(text="Файл загружен успешно!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")

    def plot_graph(self):
        if self.df is None:
            messagebox.showwarning("Нет данных", "Сначала загрузите Excel-файл.")
            return

        try:
            df = self.df.copy()
            df['Дата'] = pd.to_datetime(df['Дата'])

            plt.figure(figsize=(10, 5))
            plt.plot(df['Дата'], df['USD'], label='USD', marker='o')
            plt.plot(df['Дата'], df['EUR'], label='EUR', marker='x')
            plt.xlabel("Дата")
            plt.ylabel("Курс рубля")
            plt.title("Курс рубля к USD и EUR")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить график:\n{e}")

    def analyze_rates(self):
        if self.df is None:
            messagebox.showwarning("Нет данных", "Сначала загрузите Excel-файл.")
            return

        try:
            df = self.df.copy()
            df['Дата'] = pd.to_datetime(df['Дата'])
            df['USD_diff'] = df['USD'].diff()
            df['EUR_diff'] = df['EUR'].diff()

            usd_max_drop = df['USD_diff'].idxmax()
            usd_max_rise = df['USD_diff'].idxmin()
            eur_max_drop = df['EUR_diff'].idxmax()
            eur_max_rise = df['EUR_diff'].idxmin()

            result = f"""📊 Анализ изменений курса рубля:

💵 USD:
- 📉 Максимальное укрепление рубля (падение USD): {abs(df.loc[usd_max_rise, 'USD_diff']):.2f} руб. ({df.loc[usd_max_rise, 'Дата'].date()})
- 📈 Максимальное ослабление рубля (рост USD): {abs(df.loc[usd_max_drop, 'USD_diff']):.2f} руб. ({df.loc[usd_max_drop, 'Дата'].date()})

💶 EUR:
- 📉 Максимальное укрепление рубля (падение EUR): {abs(df.loc[eur_max_rise, 'EUR_diff']):.2f} руб. ({df.loc[eur_max_rise, 'Дата'].date()})
- 📈 Максимальное ослабление рубля (рост EUR): {abs(df.loc[eur_max_drop, 'EUR_diff']):.2f} руб. ({df.loc[eur_max_drop, 'Дата'].date()})
"""
            self.analysis_output.delete(1.0, tk.END)
            self.analysis_output.insert(tk.END, result)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить анализ:\n{e}")

    def forecast_plot(self):
        if self.df is None:
            messagebox.showwarning("Нет данных", "Сначала загрузите Excel-файл.")
            return

        try:
            N = int(self.forecast_entry.get())
            df = self.df.copy()
            df['Дата'] = pd.to_datetime(df['Дата'])

            usd_forecast = df['USD'].rolling(window=N).mean().dropna()
            eur_forecast = df['EUR'].rolling(window=N).mean().dropna()

            last_date = df['Дата'].iloc[-1]
            forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=N)

            usd_pred = [usd_forecast.iloc[-1]] * N
            eur_pred = [eur_forecast.iloc[-1]] * N

            plt.figure(figsize=(10, 5))
            plt.plot(df['Дата'], df['USD'], label='USD', marker='o')
            plt.plot(df['Дата'], df['EUR'], label='EUR', marker='x')
            plt.plot(forecast_dates, usd_pred, label='USD прогноз', linestyle='--')
            plt.plot(forecast_dates, eur_pred, label='EUR прогноз', linestyle='--')

            plt.xlabel("Дата")
            plt.ylabel("Курс рубля")
            plt.title("Курс рубля с прогнозом")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить прогноз:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyAnalyzerApp(root)
    root.mainloop()
