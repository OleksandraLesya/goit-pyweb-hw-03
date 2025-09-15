# factorize_numbers.py

import time
import sys
from multiprocessing import Pool, cpu_count, current_process
from logger import logger  # Import shared logger


def factorize_single(n: int) -> list[int]:
    """
    Returns a list of all divisors of a given integer.
    """
    divisors = []
    for i in range(1, n + 1):
        if n % i == 0:
            divisors.append(i)
    logger.info(f"Done factorizing {n} in {current_process().name}")
    return divisors


def factorize_sync(*numbers: int) -> list[list[int]]:
    """
    Factorizes numbers synchronously, one after the other.
    """
    logger.info("Starting synchronous factorization...")
    results = []
    for number in numbers:
        results.append(factorize_single(number))
    logger.info("Synchronous factorization complete.")
    return results


def factorize_parallel(*numbers: int) -> list[list[int]]:
    """
    Factorizes numbers in parallel using multiprocessing.
    """
    logger.info("Starting parallel factorization...")
    num_cores = cpu_count()
    logger.info(f"Using {num_cores} CPU cores for parallel processing.")

    with Pool(processes=num_cores) as pool:
        results = pool.map(factorize_single, numbers)

    logger.info("Parallel factorization complete.")
    return results


if __name__ == '__main__':
    test_numbers = (128, 255, 99999, 10651060)

    # --- 1. Run Synchronous Version ---
    logger.info("--- Running Synchronous Factorization ---")
    start_time_sync = time.time()
    a_sync, b_sync, c_sync, d_sync = factorize_sync(*test_numbers)
    end_time_sync = time.time()
    sync_duration = end_time_sync - start_time_sync
    logger.info(f"Synchronous factorization took: {sync_duration:.4f} seconds")

    logger.info("Verifying synchronous results...")
    assert a_sync == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b_sync == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c_sync == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d_sync == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158,
                      304316, 380395, 532553, 760790, 1065106, 1521580, 2130212,
                      2662765, 5325530, 10651060]
    logger.info("Synchronous results verified successfully!")

    # --- 2. Run Parallel Version ---
    logger.info("--- Running Parallel Factorization ---")
    start_time_parallel = time.time()
    a_parallel, b_parallel, c_parallel, d_parallel = factorize_parallel(*test_numbers)
    end_time_parallel = time.time()
    parallel_duration = end_time_parallel - start_time_parallel
    logger.info(f"Parallel factorization took: {parallel_duration:.4f} seconds")

    logger.info("Verifying parallel results...")
    assert a_parallel == a_sync
    assert b_parallel == b_sync
    assert c_parallel == c_sync
    assert d_parallel == d_sync
    logger.info("Parallel results verified successfully!")

    logger.info("--- Performance Comparison ---")
    logger.info(f"Synchronous: {sync_duration:.4f} seconds")
    logger.info(f"Parallel:    {parallel_duration:.4f} seconds")
    if sync_duration > parallel_duration:
        logger.info(f"Parallel version was {sync_duration / parallel_duration:.2f} times faster!")
    else:
        logger.info("Parallel version was not faster or was slower (this can happen for small inputs).")

    # Optional: Run with command line arguments
    if len(sys.argv) > 1:
        logger.info("--- Running with command line arguments (Parallel) ---")
        try:
            cmd_numbers = [int(arg) for arg in sys.argv[1:]]
            cmd_start_time = time.time()
            cmd_results = factorize_parallel(*cmd_numbers)
            cmd_end_time = time.time()
            cmd_duration = cmd_end_time - cmd_start_time
            logger.info(f"Factorization for command line numbers took: {cmd_duration:.4f} seconds")
            for number, divisors in zip(cmd_numbers, cmd_results):
                logger.info(f"Factors of {number}: {divisors}")
        except ValueError:
            logger.error("Please provide only integers as command line arguments.")
        except Exception as e:
            logger.error(f"An error occurred with command line arguments: {e}")
