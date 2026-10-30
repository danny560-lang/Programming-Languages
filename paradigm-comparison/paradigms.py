"""
Programming Paradigm Comparison
Author: Daniel Olaosebikan

Problem: Given a list of integers, filter out all even numbers, square the
remaining odd numbers, and return the result as a new list.

The same algorithm is implemented three times:
    1. Imperative
    2. Object-oriented
    3. Functional
"""

from functools import reduce


# =============================================================================
# 1. IMPERATIVE APPROACH
# =============================================================================
# The imperative paradigm describes HOW to reach the result as an explicit,
# ordered sequence of statements that change program state step by step.

def square_odds_imperative(numbers):
    # State: create a mutable result list that will be changed as we go.
    result = []

    # Explicit control flow: a for loop visits each element in order.
    for number in numbers:
        # Explicit decision: a conditional statement checks each value.
        if number % 2 != 0:
            # Compute the square and store it in a temporary variable.
            squared = number * number
            # State mutation: append modifies the result list in place.
            result.append(squared)
        # Even numbers fall through and are simply never appended.

    # The final state of the variable is the answer.
    return result


# =============================================================================
# 2. OBJECT-ORIENTED APPROACH
# =============================================================================
# The object-oriented paradigm organizes code around objects that bundle data
# (attributes) with the behavior (methods) that operates on that data.

class NumberProcessor:
    """Base class that defines the general processing workflow."""

    def __init__(self, numbers):
        # Encapsulation: the input data is stored inside the object and kept
        # "private" by convention (leading underscore), so outside code works
        # with the object's methods instead of touching the data directly.
        self._numbers = list(numbers)  # copy so the caller's list is not changed

    def should_keep(self, number):
        # Abstraction: subclasses decide WHAT to keep; the base class only
        # knows that a keep/discard decision must be made.
        raise NotImplementedError("Subclasses must implement should_keep()")

    def transform(self, number):
        # Abstraction: subclasses decide HOW to transform a kept value.
        raise NotImplementedError("Subclasses must implement transform()")

    def process(self):
        # The template workflow lives in one place. It calls the overridable
        # methods, so the class controls the steps while subclasses supply the
        # details (template method pattern).
        processed = []
        for number in self._numbers:
            if self.should_keep(number):
                processed.append(self.transform(number))
        return processed


class OddSquareProcessor(NumberProcessor):
    """Inheritance: reuses the workflow from NumberProcessor and specializes it."""

    def should_keep(self, number):
        # Polymorphism: this override gives the generic process() method the
        # "keep only odd numbers" behavior for this specific object type.
        return number % 2 != 0

    def transform(self, number):
        # Polymorphism: this override supplies the "square the value" behavior.
        return number ** 2


def square_odds_oop(numbers):
    # Objects are created and then asked to do the work by sending them a
    # message (calling a method), rather than the caller running the steps.
    processor = OddSquareProcessor(numbers)
    return processor.process()


# =============================================================================
# 3. FUNCTIONAL APPROACH
# =============================================================================
# The functional paradigm describes WHAT the result is by composing pure
# functions. Data is never mutated; each step returns a new value.

# Pure function: output depends only on its input and has no side effects.
def is_odd(n):
    return n % 2 != 0


# Pure function: always returns the same square for the same input.
def square(n):
    return n * n


# Higher-order function: takes functions as arguments and returns a new
# function that applies them right to left (function composition).
def compose(*functions):
    return lambda data: reduce(lambda acc, f: f(acc), reversed(functions), data)


# Build the pipeline declaratively. No loops, no counters, no mutable state:
#   1. filter(is_odd, data)  -> lazily keeps only odd values
#   2. map(square, ...)      -> lazily squares each kept value
#   3. list(...)             -> produces a brand-new list as the result
square_odds_functional = compose(
    list,
    lambda data: map(square, data),
    lambda data: filter(is_odd, data),
)


# =============================================================================
# DRIVER / TEST CODE
# =============================================================================
def main():
    test_cases = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [-5, -4, -3, 0, 3, 4, 5],
        [2, 4, 6, 8],
        [],
    ]

    implementations = [
        ("Imperative", square_odds_imperative),
        ("Object-Oriented", square_odds_oop),
        ("Functional", square_odds_functional),
    ]

    print("=" * 60)
    print(" Filter Evens and Square Odds: Paradigm Comparison")
    print("=" * 60)

    for numbers in test_cases:
        original = list(numbers)  # used to confirm the input is unchanged
        print(f"\nInput: {numbers}")
        results = []
        for name, func in implementations:
            output = func(numbers)
            results.append(output)
            print(f"  {name:<16}-> {output}")

        all_match = all(r == results[0] for r in results)
        print(f"  All paradigms match: {all_match}")
        print(f"  Original list unchanged: {numbers == original}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
