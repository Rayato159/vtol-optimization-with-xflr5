#MTOW is going to estimated by a payload.

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_csv('../data/VTOL_data.csv')

X = df[['Payload_kg']]
y = df['MTOW_kg']

model = LinearRegression()
model.fit(X, y)
r2 = model.score(X, y)

X_plot = np.linspace(df['Payload_kg'].min(), df['Payload_kg'].max(), 100)
y_predict = model.predict(X_plot.reshape(-1, 1))

plt.title(f'Weight_Estimation R^2 = {round(r2, 2)}')
plt.xlabel('Payload (kg)')
plt.ylabel('MTOW (kg)')
plt.scatter(X, y)
plt.plot(X_plot, y_predict, color='#FF0000')
plt.show()

print(f'MTOW_Estimate = {model.predict(np.array([2.3]).reshape(-1, 1))[0]}')