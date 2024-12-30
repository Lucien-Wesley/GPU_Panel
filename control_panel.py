import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from oil_gauge import OilGauge
from fuel_gauge import FuelGauge
from speed_gauge import SpeedGauge
from i2c_interface import I2CInterface

class ControlPanelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Avion Control Panel")
        self.root.geometry("850x550")
        self.root.configure(bg="white")
        self.is_on = True

        self.i2c = I2CInterface()  # Initialize I2C interface

        self.canvas = tk.Canvas(self.root, width=850, height=550, bg="white", highlightthickness=0)
        self.canvas.place(x=0, y=0)

        # Draw grid rectangles
        self.canvas.create_rectangle(10, 10, 840, 540, outline="black", width=2)  # Outer rectangle

        # ========================== IMAGES ========================== #
        self.gpu_image = self.load_image("images/gpu_image.jpg", (140, 100))
        self.airplane_image = self.load_image("images/plane_not_connected.jpg", (100, 66))
        self.airplane_image_full = self.load_image("images/plane_full.jpg", (100, 66)) 
        self.light_on_image = self.load_image("images/light_on.jpg", (50, 50))
        self.light_off_image = self.load_image("images/light_off.jpg", (50, 50))

        # ========================== WIDGETS ========================== #
        self.on_off_image()
        self.look_action()
        self.create_gpu_image()
        self.connection_lines()
        self.create_airplane_images()
        self.create_status_grid()
        self.create_gauges()
        self.update_gauge_values(0, 0, 0)
        self.update_display()

    def load_image(self, path, size):
        """Load and resize an image."""
        try:
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None
        
    def on_off_image(self):
        if self.is_on:
            light_state_image = tk.Label(self.root, image=self.light_on_image, bg="white")
        else:
            light_state_image = tk.Label(self.root, image=self.light_off_image, bg="white")
        light_state_image.place(x=770, y=20)

    def look_action(self, action="Action"):
        canvas = tk.Canvas(self.root, width=250, height=50, bg="white", highlightthickness=0)
        canvas.place(x=15, y=15)

        # Draw grid rectangles
        canvas.create_rectangle(0, 0, 250, 50, outline="black", width=2)  # Outer rectangle

        title_label = tk.Label(canvas, text=action, font=("Poppins", 12, "bold"), bg="white")
        title_label.place(x=10, y=10)

    def create_gpu_image(self):
        """Place the GPU image at the top-center."""
        if self.gpu_image:
            gpu_label = tk.Label(self.root, image=self.gpu_image, bg="white")
            gpu_label.place(x=350, y=40)

    def connection_lines(self):
        self.connection_lines = {
            "line1": self.canvas.create_line(400, 90, 150, 90, fill="black", width=2, dash=(5, 2)),
            "line2": self.canvas.create_line(150, 90, 150, 220, fill="black", width=2, dash=(5, 2)),
            "line3": self.canvas.create_line(330, 90, 330, 220, fill="black", width=2, dash=(5, 2)),
            "line4": self.canvas.create_line(520, 90, 520, 220, fill="black", width=2, dash=(5, 2)),
            "line5": self.canvas.create_line(400, 90, 671, 90, fill="black", width=2, dash=(5, 2)),
            "line6": self.canvas.create_line(670, 90, 670, 220, fill="black", width=2, dash=(5, 2))
        }

    def create_airplane_images(self):
        """Place 4 airplane images in a row."""
        positions = [100, 270, 460, 610]
        for pos in positions:
            if self.airplane_image:
                airplane_label = tk.Label(self.root, image=self.airplane_image, bg="white")
                airplane_label.place(x=pos, y=180)
                if pos == 100:
                    self.airplane_label1 = airplane_label
                if pos == 270:
                    self.airplane_label2 = airplane_label
                if pos == 460:
                    self.airplane_label3 = airplane_label
                if pos == 610:
                    self.airplane_label4 = airplane_label

    def create_status_grid(self):
        """Create the grid displaying ON/OFF statuses."""
        labels = ["S1", "S2", "S3", "S4"]
        x_positions = [100, 260, 430, 610]
        y_position = 270

        self.draw_grid_lines()
        for i, pos in enumerate(x_positions):
            # Top row - Section labels
            section_label = tk.Label(self.root, text=labels[i], font=("Poppins", 12, "bold"), bg="white")
            section_label.place(x=pos+50, y=y_position)

            # Middle row - Status OFF
            status_label = tk.Label(self.root, text="OFF", fg="red", font=("Poppins", 12), bg="white")
            status_label.place(x=pos+50, y=y_position+40)

            # Bottom row - Placeholder ("-")
            placeholder_label = tk.Label(self.root, text="-", font=("Poppins", 12), bg="white")
            placeholder_label.place(x=pos+50, y=y_position+80)
            if i==0:
                self.s1_status_label = status_label
                self.s1_current_label = placeholder_label
            elif i==1:
                self.s2_status_label = status_label
                self.s2_current_label = placeholder_label
            elif i==2:
                self.s3_status_label = status_label
                self.s3_current_label = placeholder_label
            elif i==3:
                self.s4_status_label = status_label
                self.s4_current_label = placeholder_label

        # Draw grid lines
        #self.draw_grid_lines()

    def draw_grid_lines(self):
        """Draw grid lines for the status table."""
        canvas = tk.Canvas(self.root, width=820, height=150, bg="white", highlightthickness=0)
        canvas.place(x=15, y=260)

        # Draw grid rectangles
        canvas.create_rectangle(55, 0, 750, 120, outline="black", width=2)  # Outer rectangle
        for i in range(1, 4):
            canvas.create_line(55 + i * 170, 0, 55 + i * 170, 120, fill="black", width=2)  # Vertical lines
        canvas.create_line(55, 40, 750, 40, fill="black", width=2)  # First horizontal line
        canvas.create_line(55, 80, 750, 80, fill="black", width=2)  # Second horizontal line

    def create_gauges(self):
        """Create empty boxes for Fuel, Oil, and Speed gauges."""
        titles = ["Fuel", "Oil", "Speed"]
        x_positions = [120, 350, 580]

        for i, title in enumerate(titles):
            # Title label
            title_label = tk.Label(self.root, text=title, font=("Poppins", 12, "bold"), bg="white")
            title_label.place(x=x_positions[i]-(len(title))*9, y=450)

            # Box outline
            canvas = tk.Canvas(self.root, width=120, height=100, bg="white", highlightthickness=2, highlightbackground="black")
            if i==0:
                self.fuel_gauge = FuelGauge(canvas, size=(120, 105))
            if i==1:
                self.oil_gauge = OilGauge(canvas, size=(110, 63))
            if i==2:
                self.speed_gauge = SpeedGauge(canvas, max_value=8000, min_angle=30, max_angle=180, num_segments=5, size=(120, 105))
            canvas.place(x=x_positions[i]+15, y=390)
    

    
    def update_fuel_gauge(self, value):
        """Met à jour la jauge de carburant."""
        self.fuel_gauge.update_gauge(value)

    def update_speed_gauge(self, value):
        """Met à jour la jauge de vitesse."""
        self.speed_gauge.update_gauge(value)

    def update_oil_gauge(self, value):
        """Met à jour la jauge d'huile."""
        self.oil_gauge.update_gauge(value)

    def update_connection_line(self, active):
        """Met à jour les lignes de connexion."""
        style = {"dash": () if active else (5, 2), "fill": "blue" if active else "black"}
        self.canvas.itemconfig(self.connection_lines["line1"], **style)
        self.canvas.itemconfig(self.connection_lines["line2"], **style)

    def update_gauge_values(self, fuel, oil, speed):
        """Met à jour toutes les jauges avec de nouvelles valeurs."""
        self.update_fuel_gauge(fuel)
        self.update_oil_gauge(oil)
        self.update_speed_gauge(speed)
        
    def update_voltage_label(self, label, voltage):
        if voltage is not None:
            label.config(text=f"{voltage}V", fg="black")
        else:
            label.config(text="OFF", fg="red")

    def update_current_label(self, label, current):
        if current is not None:
            label.config(text=f"{current}A", fg="black")
        else:
            label.config(text="-", fg="black")
    def update_display(self):
        # Get values from the I2C interface
        if self.is_on:
            s1_voltage = self.i2c.get_voltage("S1")
            s2_voltage = self.i2c.get_voltage("S2")
            s3_voltage = self.i2c.get_voltage("S3")
            
            s1_current = self.i2c.get_current("S1")
            s2_current = self.i2c.get_current("S2")
            s3_current = self.i2c.get_current("S3")
            
            gauges_values = self.i2c.get_gauges_values()
            battery_full = self.i2c.is_battery_full()

            
        else:
            s1_voltage = None
            s2_voltage = None
            s3_voltage = None
            s1_current = None
            s2_current = None
            s3_current = None
            battery_full = False
            gauges_values = {
            "fuel":0,
            "oil":0,
            "rpm":0
            }
            
        self.update_gauge_values(gauges_values["fuel"], gauges_values["oil"], gauges_values["rpm"])
        # Update voltage labels
        self.update_voltage_label(self.s1_status_label, s1_voltage)
        self.update_voltage_label(self.s2_status_label, s2_voltage)
        self.update_voltage_label(self.s3_status_label, s3_voltage)

        # Update current labels
        self.update_current_label(self.s1_current_label, s1_current)
        self.update_current_label(self.s2_current_label, s2_current)
        self.update_current_label(self.s3_current_label, s3_current)
        
        # Update airplane image based on battery status
        if battery_full:
            self.airplane_label1.config(image=self.airplane_image_full)
        else:
            self.airplane_label1.config(image=self.airplane_image)

        # Update the connection line to the airplane
        if s1_current:
            self.canvas.itemconfig(self.connection_lines["line1"], dash=(), fill="blue")
            self.canvas.itemconfig(self.connection_lines["line2"], dash=(), fill="blue")
        else:
            self.canvas.itemconfig(self.connection_lines["line1"], dash=(5, 2), fill="black")
            self.canvas.itemconfig(self.connection_lines["line2"], dash=(5, 2), fill="black")
        if s2_current:
            self.canvas.itemconfig(self.connection_lines["line3"], dash=(), fill="blue")
        else:
            self.canvas.itemconfig(self.connection_lines["line3"], dash=(5, 2), fill="black")
        if s3_current:
            self.canvas.itemconfig(self.connection_lines["line4"], dash=(), fill="blue")
            self.canvas.itemconfig(self.connection_lines["line5"], dash=(), fill="blue")
        else:
            self.canvas.itemconfig(self.connection_lines["line4"], dash=(5, 2), fill="black")
            self.canvas.itemconfig(self.connection_lines["line5"], dash=(5, 2), fill="black")

        if self.is_on:
            self.root.after(1000, self.update_display)

if __name__ == "__main__":
    root = tk.Tk()
    app = ControlPanelApp(root)
    root.mainloop()