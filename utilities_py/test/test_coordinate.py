from utilities_py import Coordinate, generate_neighbours, Grid

import pytest


def test_coordinate_addition():
    """Verify Coordinates can be added to each other."""

    # 1. Prepare
    c1 = Coordinate(2, 3)
    c2 = Coordinate(4, 5)

    # 2. Execute
    result_add = c1 + c2
    result_iadd = c1
    result_iadd += c2

    # 3. Verify
    assert result_add == Coordinate(6, 8)
    assert result_iadd == Coordinate(6, 8)


def test_coordinate_subtraction():
    """Verify Coordinates can be subtracted from each other."""

    # 1. Prepare
    c1 = Coordinate(5, 7)
    c2 = Coordinate(2, 3)

    # 2. Execute
    result_sub = c1 - c2
    result_isub = c1
    result_isub -= c2

    # 3. Verify
    assert result_sub == Coordinate(3, 4)
    assert result_isub == Coordinate(3, 4)


def test_coordinate_multiplication():
    """Verify Coordinates can be scaled by multiplication with scalars."""

    # 1. Prepare
    c1 = Coordinate(3, 4)
    c2 = Coordinate(2, 3)

    # 2. Execute
    result_mul = c1 * 2
    result_imul = c1
    result_imul *= 2
    result_rmul = 2 * c2

    # 3. Verify
    assert result_mul == Coordinate(6, 8)
    assert result_imul == Coordinate(6, 8)
    assert result_rmul == Coordinate(4, 6)


def test_coordinate_equality():
    """Verify Coordinates can be compared for equality."""

    # 1. Prepare
    c1 = Coordinate(3, 4)
    c2 = Coordinate(3, 4)
    c3 = Coordinate(5, 6)

    # 2. Execute & Verify
    assert c1 == c2
    assert c1 != c3
    assert c1 == (3, 4)
    assert c1 != (5, 6)

    with pytest.raises(NotImplementedError):
        _ = c1 == (3, 4, 1)  # type: ignore

    with pytest.raises(NotImplementedError):
        _ = c1 == 5  # type: ignore


def test_coordinate_less_then():
    """Verify Coordinates can be compared with the < operator."""

    # 1. Prepare
    c1 = Coordinate(3, 4)
    c2 = Coordinate(3, 4)
    c3 = Coordinate(5, 6)

    # 2. Execute & Verify
    assert c1 < c3
    assert not c1 < c2


def test_coordinate_repr():
    """Verify the string representation of the Coordinate class."""

    # 1. Prepare
    c = Coordinate(3, 4)

    # 2. Execute
    c_repr = repr(c)

    # 3. Verify
    assert c_repr == "<Coordinate x: 3, y: 4>"


def test_generate_neighbours_for_coordinate():
    """Verify generate_neighbours generates neighbours for a Coordinate, useful for grids."""

    # 1. Prepare
    c = Coordinate(0, 0)

    # 2. Execute
    result_reduced = list(generate_neighbours(c, include_diagonals=False))
    result_all = list(generate_neighbours(c, include_diagonals=True))

    # 3. Verify
    expected_reduced_neighbours = {
        Coordinate(0, 1),
        Coordinate(0, -1),
        Coordinate(1, 0),
        Coordinate(-1, 0),
    }
    assert len(result_reduced) == len(set(expected_reduced_neighbours))
    assert set(result_reduced) == set(expected_reduced_neighbours)

    expected_all_neighbours = {
        Coordinate(0, 1),
        Coordinate(0, -1),
        Coordinate(1, 0),
        Coordinate(-1, 0),
        Coordinate(1, 1),
        Coordinate(1, -1),
        Coordinate(-1, 1),
        Coordinate(-1, -1),
    }
    assert len(result_all) == len(set(expected_all_neighbours))
    assert set(result_all) == set(expected_all_neighbours)


