import os, sys
import utils
import ndspy.rom

projDir = utils.ROOT_DIR
assetsDir = utils.ROOT_DIR + "assets/"

regions = {"E":"USA", "P":"Europe", "J":"Japan"}
games = {
            "LAYTON4":"Professor Layton and the Last Specter",
            "LAYTON3":"Professor Layton and the Unwound Future",
            "LAYTON2":"Professor Layton and the Diabolical Box",
            "LAYTON1":"Professor Layton and the Curious Village"
        }

if len(sys.argv) != 2:
    print("Usage: extract_rom_contents.py rom.nds")
    exit(-1)

try:
    rom = ndspy.rom.NintendoDSRom.fromFile(sys.argv[1])

except FileNotFoundError:
    print("rom.nds does not exist")
    exit(1)

romName = rom.name.decode()
romId = rom.idCode.decode()
romRegion = regions[romId[3]]

print(rom.filenames)
print("Project path: " + projDir)
print("Assets path: " + assetsDir)
print("ROM name :" + romName)
print("Game name: " + games[romName])
print("ROM ID: " + romId)
print("ROM region : " + romRegion)

gameAssetsDir = assetsDir + romName

# Due to the formatting of rom.filenames and the lack of a proper iterator,
# we are forced to check a tabIndex to see in which directory we are
directories = []    # List of directories which we access with the tabIndex. index 0 is parent of index 1 etc
paths = []          # Stores our formatted paths with their filenames
offset = 5          # 4 id numbers + 1 space
fileOrDirName = None

for line in rom.filenames._strList():
    tabIndex = line.count("    ")
    fileOrDirName = line[offset + tabIndex * 4:]

    # If we are dealing with a directory
    if line[-1] == "/":
        directories = directories[:tabIndex]
        directories.append(fileOrDirName)
        paths.append("".join(directories))
    else:
    # If we are working with a file
        paths.append("".join(directories) + fileOrDirName)


print("Extracting into: " + gameAssetsDir)
# If our gameAssetsDir already exists, skip creation and cd into the directory
if not os.path.exists(gameAssetsDir):
    os.mkdir(gameAssetsDir)
os.chdir(gameAssetsDir)

for path in paths:
    # If we are dealing with a directory
    if path[-1] == "/":
        os.makedirs(path, exist_ok=True)
        print("Created dir: " + path)
    else:
    # If we are dealing with a file
        fileData = rom.getFileByName(path)
        with open(path, 'wb') as f:
            f.write(fileData)
            print("Created file: " + path)

print("Done.")
