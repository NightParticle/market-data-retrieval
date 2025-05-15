import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # For embedding matplotlib plot in tkinter
import mplfinance as mpf
import tkinter as tk
from tkinter import ttk


class MyApp:
    def __init__(self, root):
        # Basic window setup
        self.root = root
        self.root.title("Market Data")
        self.root.geometry("1000x600")
        self.root.configure(bg="white")

        self.label = ttk.Label(self.root, text="Welcome")
        self.label.pack()

        # This is a placeholder for the plot canvas
        self.canvas = None

        self.create_widgets()

    def create_widgets(self):
        # Add input for selecting symbol to get data from
        self.symbol_label = ttk.Label(self.root, text="Symbol name: ")
        self.symbol_label.pack(pady=10)

        self.entry = ttk.Entry(self.root)
        self.entry.pack()

        # Button used for getting and plotting a symbol
        self.get_data_button = ttk.Button(
            self.root, 
            text="Get data", 
            command=lambda: self.get_symbol_data(self.entry.get())
        )
        self.get_data_button.pack(pady=10)

    def get_symbol_data(self, sym):
        sym_data = yf.download(sym, period="3mo", interval="1d")
        sym_data.index.name = "Date"

        # Clean data for mpfinance, we need single index not multi
        if isinstance(sym_data.columns, pd.MultiIndex):
            sym_data.columns = sym_data.columns.get_level_values(0)

        # Clear canvas if already exists
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Create the plot
        fig, ax = plt.subplots(figsize=(7,5))
        mpf.plot(sym_data, type="candle", style="yahoo", ax=ax)
        ax.set_title(f"{sym.upper()} over 1 month")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")

        # Embed the plot in tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=10)
        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
