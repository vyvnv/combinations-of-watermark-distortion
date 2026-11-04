import os
import math

from concurrent.futures import ThreadPoolExecutor
from watermarks import dct_watermark
from pathlib import Path
import csv
import numpy as np

def calc_correlation(watermark, watermark_name, embedding_level, input_filename, filter_name):
    name_prefix = "correlation_tests/" + str(embedding_level)

    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')

    reference_name = name_prefix + "/reference/" + str(filename_wo_ext) + ".bmp"
    watermarked_name = name_prefix + "/watermarked/" + str(filename_wo_ext) + ".bmp"
    if filter_name:
        watermarked_name = name_prefix + "/" + filter_name + "/" + str(filename_wo_ext) + ".bmp"

    resultWatermarkedNC = watermark.get_correlation(watermarked_name, reference_name)

    reference_name = name_prefix + "/reference_wo_embedding/" + str(filename_wo_ext) + ".bmp"
    resultNotWatermarkedNC = watermark.get_correlation(watermarked_name, reference_name)


    return [filename, resultWatermarkedNC, resultNotWatermarkedNC]

def get_results_file_name(watermark_name, embedding_level, filter_name, suffix):
    os.makedirs("correlation_tests/" + str(embedding_level) + "/" + watermark_name, exist_ok=True)

    csv_file_name = "correlation_tests/" + str(embedding_level) + "/" + watermark_name + "/correlations_" + watermark_name + "_" + str(embedding_level)
    if filter_name:
        csv_file_name = "correlation_tests/" + str(embedding_level) + "/" + watermark_name + "/correlations_" + watermark_name + "_" + str(embedding_level) + "_" + filter_name

    csv_file_name += ".csv"

    return csv_file_name

def get_zscore_file_name(watermark_name, embedding_level, filter_name, suffix):
    os.makedirs("correlation_tests/" + str(embedding_level) + "/" + watermark_name, exist_ok=True)
    
    csv_file_name = "correlation_tests/" + str(embedding_level) + "/" + watermark_name + "/zscores_" + watermark_name + "_" + str(embedding_level)
    if filter_name:
        csv_file_name = "correlation_tests/" + str(embedding_level) + "/" + watermark_name + "/zscores_" + watermark_name + "_" + str(embedding_level) + "_" + filter_name

    csv_file_name += "_" + suffix + ".csv"

    return csv_file_name


def calc_correlations_multithread(watermark, watermark_name, embedding_level, filter_name, suffix):
    threadPool = ThreadPoolExecutor()

    directory = os.fsencode("images/")

    futures = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        future = threadPool.submit(calc_correlation, watermark, watermark_name, embedding_level, filename, filter_name)
        futures.append(future)

    csv_file_name = get_results_file_name(watermark_name, embedding_level, filter_name, suffix)

    csv_file = open(csv_file_name, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csv_file)

    for future in futures:
        result = future.result()
        writer.writerow(result)

def calc_correlations(watermark, watermark_name, embedding_level, filter_name, suffix):
    calc_correlations_multithread(watermark, watermark_name, embedding_level, filter_name, suffix)

def calc_distibution(watermark, watermark_name, embedding_level, filter_name, suffix):
    csv_file_name = get_results_file_name(watermark_name, embedding_level, filter_name, suffix)

    csv_file = open(csv_file_name, 'r', newline='', encoding='utf-8')
    reader = csv.reader(csv_file, quoting=csv.QUOTE_MINIMAL)

    y_zero= []
    y_one = []

    for row in reader:
        y_one.append(float(row[1]))
        y_zero.append(float(row[2]))

    y_zero = np.array(y_zero)
    y_one = np.array(y_one)

    mean_zero = np.mean(y_zero)
    std_zero = np.std(y_zero)

    mean_one = np.mean(y_one)
    std_one = np.std(y_one)

    return [mean_zero, std_zero, mean_one, std_one]

def convert_to_zscore(watermark, watermark_name, embedding_level, filter_name, suffix, distibution):
    csv_file_name = get_results_file_name(watermark_name, embedding_level, filter_name, suffix)
    zscore_file_name = get_zscore_file_name(watermark_name, embedding_level, filter_name, suffix)

    csv_file = open(csv_file_name, 'r', newline='', encoding='utf-8')
    reader = csv.reader(csv_file, quoting=csv.QUOTE_MINIMAL)

    zscore_file = open(zscore_file_name, 'w', newline='', encoding='utf-8')
    writer = csv.writer(zscore_file)


    for row in reader:
        row[1] = (float(row[1]) - distibution[0]) / distibution[1]
        row[2] = (float(row[2]) - distibution[0]) / distibution[1]
        writer.writerow(row)

if __name__ == "__main__":
    embedding_level = 5

    calc_correlations(dct_watermark, "dct_watermark", embedding_level, "", "")
    #calc_correlations(dct_watermark, "dct_watermark", embedding_level, "blur", "")
