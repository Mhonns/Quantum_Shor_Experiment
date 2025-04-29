import math
import random
import time

def is_prime(n, k=5):
    """Miller-Rabin primality test with trial division precheck"""
    if n <= 1:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randint(2, min(n-2, 1<<20))
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s-1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def brent_pollard_factor(n):
    """Brent's optimized Pollard's Rho algorithm"""
    if n%2 == 0: return 2
    if n%3 == 0: return 3
    if n%5 == 0: return 5
    
    y, c, m = random.randint(1, n-1), random.randint(1, n-1), random.randint(1, n-1)
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for _ in range(r):
            y = (pow(y, 2, n) + c) % n
        k = 0
        while k < r and g == 1:
            ys = y
            for _ in range(min(m, r-k)):
                y = (pow(y, 2, n) + c) % n
                q = (q * abs(x - y)) % n
            g = math.gcd(q, n)
            k += m
        r *= 2
    
    if g == n:
        while True:
            ys = (pow(ys, 2, n) + c) % n
            g = math.gcd(abs(x - ys), n)
            if g != 1:
                break
    return g

def factor(n):
    """Recursive factorization function"""
    factors = []
    def _factor(n):
        if n == 1: return
        if is_prime(n):
            factors.append(n)
            return
        d = brent_pollard_factor(n)
        _factor(d)
        _factor(n//d)
    _factor(n)
    return sorted(factors)

def factor_with_lookup(n):
    """Timed factorization wrapper"""
    start = time.perf_counter_ns()
    factors = factor(n)
    end = time.perf_counter_ns()
    return factors, end - start

test_numbers = [
    15,  # 3 * 5
    15,  # 3 * 5
    15,  # 3 * 5
    21,  # 3 * 7
    21,  # 3 * 7
    21,  # 3 * 7
]

# Store results and timings
results = []
timings = []

for n in test_numbers:
    factors, time_ns = factor_with_lookup(n)
    results.append((n, factors))
    timings.append(time_ns)

# Display results
print("Factorization Results:")
for n, factors in results:
    print(f"{n}: {factors}")

print("\nExecution Times (nanoseconds):")
print(timings)