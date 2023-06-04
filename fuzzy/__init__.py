import numpy as np
import matplotlib.pyplot as plt


class Fuzzy:
    def __init__(self, x_size, step, n, name):
        self.X = np.zeros(x_size + 1)
        for i in range(0, x_size + 1):
            self.X[i] = i * step
        self.Y = np.zeros((n, x_size + 1))
        self.term_names = [""] * n
        self.term_colors = [""] * n
        self.step = step
        self.n = n
        self.x_size = x_size
        self.name = name

    def get_values(self, x):
        vals = np.zeros(self.n)
        x = int(x / self.step)
        for i in range(0, self.n):
            vals[i] = self.Y[i][x]
        return vals

    def add_term(self, term, index, name, color):
        self.Y[index] = term
        self.term_names[index] = name
        self.term_colors[index] = color

    def create_singleton(self, a):
        term = np.zeros(self.x_size + 1)
        for i in range(0, self.x_size + 1):
            x = i * self.step
            if x == a:
                figure = 1
            else:
                figure = 0
            term[i] = figure
        return term

    def create_triangle(self, a, b, c):
        term = np.zeros(self.x_size + 1)
        for i in range(0, self.x_size + 1):
            x = i * self.step
            if a <= x <= b:
                figure = (x - a) / (b - a) if (b - a) != 0 else 1 if x == a else 0
            elif b < x <= c:
                figure = (c - x) / (c - b) if (c - b) != 0 else 1 if x == c else 0
            else:
                figure = 0
            term[i] = figure
        return term

    def create_trapezoid(self, a, b, c, d):
        term = np.zeros(self.x_size + 1)
        for i in range(0, self.x_size + 1):
            x = i * self.step
            if a <= x <= b:
                figure = (x - a) / (b - a) if (b - a) != 0 else 1 if x == a else 0
            elif b <= x <= c:
                figure = 1
            elif c < x <= d:
                figure = (d - x) / (d - c) if (d - c) != 0 else 1 if x == d else 0
            else:
                figure = 0
            term[i] = figure
        return term

    def create_gaussian(self, a, b):
        term = np.zeros(self.x_size + 1)
        for i in range(0, self.x_size + 1):
            x = i * self.step
            if b != 0:
                figure = np.exp(-0.5 * ((x - a) / b) ** 2)
            else:
                figure = 1 if x == a else 0
            term[i] = figure
        return term

    def draw_all_fuzzy_sets(self):
        plt.figure()
        for i in range(self.n):
            plt.plot(self.X, self.Y[i], label=self.term_names[i], color=self.term_colors[i])
        plt.xlabel(f'{self.name}')
        plt.ylabel(f'u({self.name})')
        plt.legend()
        plt.show()

    @staticmethod
    def fuzzy_and(term1, term2):
        return np.minimum(term1, term2)

    @staticmethod
    def fuzzy_or(term1, term2):
        return np.maximum(term1, term2)

    @staticmethod
    def fuzzy_not(term):
        return 1 - term

    def aggregate_all_terms(self):
        a_set = np.zeros(self.X.size)
        for i in range(self.n):
            a_set = np.maximum(a_set, self.Y[i])
        # return new fuzzyset with aggregated values
        new_set = Fuzzy(self.x_size, self.step, 1, self.name)
        new_set.Y[0] = a_set
        new_set.term_names = ["Aggregate"]
        new_set.term_colors = ["black"]
        return new_set

    def clip_set(self, vals):
        s = np.zeros((self.n, self.x_size + 1))
        for i in range(self.n):
            for j in range(self.x_size + 1):
                s[i][j] = min(self.Y[i][j], vals[i])
        # return new fuzzyset with clipped values
        new_set = Fuzzy(self.x_size, self.step, self.n, self.name)
        new_set.Y = s
        new_set.term_names = self.term_names
        new_set.term_colors = self.term_colors
        return new_set

    @staticmethod
    def draw_fuzzy_sets(fuzzy_array):
        fig, axes = plt.subplots(len(fuzzy_array), 1)

        for i, fuzzy_set in enumerate(fuzzy_array):
            ax = axes[i]
            for j in range(fuzzy_set.n):
                ax.plot(fuzzy_set.X, fuzzy_set.Y[j], label=fuzzy_set.term_names[j], color=fuzzy_set.term_colors[j])
            ax.set_xlabel(fuzzy_set.name)
            ax.set_ylabel(f'u({fuzzy_set.name})')
            ax.legend()

        plt.tight_layout()
        plt.show()

    @staticmethod
    def defuzzify(fuzzy_set):
        numerator = 0
        denominator = 0

        for i in range(fuzzy_set.n):
            for j in range(fuzzy_set.x_size + 1):
                numerator += fuzzy_set.X[j] * fuzzy_set.Y[i][j]
                denominator += fuzzy_set.Y[i][j]

        if denominator != 0:
            defuzz_value = numerator / denominator
        else:
            defuzz_value = 0

        return defuzz_value


# Create input fuzzy set
input_set = Fuzzy(x_size=100, step=.5, n=3, name='input')

A = input_set.create_trapezoid(0, 0, 20, 30)
B = input_set.create_triangle(20, 30, 40)
C = input_set.create_trapezoid(30, 40, 50, 50)

input_set.add_term(A, 0, "A", "red")
input_set.add_term(B, 1, "B", "blue")
input_set.add_term(C, 2, "C", "green")

# create output fuzzy set
output_set = Fuzzy(100, 1, 3, 'output')
D = output_set.create_triangle(0, 0, 50)
E = output_set.create_triangle(20, 60, 80)
F = output_set.create_triangle(60, 100, 100)

output_set.add_term(D, 0, "D", "red")
output_set.add_term(E, 1, "E", "blue")
output_set.add_term(F, 2, "F", "green")

input_val = 33

clipped_set = output_set.clip_set(input_set.get_values(input_val))
aggregated_set = clipped_set.aggregate_all_terms()

Fuzzy.draw_fuzzy_sets([input_set, output_set, aggregated_set])

print("Defuzzified value:", Fuzzy.defuzzify(aggregated_set))
