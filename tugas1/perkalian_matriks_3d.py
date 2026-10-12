"""Perkalian matriks batch untuk dua array tiga dimensi."""

from typing import Sequence


def multiply_3d(
    left: Sequence[Sequence[Sequence[float]]],
    right: Sequence[Sequence[Sequence[float]]],
) -> list[list[list[float]]]:
    """Kalikan matriks pada setiap pasangan lapisan dari dua array 3D."""
    if not left or not right:
        raise ValueError("Array tidak boleh kosong.")
    if len(left) != len(right):
        raise ValueError("Jumlah lapisan kedua array harus sama.")

    result: list[list[list[float]]] = []
    for batch_index, (left_matrix, right_matrix) in enumerate(zip(left, right), start=1):
        if not left_matrix or not right_matrix:
            raise ValueError(f"Matriks pada lapisan {batch_index} tidak boleh kosong.")

        left_columns = len(left_matrix[0])
        right_columns = len(right_matrix[0])
        if left_columns == 0 or right_columns == 0:
            raise ValueError(f"Matriks pada lapisan {batch_index} tidak boleh kosong.")
        if any(len(row) != left_columns for row in left_matrix):
            raise ValueError(f"Baris array pertama pada lapisan {batch_index} tidak seragam.")
        if any(len(row) != right_columns for row in right_matrix):
            raise ValueError(f"Baris array kedua pada lapisan {batch_index} tidak seragam.")
        if left_columns != len(right_matrix):
            raise ValueError(
                f"Dimensi dalam lapisan {batch_index} tidak cocok: "
                f"{left_columns} kolom pada array pertama, "
                f"tetapi {len(right_matrix)} baris pada array kedua."
            )

        product = [
            [
                sum(left_row[k] * right_matrix[k][column] for k in range(left_columns))
                for column in range(right_columns)
            ]
            for left_row in left_matrix
        ]
        result.append(product)

    return result


def read_array(name: str) -> list[list[list[float]]]:
    """Baca dimensi dan nilai elemen satu array 3D dari terminal."""
    dimensions = input(
        f"Dimensi array {name} (jumlah_lapisan baris kolom): "
    ).split()
    if len(dimensions) != 3:
        raise ValueError("Masukkan tepat tiga dimensi, dipisahkan dengan spasi.")

    try:
        batch_size, row_count, column_count = map(int, dimensions)
    except ValueError as error:
        raise ValueError("Dimensi harus berupa bilangan bulat.") from error
    if min(batch_size, row_count, column_count) <= 0:
        raise ValueError("Semua dimensi harus lebih besar dari nol.")

    array: list[list[list[float]]] = []
    for batch_index in range(batch_size):
        matrix: list[list[float]] = []
        print(f"Masukkan elemen lapisan {batch_index + 1} array {name}:")
        for row_index in range(row_count):
            values = input(
                f"  Baris {row_index + 1} ({column_count} angka, pisahkan dengan spasi): "
            ).split()
            if len(values) != column_count:
                raise ValueError(
                    f"Baris harus berisi tepat {column_count} angka."
                )
            try:
                matrix.append([float(value) for value in values])
            except ValueError as error:
                raise ValueError("Elemen matriks harus berupa angka.") from error
        array.append(matrix)

    return array


def main() -> int:
    print("Perkalian Matriks untuk Array 3D")
    print("Setiap lapisan dari array A dikalikan dengan lapisan yang bersesuaian di B.\n")

    try:
        array_a = read_array("A")
        array_b = read_array("B")
        product = multiply_3d(array_a, array_b)
    except (ValueError, EOFError) as error:
        print(f"Input tidak valid: {error}")
        return 1

    print("\nHasil perkalian:")
    for batch_index, matrix in enumerate(product, start=1):
        print(f"Lapisan {batch_index}:")
        for row in matrix:
            print("  " + " ".join(f"{value:g}" for value in row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
