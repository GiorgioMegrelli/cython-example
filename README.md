# cython-example
An example of Cython

## Environment

Build an image:

```shell
docker build -t cython-dev .
```

Run the image:

```shell
docker run -it --rm -v "$(pwd):/app" cython-dev
```

Compile the module:

```shell
python3 setup.py build_ext --inplace
```

## Scripts

Ensure that no previous build exists:

```shell
./clear.sh
```

Build `C` libraries and generated python files:

```shell
./compile.sh
```

## Results

Run to check results:

```shell
python3 test.py
```

An output:
```text
--------------------------------
|   Name | Avg Time | Repeat N |
================================
| cython | 2.078 s. |       10 |
--------------------------------
| python | 3.946 s. |       10 |
--------------------------------
```
