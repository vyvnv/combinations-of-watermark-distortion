import sys
import shutil
import os
import subprocess

def get_score(path1, path2):
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg executable is not Found")
        return -1

    out = subprocess.run(["ffmpeg", "-i", path1, "-i", path2, "-lavfi", "psnr", "-f", "null", "/dev/null"], capture_output=True, text=True)
    position = out.stderr.find("average:")
    output = out.stderr
    if position < 0:
        output = out.stdout
        position = out.stdout.find("average:")
        if position < 0:
            return 0

    
    position += len("average:")
    str = output[position:-1]
    position = str.find(" ")
    value = str[0:position]

    return float(value)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("`path1` and `path2` arguments expected")
        exit(1)

    print(get_score(sys.argv[1], sys.argv[2]))
