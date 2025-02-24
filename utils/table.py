from functools import reduce
from typing import Any, Dict, List


class TableView:
    def __init__(self, data: Dict[str, List[Any]]):
        self._data = TableView._check_table(data)
        self._col_letter = "|"
        self._row_letter = "-"
        self._head_row_letter = "="

    @staticmethod
    def _check_table(data: Dict[str, List[Any]]) -> Dict[str, List[str]]:
        if any(map(lambda x: x == "", data.keys())):
            raise ValueError("A Column is empty")
        col_heights = [(k, len(v)) for k, v in data.items()]
        first_col = col_heights[0][1]
        for col_name, col_h in col_heights[1:]:
            if col_h != first_col:
                raise ValueError(
                    f"Invalid height for '{col_name}': correct={first_col}, actual={col_h}"
                )
        return {k: list(map(str, v)) for k, v in data.items()}

    def format(self) -> str:
        columns = list(self._data.keys())
        max_widths = {
            k: reduce(max, map(len, v), len(k)) for k, v in self._data.items()
        }
        line_len = (
            sum(max_widths.values())
            + (len(columns) + 1) * len(self._col_letter)
            + len(columns) * 2
        )
        simple_line = self._row_letter * line_len

        str_builder = [
            simple_line,
            self._build_header(columns, max_widths),
            self._head_row_letter * line_len,
        ]
        for entry in zip(*[self._data[col] for col in columns]):
            entry_with_keys = {k: v for k, v in zip(columns, entry)}
            str_builder.append(self._build_row(columns, max_widths, entry_with_keys))
            str_builder.append(simple_line)

        return "\n".join(str_builder)

    def _build_header(self, cols: List[str], max_widths: Dict[str, int]) -> str:
        return self._build_row(cols, max_widths, {col: col for col in cols})

    def _build_row(
        self, cols: List[str], max_widths: Dict[str, int], values_dict: Dict[str, str]
    ) -> str:
        values = [str(values_dict[col]).rjust(max_widths[col], " ") for col in cols]
        row = self._col_letter.join([f" {val} " for val in values])
        return self._col_letter + row + self._col_letter
