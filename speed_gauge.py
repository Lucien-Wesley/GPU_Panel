import tkinter as tk
import math
import tkinter.font as tkFont

class SpeedGauge:
    def __init__(self, master, max_value=6000, min_angle=0, max_angle=180, num_segments=5,size=(100,80,)):
        self.master = master
        
        self.max_value = max_value  # Set the maximum value for the gauge
        self.min_angle = min_angle  # Set the minimum angle for the gauge
        self.max_angle = max_angle  # Set the maximum angle for the gauge
        self.num_segments = num_segments  # Set the number of segments
        self.size = size
        self.min_value = 0

        # Canvas setup
        self.canvas = tk.Canvas(master, width=self.size[0], height=self.size[1], bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=20, pady=20)

        # Initialize gauge parameters
        self.center_x, self.center_y, self.radius = self.size[0]//2, self.size[1]//1.5, self.size[1]//2
        self.base_radius = 10  # Radius of the circular base
        
        # Create font for label
        self.font = tkFont.Font(family="Helvetica", size=20, weight="bold")

        # Label to display the RPM
        self.label_var = tk.StringVar()
        self.label = tk.Label(master, textvariable=self.label_var, font=self.font, bg="white")
        self.label.place(x=self.center_x, y=self.center_y + 35)  # Initial placement

        # Draw gauge
        self.draw_gauge()
        self.update_gauge(0)

    def draw_gauge(self):
        total_angle = self.max_angle - self.min_angle  # Calculate the span of the arc

        for i in range(self.num_segments):
            # Calculate the start angle for each segment based on min_angle and total_angle
            start_angle = self.min_angle + i * (total_angle / self.num_segments)
            segment_extent = (total_angle / self.num_segments) - 2  # Slightly reduce to create a gap
            
            # Gradually increase the width from 20 to 5 across segments (reverse the logic)
            width = 20 - (i / (self.num_segments - 1)) * (20 - 5) if self.num_segments > 1 else 20
            inner_radius = self.radius - (width / 2)  # Inner radius based on width

            # Draw each segment as an arc
            self.canvas.create_arc(
                self.center_x - inner_radius, self.center_y - inner_radius,
                self.center_x + inner_radius, self.center_y + inner_radius,
                start=start_angle, extent=segment_extent,
                style="arc", width=width, outline="black", tags="arc")

        # Labels for "0" and "MAX" (max_value)
        self.canvas.create_text(
            self.center_x + 10 + self.radius * math.cos(math.radians(self.max_angle)),
            self.center_y - self.radius * math.sin(math.radians(self.max_angle)),
            text="0", font=("Helvetica", 14, "bold"), fill="black")
        
        self.canvas.create_text(
            self.center_x - 5 + self.radius * math.cos(math.radians(0)),
            self.center_y -  self.radius * math.sin(math.radians(0)),
            text="RPM", font=("Helvetica", 14, "bold"), fill="black")

        # Draw the circular base of the needle
        self.canvas.create_oval(self.center_x - self.base_radius, self.center_y - self.base_radius,
                                self.center_x + self.base_radius, self.center_y + self.base_radius,
                                fill="black")

    def update_gauge(self, value):
        # Remove the existing needle
        self.canvas.delete("needle")
        
        # Map value to angle between min_angle and max_angle
        angle =  ((value - self.min_value) / (self.max_value - self.min_value)) * (self.max_angle - self.min_angle)

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

        # Update label with current RPM
        self.label_var.set(f"{value} RPM")

        # Center the label based on its width
        label_width = self.font.measure(self.label_var.get())  # Measure the width of the label text
        self.label.place(x=self.center_x - (label_width // 3), y=self.center_y + 35)  # Adjust x position to center it
