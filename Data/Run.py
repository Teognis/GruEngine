import sys
import os

FOLDER = os.path.dirname(os.path.realpath(__file__))
COMPILER = "C:\Users\Teognis\Documents\GitHub\GruEngine\Compile"
GRU_FOLDER = "C:\Users\Teognis\Documents\GitHub\GruEngine"
sys.path.insert(0, GRU_FOLDER)
SYSTEM = os.path.join(GRU_FOLDER, "system")
sys.path.insert(0, SYSTEM)
sys.path.insert(0, COMPILER)

from compiler import Compiler
compiler = Compiler()
stream = compiler.compile(FOLDER)
gru_file = compiler.dump(stream, FOLDER)

import GruEngine
GruEngine.Main(gru_file).start()
