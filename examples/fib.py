import time

fibonacci_numbers = [1, 1]

while True:
    print(fibonacci_numbers[-1])
    fibonacci_numbers.append(fibonacci_numbers[-1] + fibonacci_numbers[-2])
    time.sleep(1)