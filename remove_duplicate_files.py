import os, sys, shutil
input_dir =  sys.argv[1]
output_dir = sys.argv[2]
files = os.listdir(output_dir)
for file in files:
    if os.path.exists(os.path.join(input_dir, file)):
        if os.path.isfile(os.path.join(output_dir, file)):
            os.remove(os.path.join(output_dir, file))
        elif os.path.isdir(os.path.join(output_dir, file)):
            shutil.rmtree(os.path.join(output_dir, file))
