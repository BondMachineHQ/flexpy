#!/usr/bin/env python3
"""
Test script to demonstrate tree printing for unimplemented functions.

This test demonstrates that when flexpy encounters an unimplemented function,
it now displays the sympy expression tree instead of just throwing a generic error.
"""

import sys
import sympy as sp
from io import StringIO

# Add parent directory to path
sys.path.insert(0, '..')

from basmengine import basmArgsProcessor


class MockEngine:
    """Mock engine object for testing"""
    def __init__(self):
        self.debug = False
        self.mindex = 0
        self.basm = ""
        self.prefix = "test"
        self.opsstring = "add:test,mul:test"
        self.params = ""
        self.neurons = {}
    
    def addToStatistics(self, neuron):
        if neuron not in self.neurons:
            self.neurons[neuron] = 1
        else:
            self.neurons[neuron] += 1


def test_unimplemented_function():
    """Test that unimplemented functions display a tree"""
    print("Testing unimplemented function (tan)...")
    
    x = sp.Symbol('x')
    expr = sp.tan(x)
    
    engine = MockEngine()
    engine.basmArgsProcessor = basmArgsProcessor.__get__(engine, MockEngine)
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    try:
        result = engine.basmArgsProcessor(expr, 1)
        sys.stdout = old_stdout
        print("ERROR: Should have raised SystemExit")
        return False
    except SystemExit:
        sys.stdout = old_stdout
        output = captured_output.getvalue()
        
        # Check that output contains expected elements
        if "Unimplemented: tan is not supported" in output:
            print("✓ Descriptive error message found")
        else:
            print("✗ Missing descriptive error message")
            print(f"Output was: {output}")
            return False
            
        if "Expression tree:" in output:
            print("✓ Tree header found")
        else:
            print("✗ Missing tree header")
            print(f"Output was: {output}")
            return False
            
        if "tan: tan(x)" in output:
            print("✓ Tree structure found")
        else:
            print("✗ Missing tree structure")
            print(f"Output was: {output}")
            return False
        
        print("\nActual output:")
        print(output)
        return True


def test_implemented_function():
    """Test that implemented functions still work"""
    print("\nTesting implemented function (Add)...")
    
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    expr = x + y
    
    engine = MockEngine()
    engine.basmArgsProcessor = basmArgsProcessor.__get__(engine, MockEngine)
    
    try:
        result = engine.basmArgsProcessor(expr, 1)
        print("✓ Implemented function processed without error")
        return True
    except SystemExit as e:
        print(f"✗ Implemented function raised SystemExit: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Testing unimplemented function tree printing")
    print("=" * 60)
    
    test1_pass = test_unimplemented_function()
    test2_pass = test_implemented_function()
    
    print("\n" + "=" * 60)
    if test1_pass and test2_pass:
        print("All tests passed! ✓")
        sys.exit(0)
    else:
        print("Some tests failed! ✗")
        sys.exit(1)
