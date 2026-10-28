"""Точка входа: python3 main.py."""


def main():
    from config import parse_args
    config = parse_args()
    from gui import run
    run(config)


if __name__ == "__main__":
    main()
