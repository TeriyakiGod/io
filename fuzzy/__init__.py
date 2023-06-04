import numpy as np
import matplotlib.pyplot as plt


class Fuzzy:
    """
    Represents a fuzzy set with multiple terms.

    Attributes:
        X (numpy.ndarray): Array of X-axis values for the fuzzy set.
        Y (numpy.ndarray): 2D array of membership values for each term in the fuzzy set.
        terms (list): List of tuples representing the name and color of each term.
        step (float): Step size between X-axis values.
        n (int): Number of terms in the fuzzy set.
        x_size (int): Size of the X-axis array.
        name (str): Name of the fuzzy set.
    """

    def __init__(self, x_size, step, n, name):
        """
        Initializes a Fuzzy instance.

        Args:
            x_size (int): Size of the X-axis array.
            step (float): Step size between X-axis values.
            n (int): Number of terms in the fuzzy set.
            name (str): Name of the fuzzy set.
        """
        self.X = np.zeros(x_size + 1)
        for i in range(0, x_size + 1):
            self.X[i] = i * step
        self.Y = np.zeros((n, x_size + 1))
        self.terms = []
        self.step = step
        self.n = n
        self.x_size = x_size
        self.name = name

    def get_values(self, x):
        """
        Get the membership values for a given x value.

        Args:
            x (float): X value.

        Returns:
            numpy.ndarray: Array of membership values for the given x value.
        """
        vals = np.zeros(self.n)
        x = int(x / self.step)
        if x <= self.x_size:
            for i in range(0, self.n):
                vals[i] = self.Y[i][x]
        return vals

    def add_term(self, term, name, color):
        """
        Add a term to the fuzzy set.

        Args:
            term (Term): Fuzzy term to add.
            name (str): Name of the term.
            color (str): Color of the term in the plot.
        """
        self.Y[len(self.terms)] = term.values
        self.terms.append((name, color))

    def create_singleton(self, a):
        """
        Create a singleton fuzzy term.

        Args:
            a (float): Value of the singleton.

        Returns:
            Term: Singleton fuzzy term.
        """
        values = np.zeros(self.x_size + 1)
        for i in range(0, self.x_size + 1):
            x = i * self.step
            if x == a:
                figure = 1
            else:
                figure = 0
            values[i] = figure
        return Term(values)

    def create_triangle(self, a, b, c):
        """
        Create a triangular fuzzy term.

        Args:
            a (float): Left boundary of the triangle.
            b (float): Peak of the triangle.
            c (float): Right boundary of the triangle.

        Returns:
            Term: Triangular fuzzy term.
        """
        values = np.zeros(self.x_size + 1)
        for i in range(0, self.x_size + 1):
            x = i * self.step
            if a <= x <= b:
                figure = (x - a) / (b - a) if (b - a) != 0 else 1 if x == a else 0
            elif b < x <= c:
                figure = (c - x) / (c - b) if (c - b) != 0 else 1 if x == c else 0
            else:
                figure = 0
            values[i] = figure
        return Term(values)

    def create_trapezoid(self, a, b, c, d):
        """
        Create a trapezoidal fuzzy term.

        Args:
            a (float): Left boundary of the trapezoid.
            b (float): Left slope of the trapezoid.
            c (float): Right slope of the trapezoid.
            d (float): Right boundary of the trapezoid.

        Returns:
            Term: Trapezoidal fuzzy term.
        """
        values = np.zeros(self.x_size + 1)
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
            values[i] = figure
        return Term(values)

    def create_gaussian(self, a, b):
        """
        Create a Gaussian fuzzy term.

        Args:
            a (float): Mean of the Gaussian.
            b (float): Standard deviation of the Gaussian.

        Returns:
            Term: Gaussian fuzzy term.
        """
        values = np.zeros(self.x_size + 1)
        for i in range(0, self.x_size + 1):
            x = i * self.step
            if b != 0:
                figure = np.exp(-0.5 * ((x - a) / b) ** 2)
            else:
                figure = 1 if x == a else 0
            values[i] = figure
        return Term(values)

    def draw_fuzzy_set(self, index):
        """
        Draw a plot of a specific fuzzy term.

        Args:
            index (int): Index of the term to plot.
        """
        plt.plot(self.X, self.Y[index], label=self.terms[index][0], color=self.terms[index][1])
        plt.xlabel('X')
        plt.ylabel('Membership')
        plt.title('Fuzzy Set {}'.format(index))
        plt.legend()
        plt.show()

    def draw_all_fuzzy_sets(self):
        """
        Draw a plot of all fuzzy terms in the fuzzy set.
        """
        plt.figure()
        for i in range(self.n):
            plt.plot(self.X, self.Y[i], label=self.terms[i][0], color=self.terms[i][1])
        plt.xlabel(f'{self.name}')
        plt.ylabel(f'u({self.name})')
        plt.legend()
        plt.show()

    @staticmethod
    def fuzzy_and(term1, term2):
        """
        Perform fuzzy AND operation between two terms.

        Args:
            term1 (Term): First term.
            term2 (Term): Second term.

        Returns:
            numpy.ndarray: Result of the fuzzy AND operation.
        """
        return np.minimum(term1.values, term2.values)

    @staticmethod
    def fuzzy_or(term1, term2):
        """
        Perform fuzzy OR operation between two terms.

        Args:
            term1 (Term): First term.
            term2 (Term): Second term.

        Returns:
            numpy.ndarray: Result of the fuzzy OR operation.
        """
        return np.maximum(term1.values, term2.values)

    @staticmethod
    def fuzzy_not(term):
        """
        Perform fuzzy NOT operation on a term.

        Args:
            term (Term): Term to negate.

        Returns:
            numpy.ndarray: Result of the fuzzy NOT operation.
        """
        return 1 - term.values

    def sum_all_terms(self):
        """
        Sum all terms in the fuzzy set.

        Returns:
            Fuzzy: Fuzzy set with summed values.
        """
        s = np.zeros(self.X.size)
        for i in range(self.n):
            s = self.fuzzy_or(s, self.Y[i])
        # return new fuzzyset with summed values
        new_set = Fuzzy(self.x_size, self.step, 1, self.name)
        new_set.Y = s
        new_set.terms = [("Sum", "black")]
        return new_set

    def clip_set(self, vals):
        """
        Clip the fuzzy set based on a given set of values.

        Args:
            vals (numpy.ndarray): Array of clipping values for each term.

        Returns:
            Fuzzy: Fuzzy set with clipped values.
        """
        s = np.zeros((self.n, self.x_size + 1))
        for i in range(self.n):
            for j in range(self.x_size + 1):
                s[i][j] = min(self.Y[i][j], vals[i])
        # return new fuzzyset with clipped values
        new_set = Fuzzy(self.x_size, self.step, self.n, self.name)
        new_set.Y = s
        new_set.terms = self.terms
        return new_set


# Create input fuzzy set
input_set = Fuzzy(x_size=100, step=.5, n=3, name='input')

A = input_set.create_trapezoid(0, 0, 20, 30)
B = input_set.create_triangle(20, 30, 40)
C = input_set.create_trapezoid(30, 40, 50, 50)

input_set.add_term(A, "A", "red")
input_set.add_term(B, "B", "blue")
input_set.add_term(C, "C", "green")

# create output fuzzy set
output_set = Fuzzy(100, 1, 3, 'output')
D = output_set.create_triangle(0, 0, 50)
E = output_set.create_triangle(20, 60, 80)
F = output_set.create_triangle(60, 100, 100)

output_set.add_term(D, "D", "red")
output_set.add_term(E, "E", "blue")
output_set.add_term(F, "F", "green")

input_val = 33

clipped_set = output_set.clip_set(input_set.get_values(input_val))
summed_set = output_set.sum_all_terms()
summed_set.draw_fuzzy_set(0)
