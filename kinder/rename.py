from os import rename
from os import listdir
from os.path import isfile, join

filesDir = './data'

files = [f for f in listdir(filesDir) if isfile(join(filesDir, f))]

counter = 1
for f in files:
    new_path = join(filesDir, r'kinder_' + str(counter) + '.jpg')
    old_path = join(filesDir, f)
    rename(old_path, new_path)
    counter += 1