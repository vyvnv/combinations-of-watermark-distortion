import sys
import shutil
import os
import subprocess

#ffmpeg_unsharp_path = "/home/user/test/ffmpeg/ffmpeg-7.0.1/ffmpeg"
ffmpeg_unsharp_path = "D:\\problems\\ffmpeg\\ffmpeg-n7.1-latest-win64-lgpl-shared-7.1\\bin\\ffmpeg.exe" #path to patched ffmpeg with unlimited unsparp strength

dct_eraser_path = "D:\\projects\\watermarks\\project\\apps\\RelWithDebInfo\\dct_eraser.exe"
def dct_eraser(filter, path_source, path_output):

    percentage = 100
    if "=" in filter:
        percentage = filter.split('=')[1]

    subprocess.call([dct_eraser_path, "-i", path_source, "-o", path_output, "--erase_probability", percentage], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
def run(filter, path_source, path_output):
    if "dct_eraser" in filter:
        dct_eraser(filter, path_source, path_output)
        return


    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg executable is not Found")
        return -1
    
    if filter == "mjpeg":
        subprocess.call(["ffmpeg", "-y", "-i", path_source, "-vcodec", "mjpeg"] + ["-qmin", "10", "-qmax", "10" ] + [path_output], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return

    ffmpeg_exe = "ffmpeg"
    if "unsharp" in filter:
        ffmpeg_exe = "ffmpeg"

    subprocess.call([ffmpeg_exe, "-y", "-i", path_source, "-vf", filter, path_output], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
#    if len(sys.argv) != 2:
#        print("`path_source` argument expected")
#        exit(1)

    run("dct_eraser=100", "12830823_87d2654e31.jpg", "dct_eraser_100.bmp")
    run("dct_eraser=80", "12830823_87d2654e31.jpg", "dct_eraser_80.bmp")
    run("dct_eraser=50", "12830823_87d2654e31.jpg", "dct_eraser_50.bmp")
    run("dct_eraser=10", "12830823_87d2654e31.jpg", "dct_eraser_10.bmp")

#    run("dctdnoiz=s=10", sys.argv[1], "dctdnoiz.png")
#    run("unsharp=chroma_msize_x=14:chroma_msize_y=14:chroma_amount=-0.25", sys.argv[1], "unsharp1.png")
#    run("unsharp=5:5:-1:5:5:-1", sys.argv[1], "unsharp_1.png")
#    run("unsharp=7:7:-1:7:7:-1", sys.argv[1], "unsharp_8_1.png")
#    run("unsharp=11:11:-1:11:11:-1", sys.argv[1], "unsharp_11_1.png")
#    run("unsharp=11:11:10:11:11:10", sys.argv[1], "unsharp_10.png")
#    run("unsharp=11:11:5.1:11:11:5.1", sys.argv[1], "unsharp_51.png")

#    run("colorlevels=rimin=0.039:gimin=0.039:bimin=0.039:rimax=0.96:gimax=0.96:bimax=0.96", sys.argv[1], sys.argv[2])
#    run("colorlevels=rimin=0.058:gimin=0.058:bimin=0.058", sys.argv[1], "darker.png")

#    run("colorlevels=rimin=0.039:gimin=0.039:bimin=0.039:rimax=0.96:gimax=0.96:bimax=0.96", sys.argv[1], "contrast.png")

#    run("colorlevels=rimax=0.9:gimax=0.9:bimax=0.9", sys.argv[1], "lighter1.png")
#    run("colorlevels=rimax=0.1:gimax=0.1:bimax=0.1", sys.argv[1], "lighter2.png")
#    run("colorlevels=rimax=0.6:gimax=0.6:bimax=0.6", sys.argv[1], "lighter3.png")
#    run("colorlevels=romin=0.05:gomin=0.05:bomin=0.05", sys.argv[1], "brightness05.png")
#    run("colorlevels=romin=0.1:gomin=0.1:bomin=0.1", sys.argv[1], "brightness1.png")
#    run("colorlevels=romin=0.2:gomin=0.2:bomin=0.2", sys.argv[1], "brightness2.png")

#    run("colorlevels=romin=0.5:gomin=0.5:bomin=0.5", sys.argv[1], "brightness5.png")
#    run("noise=alls=100:allf=u", sys.argv[1], "noise110.png")
#    run("noise=alls=50:allf=u", sys.argv[1], "noise1.png")

#    run("nlmeans=s=10", sys.argv[1], "nlmeans.png")
#    run("pixelize=w=3:h=3", sys.argv[1], "pixelize3.png")
#    run("pixelize=w=2:h=2", sys.argv[1], "pixelize2.png")
#    run("pixelize=w=1:h=1", sys.argv[1], "pixelize1.png")
#    run("fftdnoiz=sigma=15", sys.argv[1], "fftdnoiz.png")
#    run("mjpeg", sys.argv[1], "out.png")

