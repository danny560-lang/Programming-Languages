"""Typing and scope demonstrations for the Module Three activity."""

# Part One: Python is dynamically typed. This annotated assignment documents
# an intended type, but Python does not enforce it at compile time.
def typing_examples():
    print("Part One: typing")
    value: int = 10
    print(f"Initial value ({type(value).__name__}): {value}")

    # Deliberate mismatch: an int annotation does not prevent a str assignment.
    value = "ten"  # type: ignore[assignment]  # Runtime still permits this.
    print(f"After mismatch ({type(value).__name__}): {value}")
    try:
        print(value + 1)  # Runtime TypeError: str and int cannot be added.
    except TypeError as error:
        print(f"Mismatch error: {error}")

    # Corrected version: keep the value an int so arithmetic is valid.
    corrected_value: int = 10
    corrected_value += 1
    print(f"Corrected int arithmetic: {corrected_value}")
    # Or explicitly convert numeric text before arithmetic.
    converted_value = int("10") + 1
    print(f"Corrected conversion: {converted_value}")

# Part Two: normal nested functions use lexical (static) name lookup.
def lexical_demo():
    print("\nPart Two: lexical scoping")
    x = "defined-here"  # Enclosing lexical binding used by show().

    def show():
        # Python searches show's local, then lexical enclosing scopes.
        print(f"Lexical show sees: {x}")

    def caller():
        x = "caller's x"  # This binding is not in show's lexical scope.
        print(f"Caller local is: {x}")
        show()  # Resolves x to lexical_demo's value, not caller's.

    caller()
    show()

# Python has no native dynamic scoping. This simulation passes an explicit
# environment representing the active caller chain, then searches it inward-out.
def dynamic_demo():
    print("\nSimulated dynamic scoping")
    global_env = {"x": "global x"}

    def show_dynamic(environments):
        # Search active environments from the most recent caller outward.
        for environment in reversed(environments):
            if "x" in environment:
                print(f"Dynamic show sees: {environment['x']}")
                return
        print("Dynamic show: x is undefined")

    def caller():
        caller_env = {"x": "caller's x"}  # Nearest active x wins.
        show_dynamic([global_env, caller_env])

    caller()
    show_dynamic([global_env])  # Without caller binding, global x is used.

if __name__ == "__main__":
    typing_examples()
    lexical_demo()
    dynamic_demo()
