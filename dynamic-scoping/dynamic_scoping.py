"""
Module Three Activity - Part Two: Simulated dynamic scoping
Dani Olaosebikan

Python always uses lexical scoping, so dynamic scoping is simulated here.
The DynamicScope class keeps an explicit stack of call frames:

  * calling a function pushes a frame holding that function's locals
  * returning pops the frame
  * looking up a name searches the stack from the MOST RECENT CALLER back
    to the oldest frame - where the function was written does not matter

Each example mirrors the same-numbered example in lexical.py. Functions read
and write variables only through env.get / env.set / env.define so that
every lookup goes through the simulated call stack.
"""

from contextlib import contextmanager


class DynamicScope:
    def __init__(self):
        self.stack = [("<global>", {})]

    @contextmanager
    def frame(self, func_name):
        self.stack.append((func_name, {}))      # function entered: push frame
        try:
            yield
        finally:
            self.stack.pop()                    # function returned: pop frame

    def define(self, name, value):
        """Create a variable in the current (top) frame, like a local assignment."""
        self.stack[-1][1][name] = value

    def get(self, name):
        """Dynamic lookup: newest frame first, then each caller in turn."""
        for _, frame in reversed(self.stack):
            if name in frame:
                return frame[name]
        raise NameError(name)

    def set(self, name, value):
        """Update the nearest existing binding on the call stack
        (the dynamic counterpart of 'nonlocal')."""
        for _, frame in reversed(self.stack):
            if name in frame:
                frame[name] = value
                return
        raise NameError(name)

    def where(self, name):
        for func_name, frame in reversed(self.stack):
            if name in frame:
                return func_name
        return None


env = DynamicScope()


def example_1():
    with env.frame("example_1"):
        env.define("x", "outer")

        def inner():
            with env.frame("inner"):
                # Stack: <global> -> example_1 -> inner
                # inner has no x -> check caller example_1 -> "outer"
                print(f"Inner sees: {env.get('x')}   [found in {env.where('x')}]")

        inner()
        print(f"Outer has: {env.get('x')}")


def example_2():
    with env.frame("example_2"):
        env.define("x", 10)

        def middle():
            with env.frame("middle"):
                env.define("x", 20)

                def inner():
                    with env.frame("inner"):
                        # Stack: <global> -> example_2 -> middle -> inner
                        # inner has no x -> nearest caller with x is middle -> 20
                        print(f"Inner sees: {env.get('x')}   [found in {env.where('x')}]")

                inner()
                print(f"Middle has: {env.get('x')}")

        middle()
        # middle's frame was popped when it returned, so x -> example_2's 10
        print(f"Outer has: {env.get('x')}")


def example_3():
    with env.frame("example_3"):
        env.define("count", 0)

        def increment():
            with env.frame("increment"):
                # Stack: <global> -> example_3 -> counter -> increment
                # count is not in increment or counter -> found in example_3
                env.set("count", env.get("count") + 1)
                return env.get("count")

        def get_counter():
            with env.frame("get_counter"):
                def counter():
                    with env.frame("counter"):
                        return increment()
                return counter          # get_counter's frame is popped on return

        my_counter = get_counter()
        print(my_counter())             # 1
        print(my_counter())             # 2
        print(env.get("count"))         # 2


def example_4():
    with env.frame("example_4"):
        env.define("name", "global")

        def outer():
            with env.frame("outer"):
                env.define("name", "outer")

                def inner():
                    with env.frame("inner"):
                        env.define("name", "inner")     # top frame -> found first
                        print(f"Inner: {env.get('name')}")

                inner()                                 # inner's frame popped
                print(f"Outer: {env.get('name')}")      # -> outer's "outer"

        outer()                                         # outer's frame popped
        print(f"Global: {env.get('name')}")             # -> example_4's "global"


def example_5():
    with env.frame("example_5"):
        env.define("x", "defined-here")

        def show():
            with env.frame("show"):
                # show has no x, so the CALLER decides which x it sees
                print(f"show sees: {env.get('x')}   [found in {env.where('x')}]")

        def caller():
            with env.frame("caller"):
                env.define("x", "caller's x")
                # Stack: <global> -> example_5 -> caller -> show
                # show has no x -> caller has x -> "caller's x"
                show()

        caller()
        # Stack: <global> -> example_5 -> show
        # show has no x -> example_5 has x -> "defined-here"
        show()


if __name__ == "__main__":
    print("Example 1:")
    example_1()

    print("\nExample 2:")
    example_2()

    print("\nExample 3:")
    example_3()

    print("\nExample 4:")
    example_4()

    print("\nExample 5 (added):")
    example_5()
