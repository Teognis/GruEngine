import sys
import os
GRU_FOLDER = "C:\Users\Teognis\Documents\GitHub\GruEngine"
sys.path.insert(0, GRU_FOLDER)
SYSTEM = os.path.join(GRU_FOLDER, "system")
sys.path.insert(0, SYSTEM)
import GruEngine
import Compile
gru_file = Compile.gru_file
main = GruEngine.Main(gru_file)
main.start()