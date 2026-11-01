import calc_correlations

import csv

import config
from itertools import combinations

def get_full_results_file_name(watermark_name, level, full=0):
    csv_file_name = "correlation_tests/" + "/" + str(level) + "/" + watermark_name + "/" + watermark_name + "_" + str(level)

    return csv_file_name + str(".csv")

def get_fusion_results_file_name(watermarks_names, level, suffix):
    csv_file_name = "fusion_" + str(level)

    for watermark_name in watermarks_names:
        csv_file_name += "_" + watermark_name

    return csv_file_name + "_" + suffix + str(".csv")

def combine_results(watermarks_names, level):
    file_names = []
    files = []
    readers = []

    for watermark_name in watermarks_names:
        file_name = get_full_results_file_name(watermark_name, level)
        file_names.append(file_name)
        f = open(file_name, 'r', newline='', encoding='utf-8')
        files.append(f)
        readers.append(csv.reader(f, quoting=csv.QUOTE_MINIMAL))


    sum_fusion_file_name = get_fusion_results_file_name(watermarks_names, level, "sum")
    sum_fusion_file = open(sum_fusion_file_name, 'w', newline='', encoding='utf-8')
    writer_sum = csv.writer(sum_fusion_file)

    min_fusion_file_name = get_fusion_results_file_name(watermarks_names, level, "min")
    min_fusion_file = open(min_fusion_file_name, 'w', newline='', encoding='utf-8')
    writer_min = csv.writer(min_fusion_file)

    max_fusion_file_name = get_fusion_results_file_name(watermarks_names, level, "max")
    max_fusion_file = open(max_fusion_file_name, 'w', newline='', encoding='utf-8')
    writer_max = csv.writer(max_fusion_file)


    for rows in zip(*readers):       
        file_name = rows[0][0]
        sum_val1 = 0.0
        sum_val2 = 0.0

        min_val1 = float(rows[0][1])
        min_val2 = float(rows[0][2])

        max_val1 = min_val1
        max_val2 = min_val2


        for r in rows:
            if r[0] != file_name:
                print(f"Error: Row name mismatch: {r[0]} != {file_name}")
            
            r_1 = float(r[1])
            r_2 = float(r[2])
            sum_val1 += float(r[1])
            sum_val2 += float(r[2])

            if min_val1 > r_1:
                min_val1 = r_1
            if min_val2 > r_2:
                min_val2 = r_2

            if max_val1 < r_1:
                max_val1 = r_1
            if max_val2 < r_2:
                max_val2 = r_2

        writer_sum.writerow([file_name, sum_val1, sum_val2])
        writer_min.writerow([file_name, min_val1, min_val2])
        writer_max.writerow([file_name, max_val1, max_val2])

for watermark, watermark_name in zip(config.watermarks, config.watermark_names):
    distibution =  calc_correlations.calc_distibution(watermark, watermark_name, config.level, None, "evaluation")
    full_file_name = get_full_results_file_name(watermark_name, config.level)

    full_file = open(full_file_name, "w")

    for filter_name, filter_params in config.filters.items():
        #calc_correlations.convert_to_zscore(watermark, watermark_name, config.level, filter_name, "test", distibution)
        
        file_filter = open(calc_correlations.get_results_file_name(watermark_name, config.level, filter_name, "test"), "r")
        for line in file_filter:
            full_file.write(line)

    full_file.close()

for length in range(2, len(config.watermark_names) + 1):
    for combo in combinations(range(len(config.watermark_names)), length): 
        selected_names = [config.watermark_names[i] for i in combo]
        combine_results(selected_names, config.level)
