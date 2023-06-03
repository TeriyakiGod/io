import numpy as np
import matplotlib.pyplot as plt


class Term:
    """
    Represents a fuzzy term with membership values.

    Attributes:
        values (numpy.ndarray): Array of membership values for each point in the fuzzy set.
    """

    def __init__(self, values):
        self.values = values


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


# Usage example
fuzzy_set = Fuzzy(100, 0.1, 3, "Example Fuzzy Set")

# Create terms
term1 = fuzzy_set.create_singleton(30)
term2 = fuzzy_set.create_triangle(20, 40, 60)
term3 = fuzzy_set.create_gaussian(70, 10)

# Add terms to fuzzy set
fuzzy_set.add_term(term1, "Singleton", "red")
fuzzy_set.add_term(term2, "Triangle", "green")
fuzzy_set.add_term(term3, "Gaussian", "blue")

# Draw all fuzzy terms
fuzzy_set.draw_all_fuzzy_sets()

# Get membership values for a specific x value
x_value = 35
values = fuzzy_set.get_values(x_value)
print("Membership values for x =", x_value, ":", values)
