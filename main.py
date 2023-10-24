import threading
import time
import itertools

def collatz_sequence_steps(n):
    start_time = time.time()
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    end_time = time.time()
    return end_time - start_time, steps


def calculate_average_steps_for_numbers(num_numbers, num_threads):
    start_time = time.time()
    results = {
        'total_time': 0,
        'total_steps': 0,
    }
    lock = threading.Lock()
    numbers_to_process = itertools.cycle(range(1, num_numbers + 1))

    def process_numbers():
        nonlocal results
        for _ in range(num_numbers // num_threads):
            n = next(numbers_to_process)
            time_per_number, steps_per_number = collatz_sequence_steps(n)
            with lock:
                results['total_time'] += time_per_number
                results['total_steps'] += steps_per_number

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=process_numbers)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    results['execution_time'] = end_time - start_time
    return results

if __name__ == "__main__":
    num_numbers = int(input("Enter the number of numbers: "))
    num_threads = int(input("Enter the number of threads: "))
    results = calculate_average_steps_for_numbers(num_numbers, num_threads)
    total_steps = results['total_steps']
    execution_time = results['execution_time']
    print(f"Average number of steps: {total_steps/num_numbers:.2f}")
    print(f"Execution time of all threads: {execution_time:.5f} seconds")
