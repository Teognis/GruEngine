import sys
COMPILER = "C:\Users\Teognis\Documents\GitHub\GruEngine\Compile"
sys.path.insert(0, COMPILER)
from compiler import Compiler
compiler = Compiler(file=None, portable=True)