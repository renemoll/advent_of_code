import typing
import pytest

from utilities_py import Matrix, SparseMatrix


def test_matrix_row_access():
    """Verify each row can be accessed directly."""

    # 1. Prepare
    matrix = Matrix(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
    )

    # 2. Execute & Verify
    assert matrix.row(0) == [1, 2, 3]
    assert matrix.row(1) == [4, 5, 6]
    assert matrix.row(2) == [7, 8, 9]


def test_matrix_column_access():
    """Verify each column can be accessed directly."""

    # 1. Prepare
    matrix = Matrix(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
    )

    # 2. Execute & Verify
    assert matrix.column(0) == [1, 4, 7]
    assert matrix.column(1) == [2, 5, 8]
    assert matrix.column(2) == [3, 6, 9]


def test_matrix_str_and_repr():
    """Verify the string representation of the Matrix class."""

    # 1. Prepare
    matrix = Matrix(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
    )

    # 2. Execute
    matrix_str = str(matrix)
    matrix_repr = repr(matrix)

    # 3. Verify
    assert matrix_str == "1 2 3\n4 5 6\n7 8 9"
    assert matrix_repr == "<Matrix rows: 3, columns: 3>"


def test_matrix_equality():
    """Verify a Matrix object can be compared for equality, on size and content."""

    # 1. Prepare
    matrix_a_3x3 = Matrix(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
    )

    matrix_a_1x9 = Matrix(
        [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
        ]
    )

    matrix_a_2x3 = Matrix(
        [
            [1, 2, 3],
            [4, 5, 6],
        ]
    )

    matrix_b_3x3 = Matrix(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
    )

    # 2. Execute and verify
    assert matrix_a_3x3 == matrix_b_3x3
    assert matrix_a_3x3 != matrix_a_1x9
    assert matrix_a_3x3 != matrix_a_2x3

    with pytest.raises(AttributeError):
        matrix_a_2x3 == 1

    with pytest.raises(AttributeError):
        matrix_a_1x9 == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_matrix_elimination():
    """Verify Gaussian elimination on a simple matrix."""

    # 1. Prepare
    matrix = Matrix(
        [
            [2, 4, 6],
            [1, 3, 5],
            [0, 2, 4],
        ]
    )

    augmented_matrix = Matrix(
        [
            [2, 1, -1, 8],
            [-3, -1, 2, -11],
            [-2, 1, 2, -3],
        ],
        augmented_matrix_columns=1,
    )

    matrix_free_variables = Matrix(
        [
            [0, 3, -6, 6, 4, -5],
            [3, -7, 8, -5, 8, 9],
            [3, -9, 12, -9, 6, 15],
        ],
        augmented_matrix_columns=1,
    )

    # 2. Execute
    result1 = matrix.gaussian_elimination()
    result2 = augmented_matrix.gaussian_elimination()
    result3 = matrix_free_variables.gaussian_elimination()
    matrix_free_variables.transform(int)

    # 3. Verify
    assert matrix == Matrix(
        [
            [1.0, 0.0, -1.0],
            [0.0, 1.0, 2.0],
            [0.0, 0.0, 0.0],
        ]
    )
    assert result1 is Matrix.Solution.NO_SOLUTION
    assert matrix.pivot_variables() == [0, 1]
    assert matrix.free_variables() == [2]

    assert augmented_matrix == Matrix(
        [
            [1.0, 0.0, 0.0, 2.0],
            [0.0, 1.0, 0.0, 3.0],
            [0.0, 0.0, 1.0, -1.0],
        ]
    )
    assert result2 is Matrix.Solution.UNIQUE_SOLUTION
    assert augmented_matrix.pivot_variables() == [0, 1, 2]
    assert augmented_matrix.free_variables() == []

    assert matrix_free_variables == Matrix(
        [
            [1, 0, -2, 3, 0, -24],
            [0, 1, -2, 2, 0, -7],
            [0, 0, 0, 0, 1, 4],
        ]
    )
    assert result3 is Matrix.Solution.INFINITE_SOLUTIONS
    assert matrix_free_variables.pivot_variables() == [0, 1, 4]
    assert matrix_free_variables.free_variables() == [2, 3]


def test_matrix_transform():
    """Verify a function can be applied to all elements in a Matrix."""

    # 1. Prepare
    matrix = Matrix(
        [
            [2, 4, 6],
            [1, 3, 5],
            [0, 2, 4],
        ]
    )

    # 2. Execute
    matrix.transform(lambda x: chr(48 + x))

    # 3. Verify
    assert matrix == Matrix(
        [
            ["2", "4", "6"],
            ["1", "3", "5"],
            ["0", "2", "4"],
        ]
    )


def test_sparsematrix_data_access():
    """Verify that data access in SparseMatrix works as expected."""

    # 1. Prepare
    sparse_matrix = SparseMatrix(
        """##########
#.#......#
#...S....#
#.#.######""".splitlines(),
        predicate=lambda x: x in ("#", "S"),
    )

    # 2. Execute & verify
    for key in sparse_matrix:
        value = sparse_matrix[key]
        assert value in ("#", "S")

        if value == "S":
            sparse_matrix[key] = "E"
            assert sparse_matrix[key] == "E"


def test_sparsematrix_find():
    """Verify that a value can be found in a SparseMatrix, returning its index."""

    # 1. Prepare
    sparse_matrix = SparseMatrix(
        """##########
#.#......#
#...S....#
#.#.######""".splitlines(),
        predicate=lambda x: x in ("#", "S"),
    )

    # 2. Execute
    index = sparse_matrix.find("S")

    # 3. Verify
    x = index % sparse_matrix._stride
    y = index // sparse_matrix._stride
    assert (x, y) == (4, 2)
    assert sparse_matrix[index] == "S"

    with pytest.raises(KeyError):
        sparse_matrix.find(".")


def test_sparsematrix_neighbours():
    """Verify that the neighbours method of SparseMatrix returns valid neighbouring Coordinates."""

    # 1. Prepare
    sparse_matrix = SparseMatrix(
        """##########
#.#......#
#..S#....#
#.#.######""".splitlines(),
        predicate=lambda x: x in ("#", "S"),
    )

    def key_to_coordinate(index: int) -> typing.Tuple[int, int]:
        x = index % sparse_matrix._stride
        y = index // sparse_matrix._stride
        return (x, y)

    # 2. Execute
    centre = sparse_matrix.find("S")
    result_all = list(sparse_matrix.neighbours(centre, include_diagonals=True))
    result_reduced = list(sparse_matrix.neighbours(centre, include_diagonals=False))

    # 3. Verify
    expected_reduced_neighbours = {
        (4, 2),
    }
    assert len(result_reduced) == len(set(expected_reduced_neighbours))
    assert set([key_to_coordinate(x) for x in result_reduced]) == set(
        expected_reduced_neighbours
    )

    expected_all_neighbours = {
        (2, 1),
        (4, 2),
        (2, 3),
        (4, 3),
    }
    assert len(result_all) == len(set(expected_all_neighbours))
    assert set([key_to_coordinate(x) for x in result_all]) == set(
        expected_all_neighbours
    )
