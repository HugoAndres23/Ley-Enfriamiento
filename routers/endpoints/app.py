import numpy as np
import time

class Soplete:
    def __init__(self):
        self.temperatura = 0
        self.radio = 0
        self.posicion = (15, 15)

class Placa:
    def __init__(self):
        self.size = 31
        self.temperatura_ambiente = 20
        self.temperatura = np.full((self.size, self.size), self.temperatura_ambiente)
        self.ultimo_tiempo = time.time()
        self.coeficiente_calor = 0.1
        self.coeficiente_disipacion = 0.25

    def aplicar_soplete(self, soplete):
        """Aplica calor basado en tiempo transcurrido y gradiente térmico."""
        tiempo_actual = time.time()
        delta_t = tiempo_actual - self.ultimo_tiempo
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
                nueva_temperatura[x, y] += self.coeficiente_disipacion * laplaciano
        self.temperatura = nueva_temperatura

    def enfriar_lentamente(self):
        """Reduce la temperatura hacia la temperatura ambiente."""
        for x in range(self.size):
            for y in range(self.size):
                if self.temperatura[x, y] > self.temperatura_ambiente:
                    self.temperatura[x, y] -= 0.005
                    self.temperatura[x, y] = max(self.temperatura[x, y], self.temperatura_ambiente)
