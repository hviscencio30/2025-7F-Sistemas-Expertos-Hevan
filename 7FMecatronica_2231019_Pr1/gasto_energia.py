import pandas as pd
from sklearn.linear_model import LinearRegression

# Cargar datos
data = pd.read_csv("data.csv")

# Separar variables independientes y dependientes
X = data[["Horas_Aire", "Horas_Calefaccion", "Horas_PC"]]
y = data["Gasto"]

# Crear y entrenar el modelo
model = LinearRegression()
model.fit(X, y)

# Mostrar coeficientes
print("Coeficientes del modelo:", model.coef_)
print("Intersección (bias):", model.intercept_)

# Predecir nuevo caso de la vida diaria
nuevo_caso = pd.DataFrame({"Horas_Aire":[3], "Horas_Calefaccion":[1], "Horas_PC":[4]})
prediccion = model.predict(nuevo_caso)
print(f"Predicción de gasto para el nuevo caso: {prediccion[0]:.2f} kWh")