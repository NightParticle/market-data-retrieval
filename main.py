import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk


class MyApp:
    def __init__(self, root):
        # Basic window setup
        self.root = root
        self.root.title("Market Data")
        self.root.geometry("1000x600")

        self.label = ttk.Label(self.root, text="Welcome")
        self.label.pack()

        self.create_widgets()

    def create_widgets(self):
        # Add input for selecting symbol to get data from
        self.symbol_label = ttk.Label(self.root, text="Symbol name: ")
        self.symbol_label.pack(pady=10)

        self.entry = ttk.Entry(self.root)
        self.entry.pack()

        self.get_data_button = ttk.Button(
            self.root, 
            text="Get data", 
            command=lambda: self.get_symbol_data(self.entry.get())
        )
        self.get_data_button.pack(pady=10)

        # change this later
        self.mean_label = ttk.Label(text="No Data")
        self.mean_label.pack()

    def get_symbol_data(self, sym):
        sym_data = yf.download(sym, period="1mo")
        mean = np.mean(sym_data["Close"])
        self.mean_label.config(text=f"Mean closing: {mean}")
        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()