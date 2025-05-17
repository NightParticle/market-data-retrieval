class SMA:
    def __init__(self, data, window):
        self.window = window
        self.sma = self.create_sma(data)

    def create_sma(self, data):
        sma = data.rolling(window=self.window).mean()
        return sma