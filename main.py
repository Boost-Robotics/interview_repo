"""
main.py – starter entry point for the interview exercise.

Feel free to modify, extend, or replace this file as you see fit.
"""


def greet(name: str) -> str:
    """Return a greeting string for the given name."""
    return f"Hello, {name}! Welcome to the interview exercise."


def main() -> None:
    print(greet("Interviewee"))


if __name__ == "__main__":
    main()
