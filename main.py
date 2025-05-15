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

        self.label = ttk.Label(root, text="Welcome")
        self.label.pack()

    def create_wdigets(self):
        


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()