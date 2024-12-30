import tkinter as tk
from fuel_gauge import FuelGauge
from oil_gauge import OilGauge
from speed_gauge import SpeedGauge

from control_panel import ControlPanelApp

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.control_panel = ControlPanelApp(self.root)
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
