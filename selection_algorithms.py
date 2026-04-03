"""
Assignment 6 - Part 1: Selection Algorithms
Author: Reza Shrestha

Implements:
  - Deterministic selection (Median of Medians) - O(n) worst-case
  - Randomized Quickselect - O(n) expected time

Both algorithms find the k-th smallest element (1-indexed) in an unsorted array.
"""

import random
import time
import statistics


# ─────────────────────────────────────────────────────────────────────────────
# Deterministic Selection: Median of Medians
# ─────────────────────────────────────────────────────────────────────────────

def insertion_sort(arr):
    """Sort a small array in-place using insertion sort."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def median_of_medians(arr, k):
    """
    Deterministic selection algorithm (Median of Medians).

    Finds the k-th smallest element (1-indexed) in arr in O(n) worst-case time.

    Parameters
    ----------
    arr : list
        Input list of comparable elements (not modified).
    k : int
        1-indexed rank of the desired element.

    Returns
    -------
    The k-th smallest element in arr.

    Raises
    ------
    ValueError
        If k is out of range.
    """
    if not arr:
        raise ValueError("Array must not be empty.")
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} is out of range for array of length {len(arr)}.")

    return _mom_select(list(arr), k)


def _mom_select(arr, k):
    """Internal recursive helper for Median of Medians."""
    n = len(arr)

    # Base case: array small enough to sort directly
    if n <= 5:
        return sorted(arr)[k - 1]

    # Step 1: Divide into groups of 5 (last group may be smaller)
    chunks = [arr[i:i + 5] for i in range(0, n, 5)]

    # Step 2: Find the median of each group
    medians = [sorted(chunk)[len(chunk) // 2] for chunk in chunks]

    # Step 3: Recursively find the median of medians
    pivot = _mom_select(medians, (len(medians) + 1) // 2)

    # Step 4: Partition around the pivot
    low  = [x for x in arr if x < pivot]
    mid  = [x for x in arr if x == pivot]
    high = [x for x in arr if x > pivot]

    # Step 5: Recurse into the correct partition
    if k <= len(low):
        return _mom_select(low, k)
    elif k <= len(low) + len(mid):
        return pivot
    else:
        return _mom_select(high, k - len(low) - len(mid))


# ─────────────────────────────────────────────────────────────────────────────
# Randomized Quickselect
# ─────────────────────────────────────────────────────────────────────────────

def randomized_quickselect(arr, k):
    """
    Randomized selection algorithm (Randomized Quickselect).

    Finds the k-th smallest element (1-indexed) in arr in O(n) expected time.

    Parameters
    ----------
    arr : list
        Input list of comparable elements (not modified).
    k : int
        1-indexed rank of the desired element.

    Returns
    -------
    The k-th smallest element in arr.

    Raises
    ------
    ValueError
        If k is out of range.
    """
    if not arr:
        raise ValueError("Array must not be empty.")
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} is out of range for array of length {len(arr)}.")

    return _rqs_select(list(arr), k)


def _rqs_select(arr, k):
    """Internal recursive helper for Randomized Quickselect."""
    n = len(arr)

    # Base case
    if n == 1:
        return arr[0]

    # Step 1: Choose a random pivot
    pivot = random.choice(arr)

    # Step 2: Partition
    low  = [x for x in arr if x < pivot]
    mid  = [x for x in arr if x == pivot]
    high = [x for x in arr if x > pivot]

    # Step 3: Recurse into the correct partition
    if k <= len(low):
        return _rqs_select(low, k)
    elif k <= len(low) + len(mid):
        return pivot
    else:
        return _rqs_select(high, k - len(low) - len(mid))


# ─────────────────────────────────────────────────────────────────────────────
# Empirical Benchmarking
# ─────────────────────────────────────────────────────────────────────────────

def benchmark(func, arr, k, repeats=5):
    """Return average wall-clock time (seconds) over `repeats` runs."""
    times = []
    for _ in range(repeats):
        data = list(arr)           # fresh copy each run
        start = time.perf_counter()
        func(data, k)
        times.append(time.perf_counter() - start)
    return statistics.mean(times)


def run_empirical_analysis():
    """Run benchmarks across sizes and distributions, print a summary table."""
    sizes = [1_000, 5_000, 10_000, 50_000, 100_000]
    distributions = {
        "random":         lambda n: random.sample(range(n * 10), n),
        "sorted":         lambda n: list(range(n)),
        "reverse-sorted": lambda n: list(range(n, 0, -1)),
        "duplicates":     lambda n: [random.randint(0, n // 10) for _ in range(n)],
    }

    header = f"{'Distribution':<16} {'Size':>8}  {'MoM (ms)':>10}  {'RQS (ms)':>10}  {'Ratio MoM/RQS':>14}"
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)

    results = []
    for dist_name, gen in distributions.items():
        for n in sizes:
            arr = gen(n)
            k   = n // 2          # median-rank element

            t_mom = benchmark(median_of_medians,      arr, k) * 1000
            t_rqs = benchmark(randomized_quickselect, arr, k) * 1000
            ratio = t_mom / t_rqs if t_rqs > 0 else float("inf")

            print(f"{dist_name:<16} {n:>8}  {t_mom:>10.3f}  {t_rqs:>10.3f}  {ratio:>14.2f}x")
            results.append({
                "distribution": dist_name,
                "n": n,
                "mom_ms": round(t_mom, 4),
                "rqs_ms": round(t_rqs, 4),
                "ratio":  round(ratio, 4),
            })

    print(separator)
    return results


# ─────────────────────────────────────────────────────────────────────────────
# Correctness Tests
# ─────────────────────────────────────────────────────────────────────────────

def run_tests():
    """Smoke-test both algorithms against Python's sorted()."""
    test_cases = [
        ([3, 1, 4, 1, 5, 9, 2, 6], 1),
        ([3, 1, 4, 1, 5, 9, 2, 6], 4),
        ([3, 1, 4, 1, 5, 9, 2, 6], 8),
        ([42],                      1),
        (list(range(100, 0, -1)),   37),
        ([5, 5, 5, 5, 5],           3),
    ]

    print("Correctness Tests")
    print("-" * 60)
    all_pass = True
    for arr, k in test_cases:
        expected = sorted(arr)[k - 1]
        mom_res  = median_of_medians(arr, k)
        rqs_res  = randomized_quickselect(arr, k)
        ok = (mom_res == expected == rqs_res)
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_pass = False
        print(f"  [{status}]  arr[0:5]={arr[:5]}...  k={k}  "
              f"expected={expected}  MoM={mom_res}  RQS={rqs_res}")
    print(f"\nAll tests passed: {all_pass}\n")
    return all_pass


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("Part 1: Selection Algorithms")
    print("=" * 60)
    run_tests()
    print("\nEmpirical Benchmark (wall-clock averages over 5 runs):\n")
    run_empirical_analysis()