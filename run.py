from interpreter import run_code
import sys

if len(sys.argv) > 1:
    path = sys.argv[1]
    code = open(path, "r").read()
    run_code(code)
