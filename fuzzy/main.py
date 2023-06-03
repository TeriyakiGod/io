import fuzzy

# Create input fuzzy set
input_set = fuzzy.Fuzzy(x_size=100, step=.5, n=3, name='input')

A = input_set.create_trapezoid(0, 0, 20, 30)
B = input_set.create_triangle(20, 30, 40)
C = input_set.create_trapezoid(30, 40, 50, 50)

input_set.add_term(A, "A", "red")
input_set.add_term(B, "B", "blue")
input_set.add_term(C, "C", "green")

# create output fuzzy set
output_set = fuzzy.Fuzzy(100, 1, 3, 'output')
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
