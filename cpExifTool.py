import glob
import sys
import subprocess
import os

dirname = sys.argv[1]
dirname = dirname if dirname.endswith('/') else f'{dirname}/'
in_files = sorted(glob.glob(f'{dirname}selected/*'))
out_files = []
for out_file in glob.glob(f'{dirname}dev/*.jpg'):
    token = out_file.split('.')
    new_out_file = f'{token[0]}.{token[1].zfill(3)}.{token[2]}.jpg'
    out_files.append(new_out_file)
    os.rename(out_file, new_out_file)
out_files = sorted(out_files)


if len(in_files) == len(out_files):
    for i in range(len(in_files)):
        in_file = in_files[i]
        out_file = out_files[i]
        cmd = f'exiftool -tagsfromfile ./{in_file} -all:all ./{out_file}'
        print(cmd)
        subprocess.run(cmd, shell=True)

        new_outfile_name = f'{dirname}dev/{in_file.split("/")[2]}'
        print(f'rename {out_file} to {new_outfile_name}')
        os.rename(out_file, new_outfile_name)