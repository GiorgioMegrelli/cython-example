from example import run_as_cython, run_as_python
from utils import TimeMeasurer


def main():
    measurer = TimeMeasurer(repeat_n=10)
    measurer.measure("cython", run_as_cython)
    measurer.measure("python", run_as_python)
    print(measurer.as_table())


if __name__ == "__main__":
    main()
