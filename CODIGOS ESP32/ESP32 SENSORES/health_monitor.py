class HealthMonitor:
    def __init__(self, sensor):
        self.sensor = sensor
        self.beats = 0

    def calculate_bpm(self, value_red):
        """Calcular el BPM basado en las lecturas de rojo"""
        minima = min(self.sensor.history_red)
        maxima = max(self.sensor.history_red)
        threshold_on = minima + (maxima - minima) * 0.75  # Umbral 75%
        threshold_off = minima + (maxima - minima) * 0.5  # Umbral 50%

        if value_red > 1000:  # Confirmar que haya un dedo
            if not self.sensor.beat and value_red > threshold_on:
                self.sensor.beat = True
                t_us = ticks_diff(ticks_us(), self.sensor.t_start)
                self.sensor.t_start = ticks_us()
                bpm = 60 / (t_us / 1e6)  # Calcular BPM

                if bpm < 500:  # Filtrar valores erróneos
                    self.sensor.beats_history.append(bpm)
                    if len(self.sensor.beats_history) > 10:  # Buffer de 10 BPM
                        self.sensor.beats_history.pop(0)
                    self.beats = sum(self.sensor.beats_history) / len(self.sensor.beats_history)  # Promedio BPM
            elif self.sensor.beat and value_red < threshold_off:
                self.sensor.beat = False
        else:
            self.sensor.beat = False

    def calculate_spo2(self):
        """Calcular SpO₂ basado en las lecturas de rojo e IR"""
        dc_red = sum(self.sensor.history_red) / len(self.sensor.history_red)
        ac_red = max(self.sensor.history_red) - min(self.sensor.history_red)

        dc_ir = sum(self.sensor.history_ir) / len(self.sensor.history_ir)
        ac_ir = max(self.sensor.history_ir) - min(self.sensor.history_ir)

        if dc_red > 0 and dc_ir > 0:
            ratio = (ac_red / dc_red) / (ac_ir / dc_ir)
            spo2 = 110 - 25 * ratio  # Fórmula empírica
            return max(0, min(100, spo2))  # Limitar rango a 0-100%
        return None

    def get_bpm_and_spo2(self):
        """Obtener BPM y SpO₂"""
        red_reading, ir_reading = self.sensor.read_data()
        self.sensor.update_history(red_reading, ir_reading)
        self.calculate_bpm(red_reading)
        spo2 = self.calculate_spo2()
        return round(self.beats, 2), round(spo2, 2) if spo2 else None
