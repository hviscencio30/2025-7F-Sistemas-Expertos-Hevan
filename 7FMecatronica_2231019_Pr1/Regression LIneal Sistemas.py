import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Datos simulados de la vida real
# -----------------------------
# Cantidades producidas (en unidades)
x = np.array([10, 20, 30, 40, 50, 60])

# Costos reales registrados (costo fijo + costo variable por unidad)
# Ejemplo: costo fijo = 200, costo variable = 50 → Costo total = 200 + 50 * x
y = 200 + 50 * x + np.random.randint(-20, 20, size=len(x))  # con algo de ruido

# -----------------------------
# Función para calcular error cuadrático medio
# -----------------------------
def calcular_error(w, b, x, y):
    y_pred = w * x + b
    error = np.mean((y - y_pred)**2)
    return error

# -----------------------------
# Búsqueda de los mejores parámetros w y b
# -----------------------------
w_values = np.arange(40, 61, 1)   # probar costos variables entre 40 y 60
b_values = np.arange(150, 251, 10) # probar costos fijos entre 150 y 250

best_w, best_b, min_error = None, None, float("inf")

for w in w_values:
    for b in b_values:
        e = calcular_error(w, b, x, y)
        if e < min_error:
            best_w, best_b, min_error = w, b, e

print(f"Mejor costo variable (w): {best_w}")
print(f"Mejor costo fijo (b): {best_b}")
print(f"Error mínimo: {min_error:.2f}")

# -----------------------------
# Visualización
# -----------------------------
y_pred = best_w * x + best_b

plt.scatter(x, y, color="blue", label="Datos reales (costos observados)")
plt.plot(x, y_pred, color="red", label=f"Modelo estimado: Costo = {best_w}*x + {best_b}")
plt.xlabel("Unidades producidas")
plt.ylabel("Costo total")
plt.title("Estimación de costos de producción")
plt.legend()
plt.grid()
plt.show()
