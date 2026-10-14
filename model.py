import numpy as np
from sklearn.linear_model import LinearRegression

# Sample training data
# [food_prepared, food_sold, remaining_food]
X = np.array([
    [100, 90, 10],
    [120, 100, 20],
    [150, 120, 30],
    [200, 160, 40],
    [250, 200, 50],
    [300, 240, 60],
    [180, 150, 30],
    [220, 180, 40]
])

# Actual surplus values for training
y = np.array([
    10,
    20,
    30,
    40,
    50,
    60,
    30,
    40
])

model = LinearRegression()

model.fit(X, y)


def predict_surplus(food_prepared, food_sold, remaining_food):

    data = np.array([
        [food_prepared, food_sold, remaining_food]
    ])

    prediction = model.predict(data)

    surplus = round(float(prediction[0]), 2)

    if surplus < 0:
        surplus = 0

    return surplus