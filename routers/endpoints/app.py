import numpy as np
import time

class Soplete:
    def __init__(self):
        self.temperatura = 0  # Temperatura del soplete
        self.radio = 3  # Radio de influencia
        self.posicion = (15, 15)  # Posición inicial

class Placa:
    def __init__(self):
        self.size = 30
        self.temperatura_ambiente = 20
        self.temperatura = np.full((self.size, self.size), self.temperatura_ambiente)
        self.ultimo_tiempo = time.time()  # Marca de tiempo para cálculo de incremento
        self.coeficiente_calor = 0.1  # Ajustable para simular transferencia térmica
        self.coeficiente_disipacion = 0.25  # Ajustable para disipación global

    def aplicar_soplete(self, soplete):
        """Aplica calor basado en tiempo transcurrido y gradiente térmico."""
        tiempo_actual = time.time()
        delta_t = tiempo_actual - self.ultimo_tiempo  # Tiempo transcurrido
        self.ultimo_tiempo = tiempo_actual

        x0, y0 = soplete.posicion
        for x in range(max(0, x0 - soplete.radio), min(self.size, x0 + soplete.radio + 1)):
            for y in range(max(0, y0 - soplete.radio), min(self.size, y0 + soplete.radio + 1)):
                if (x - x0)**2 + (y - y0)**2 <= soplete.radio**2:
                    # Calcular incremento basado en el gradiente térmico y tiempo
                    delta_T = (
                        self.coeficiente_calor
                        * (soplete.temperatura - self.temperatura[x, y])
                        * delta_t
                    )
                    self.temperatura[x, y] += delta_T
                    # Asegurar que la temperatura no exceda la del soplete
                    self.temperatura[x, y] = min(self.temperatura[x, y], soplete.temperatura)

        self.disipar_calor()

    def disipar_calor(self):
        """Disipa el calor en toda la placa usando un Laplaciano."""
        nueva_temperatura = self.temperatura.copy()
        for x in range(0, self.size - 1):
            for y in range(0, self.size - 1):
                # Calcular Laplaciano con vecinos inmediatos
                laplaciano = (
                    self.temperatura[x+1, y] + self.temperatura[x-1, y] +
                    self.temperatura[x, y+1] + self.temperatura[x, y-1] -
                    4 * self.temperatura[x, y]
                )
                # Aplicar disipación basada en el Laplaciano
                nueva_temperatura[x, y] += self.coeficiente_disipacion * laplaciano
        # Actualizar temperatura con los cambios aplicados
        self.temperatura = nueva_temperatura
