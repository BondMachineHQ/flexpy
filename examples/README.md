# Flexpy Examples

This directory contains example expression files demonstrating various features of Flexpy.

## Example Files

### simple_addition.txt
Basic addition of two variables. Good starting point for learning Flexpy.

**Usage (from repository root):**
```bash
python flexpy.py -e examples/simple_addition.txt -o simple_addition.basm --basm
```

**Usage (from examples directory):**
```bash
python ../flexpy.py -e simple_addition.txt -o simple_addition.basm --basm
```

### polynomial.txt
Polynomial expression demonstrating power and multiplication operations.

**Usage (from repository root):**
```bash
python flexpy.py -e examples/polynomial.txt -o polynomial.basm --basm
```

**Usage (from examples directory):**
```bash
python ../flexpy.py -e polynomial.txt -o polynomial.basm --basm
```

### trigonometric.txt
Trigonometric functions (sine and cosine).

**Usage (from repository root):**
```bash
python flexpy.py -e examples/trigonometric.txt -o trigonometric.basm --basm
```

**Usage (from examples directory):**
```bash
python ../flexpy.py -e trigonometric.txt -o trigonometric.basm --basm
```

### matrix_operations.txt
Matrix operations example showing how to work with matrices in Flexpy.

**Usage (from repository root):**
```bash
python flexpy.py -e examples/matrix_operations.txt -o matrix_operations.basm --basm
```

**Usage (from examples directory):**
```bash
python ../flexpy.py -e matrix_operations.txt -o matrix_operations.basm --basm
```

### complex_expression.txt
Complex expression combining multiple operations including square root.

**Usage (from repository root):**
```bash
python flexpy.py -e examples/complex_expression.txt -o complex_expression.basm --basm
```

**Usage (from examples directory):**
```bash
python ../flexpy.py -e complex_expression.txt -o complex_expression.basm --basm
```

## Configuration File

### example_config.json
Example JSON configuration file showing how to pass custom parameters.

**Usage (from repository root):**
```bash
python flexpy.py -e examples/simple_addition.txt -o output.basm --basm --config-file examples/example_config.json
```

**Usage (from examples directory):**
```bash
python ../flexpy.py -e simple_addition.txt -o output.basm --basm --config-file example_config.json
```

## Running Examples

**Note:** Commands can be run from either the repository root or the examples directory.

### From the repository root:

```bash
# Generate BASM output
python flexpy.py -e examples/simple_addition.txt -o output.basm --basm

# Generate HLS output
python flexpy.py -e examples/simple_addition.txt -o output.hls --hls

# With debug mode
python flexpy.py -e examples/simple_addition.txt -o output.basm --basm -d

# With custom data type
python flexpy.py -e examples/simple_addition.txt -o output.basm --basm -t float64

# Get only I/O mapping
python flexpy.py -e examples/simple_addition.txt --iomap-only --basm
```

### From the examples directory:

```bash
# Generate BASM output
python ../flexpy.py -e simple_addition.txt -o output.basm --basm

# Generate HLS output
python ../flexpy.py -e simple_addition.txt -o output.hls --hls

# With debug mode
python ../flexpy.py -e simple_addition.txt -o output.basm --basm -d

# With custom data type
python ../flexpy.py -e simple_addition.txt -o output.basm --basm -t float64

# Get only I/O mapping
python ../flexpy.py -e simple_addition.txt --iomap-only --basm
```

## Creating Your Own Examples

To create a new expression file:

1. Create a `.txt` file with Python code
2. Import sympy (and optionally numpy if needed for arrays)
3. Define symbolic variables using `sp.symbols()`
4. Set `spExpr` to your expression
5. Set `testRanges = None` (or define custom test ranges)

Example template:
```python
import sympy as sp

# Define your variables
x, y = sp.symbols('x y')

# Define your expression
spExpr = x + y  # Replace with your expression

# Test ranges (optional)
testRanges = None
```

Example with numpy (for tensors):
```python
import sympy as sp
import numpy as np

# Define variables
x, y = sp.symbols('x y')

# Create a tensor expression
arr = np.array([[x, y], [y, x]])
spExpr = sp.Array(arr)

testRanges = None
```
