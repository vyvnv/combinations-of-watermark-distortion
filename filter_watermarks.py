import os
import shutil
import csv
import statistics

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tests import filter

from utils import psnr
from utils import wmaf

def filter_watermark(embedding_level, input_filename, filter_name, filter_params, source_folder="watermarked"):
    name_prefix = "correlation_tests/" + "/" + str(embedding_level)

    os.makedirs("correlation_tests", exist_ok=True)
    os.makedirs(name_prefix, exist_ok=True)
    os.makedirs(name_prefix + "/" + filter_name, exist_ok=True)
    os.makedirs(name_prefix + "/wo_embedding_" + filter_name, exist_ok=True)

    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')

    watermarked_name = name_prefix + "/" + source_folder + "/" + str(filename_wo_ext) + ".bmp"
    filtered_name = name_prefix + "/" + filter_name + "/" + str(filename_wo_ext) + ".bmp"

    filter.run(filter_params, watermarked_name, filtered_name)


def filter_watermarks_multithread(embedding_level, filter_name, filter_params, source_folder="watermarked"):
    max_threads = os.cpu_count();
    if max_threads > 4:
        max_threads -= 4
    threadPool = ThreadPoolExecutor(max_workers=max_threads)

    directory = os.fsencode("images/")

    futures = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        future = threadPool.submit(filter_watermark, embedding_level, filename, filter_name, filter_params, source_folder)
        futures.append(future)

    for future in futures:
        future.result()

def filter_watermarks(embedding_level, filter_name, filter_params, source_folder="watermarked"):
    filter_watermarks_multithread(embedding_level, filter_name, filter_params, source_folder)

def remove_files(embedding_level, filter_name):
    dir_name = "correlation_tests/" + "/" + str(embedding_level) + "/" + filter_name
    shutil.rmtree(dir_name)

    dir_name = "correlation_tests/" + "/" + str(embedding_level) + "/wo_embedding_" + filter_name
    shutil.rmtree(dir_name)

def calc_quality(filter_name, embedding_level, input_filename, metrics):
    name_prefix = "correlation_tests/" + "/" + str(embedding_level)


    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')
    image_dir = filter_name if filter_name else "watermarked"
    filtered_name = name_prefix + "/" + image_dir + "/" + str(filename_wo_ext) + ".bmp"
    input_file = "images/" + input_filename

    return metrics.get_score(input_file, filtered_name)

def calc_quality_multithread(filter_name, embedding_level, metrics):
    max_threads = os.cpu_count();
    if max_threads > 4:
        max_threads -= 4

    threadPool = ThreadPoolExecutor(max_workers=max_threads)

    directory = os.fsencode("images/")
    futures = []
    files = []
    scores = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        future = threadPool.submit(calc_quality, filter_name, embedding_level, filename, metrics)
        futures.append(future)
        files.append(filename)

    metrics_name = "wmaf"
    if metrics == psnr:
        metrics_name = "psnr"

    csv_file_name = metrics_name + "_" + str(embedding_level) + "_" + (filter_name or "no_filter") + ".csv"
    csv_file = open(csv_file_name, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csv_file)


    for future, file in zip(futures, files):
        score = future.result()
        scores.append(score)
        writer.writerow([file, score])

    return statistics.mean(scores)

def mean_psnr(filter_name, embedding_level):
    return calc_quality_multithread(filter_name, embedding_level, psnr)

def mean_wmaf(filter_name, embedding_level):
    return calc_quality_multithread(filter_name, embedding_level, wmaf)


if __name__ == "__main__":
    embedding_level = 0.5
   # filter_watermarks(embedding_level, "blur", "unsharp=3:3:-0.25:3:3:-0.25")

#    remove_files(dct_watermark, "dct_watermark", embedding_level, "blur")
    no_filter_avg_psnr = mean_psnr("", embedding_level)
    print("ср знач PSNR без фильтра  ", no_filter_avg_psnr)
    avg_psnr = mean_psnr("blur", embedding_level)
    print("ср знач PSNR  ", avg_psnr)