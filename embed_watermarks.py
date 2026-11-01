import os
import shutil

from concurrent.futures import ThreadPoolExecutor
from watermarks import dct_watermark
from pathlib import Path
from tests import filter
import csv
import statistics

from utils import psnr
from utils import wmaf


def embed_watermark(watermark,  embedding_level, input_filename, images_dir):
    name_prefix = "correlation_tests/" + str(embedding_level)

    os.makedirs("correlation_tests", exist_ok=True)
    os.makedirs(name_prefix, exist_ok=True)
    os.makedirs(name_prefix + "/watermarked/", exist_ok=True)
    os.makedirs(name_prefix + "/reference/", exist_ok=True)

    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')

    reference_name = name_prefix + "/reference/" + str(filename_wo_ext) + ".bmp"
    output_name = name_prefix + "/watermarked/" + str(filename_wo_ext) + ".bmp"
    input_file = images_dir + "/" + input_filename

    watermark.gen_reference(input_file, reference_name)
    watermark.embed(input_file, reference_name, output_name, embedding_level)

def embed_watermarks_multithread(watermark, embedding_level, images_dir):
    max_threads = os.cpu_count();
    if max_threads > 4:
        max_threads -= 4
    threadPool = ThreadPoolExecutor(max_workers=max_threads)

    directory = os.fsencode(images_dir)
    futures = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        future = threadPool.submit(embed_watermark, watermark, embedding_level, filename, images_dir)
        futures.append(future)

    for future in futures:
        future.result()

def create_reference_wo_embedding(watermark, embedding_level, input_filename, images_dir):
    name_prefix = "correlation_tests/" + str(embedding_level)

    os.makedirs("correlation_tests", exist_ok=True)
    os.makedirs(name_prefix, exist_ok=True)
    os.makedirs(name_prefix + "/reference_wo_embedding/", exist_ok=True)

    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')

    reference_name = name_prefix + "/reference_wo_embedding/" + str(filename_wo_ext) + ".bmp"
    input_file = images_dir + "/" + input_filename

    watermark.gen_reference(input_file, reference_name)

def create_references_wo_embedding_multithread(watermark, embedding_level, images_dir):
    max_threads = os.cpu_count();
    if max_threads > 4:
        max_threads -= 4

    threadPool = ThreadPoolExecutor(max_workers=max_threads)

    directory = os.fsencode(images_dir)

    futures = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        future = threadPool.submit(create_reference_wo_embedding, watermark, embedding_level, filename, images_dir)
        futures.append(future)

    for future in futures:
        future.result()

def embed_watermarks(watermark, embedding_level, images_dir):
    embed_watermarks_multithread(watermark, embedding_level, images_dir)

def create_references_wo_embedding(watermark, embedding_level, images_dir):
    create_references_wo_embedding_multithread(watermark, embedding_level, images_dir)

def remove_files(embedding_level):
    dir_name = "correlation_tests/" + str(embedding_level) + "/watermarked/"
    shutil.rmtree(dir_name)

    dir_name = "correlation_tests/" + str(embedding_level) + "/reference/"
    shutil.rmtree(dir_name)

    dir_name = "correlation_tests/" + str(embedding_level) + "/reference_wo_embedding/"
    shutil.rmtree(dir_name)

def calc_quality(embedding_level, input_filename, metrics):
    name_prefix = "correlation_tests/" + str(embedding_level)

    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')
    output_name = name_prefix + "/watermarked/" + str(filename_wo_ext) + ".bmp"
    input_file = "images/" + input_filename

    return metrics.get_score(input_file, output_name)

def calc_quality_multithread(embedding_level, metrics):
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
        future = threadPool.submit(calc_quality, embedding_level, filename, metrics)
        futures.append(future)
        files.append(filename)

    metrics_name = "wmaf"
    if metrics == psnr:
        metrics_name = "psnr"

    csv_file_name = metrics_name + "_" + str(embedding_level) + ".csv"
    csv_file = open(csv_file_name, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csv_file)


    for future, file in zip(futures, files):
        score = future.result()
        scores.append(score)
        writer.writerow([file, score])

    return statistics.mean(scores)

def mean_psnr(embedding_level):
    return calc_quality_multithread(embedding_level, psnr)

def mean_wmaf(embedding_level):
    return calc_quality_multithread(embedding_level, wmaf)

if __name__ == "__main__":
    embedding_level = 5
    embed_watermarks(dct_watermark, "dct_watermark", embedding_level, "images")
#    remove_files(dct_watermark, "dct_watermark", embedding_level)