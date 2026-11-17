from watermarks import dct_watermark


level = 0.5

watermarks = dct_watermark
watermark_name = "dct_watermark"


filters = {
    "blur": "unsharp=7:7:-1:7:7:-1",
    "jpeg": "mjpeg",
    "median_3x3": "median=radius=1:radiusV=1:planes=15",
    "median_5x5": "median=radius=2:radiusV=2:planes=15",
    "bilateral_weak": "bilateral=sigmaS=2:sigmaR=0.03:planes=7",
    "bilateral_medium": "bilateral=sigmaS=3:sigmaR=0.06:planes=7",
    "gblur_05": "gblur=sigma=0.5:steps=3:planes=15",
    "gblur_08": "gblur=sigma=0.8:steps=3:planes=15",
    "dctdnoiz_15": "dctdnoiz=s=15",
    "nlmeans_15": "nlmeans=s=15",
    "fftdnoiz_25": "fftdnoiz=sigma=25",
    "pixelize": "pixelize=w=2:h=2",
    "contrast_3": "colorlevels=rimin=0.3:gimin=0.3:bimin=0.3:rimax=0.7:gimax=0.7:bimax=0.7",
    "dark": "colorlevels=0.4:gimin=0.4:bimin=0.4",
    "noise": "noise=alls=100:allf=u",
}

for step in (2, 4, 8, 16):
    expression = f"clip({step}*floor(val/{step})+{step // 2},0,255)"
    filters[f"quantize_step{step}"] = (
        f"format=gbrp,lutrgb=r='{expression}':g='{expression}':b='{expression}'"
    )