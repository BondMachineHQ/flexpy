# Unimplemented Function Tree Printing

## Overview

When flexpy encounters an unimplemented function during sympy expression conversion, it now displays a detailed tree representation of the expression instead of just showing a generic error message.

## What Changed

Previously, when an unimplemented function was encountered, flexpy would print:
```
Unimplemented
```

Now, flexpy provides:
1. A descriptive error message indicating which function is not supported
2. A visual tree representation of the sympy expression

## Examples

### Example 1: Simple unimplemented function

Input expression: `tan(x)`

Output:
```
Unimplemented: tan is not supported

Expression tree:
tan: tan(x)
+-Symbol: x
  commutative: True
```

### Example 2: Complex expression with unimplemented function

Input expression: `tan(x + y)`

Output:
```
Unimplemented: tan is not supported

Expression tree:
tan: tan(x + y)
+-Add: x + y
  commutative: True
  +-Symbol: x
  | commutative: True
  +-Symbol: y
    commutative: True
```

## Benefits

1. **Better Error Messages**: Users now know exactly which function is causing the issue
2. **Visual Representation**: The tree structure helps users understand the expression hierarchy
3. **Debugging Aid**: Users can see the full context of where the unimplemented function appears

## Testing

Run the test suite:
```bash
cd tests
python3 test_unimplemented_tree.py
```

Run the demonstration:
```bash
cd tests
python3 demo_tree_printing.py
```

## Implementation Details

The changes were made in `basmengine.py`:
- Added import: `from sympy.printing.tree import print_tree`
- Modified error handling in `basmArgsProcessor` to display tree for unimplemented functions
- Provides context about which operation or function is not supported
