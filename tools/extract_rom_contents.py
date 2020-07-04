import os
from pathlib import Path
import ndspy.rom

projDir = Path.cwd().parent
assetsDir = projDir.joinpath('assets')

try:
    rom = ndspy.rom.NintendoDSRom.fromFile('rom.nds')

except FileNotFoundError:
    print("rom.nds does not exist")

print(rom.filenames)