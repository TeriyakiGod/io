import fuzzy as f
import numpy as np

# Create temp input fuzzy set
temp_set = f.Fuzzy(x_size=70, step=.5, n=4, name='temperature')

temp_set.add_term(temp_set.create_trapezoid(0, 0, 5, 15), 0, "cold", "blue")
temp_set.add_term(temp_set.create_triangle(5, 15, 25), 1, "cool", "green")
temp_set.add_term(temp_set.create_triangle(15, 25, 35), 2, "warm", "yellow")
temp_set.add_term(temp_set.create_trapezoid(25, 35, 45, 45), 3, "hot", "red")

# Create humidity input fuzzy set
humidity_set = f.Fuzzy(x_size=100, step=1, n=3, name='humidity')

humidity_set.add_term(humidity_set.create_trapezoid(0, 0, 25, 50), 0, "low", "blue")
humidity_set.add_term(humidity_set.create_triangle(25, 50, 100), 1, "medium", "green")
humidity_set.add_term(humidity_set.create_triangle(50, 100, 100), 2, "high", "red")

temp = 17.5
humidity = 60
water = {
    "zero": 0,
    "low": 25,
    "medium": 50,
    "high": 75,
    "maximum": 100
}

fuzzy_temp = temp_set.get_values(temp)
fuzzy_humidity = humidity_set.get_values(humidity)

print("Temperature:")
for i in range(len(fuzzy_temp)):
    print(temp_set.term_names[i], ":", fuzzy_temp[i])

print("\nHumidity:")
for i in range(len(fuzzy_humidity)):
    print(humidity_set.term_names[i], ":", fuzzy_humidity[i])

# Create rules
rules = np.zeros((temp_set.n, humidity_set.n))
rules[0][0] = water["medium"]
rules[0][1] = water["low"]
rules[0][2] = water["zero"]
rules[1][0] = water["high"]
rules[1][1] = water["low"]
rules[1][2] = water["zero"]
rules[2][0] = water["high"]
rules[2][1] = water["medium"]
rules[2][2] = water["low"]
rules[3][0] = water["maximum"]
rules[3][1] = water["high"]
rules[3][2] = water["medium"]

r2 = np.zeros((temp_set.n, humidity_set.n))
for i in range(temp_set.n):
    for j in range(humidity_set.n):
        r2[i][j] = min(fuzzy_temp[i], fuzzy_humidity[j])


water_out = {
    "zero": 0,
    "low": 0,
    "medium": 0,
    "high": 0,
    "maximum": 0
}

# get max value for each water level
for key in water:
    for i in range(temp_set.n):
        for j in range(humidity_set.n):
            if water[key] == rules[i][j]:
                water_out[key] = max(water_out[key], r2[i][j])

print("\nWater:")
for key in water_out:
    print(key, ":", water_out[key])

y = 0
for key in water_out:
    y += water_out[key] * water[key]

y /= sum(water_out.values())
print("\ny =", y)

