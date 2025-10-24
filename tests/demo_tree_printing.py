#!/usr/bin/env python3
"""
Demonstration of tree printing for unimplemented functions.

This script shows examples of how the tree is printed for various
unimplemented functions in flexpy.
"""

import sys
import sympy as sp

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


def demo_function(func_name, expr):
    """Demonstrate tree printing for a given expression"""
    print("\n" + "=" * 60)
    print(f"Example: {func_name}")
    print("=" * 60)
    print(f"Expression: {expr}")
    print()
    
    engine = MockEngine()
    engine.basmArgsProcessor = basmArgsProcessor.__get__(engine, MockEngine)
    
    try:
        result = engine.basmArgsProcessor(expr, 1)
        print(f"Note: {func_name} is actually implemented!")
    except SystemExit:
        pass


if __name__ == "__main__":
    print("Flexpy Unimplemented Function Tree Display Demo")
    print("=" * 60)
    print("When flexpy encounters an unimplemented function, it now")
    print("displays a detailed tree representation to help users")
    print("understand the expression structure.")
    
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    z = sp.Symbol('z')
    
    # Example 1: Simple unimplemented function
    demo_function("tan(x)", sp.tan(x))
    
    # Example 2: Complex expression with unimplemented function
    demo_function("tan(x) + cos(y)", sp.tan(x) + sp.cos(y))
    
    # Example 3: Nested unimplemented function
    demo_function("tan(x + y)", sp.tan(x + y))
    
    # Example 4: Multiple unimplemented functions
    demo_function("tan(x) * atan(y)", sp.tan(x) * sp.atan(y))
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)
