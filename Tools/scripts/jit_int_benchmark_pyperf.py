"""Benchmark integer arithmetic specialization with pyperf.

Run with ``./python.exe Tools/scripts/jit_int_benchmark_pyperf.py``.
Set ``PYTHON_JIT=1`` in the environment to benchmark the JIT path.
Each timed call performs enough iterations to cross the JIT threshold.
"""

import pyperf


LOOPS = 100_000


def _warmup(func):
    """Compile the hot loop before pyperf starts collecting samples."""
    if not getattr(func, "warmed", False):
        func()
        func.warmed = True
    return func


def bench_small():
    value = 0
    for _ in range(LOOPS):
        value = (value + 1) * 3 - 2
    return value


def bench_wide():
    value = 1 << 40
    for _ in range(LOOPS):
        # Keep the value non-compact and within int64 so this measures the
        # steady-state wide-int specialization instead of eventual bigint
        # growth and deoptimization.
        value -= 1
    return value


def bench_wide_three_digit_result():
    left = 1 << 62
    right = 1 << 61
    result = 0
    for _ in range(LOOPS):
        # Keep both operands and the result non-compact but within int64.
        result = left - right
    return result


def bench_shrinking_subtraction():
    value = 0
    left = 10_000_000_001
    right = 10_000_000_000
    for _ in range(LOOPS):
        value += left - right
    return value


def bench_mixed():
    value = 1
    for index in range(LOOPS):
        if index & 1:
            value += 1 << 40
        else:
            value -= 1 << 40
    return value


def bench_wide_inplace_add():
    value = 1 << 40
    for _ in range(LOOPS):
        value += 1
    return value


def bench_wide_inplace_subtract():
    value = 1 << 40
    for _ in range(LOOPS):
        value -= 1
    return value


def bench_wide_inplace_multiply():
    value = 1 << 40
    for _ in range(LOOPS):
        value *= 1
    return value


runner = pyperf.Runner()
runner.bench_func("int_small", _warmup(bench_small))
runner.bench_func("int_wide", _warmup(bench_wide))
runner.bench_func(
    "int_wide_three_digit_result", _warmup(bench_wide_three_digit_result)
)
runner.bench_func(
    "int_shrinking_subtraction", _warmup(bench_shrinking_subtraction)
)
runner.bench_func("int_mixed", _warmup(bench_mixed))
runner.bench_func("int_wide_inplace_add", _warmup(bench_wide_inplace_add))
runner.bench_func(
    "int_wide_inplace_subtract", _warmup(bench_wide_inplace_subtract)
)
runner.bench_func(
    "int_wide_inplace_multiply", _warmup(bench_wide_inplace_multiply)
)
