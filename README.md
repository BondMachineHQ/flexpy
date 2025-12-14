# Flexpy - FPGA Logic from EXpressions in Python

Flexpy is a Python package for converting symbolic mathematical expressions created with the SymPy library to BondMachine BASM code or HLS (High-Level Synthesis) code. It enables automatic generation of FPGA logic circuits from mathematical expressions.

## Features

- Convert SymPy symbolic expressions to BondMachine BASM code
- Convert SymPy expressions to HLS code
- Support for various data types (float32, float64, custom types via bmnumbers)
- Matrix and tensor operations support
- Complex number support
- Device-specific code generation
- Configurable via JSON configuration files
- Support for both synchronous and asynchronous I/O modes

## Prerequisites

Before using Flexpy, you need to have:

1. **Python 3.x** installed
2. **bmnumbers** executable available in your PATH - This is a BondMachine tool required for type system operations
   - Used to get size, prefix, and supported operations for different numeric types
   - Part of the BondMachine toolchain - visit [BondMachine](https://bondmachine.fisica.unipg.it/) for installation instructions
   - Without this tool, Flexpy will exit with an error message

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/BondMachineHQ/flexpy.git
cd flexpy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Build the standalone executable:
```bash
make package
```

### Dependencies

Flexpy requires the following Python packages:
- `sympy` - Symbolic mathematics library
- `numpy` - Numerical computing library
- `docopt` - Command-line argument parsing
- `jinja2` - Template engine for code generation
- `pyinstaller` - For building standalone executable (optional)

## Quick Start

### Basic Usage

1. Create an expression file (e.g., `simple_expr.txt`):
```python
import sympy as sp
x, y = sp.symbols('x y')
spExpr = x + y
testRanges = None
```

2. Convert to BASM:
```bash
python flexpy.py -e simple_expr.txt -o output.basm --basm
```

3. Convert to HLS:
```bash
python flexpy.py -e simple_expr.txt -o output.hls --hls
```

## Command-Line Options

```
Usage:
  flexpy -e <expression> -o <outputfile> (--basm | --hls) [-d] 
         [--config-file <config>] [-r <registersize>] [-t <type>] [--build-app] 
         [--app-file <appfile>] [--emit-bmapi-maps] 
         [--bmapi-maps-file <bmapi-maps-file>] [--io-mode <iomode>] 
         [--neuron-statistics <neuron-statistics>] [--devices <devices>] 
  flexpy -e <expression> --iomap-only --basm [-d] [--config-file <config>]
  flexpy -h | --help

Options:
  -h --help                                           Show help screen
  -e <expression>                                     Expression file to convert
  -o <outputfile>                                     Output file path
  --basm                                              Convert to BASM format
  --hls                                               Convert to HLS format
  -d                                                  Enable debug mode
  -r <registersize>, --register-size <registersize>   Register size (required for variable-size types)
  -t <type>, --data-type <type>                       Data type (default: float32)
  --config-file <config>                              JSON configuration file
  --build-app                                         Build application wrapper
  --app-file <appfile>                                Application file output path
  --emit-bmapi-maps                                   Emit BondMachine API maps
  --bmapi-maps-file <bmapi-maps-file>                 BMAPI maps output file
  --io-mode <iomode>                                  I/O mode: sync or async (default: sync)
  --iomap-only                                        Generate only I/O mapping
  --neuron-statistics <neuron-statistics>             Save neuron statistics to JSON file
  --devices <devices>                                 Comma-separated list of target devices
```

## Expression File Format

Expression files are Python scripts that define symbolic expressions using SymPy. They must define:

- `spExpr`: The main symbolic expression (can be a scalar, matrix, or tensor)
- `testRanges`: Optional test ranges for validation (can be None)

### Example 1: Simple Expression

```python
import sympy as sp

x, y, z = sp.symbols('x y z')
spExpr = x * y + z
testRanges = None
```

### Example 2: Matrix Expression

```python
import sympy as sp
import numpy as np

x, y = sp.symbols('x y')
# Create a 2x2 matrix
spExpr = sp.Matrix([[x + y, x - y], 
                    [x * y, x / y]])
testRanges = None
```

### Example 3: Complex Expression

```python
import sympy as sp

x = sp.Symbol('x')
# Expression with sine and cosine
spExpr = sp.sin(x) * sp.cos(x)
testRanges = None
```

### Example 4: Using Devices

```python
import sympy as sp

x, y = sp.symbols('x y')
# Define device functions (must be declared in --devices)
device1 = sp.Function('device1')
device2 = sp.Function('device2')

spExpr = device1(x) + device2(y)
testRanges = None
```

Run with:
```bash
python flexpy.py -e expr.txt -o output.basm --basm --devices device1,device2
```

## Configuration Files

Configuration files are JSON files that can specify custom parameters for code generation.

### Example Configuration

```json
{
  "params": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

Usage:
```bash
python flexpy.py -e expr.txt -o output.basm --basm --config-file config.json
```

## Data Types

Flexpy supports various numeric types through the `bmnumbers` tool. Common types include:

- `float32` (default) - 32-bit floating-point
- `float64` - 64-bit floating-point
- Custom types defined in BondMachine

To specify a data type:
```bash
python flexpy.py -e expr.txt -o output.basm --basm -t float64
```

For variable-size types, you must also specify the register size:
```bash
python flexpy.py -e expr.txt -o output.basm --basm -t custom_type -r 64
```

## Advanced Features

### Debug Mode

Enable debug mode to see detailed information about input/output mappings:
```bash
python flexpy.py -e expr.txt -o output.basm --basm -d
```

### I/O Modes

Flexpy supports two I/O modes:
- `sync` (default) - Synchronous I/O
- `async` - Asynchronous I/O

```bash
python flexpy.py -e expr.txt -o output.basm --basm --io-mode async
```

### Getting Only I/O Mapping

To see the input/output mapping without generating code:
```bash
python flexpy.py -e expr.txt --iomap-only --basm
```

### Neuron Statistics

Save statistics about neurons used in the computation:
```bash
python flexpy.py -e expr.txt -o output.basm --basm --neuron-statistics stats.json
```

### Building Applications

Generate a complete application with API wrapper:
```bash
python flexpy.py -e expr.txt -o output.basm --basm --build-app --app-file app.c
```

### BMAPI Maps

Generate BondMachine API mapping files:
```bash
python flexpy.py -e expr.txt -o output.basm --basm --emit-bmapi-maps --bmapi-maps-file maps.json
```

## Output Formats

### BASM Output

BASM (BondMachine Assembly) is the native assembly language for BondMachine. The output includes:
- Register size metadata
- I/O mode configuration
- Processor definitions
- Link definitions for connecting processors
- Input/output mappings

### HLS Output

HLS (High-Level Synthesis) output generates code suitable for hardware synthesis tools.

## Examples

See the `tests/` directory for additional examples:
- `tests/demo_tree_printing.py` - Demonstrates expression tree visualization
- `tests/test_unimplemented_tree.py` - Tests for unimplemented functions
- `qiskit-symb-test/` - Quantum circuit example using Qiskit

## Troubleshooting

### "Error: bmnumbers executable not found"

Make sure the `bmnumbers` tool is installed and available in your system PATH. This is a required BondMachine component.

### "Error: the type is not supported"

The specified data type is not recognized by `bmnumbers`. Check available types with:
```bash
bmnumbers --help
```

### "Unimplemented: [function] is not supported"

The specified SymPy function is not yet implemented in Flexpy's BASM or HLS engine. Check the error output for a detailed expression tree showing where the unsupported function appears.

## Related Projects

- [BondMachine](https://bondmachine.fisica.unipg.it/) - The BondMachine project
- [SymPy](https://www.sympy.org/) - Symbolic mathematics library

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Author

Copyright 2025 - Mirko Mariotti - https://www.mirkomariotti.it