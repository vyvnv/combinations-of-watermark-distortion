import csv
from pathlib import Path

from sklearn.metrics import roc_auc_score

import config
import embed_watermarks
import filter_watermarks
import calc_correlations
from itertools import combinations

def calculate_auc(correlations_csv):
    positive = []
    negative = []

    with open(correlations_csv, newline="", encoding="utf-8-sig") as csvfile:
        for _, embedded, not_embedded in csv.reader(csvfile):
            positive.append(float(embedded))
            negative.append(float(not_embedded))

    labels = [1] * len(positive) + [0] * len(negative)
    scores = positive + negative
    return roc_auc_score(labels, scores)


watermark = config.watermarks
watermark_name = config.watermark_name
level = config.level

embed_watermarks.embed_watermarks(watermark, level, "images")
embed_watermarks.create_references_wo_embedding(watermark, level, "images")

# Без фильтрации.
mean_psnr = embed_watermarks.mean_psnr(level)
calc_correlations.calc_correlations(
    watermark, watermark_name, level, None, "evaluation"
)
correlations_csv = calc_correlations.get_results_file_name(
    watermark_name, level, None, "evaluation"
)
results = [["Без фильтрации", mean_psnr, calculate_auc(correlations_csv)]]

prepared = set()

for first, second in combinations(config.filters, 2):
    combination = f"pair_stage1__{first}"
    pair_name = f"pair__{first}__{second}"

    if first not in prepared:
        filter_watermarks.filter_watermarks_multithread(level, combination, config.filters[first])
        prepared.add(first)

    filter_watermarks.filter_watermarks_multithread(level, pair_name, config.filters[second], source_folder=combination)
    mean_psnr = filter_watermarks.mean_psnr(pair_name, level)

    calc_correlations.calc_correlations(watermark, watermark_name, level, pair_name, "test")
    correlations_csv = calc_correlations.get_results_file_name(watermark_name, level, pair_name, "test")
    results.append([pair_name, mean_psnr, calculate_auc(correlations_csv)])

table_path = Path("correlation_tests") / str(level) / "experiment_results_pairs.csv"


with table_path.open("w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Фильтр", "Средний PSNR", "AUC"])
    writer.writerows(results)

print("Таблица сохранена:", table_path)