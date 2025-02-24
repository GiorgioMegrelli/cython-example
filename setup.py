import io
import os
import shutil
from contextlib import redirect_stdout
from dataclasses import dataclass
from os import path
from typing import Callable, Dict, List, Optional

from Cython.Build import cythonize
from setuptools import Extension, setup

INSTALL_DIR = "build"
CYTHON_MODULE_NAME = "example_cython"
NEW_MODULE_NAME = "example"


@dataclass(kw_only=True)
class GeneratedFiles:
    c_file: str
    object_file_full_path: str
    library_file_full_path: str
    library_file: str


def catch_output(func: Callable, *args, **kwargs) -> str:
    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        func(*args, **kwargs)
    return output_buffer.getvalue()


def write_lines_to_file(file_path: str, *lines: str):
    write_to_file(file_path, "".join([f"{l}\n" for l in lines]))


def write_to_file(file_path: str, data: str):
    with open(file_path, "w", encoding="utf-8") as writer:
        writer.write(data)


def extract_key_flags(lines: List[str]) -> Dict[str, str]:
    def is_flag(line: str) -> bool:
        return line.startswith("-")

    result = {}
    i = 0
    while i < len(lines):
        while i < len(lines) and not is_flag(lines[i]):
            i += 1
        if i + 1 < len(lines) and not is_flag(lines[i + 1]):
            key = lines[i]
            result[key] = lines[i + 1]
            i += 1
        i += 1
    return result


def extract_file_paths(lines: List[str]) -> GeneratedFiles:
    def raise_none_variable(var_name: str) -> Exception:
        return ValueError(f"'{var_name}' is None")

    is_first_line_handled = False
    c_file = None
    object_file_full_path = None
    library_file_full_path = None
    for line in lines:
        flags = extract_key_flags(line.split())
        if len(flags) > 0:
            if is_first_line_handled:
                library_file_full_path = flags.get("-o", None)
                break
            else:
                c_file = flags.get("-c", None)
                object_file_full_path = flags.get("-o", None)
                is_first_line_handled = True

    if c_file is None:
        raise raise_none_variable("c_file")
    if object_file_full_path is None:
        raise raise_none_variable("object_file_full_path")
    if library_file_full_path is None:
        raise raise_none_variable("library_file_full_path")

    library_file = library_file_full_path.split(os.sep)[-1]
    return GeneratedFiles(
        c_file=c_file,
        object_file_full_path=object_file_full_path,
        library_file_full_path=library_file_full_path,
        library_file=library_file,
    )


def delete_empty_directories(main_root: str):
    for root, dirs, _ in os.walk(main_root, topdown=False):
        for sub_dir in dirs:
            sub_dir = path.join(root, sub_dir)
            if path.exists(sub_dir) and not any(os.scandir(sub_dir)):
                shutil.rmtree(root)


def delete_all(file_paths: GeneratedFiles):
    os.remove(file_paths.c_file)
    os.remove(file_paths.object_file_full_path)
    os.remove(file_paths.library_file_full_path)
    delete_empty_directories(INSTALL_DIR)


def make_module(cython_module_name: str, file_paths: GeneratedFiles):
    def create_init_line(pkg_name) -> str:
        return f"from .{pkg_name} import run as run_as_{pkg_name}"

    os.makedirs(NEW_MODULE_NAME, exist_ok=True)
    write_lines_to_file(
        path.join(NEW_MODULE_NAME, "__init__.py"),
        create_init_line("cython"),
        create_init_line("python"),
    )
    write_lines_to_file(path.join(NEW_MODULE_NAME, ".gitignore"), "*")
    write_lines_to_file(
        path.join(NEW_MODULE_NAME, "cython.py"),
        "import ctypes",
        "import os",
        f"ctypes.CDLL(os.path.abspath('.{os.sep}{NEW_MODULE_NAME}{os.sep}{file_paths.library_file}'))",
        "",
        f"from {cython_module_name} import run",
    )
    shutil.copy("example.py", path.join(NEW_MODULE_NAME, "python.py"))
    shutil.copy(
        file_paths.library_file, path.join(NEW_MODULE_NAME, file_paths.library_file)
    )


def post_setup(cython_module_name: str, output: str):
    lines = [s.strip() for s in output.split("\n")]
    file_paths = extract_file_paths(lines)
    make_module(cython_module_name, file_paths)
    delete_all(file_paths)


def main(
    *,
    name: str,
    version: str,
    sources: List[str],
    module_name: Optional[str] = None,
):
    if module_name is None:
        module_name = name

    ext_modules = [
        Extension(
            name=name,
            sources=sources,
        )
    ]
    output = catch_output(
        setup,
        name=name,
        version=version,
        ext_modules=cythonize(ext_modules),
    )
    post_setup(name, output)


if __name__ == "__main__":
    main(
        name=CYTHON_MODULE_NAME,
        version="1.0",
        sources=["example.py"],
    )
