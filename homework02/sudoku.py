import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "")
                for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    return [values[i : i + n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    row, col = pos
    return grid[row]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    row, col = pos
    return [grid[i][col] for i in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    row, col = pos
    size = int(len(grid) ** 0.5)
    start_row = (row // size) * size
    start_col = (col // size) * size
    return [
        grid[i][j]
        for i in range(start_row, start_row + size)
        for j in range(start_col, start_col + size)
    ]


def find_empty_positions(
    grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.Tuple[int, int]]:
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == ".":
                return (row, col)
    return None


def find_possible_values(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.Set[str]:
    return (
        set("123456789")
        - set(get_row(grid, pos))
        - set(get_col(grid, pos))
        - set(get_block(grid, pos))
    )


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    pos = find_empty_positions(grid)
    if pos is None:
        return grid

    row, col = pos
    for value in find_possible_values(grid, pos):
        grid[row][col] = value
        result = solve(grid)
        if result is not None:
            return result
        grid[row][col] = "."
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    if solution is None:
        return False
    if len(solution) != 9:
        return False
    if any(len(row) != 9 for row in solution):
        return False

    required = set("123456789")

    for i in range(9):
        if set(get_row(solution, (i, 0))) != required:
            return False
        if set(get_col(solution, (0, i))) != required:
            return False
        if set(get_block(solution, ((i // 3) * 3, (i % 3) * 3))) != required:
            return False

    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    if N > 81:
        N = 81
    if N < 0:
        N = 0

    grid = [["."] * 9 for _ in range(9)]
    full_grid = solve(grid)
# Моя лабораторная работа 2
    if full_grid is None:
        return grid

    cells_to_remove = 81 - N
    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)

    for i in range(cells_to_remove):
        r, c = positions[i]
        full_grid[r][c] = "."

    return full_grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
