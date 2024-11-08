import numpy as np

class Soplete:
    def __init__(self):
        self.temperatura = 0
        self.radio = 3
        self.posicion = (15, 0)

class Placa:
    def __init__(self):
        self.size = 30
        self.temperatura_ambiente = 20
        self.disipacion = 0.5
        self.temperatura = np.full((self.size, self.size), self.temperatura_ambiente)

    def aplicar_soplete(self, soplete, incremento):
        """Aplica calor en una región circular de la placa."""
        print(f"Temperatura: {self.temperatura[soplete.posicion]}")
        x0, y0 = soplete.posicion
        for x in range(max(0, x0 - soplete.radio), min(self.size, x0 + soplete.radio + 1)):
            for y in range(max(0, y0 - soplete.radio), min(self.size, y0 + soplete.radio + 1)):
                if (x - x0)**2 + (y - y0)**2 <= soplete.radio**2:
                    self.temperatura[x, y] = min(self.temperatura[x, y] + incremento, soplete.temperatura)
        self.disipar_calor()


    def disipar_calor(self):
        """Simula la disipación del calor en la placa."""
        for x in range(self.size):
            for y in range(self.size):
                vecinos = self.obtener_vecinos(x, y)
                self.temperatura[x, y] = self.temperatura[x, y] + self.disipacion * (np.mean(vecinos) - self.temperatura[x, y])

    def obtener_vecinos(self, x, y):
        """Obtiene los vecinos de una celda en la placa."""
        vecinos = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    vecinos.append(self.temperatura[nx, ny])
        return vecinos
