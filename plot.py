import csv
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

import config


level = config.level
watermark_name = config.watermark_name
output_dir = Path("correlation_tests") / str(level)

with (output_dir / "experiment_results.csv").open(
    newline="", encoding="utf-8-sig"
) as csvfile:
    filters = [row["Фильтр"] for row in csv.DictReader(csvfile)]

if not filters or filters[0] != "Без фильтрации":
    raise ValueError("Первая строка результатов должна быть «Без фильтрации»")

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Latin Modern Roman", "CMU Serif", "DejaVu Serif"],
    "mathtext.fontset": "cm",
    "axes.unicode_minus": False,
})

plt.figure(figsize=(9, 6))

for filter_name in filters:
    no_filter = filter_name == "Без фильтрации"
    filename = f"correlations_{watermark_name}_{level}"
    if not no_filter:
        filename += f"_{filter_name}"

    correlations_csv = output_dir / watermark_name / f"{filename}.csv"

    files = []
    positive = []
    negative = []

    with correlations_csv.open(newline="", encoding="utf-8-sig") as csvfile:
        for filename, embedded, not_embedded in csv.reader(csvfile):
            files.append(filename)
            positive.append(float(embedded))
            negative.append(float(not_embedded))

    if not files:
        raise ValueError(f"Пустой CSV: {correlations_csv}")

    if len(files) != len(set(files)):
        raise ValueError(f"Повторяющиеся изображения: {correlations_csv}")

    if not np.all(np.isfinite(positive + negative)):
        raise ValueError(f"Некорректные корреляции: {correlations_csv}")

    if no_filter:
        baseline_files = set(files)
    elif set(files) != baseline_files:
        raise ValueError(f"Набор изображений отличается от базового: {correlations_csv}")

    y_true = [1] * len(positive) + [0] * len(negative)
    y_scores = positive + negative

    fpr, tpr, _ = roc_curve(y_true, y_scores, drop_intermediate=False)
    area = auc(fpr, tpr)
    tpr_at_1_percent = tpr[fpr <= 0.01].max()

    print(
        f"{filter_name}: AUC = {area:.6f}, "
    )

    label = f"{filter_name}"
    if no_filter:
        plt.plot(fpr, tpr, label=label, color="#7f7f7f", linestyle="--")
    else:
        plt.plot(fpr, tpr, label=label)

plt.xlabel("Вероятность ложного обнаружения")
plt.ylabel("Вероятность успешного обнаружения")
plt.xlim(0.0, 0.6)
plt.ylim(0.8, 1.0)
plt.legend(loc="lower right")
plt.grid(True)

graph_path = output_dir / "roc_comparison.png"
plt.savefig(graph_path, dpi=300, bbox_inches="tight")
print("График сохранён:", graph_path)
plt.show()