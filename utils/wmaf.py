import sys
import shutil
import os
import subprocess

def get_score(path1, path2):
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg executable is not Found")
        return -1

    out = subprocess.run(["ffmpeg", "-i", path1, "-i", path2, "-lavfi", "libvmaf", "-f", "null", "/dev/null"], capture_output=True, text=True)

    position = out.stderr.find("VMAF score: ")
    output = out.stderr
    if position < 0:
        output = out.stdout
        position = out.stdout.find("VMAF score: ")
        if position < 0:
            return 0

    
    position += len("VMAF score: ")
    value = output[position:-1]
    return float(value)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("`path1` and `path2` arguments expected")
        exit(1)

    print(get_score(sys.argv[1], sys.argv[2]))
