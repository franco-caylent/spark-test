# Initialize denominator
k = 1

# Initialize sum
s = 0
how_many = 10000000000
for i in range(how_many):
    if i % 100000000 == 0:
        print("{}/{} iterations".format(i,how_many))
    # even index elements are positive
    if i % 2 == 0:
        s += 4 / k
    else:

        # odd index elements are negative
        s -= 4 / k

    # denominator is odd
    k += 2

print(s)