#!/usr/bin/env python

from src.app import app


if __name__ == "__main__":
    app.run(port=8080, debug=True)
