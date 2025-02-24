import timeit
from dataclasses import dataclass
from typing import Callable, List

from utils.table import TableView

F_NAME_KEY = "Name"
AVG_TIME_KEY = "Avg Time"
REPEAT_N_KEY = "Repeat N"


@dataclass
class MeasureResult:
    f_name: str
    avg_time: float


class TimeMeasurer:
    def __init__(self, *, repeat_n: int = 10):
        self._repeat_n = repeat_n
        self._results: List[MeasureResult] = []

    def measure(self, f_name: str, f: Callable) -> float:
        exec_time = timeit.timeit(f, number=self._repeat_n)
        avg_exec_time = exec_time / self._repeat_n
        self._results.append(MeasureResult(f_name, avg_exec_time))
        return avg_exec_time

    def as_table(self) -> str:
        data = {
            F_NAME_KEY: list(map(lambda r: r.f_name, self._results)),
            AVG_TIME_KEY: list(map(lambda r: f"{r.avg_time:.3f} s.", self._results)),
            REPEAT_N_KEY: [self._repeat_n] * len(self._results)
        }
        return TableView(data).format()
