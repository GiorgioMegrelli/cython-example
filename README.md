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