def test_grid_data_access():
    """Verify that grid access and setting values via Coordinates works as expected."""

    # 1. Prepare
    data = """##########
#.#......#
#...A....#
#.#.######"""
    grid = Grid(data.splitlines())

    # 2. Execute & Verify initial access
    assert grid[Coordinate(4, 2)] == "A"
    assert grid[Coordinate(0, 0)] == "#"
    assert grid[Coordinate(1, 1)] == "."

    grid[Coordinate(4, 2)] = "B"
    assert grid[Coordinate(4, 2)] == "B"


def test_grid_row_access():
    """Verify that the neighbours method of Grid correctly handles edge Coordinates."""

    # 1. Prepare
    grid = Grid([[0, 1, 2], [3, 4, 5], [6, 7, 8]])

    # 2. Execute
    row_0 = grid.row(0)
    row_1 = grid.row(1)
    row_2 = grid.row(2)

    # 3. Verify
    assert row_0 == [0, 1, 2]
    assert row_1 == [3, 4, 5]
    assert row_2 == [6, 7, 8]


def test_grid_str_and_repr():
    """Verify the string and repr representations of the Grid class."""

    # 1. Prepare
    data = """##########
#.#......#
#...S....#
#.#.######"""
    grid = Grid(data.splitlines())

    # 2. Execute
    grid_str = str(grid)
    grid_repr = repr(grid)

    # 3. Verify
    assert grid_str == "##########\n#.#......#\n#...S....#\n#.#.######"
    assert grid_repr == "<Grid rows: 4, columns: 10>"


def test_grid_size():
    """Verify that the size property of Grid returns the correct dimensions."""

    # 1. Prepare
    data = """##########
#...A....#
#.#.######"""
    grid = Grid(data.splitlines())

    # 2. Execute & Verify
    assert grid.size() == (3, 10)


def test_grid_find():
    """Verify that a value can be found in a grid, returning its Coordinate."""

    # 1. Prepare
    data = """##########
#.#......#
#...S....#
#.#.######"""
    grid = Grid(data.splitlines())

    # 2. Execute & Verify
    assert grid.find("S") == Coordinate(4, 2)
    assert grid[grid.find("S")] == "S"


def test_grid_neighbours():
    """Verify that the neighbours method of Grid returns valid neighbouring Coordinates."""

    # 1. Prepare
    grid = Grid([[0, 1, 2], [3, 4, 5], [6, 7, 8]])

    # 2. Execute
    result_all = list(grid.neighbours(Coordinate(1, 1), include_diagonals=True))
    result_reduced = list(grid.neighbours(Coordinate(1, 1), include_diagonals=False))

    # 3. Verify
    expected_reduced_neighbours = {
        Coordinate(0, 1),
        Coordinate(2, 1),
        Coordinate(1, 0),
        Coordinate(1, 2),
    }
    assert len(result_reduced) == len(set(expected_reduced_neighbours))
    assert set(result_reduced) == set(expected_reduced_neighbours)

    expected_all_neighbours = {
        Coordinate(0, 1),
        Coordinate(2, 1),
        Coordinate(1, 0),
        Coordinate(1, 2),
        Coordinate(0, 0),
        Coordinate(0, 2),
        Coordinate(2, 0),
        Coordinate(2, 2),
    }
    assert len(result_all) == len(set(expected_all_neighbours))
    assert set(result_all) == set(expected_all_neighbours)


def test_grid_neighbours_at_edge():
    """Verify that the neighbours method of Grid correctly handles edge Coordinates."""

    # 1. Prepare
    grid = Grid([[0, 1, 2], [3, 4, 5], [6, 7, 8]])

    # 2. Execute
    result_all = list(grid.neighbours(Coordinate(0, 0), include_diagonals=True))
    result_reduced = list(grid.neighbours(Coordinate(0, 0), include_diagonals=False))

    # 3. Verify
    expected_reduced_neighbours = {
        Coordinate(1, 0),
        Coordinate(0, 1),
    }
    assert len(result_reduced) == len(set(expected_reduced_neighbours))
    assert set(result_reduced) == set(expected_reduced_neighbours)

    expected_all_neighbours = {
        Coordinate(1, 0),
        Coordinate(0, 1),
        Coordinate(1, 1),
    }
    assert len(result_all) == len(set(expected_all_neighbours))
    assert set(result_all) == set(expected_all_neighbours)
