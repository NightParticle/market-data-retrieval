import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # For embedding matplotlib plot in tkinter
import mplfinance as mpf
import tkinter as tk
from tkinter import ttk

from sma import SMA


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

        # Default ticker options
        self.sym = "AAPL"
        self.period = "3mo"
        self.interval = "1d"
        self.ta = []

        self.create_widgets()

    def create_widgets(self):
        # Container frame for all the options
        self.container = ttk.Frame(self.root)
        self.container.pack(padx=10, pady=10, fill="x")

        # Left box, for ticker options
        self.t_box = ttk.LabelFrame(self.container, text="Ticker Options")
        self.t_box.pack(side="left", expand=True, fill="both", padx=10)
        
        # Add input for selecting symbol to get data from
        self.symbol_label = ttk.Label(self.t_box, text="Symbol name: ")
        self.symbol_label.pack(pady=10)

        self.entry = ttk.Entry(self.t_box, background="white")
        self.entry.pack()

        # Right box, for ta options
        self.a_box = ttk.LabelFrame(self.container, text="Technical Analysis")
        self.a_box.pack(side="left", expand=True, fill="both", padx=10)

        self.create_sma_options(self.a_box)

        # Button used for getting and plotting a symbol
        self.get_data_button = ttk.Button(
            self.root, 
            text="Get data", 
            command=lambda: self.new_sym(self.entry.get())
        )
        self.get_data_button.pack(pady=10)

        # Additional symbol options
        self.t_options_box = ttk.LabelFrame(self.t_box, text="Additional Options")
        self.t_options_box.pack(side="left", expand=True, fill="both", padx=10)

        self.t_period_label = ttk.Label(self.t_options_box, text="Period: ")
        self.t_period_label.pack(side="left", padx=5)

        # NOTE: Refactor this later!
        period_ranges = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
        selected_period = tk.StringVar(value=period_ranges[3])

        self.t_period_dropdown = ttk.OptionMenu(self.t_options_box, selected_period, *period_ranges, command=self.update_period)
        self.t_period_dropdown.pack(side="left", padx=10)

        # Interval dropdown
        self.t_interval_label = ttk.Label(self.t_options_box, text="Interval: ")
        self.t_interval_label.pack(side="left", padx=5)

        interval_ranges = ["1h", "1d", "1wk", "1mo"]
        selected_interval = tk.StringVar(value=interval_ranges[8])

        self.t_interval_dropdown = ttk.OptionMenu(self.t_options_box, selected_interval, *interval_ranges, command=self.update_interval)
        self.t_interval_dropdown.pack(side="left", padx=10)

        #self.create_plot()

    def update_period(self, value):
        self.period = value

    def update_interval(self, value):
        self.interval = value

    def create_sma_options(self, box):
        self.sma_box = ttk.LabelFrame(box, text="SMA Analysis", style="White.TLabel")
        self.sma_box.pack(side="left", expand=True, fill="both", padx=10)

        self.win_label = ttk.Label(self.sma_box, text="Window: ")
        self.win_label.pack(side="left")

        self.win_entry = ttk.Entry(self.sma_box, background="white")
        self.win_entry.pack(side="left")

        self.sma_button = ttk.Button(
            self.sma_box, 
            text="Add SMA", 
            command=lambda: self.add_sma_analysis(int(self.win_entry.get()))
        )
        self.sma_button.pack(side="left")

    def add_sma_analysis(self, window):
        # Adds a SMA analysis to the ta list and updates plot
        sma = SMA(self.data["Close"], window)
        self.ta.append(sma)
        self.create_plot(False)

    def new_sym(self, sym):
        self.sym = sym
        self.ta = []
        print(f"P: {self.period} and I: {self.interval}")
        self.create_plot(True)

    def create_plot(self, new_sym):
        if new_sym:
            self.data = yf.download(self.sym, period=self.period, interval=self.interval)
        
        sym_data = self.data

        # Clean data for mpfinance, we need single index not multi
        if isinstance(sym_data.columns, pd.MultiIndex):
            sym_data.columns = sym_data.columns.get_level_values(0)

        # Clear canvas if already exists
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        additional_plots = []

        # Plot TA options
        for option in self.ta:
            if isinstance(option, SMA):
                window = option.window
                additional_plots.append(mpf.make_addplot(option.sma, width=2, label=f"SMA {window}"))

        # Create the plot
        fig, ax = None, None

        if additional_plots:
            fig, ax = mpf.plot(
                sym_data,
                type="candle",
                style="yahoo",
                addplot=additional_plots,
                returnfig=True,
                figsize=(7,5),
                title=f"{self.sym.upper()} over {self.period} (interval = {self.interval})",
                ylabel="Price (USD)",
            )
            ax[0].legend()
        else:
            fig, ax = mpf.plot(
                sym_data,
                type="candle",
                style="yahoo",
                returnfig=True,
                figsize=(7,5),
                title=f"{self.sym.upper()} over {self.period} (interval = {self.interval})",
                ylabel="Price (USD)",
            )

        # Embed the plot in tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=10)