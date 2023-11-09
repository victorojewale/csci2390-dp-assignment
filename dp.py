from client import count, _pretty_print
from numpy.random import laplace
import numpy as np
import sys
from matplotlib import pyplot

# Return a noised histogram that is epsilon-dp.
def dp_histogram(epsilon):
    sensitivity = 1  # 
    mu = 0  # Mean for the Laplace distribution
    b = sensitivity / epsilon  # Scale for the Laplace distribution
  
    # Get the exact histogram without noise.
    headers, rows = count(["age", "music"], False)

    # Iterate over counts and apply the Laplace noise.
    noised_rows = []
    for (age, music, value) in rows:
        # Compute the noised value.
        noise = laplace(mu, b)
        # Round the noised_value to the closest integer.
        noised_value = int(round(value + noise))

        # Append the noised value and associated group by labels.
        noised_rows.append((age, music, noised_value))  

    return headers, noised_rows

def plot(epsilon):
  ITERATIONS = 150

  # We will store the frequency for each observed value in d.
  d = {}
  for i in range(ITERATIONS):
    headers, rows = dp_histogram(epsilon)
    # Get the value of the first row (age 0 and hip hop).
    value = round(rows[0][-1])
    d[value] = d.get(value, 0) + 1

  # Turn the frequency dictionary into a plottable sequence.
  vmin, vmax = min(d.keys()) - 3, max(d.keys()) + 3
  xs = list(range(vmin, vmax + 1))
  ys = [d.get(x, 0) / ITERATIONS for x in xs]

  # Plot.
  pyplot.plot(xs, ys, 'o-', ds='steps-mid')
  pyplot.xlabel("Count value")
  pyplot.ylabel("Frequency")
  pyplot.savefig('dp-plot.png')

# Run this for epsilon 0.5
if __name__ == "__main__":
  epsilon = 0.5
  if len(sys.argv) > 1:
    epsilon = float(sys.argv[1])

  print("Using epsilon =", epsilon)
  headers, rows = dp_histogram(epsilon)
  _pretty_print(headers, rows)

  # Plotting code.
  
  print("Plotting, this may take a minute ...")
  plot(epsilon)
  print("Plot saved at 'dp-plot.png'")
  