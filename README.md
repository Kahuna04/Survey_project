# Survey and Matrix Operations Project Report

## 1. Introduction

This report documents the design and implementation of two computer programs:

1. A survey boundary calculator that computes coordinates of boundary pillars and calculates land area
2. A matrix operations calculator for addition, subtraction, and multiplication of matrices

Both programs are implemented in Python, utilizing its robust mathematical and numerical capabilities.

## 2. Survey Boundary Calculator

### 2.1 Design Overview

The survey boundary calculator is designed to:
1. Calculate the coordinates (easting and northing) of all boundary pillars given an origin point and boundary line measurements
2. Compute the area of the land parcel using the cross coordinate method

### 2.2 Algorithm Design

#### 2.2.1 Boundary Coordinate Calculation

The algorithm for calculating boundary coordinates follows these steps:
1. Start with the origin coordinates (initial easting and northing)
2. For each boundary line:
   - Convert bearing from degrees to radians
   - Calculate change in easting: distance × sin(bearing)
   - Calculate change in northing: distance × cos(bearing)
   - Add these changes to current coordinates to get the next pillar coordinates
3. Store all pillar coordinates in a list

#### 2.2.2 Area Calculation (Cross Coordinate Method)

The cross coordinate method (also known as the surveyor's formula) calculates the area as follows:
1. Extract all easting and northing values into separate lists
2. Ensure the polygon is closed (first and last coordinates match)
3. Apply the cross coordinate formula:
   - Area = 0.5 × |Σ(E₁×N₂ + E₂×N₃ + ... + Eₙ×N₁) - Σ(N₁×E₂ + N₂×E₃ + ... + Nₙ×E₁)|
4. Convert the area from square meters to acres (1 square meter = 0.000247105 acres)

### 2.3 Implementation

The implementation consists of three main functions:
- `calculate_boundary_coordinates()`: Computes coordinates of boundary pillars
- `calculate_area()`: Calculates the area using the cross coordinate method
- `main()`: Manages user input and program flow

### 2.4 Usage Example

The program prompts users to enter:
1. Origin coordinates (easting and northing)
2. Number of boundary lines
3. Distance and bearing for each boundary line

The program then displays:
1. Calculated coordinates of all boundary pillars
2. Area of the land parcel in square meters and acres

## 3. Matrix Operations Calculator

### 3.1 Design Overview

The matrix operations calculator performs three fundamental matrix operations:
1. Addition of two matrices
2. Subtraction of two matrices
3. Multiplication of two matrices

### 3.2 Algorithm Design

#### 3.2.1 Matrix Addition

For two matrices A and B of the same dimensions:
- Check if dimensions match; if not, return an error
- Add corresponding elements: C[i,j] = A[i,j] + B[i,j]

#### 3.2.2 Matrix Subtraction

For two matrices A and B of the same dimensions:
- Check if dimensions match; if not, return an error
- Subtract corresponding elements: C[i,j] = A[i,j] - B[i,j]

#### 3.2.3 Matrix Multiplication

For matrices A (m×n) and B (n×p):
- Check if inner dimensions match (columns of A = rows of B); if not, return an error
- Calculate each element of the result matrix C (m×p) as:
  C[i,j] = Σ(A[i,k] × B[k,j]) for k = 0 to n-1

### 3.3 Implementation

The implementation uses NumPy for efficient matrix operations and consists of five main functions:
- `input_matrix()`: Collects matrix dimensions and values from user
- `add_matrices()`: Performs matrix addition
- `subtract_matrices()`: Performs matrix subtraction
- `multiply_matrices()`: Performs matrix multiplication
- `display_matrix()`: Formats and displays matrices
- `main()`: Manages user input and program flow

### 3.4 Usage Example

The program prompts users to enter:
1. Dimensions and values for Matrix A
2. Dimensions and values for Matrix B

The program then displays:
1. The input matrices
2. Result of Matrix A + Matrix B (addition)
3. Result of Matrix A - Matrix B (subtraction)
4. Result of Matrix A × Matrix B (multiplication)

## 4. Technical Implementation Notes

### 4.1 Programming Language

Python was chosen for this project because:
- It has powerful numerical libraries (NumPy) for efficient matrix operations
- It provides built-in mathematical functions needed for coordinate calculations
- It's easy to read and maintain, making the code accessible

### 4.2 Dependencies

- NumPy: Used for matrix operations and efficient numerical calculations
- Math: Used for trigonometric functions in coordinate calculations

## 5. Conclusion

The developed software successfully meets the requirements specified in the project brief. The survey boundary calculator accurately computes coordinates of boundary pillars and calculates land area in both square meters and acres. The matrix operations calculator effectively performs addition, subtraction, and multiplication of matrices.

Both programs feature user-friendly interfaces with clear prompts and well-formatted output. The code is structured in a modular way, making it easy to understand, maintain, and extend if needed.

## 6. Future Improvements

Potential enhancements for future versions could include:
- Graphical visualization of the boundary coordinates
- Support for importing/exporting data from/to common file formats
- More advanced matrix operations (inverse, determinant, eigenvalues)
- A graphical user interface (GUI) for easier interaction

## 7. Appendix: Software Code

The complete source code for both programs is provided in separate files:
1. `survey_boundary_calculator.py`
2. `matrix_operations.py`