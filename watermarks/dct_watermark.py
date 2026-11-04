
import subprocess

dct_watermark_exe = "C:/Users/pryanik/6th_year/combinations-of-watermark-distortion/bin/dct_watermark.exe"
dct_skip = 16

#correlation_type:
#0 - linear correlation
#1 - normalized correlation
#2 - correlation coefficient

def gen_reference(path_source, path_output):
    subprocess.call([dct_watermark_exe , "--gen_reference", "--skip_count=" + str(dct_skip), "--in=" + path_source, "--out=" + path_output])

def embed(path_source, path_reference, path_output, alpha):
    subprocess.call([dct_watermark_exe , "--embed", "--in=" + path_source, "--reference=" + path_reference, "--out=" + path_output, "--skip_count=" + str(dct_skip), "--alpha=" + str(alpha)])

def get_correlation(path, path_reference):
    exe_params = [dct_watermark_exe , "--get_correlation", "--in=" + path, "--reference=" + path_reference, "--skip_count=" + str(dct_skip),  "--correlation=" + str(1)]
    out = subprocess.run(exe_params, capture_output=True, text=True)

    correlcation = 0
    try:
        correlcation = float(out.stdout)
    except ValueError:
        correlcation = 0

    return correlcation



