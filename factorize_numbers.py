import time
import sys
from multiprocessing import Pool, cpu_count, current_process
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(processName)s: %(message)s')


def factorize_single(n: int) -> list[int]:
    divisors = []
    for i in range(1, n + 1):
        if n % i == 0:
            divisors.append(i)
    logging.info(f"Done factorizing {n} in {current_process().name}")
    return divisors


def factorize_sync(*numbers: int) -> list[list[int]]:
    logging.info("Starting synchronous factorization...")
    results = []
    for number in numbers:
        results.append(factorize_single(number))
    logging.info("Synchronous factorization complete.")
    return results


def factorize_parallel(*numbers: int) -> list[list[int]]:
    logging.info("Starting parallel factorization...")
    num_cores = cpu_count()
    logging.info(f"Using {num_cores} CPU cores for parallel processing.")

    with Pool(processes=num_cores) as pool:
        # pool.map applies factorize_single to each number in the 'numbers' iterable
        # and collects the results.
        results = pool.map(factorize_single, numbers)

    logging.info("Parallel factorization complete.")
    return results


if __name__ == '__main__':
    # Test numbers as provided in the assignment
    test_numbers = (128, 255, 99999, 10651060)

    # --- 1. Run Synchronous Version ---
    logging.info("--- Running Synchronous Factorization ---")
    start_time_sync = time.time()  # Start time measurement
    # Call the synchronous version of factorize
    a_sync, b_sync, c_sync, d_sync = factorize_sync(*test_numbers)
    end_time_sync = time.time()  # End time measurement
    sync_duration = end_time_sync - start_time_sync
    logging.info(f"Synchronous factorization took: {sync_duration:.4f} seconds")

    # Verify synchronous results using assert
    logging.info("Verifying synchronous results...")
    assert a_sync == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b_sync == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c_sync == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d_sync == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790,
                      1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    logging.info("Synchronous results verified successfully!")

    # --- 2. Run Parallel Version ---
    logging.info("--- Running Parallel Factorization ---")
    start_time_parallel = time.time()  # Start time measurement
    # Call the parallel version of factorize
    a_parallel, b_parallel, c_parallel, d_parallel = factorize_parallel(*test_numbers)
    end_time_parallel = time.time()  # End time measurement
    parallel_duration = end_time_parallel - start_time_parallel
    logging.info(f"Parallel factorization took: {parallel_duration:.4f} seconds")

    # Verify parallel results using assert
    logging.info("Verifying parallel results...")
    assert a_parallel == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b_parallel == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c_parallel == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d_parallel == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790,
                          1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    logging.info("Parallel results verified successfully!")

    logging.info("--- Performance Comparison ---")
    logging.info(f"Synchronous: {sync_duration:.4f} seconds")
    logging.info(f"Parallel:    {parallel_duration:.4f} seconds")
    if sync_duration > parallel_duration:
        logging.info(f"Parallel version was {sync_duration / parallel_duration:.2f} times faster!")
    else:
        logging.info("Parallel version was not faster or was slower (this can happen for small inputs).")

    # Optional: Run with command line arguments (Parallel)
    if len(sys.argv) > 1:
        logging.info("--- Running with command line arguments (Parallel) ---")
        try:
            cmd_numbers = [int(arg) for arg in sys.argv[1:]]
            cmd_start_time = time.time()
            cmd_results = factorize_parallel(*cmd_numbers)
            cmd_end_time = time.time()
            cmd_duration = cmd_end_time - cmd_start_time
            logging.info(f"Factorization for command line numbers took: {cmd_duration:.4f} seconds")
            for number, divisors in zip(cmd_numbers, cmd_results):
                logging.info(f"Factors of {number}: {divisors}")
        except ValueError:
            logging.error("Please provide only integers as command line arguments.")
        except Exception as e:
            logging.error(f"An error occurred with command line arguments: {e}")
