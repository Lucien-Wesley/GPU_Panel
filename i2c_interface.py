import smbus  # Nécessite que ce module soit installé pour votre système (Raspberry Pi typiquement)
import RPi.GPIO as GPIO  # Nécessite la bibliothèque RPi.GPIO

class I2CInterface:
    """
    Classe pour gérer la communication I2C et les boutons GPIO pour un GPU d'avion.
    """
    # Configuration des boutons GPIO
    BUTTONS = {
        "on_off": 17,
        "start": 27,
        "emergency": 22,
        "s1": 10,
        "s2": 9,
        "s3": 11
    }

    # Adresses I2C des périphériques
    I2C_ADDRESSES = {
        "avr": 0x40,
        "sensor": 0x41,
        "mcu": 0x42
    }

    # Commandes associées aux boutons
    COMMANDS = {
        17: [0x01, 0x02, 0x03],
        27: [0x04, 0x05, 0x06],
        22: [0x07, 0x08, 0x09],
        10: [0x10, 0x11, 0x12],
        9: [0x13, 0x14, 0x15],
        11: [0x16, 0x17, 0x18]
    }

    def __init__(self):
        """
        Initialise les connexions GPIO et I2C.
        """
        # GPIO initialisation
        GPIO.setmode(GPIO.BCM)
        for pin in self.BUTTONS.values():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=self._button_callback, bouncetime=300)

        # Initialisation I2C
        try:
            self.bus = smbus.SMBus(1)  # Bus I2C 1 pour Raspberry Pi
        except Exception as e:
            print(f"Erreur d'initialisation du bus I2C : {e}")
            self.bus = None

    def read_sensor_data(self, i2c_address):
        """
        Lit les données du capteur via I2C.
        """
        if not self.bus:
            print("Le bus I2C n'est pas initialisé.")
            return None

        try:
            # Lecture de 16 octets sur l'adresse donnée
            data = self.bus.read_i2c_block_data(i2c_address, 0, 16)
            return {
                'V1': data[0],
                'V2': data[1],
                'V3': data[2],
                'I1': data[3],
                'I2': data[4],
                'I3': data[5],
                'FUEL': data[6],
                'OIL': data[7],
                'RPM': (data[8] << 8) | data[9],
                'MTEMP': data[10]
            }
        except Exception as e:
            print(f"Erreur lors de la lecture I2C ({hex(i2c_address)}): {e}")
            return None

    def get_voltage(self, sensor_id):
        """
        Retourne la tension lue via I2C pour un capteur donné.
        """
        sensor_data = self.read_sensor_data(self.I2C_ADDRESSES["sensor"])
        if sensor_data:
            return sensor_data.get(f'V{sensor_id}', None)
        print("Données capteur indisponibles.")
        return None

    def get_current(self, sensor_id):
        """
        Retourne le courant lu via I2C pour un capteur donné.
        """
        sensor_data = self.read_sensor_data(self.I2C_ADDRESSES["sensor"])
        if sensor_data:
            return sensor_data.get(f'I{sensor_id}', None)
        print("Données capteur indisponibles.")
        return None

    def is_power_on(self, sensor_id):
        """
        Vérifie si le capteur spécifié est sous tension via les données I2C.
        """
        voltage = self.get_voltage(sensor_id)
        return voltage is not None and voltage > 0

    def is_battery_full(self):
        """
        Vérifie si la batterie est pleine en fonction des données FUEL via I2C.
        """
        sensor_data = self.read_sensor_data(self.I2C_ADDRESSES["sensor"])
        if sensor_data:
            return sensor_data.get('FUEL', 0) == 100  # Considère 100% comme étant pleine
        print("Impossible de vérifier l'état de la batterie.")
        return False

    def get_gauges_values(self):
        """
        Retourne les valeurs des jauges (carburant, huile, RPM) à partir des données I2C.
        """
        sensor_data = self.read_sensor_data(self.I2C_ADDRESSES["sensor"])
        if sensor_data:
            return {
                "fuel": sensor_data.get('FUEL', 0),
                "oil": sensor_data.get('OIL', 0),
                "rpm": sensor_data.get('RPM', 0)
            }
        print("Données des jauges indisponibles.")
        return {"fuel": 0, "oil": 0, "rpm": 0}

    def _button_callback(self, channel):
        """
        Callback pour les boutons GPIO.
        """
        if channel in self.COMMANDS:
            command = self.COMMANDS[channel]
            print(f"Commande exécutée pour le bouton {channel} : {command}")
            self.send_command(command)

    def send_command(self, command):
        """
        Envoie une commande via I2C.
        """
        if not self.bus:
            print("Le bus I2C n'est pas initialisé.")
            return

        try:
            for byte in command:
                self.bus.write_byte(self.I2C_ADDRESSES["avr"], byte)
                print(f"Commande {byte} envoyée à {hex(self.I2C_ADDRESSES['avr'])}")
        except Exception as e:
            print(f"Erreur lors de l'envoi de la commande I2C : {e}")


# Exemple d'utilisation
if __name__ == "__main__":
    gpu = I2CInterface()

    # Lecture des capteurs
    sensor_data = gpu.read_sensor_data(I2CInterface.I2C_ADDRESSES["sensor"])
    if sensor_data:
        print("Données capteurs :", sensor_data)

    # Lecture des jauges
    gauges = gpu.get_gauges_values()
    print("Jauges :", gauges)

    # Vérification de la tension et du courant
    for sensor_id in range(1, 4):  # Capteurs S1, S2, S3
        print(f"Tension capteur S{sensor_id} :", gpu.get_voltage(sensor_id))
        print(f"Courant capteur S{sensor_id} :", gpu.get_current(sensor_id))

    # Maintenir le programme en attente pour écouter les boutons
    try:
        input("Appuyez sur Entrée pour quitter...\n")
    finally:
        GPIO.cleanup()
