from client import avg, count, count0, _pretty_print
from dp import dp_histogram

# This function should expose the true value of some aggregate/query
# by abusing the fact that you can make many such queries.
# query_func is a 0-arguments function, every time you call it, you execute the
# query once and get one set of results.
def expose(query_func):
    headers, many_results = None, []
    # Make many queries and save their results.
    print("Making 200 queries with noise. This may take a minute...")
    for i in range(200):
        headers, results = query_func()
        many_results.append(results)

    # Expose the value of the query.
    exposed_result = []
    num_iterations = len(many_results)
    rows = len(many_results[0])
    # This generates a single table with `rows` rows; your task is to use
    # `many_results` to compute each row's aggregation value.
    for r in range(rows):
        # Initialize the sum of noisy values for the current row.
        sum_noisy_values = 0
        for i in range(num_iterations):
            sum_noisy_values += many_results[i][r][-1]
        # Calculate the average of noisy values by dividing the sum by the number of iterations.
        average_noisy_value = sum_noisy_values / num_iterations
        # Round the average to get an integer value, as the original data was in integers.
        rounded_average = round(average_noisy_value)
        # Get the labels from the first set of results (these are not affected by noise).
        labels = tuple(many_results[0][r][:-1])
        # Combine the labels with the rounded average to form the exposed result for this row.
        exposed_row = labels + (rounded_average,)
        # Add the exposed result to the list of results to be returned.
        exposed_result.append(exposed_row)
    
    return headers, exposed_result


if __name__ == "__main__":
    # For testing: if your expose function works, then you should be able
    # to expose the original results of the age and music histogram from 
    # the noised data.
    print("TESTING: the two histograms should be (almost) equal.\n")

    print("Non-noised histogram (from part 1):")
    headers, result = count(["age", "music"], False)
    _pretty_print(headers, result)

    # Use the expose function with the dp_histogram function as the query.
    headers, result = expose(lambda: dp_histogram(0.5))
    _pretty_print(headers, result)  

    # The following code is commented out; remove the triple quotes to use it.
  
    print("Exposing average:")
    headers, result = expose(lambda: avg(["programming"], "age", True))
    _pretty_print(headers, result)
    print("")
    
    print("Exposing count:")
    headers, result = expose(lambda: count0(["programming"], True))
    _pretty_print(headers, result)
    print("")
   