import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class CurrencyAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ курса рубля")
        self.root.geometry("800x600")

        self.label = tk.Label(root, text="Загрузите Excel-файл с курсами валют")
        self.label.pack(pady=10)

        self.button = tk.Button(root, text="Открыть файл", command=self.load_file)
        self.button.pack(pady=5)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyAnalyzerApp(root)
    root.mainloop()
