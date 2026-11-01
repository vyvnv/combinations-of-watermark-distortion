import calc_correlations
import embed_watermarks
import filter_watermarks

import config

embed_watermarks.embed_watermarks(config.watermarks[0], config.level, "images")
embed_watermarks.create_references_wo_embedding(config.watermarks[0], config.level, "images")

mean_psnr = embed_watermarks.mean_psnr(config.level)
mean_wmaf = embed_watermarks.mean_wmaf(config.level)
print("\tMean PSNR: %.4f" % mean_psnr)
print("\tMean WMAF: %.4f" % mean_wmaf)

for watermark, watermark_name in zip(config.watermarks, config.watermark_names):
    print ("%s" % (watermark_name))
    calc_correlations.calc_correlations(watermark, watermark_name, config.level, None, "evaluation")
    distibution =  calc_correlations.calc_distibution(watermark, watermark_name, config.level, None, "evaluation")
    print ("\tmean(zero) = %.10f \n\tstd_dev(zero) = %.10f \n\tmean(one) = %.10f \n\tstd_dev(one) = %.10f" % (distibution[0], distibution[1], distibution[2], distibution[3]))

for filter_name, filter_params in config.filters.items():
    print("%s" % filter_name)
    filter_watermarks.filter_watermarks(config.level, filter_name, filter_params)

    mean_psnr = filter_watermarks.mean_psnr(filter_name, config.level)
    mean_wmaf = filter_watermarks.mean_wmaf(filter_name, config.level)
    print("\tMean PSNR: %.4f" % mean_psnr)
    print("\tMean WMAF: %.4f" % mean_wmaf)

    for watermark, watermark_name in zip(config.watermarks, config.watermark_names):
        print ("\t%s" % (watermark_name))
        calc_correlations.calc_correlations(watermark, watermark_name, config.level, filter_name, "test")
        distibution =  calc_correlations.calc_distibution(watermark, watermark_name, config.level, filter_name, "test")

        print ("\t\tmean(zero) = %.10f \n\t\tstd_dev(zero) = %.10f \n\t\tmean(one) = %.10f \n\t\tstd_dev(one) = %.10f" % (distibution[0], distibution[1], distibution[2], distibution[3]))

    filter_watermarks.remove_files(config.level, filter_name)

embed_watermarks.remove_files(config.level)
