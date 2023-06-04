import fuzzy as f

# Create input fuzzy set
input_set = f.Fuzzy(x_size=100, step=.5, n=3, name='input')

A = input_set.create_trapezoid(0, 0, 20, 30)
B = input_set.create_triangle(20, 30, 40)
C = input_set.create_trapezoid(30, 40, 50, 50)

input_set.add_term(A, 0, "A", "red")
input_set.add_term(B, 1, "B", "blue")
input_set.add_term(C, 2, "C", "green")

# create output fuzzy set
output_set = f.Fuzzy(100, 1, 3, 'output')
D = output_set.create_triangle(0, 0, 50)
E = output_set.create_triangle(20, 60, 80)
F = output_set.create_triangle(60, 100, 100)

output_set.add_term(D, 0, "D", "red")
output_set.add_term(E, 1, "E", "blue")
output_set.add_term(F, 2, "F", "green")

input_val = 33

clipped_set = output_set.clip_set(input_set.get_values(input_val))
aggregated_set = clipped_set.aggregate_all_terms()

f.Fuzzy.draw_fuzzy_sets([input_set, output_set, aggregated_set])

print("Defuzzified value:", f.Fuzzy.defuzzify(aggregated_set))
