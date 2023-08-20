from multiprocessing import cpu_count, Pool, current_process
from time import time
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def factorize(num: int):      
    divisors = []
    for i in range(1, num + 1):
        if num % i == 0:
            divisors.append(i)
    logger.debug(f'In process {current_process()} factorizing {num}')

    return divisors


def main(nums: list[int]):    
    with Pool(processes=num_cores) as pool:
        proc = pool.map(factorize, nums)
        logger.debug(f'Results: {proc}')

    return proc


if __name__ == "__main__": 
    start = time()
    list_numbers = [128, 255, 99999, 10651060]
    num_cores = cpu_count()
    a, b, c, d  = main(list_numbers)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    finish = time()
    print('Execution time: ', finish - start, ' sec')
