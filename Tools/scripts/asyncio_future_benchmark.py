"""Benchmark Future completion and callback scheduling."""

import asyncio

import pyperf


def make_benchmark(future_type, callback_count):
    loop = asyncio.new_event_loop()
    callback = lambda future: None

    def benchmark():
        future = future_type(loop=loop)
        for _ in range(callback_count):
            future.add_done_callback(callback)
        future.set_result(None)

    return benchmark


runner = pyperf.Runner()
for name, future_type in (("native", asyncio.Future),
                          ("python", asyncio.futures._PyFuture)):
    for callback_count in (0, 1, 10, 100):
        runner.bench_func(
            f"future_set_result_{name}_{callback_count}",
            make_benchmark(future_type, callback_count),
        )
