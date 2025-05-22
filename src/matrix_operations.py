import numpy as np

def input_matrix(matrix_name):
    """
    Get matrix dimensions and values from user input.
    
    Parameters:
    matrix_name (str): Name of the matrix for display purposes
    
    Returns:
    numpy.ndarray: The input matrix
    """
    print(f"\nEnter dimensions for {matrix_name}:")
    rows = int(input("Number of rows: "))
    cols = int(input("Number of columns: "))
    
    print(f"\nEnter values for {matrix_name} ({rows}x{cols}):")
    matrix = []
    
    for i in range(rows):
        row = []
        for j in range(cols):
            value = float(input(f"Enter element at position ({i+1},{j+1}): "))
            row.append(value)
        matrix.append(row)
    
    return np.array(matrix)

def add_matrices(matrix_a, matrix_b):
    """
    Add two matrices.
    
    Parameters:
    matrix_a (numpy.ndarray): First matrix
    matrix_b (numpy.ndarray): Second matrix
    
    Returns:
    numpy.ndarray: Result of addition or None if dimensions don't match
    """
    if matrix_a.shape != matrix_b.shape:
        print("Error: Matrices must have the same dimensions for addition.")
        return None
    
    return matrix_a + matrix_b

def subtract_matrices(matrix_a, matrix_b):
    """
    Subtract second matrix from first matrix.
    
    Parameters:
    matrix_a (numpy.ndarray): First matrix
    matrix_b (numpy.ndarray): Second matrix
    
    Returns:
    numpy.ndarray: Result of subtraction or None if dimensions don't match
    """
    if matrix_a.shape != matrix_b.shape:
        print("Error: Matrices must have the same dimensions for subtraction.")
        return None
    
    return matrix_a - matrix_b

def multiply_matrices(matrix_a, matrix_b):
    """
    Multiply two matrices.
    
    Parameters:
    matrix_a (numpy.ndarray): First matrix
    matrix_b (numpy.ndarray): Second matrix
    
    Returns:
    numpy.ndarray: Result of multiplication or None if dimensions don't allow multiplication
    """
    if matrix_a.shape[1] != matrix_b.shape[0]:
        print("Error: Number of columns in first matrix must equal number of rows in second matrix.")
        return None
    
    return np.matmul(matrix_a, matrix_b)

def display_matrix(matrix, matrix_name):
    """
    Display a matrix with proper formatting.
    
    Parameters:
    matrix (numpy.ndarray): Matrix to display
    matrix_name (str): Name of the matrix for display purposes
    """
    print(f"\n{matrix_name}:")
    for row in matrix:
        print(" ".join(f"{val:8.2f}" for val in row))

def main():
    print("=== MATRIX OPERATIONS CALCULATOR ===")
    print("This program performs basic matrix operations.")
    
    # Input matrices
    matrix_a = input_matrix("Matrix A")
    matrix_b = input_matrix("Matrix B")
    
    # Display input matrices
    display_matrix(matrix_a, "Matrix A")
    display_matrix(matrix_b, "Matrix B")
    
    # Matrix addition
    result_addition = add_matrices(matrix_a, matrix_b)
    if result_addition is not None:
        display_matrix(result_addition, "Matrix A + Matrix B (Addition)")
    
    # Matrix subtraction
    result_subtraction = subtract_matrices(matrix_a, matrix_b)
    if result_subtraction is not None:
        display_matrix(result_subtraction, "Matrix A - Matrix B (Subtraction)")
    
    # Matrix multiplication
    result_multiplication = multiply_matrices(matrix_a, matrix_b)
    if result_multiplication is not None:
        display_matrix(result_multiplication, "Matrix A × Matrix B (Multiplication)")

if __name__ == "__main__":
    main()