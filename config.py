from watermarks import dct_watermark

level = 0.5

watermarks = dct_watermark
watermark_name = "dct_watermark"


filters = {
    "blur": "unsharp=7:7:-1:7:7:-1",
    "dctdnoiz_15": "dctdnoiz=s=15",
    "nlmeans_15": "nlmeans=s=15",
    "fftdnoiz_25": "fftdnoiz=sigma=25",
    "pixelize": "pixelize=w=2:h=2",
    "jpeg": "mjpeg",
    "contrast_3": "colorlevels=rimin=0.3:gimin=0.3:bimin=0.3:rimax=0.7:gimax=0.7:bimax=0.7",
    "dark": "colorlevels=0.4:gimin=0.4:bimin=0.4",
    "noise": "noise=alls=100:allf=u",
}