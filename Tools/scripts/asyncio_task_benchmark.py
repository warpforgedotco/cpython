"""Benchmark native asyncio Task stepping and wakeups."""

import asyncio

import pyperf


STEPS = 1000


async def task_chain():
    for _ in range(STEPS):
        await asyncio.sleep(0)


def benchmark_task_chain():
    loop.run_until_complete(task_chain())


loop = asyncio.new_event_loop()
runner = pyperf.Runner()
runner.bench_func("asyncio_task_step_chain", benchmark_task_chain)
loop.close()
