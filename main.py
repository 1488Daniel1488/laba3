import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

class CurrencyAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ курса рубля")
        self.root.geometry("800x600")

        self.label = tk.Label(root, text="Загрузите Excel-файл с курсами валют")
        self.label.pack(pady=10)

        self.load_button = tk.Button(root, text="Открыть файл", command=self.load_file)
        self.load_button.pack(pady=5)

        self.plot_button = tk.Button(root, text="Построить график", command=self.plot_graph)
        self.plot_button.pack(pady=5)

        self.text = tk.Text(root, height=30, width=100)
        self.text.pack(padx=10, pady=10)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyAnalyzerApp(root)
    root.mainloop()
