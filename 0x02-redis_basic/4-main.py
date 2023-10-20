#!/usr/bin/env python3

from web import get_page


def main():
    url = 'http://slowwly.robertomurray.co.uk'
    while True:
        try:
            get_page(url)
        except KeyboardInterrupt:
            exit(130)


if __name__ == "__main__":
    main()
