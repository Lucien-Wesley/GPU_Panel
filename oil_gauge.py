import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk  # Requires the Pillow library

class OilGauge:
    def __init__(self, master, icon_path="images/gauge_oil.jpg", size=(100, 100)):
        self.master = master
        self.size = size
        self.icon_path = icon_path

        # Canvas setup
        self.canvas = tk.Canvas(master, width=self.size[0], height=self.size[1] + 40, bg="white",highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=20, pady=20)

        # Load and display the oil icon
        self.load_icon()

        # Create font for label
        self.font = tkFont.Font(family="Helvetica", size=20, weight="bold")

        # Label to display the oil level in liters
        self.label_var = tk.StringVar()
        self.label = tk.Label(master, textvariable=self.label_var, font=self.font, bg="white")
        self.label.place(x=self.size[0] // 2 - 20, y=self.size[1] + 8)

        # Initial gauge value
        self.update_gauge(0.0)  # Set initial level, e.g., 0.0L

    def load_icon(self):
        # Load the oil icon
        try:
            self.icon_image = Image.open(self.icon_path)
            self.icon_image = self.icon_image.resize((self.size[0], self.size[1]), Image.Resampling.LANCZOS)
            self.icon_photo = ImageTk.PhotoImage(self.icon_image)
            # Display the icon
            self.canvas.create_image(self.size[0] // 2, self.size[1] // 2, image=self.icon_photo)
        except Exception as e:
            print("Error loading icon:", e)

    def update_gauge(self, value):
        # Update label with current oil level
        self.label_var.set(f"{value}L")
        # Center the label based on its width
        label_width = self.font.measure(self.label_var.get())
        self.label.place(x=(self.size[0] // 2) , y=self.size[1] * 1.6)
