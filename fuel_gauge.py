import tkinter as tk
import math
import tkinter.font as tkFont

class FuelGauge:
    def __init__(self, master, size=(100,80,)):
        self.master = master
        #self.master.title("Fuel Gauge Example")

        # Canvas setup
        self.size = size
        self.canvas = tk.Canvas(master, width=self.size[0], height=self.size[1], bg="white",highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=20, pady=20)

        # Initialize gauge parameters
        self.center_x, self.center_y, self.radius = self.size[0] // 2, self.size[1] // 1.5 , self.size[1] // 2
        self.base_radius = 10  # Radius of the circular base
        
        # Create font for label
        self.font = tkFont.Font(family="Helvetica", size=20, weight="bold")

        # Label to display the fuel level in liters
        self.label_var = tk.StringVar()
        self.label = tk.Label(master, textvariable=self.label_var, font=self.font, bg="white")
        self.label.place(x=self.center_x, y=self.center_y + 35)  # Initial placement

        # Initial gauge drawing and value update
        self.draw_gauge()
        self.update_gauge(0)

    def draw_gauge(self):
        # Draw base arc
        self.canvas.create_arc(self.center_x - self.radius, self.center_y - self.radius,
                                self.center_x + self.radius, self.center_y + self.radius, 
                                start=0, extent=180, style="arc", width=5)

        # E and F labels
        self.canvas.create_text(self.center_x - self.radius + 20, self.center_y, 
                                 text="E", font=("Helvetica", 12, "bold"), fill="red")
        self.canvas.create_text(self.center_x + self.radius - 20, self.center_y, 
                                 text="F", font=("Helvetica", 12, "bold"))

        # Fuel icon
        self.canvas.create_text(self.center_x, self.center_y - 30, text="⛽", font=("Helvetica", 12))

        # Draw ticks on the arc
        self.draw_ticks()

        # Draw the circular base of the needle
        self.canvas.create_oval(self.center_x - self.base_radius, self.center_y - self.base_radius,
                                self.center_x + self.base_radius, self.center_y + self.base_radius,
                                fill="black")

    def draw_ticks(self):
        for i in range(0, 11):  # Draw ticks at each 10% increment
            angle = i * 18  # 0 to 180 degrees (10 ticks for each 10% increment)
            # Calculate start and end points for each tick
            start_x = self.center_x + (self.radius - 10) * math.cos(math.radians(180 - angle))
            start_y = self.center_y - (self.radius - 10) * math.sin(math.radians(180 - angle))
            end_x = self.center_x + self.radius * math.cos(math.radians(180 - angle))
            end_y = self.center_y - self.radius * math.sin(math.radians(180 - angle))

            # Make the 0%, 50%, and 100% ticks wider
            tick_width = 4 if i in [0, 5, 10] else 2

            # Set color: red for 0% (E), black for others
            tick_color = "red" if i == 0 else "black"

            # Draw the tick line
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill=tick_color, width=tick_width)

    def update_gauge(self, value):
        self.canvas.delete("needle")
        angle = (value / 100) * 180  # Map value to 0-180 degrees

        # Calculate the main tip point of the needle
        needle_length = self.radius - 15  # Shorten the needle to avoid touching the arc
        x_tip = self.center_x + needle_length * math.cos(math.radians(180 - angle))
        y_tip = self.center_y - needle_length * math.sin(math.radians(180 - angle))

        # Calculate the two base points of the needle triangle
        needle_base_width = 8  # Width of the needle base
        x_base1 = self.center_x + (needle_base_width / 2) * math.sin(math.radians(180 - angle))
        y_base1 = self.center_y + (needle_base_width / 2) * math.cos(math.radians(180 - angle))
        x_base2 = self.center_x - (needle_base_width / 2) * math.sin(math.radians(180 - angle))
        y_base2 = self.center_y - (needle_base_width / 2) * math.cos(math.radians(180 - angle))

        # Draw the needle as a triangle
        self.canvas.create_polygon(x_base1, y_base1, x_base2, y_base2, x_tip, y_tip, 
                                   fill="red", outline="red", tags="needle")

        # Update label with current value
        self.label_var.set(f"{value}L")

        # Center the label based on its width
        label_width = self.font.measure(self.label_var.get())  # Measure the width of the label text
        self.label.place(x=self.center_x - (label_width // 8), y=self.center_y + 35)  # Adjust x position to center it
