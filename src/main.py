import sys
from core import AppCore


def main() -> int:
    core = AppCore()
    return core.run()


if __name__ == "__main__":
    sys.exit(main())