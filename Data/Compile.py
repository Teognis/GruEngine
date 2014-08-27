import sys
COMPILER = "C:\Users\Teognis\Documents\GitHub\GruEngine\Compile"
sys.path.insert(0, COMPILER)
from compiler import Compiler
compiler = Compiler(filename=None, portable=True)
gru_file = compiler.filename