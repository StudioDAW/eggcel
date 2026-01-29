from typing import Dict, List


class _Cell:
    col_str: str
    row_str: str
    column: int
    row: int
    formula: str
    content: str
    def __init__(self, value, col_str:str, row_str:str, column:int, row:int, formula:str):
        self._value = value
        self.cell_id = col_str+row_str
        self.col_str = col_str
        self.row_str = row_str
        self.column = column
        self.row = row
        self.formula = formula

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val


class Text(_Cell):
    def __init__(self, value, col_str: str, row_str: str, column: int, row: int, formula: str):
        super().__init__(value, col_str, row_str, column, row, formula)


    @_Cell.value.setter
    def value(self, val):
        if isinstance(val, int):
            cells.pop(self.cell_id)
            cells[self.cell_id] = Integer(val, self.col_str, self.row_str, self.column, self.row, self.formula)
            del self
        else:
            self._value = str(val)

    def __str__(self) -> str:
        return str(self.value)

    def __float__(self) -> float:
        print(self._value)
        cells.pop(self.cell_id)
        cells[self.cell_id] = Integer(float(self._value), self.col_str, self.row_str, self.column, self.row, self.formula)
        del self
        return 0.0

    def __getattr__(self, attr):
        return getattr(self.value, attr)

    def __type__(self):
        return "Text"

    def __len__(self):
        return len(self.value)

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

    def __mul__(self, other):
        return str(self) * other

    def __rmul__(self, other):
        return other * str(self)


class Integer(_Cell):
    def __init__(self, value, col_str: str, row_str: str, column: int, row: int, formula: str):
        super().__init__(value, col_str, row_str, column, row, formula)

    @_Cell.value.setter
    def value(self, val):
        if isinstance(val, str):
            cells.pop(self.cell_id)
            cells[self.cell_id] = Text(val, self.col_str, self.row_str, self.column, self.row, self.formula)
            del self
        else:
            self._value = int(val)

    def __int__(self) -> int:
        return int(self.value)
        
    def __getattr__(self, attr):
        return getattr(self.value, attr)


class Float(_Cell):
    def __init__(self, value, col_str: str, row_str: str, column: int, row: int, formula: str):
        super().__init__(value, col_str, row_str, column, row, formula)

    def __float__(self) -> float:
        return float(self.value)
        
    def __getattr__(self, attr):
        return getattr(self.value, attr)


CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

cells: Dict[str, Text|Integer] = {}
columns: List[List[str]] = []
rows: List[List[str]] = []

ROWS = 30
COLS = 60

for _ in range(ROWS):
    rows.append([])

for c in range(COLS):
    column = []
    for r in range(ROWS):
        i = c//len(CHARS)
        if i == 0:
            col_str = f"{CHARS[c]}"
        else:
            col_str = f"{CHARS[i-1]}{CHARS[c-i*len(CHARS)]}"
        cell_id = col_str + str(r+1)
        cells[cell_id] = Text("", col_str, str(r+1), c, r, "")
        column.append(cell_id)
        rows[r].append(cell_id)
    columns.append(column)
