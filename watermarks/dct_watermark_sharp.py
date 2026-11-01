import subprocess
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from tests import filter

dct_watermark_exe = "D:/projects/watermarks/project/apps/RelWithDebInfo/dct_watermark.exe"

dct_skip = 16
#sharp_strengths = 4
sharp_strengths = 52

#correlation_type:
#0 - linear correlation
#1 - normalized correlation
#2 - correlation coefficient

def gen_reference(path_source, path_output):
    subprocess.call([dct_watermark_exe , "--gen_reference", "--skip_count=" + str(dct_skip), "--in=" + path_source, "--out=" + path_output])

def embed(path_source, path_reference, path_output, alpha):
    subprocess.call([dct_watermark_exe , "--embed", "--in=" + path_source, "--reference=" + path_reference, "--out=" + path_output, "--skip_count=" + str(dct_skip), "--alpha=" + str(alpha)])

def get_correlation(path, path_reference):
    path_sharp = path + "_sharp_tmp.bmp"

    filter.run("unsharp=11:11:" + str(sharp_strengths) + ":11:11:" + str(sharp_strengths), path, path_sharp)

    exe_params = [dct_watermark_exe , "--get_correlation", "--in=" + path_sharp, "--reference=" + path_reference, "--skip_count=" + str(dct_skip),  "--correlation=" + str(1)]
    out = subprocess.run(exe_params, capture_output=True, text=True)

    correlcation = 0
    try:
        correlcation = float(out.stdout)
    except ValueError:
        correlcation = 0

    return correlcation

if __name__ == "__main__":
    gen_reference("3637013_c675de7705.jpg", "reference.bmp")
    embed("3637013_c675de7705.jpg", "reference.bmp", "watermarked.png", 10)

    print(get_correlation("watermarked.png", "reference.bmp"))
    print(get_correlation("3637013_c675de7705.jpg", "reference.bmp"))
