import sys
import csv
import numpy as np
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt


if len(sys.argv) != 5:
    print("arguments expected correlations_no_filter.csv correlations_blur.csv psnr_no_filter.csv psnr_blur.csv")
    exit(1)

positive = []
negative = []
positiveFiltered = []
negativeFiltered = []

psnr = []
psnrFiltered = []

files = []
filesFiltered = []
psnrFiles = []
psnrFilesFiltered = []


with open(sys.argv[1]) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        files.append(row[0])
        positive.append(float(row[1]))
        negative.append(float(row[2]))

with open(sys.argv[2]) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        filesFiltered.append(row[0])
        positiveFiltered.append(float(row[1]))
        negativeFiltered.append(float(row[2]))

with open(sys.argv[3]) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        psnrFiles.append(row[0])
        psnr.append(float(row[1]))


with open(sys.argv[4]) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        psnrFilesFiltered.append(row[0])
        psnrFiltered.append(float(row[1]))


# Проверка данных

if len(files) != len(set(files)) or len(filesFiltered) != len(set(filesFiltered)):
    raise ValueError("повторяющиеся изображения")

if set(files) != set(filesFiltered) or set(files) != set(psnrFiles) or set(files) != set(psnrFilesFiltered):
    raise ValueError("изображения в CSV не совпадают")

if not np.all(np.isfinite(positive + negative + positiveFiltered + negativeFiltered + psnr + psnrFiltered)):
    raise ValueError("обнаружены некорректные числовые значения")


# ROC без фильтрации
y_true = np.concatenate([np.ones_like(positive), np.zeros_like(negative)])
y_scores = np.concatenate([positive, negative])
fpr, tpr, thresholds = roc_curve(y_true, y_scores)
auc_no_filter = auc(fpr, tpr)

# ROC после фильтрации
y_true_filtered = np.concatenate([np.ones_like(positiveFiltered), np.zeros_like(negativeFiltered)])
y_scores_filtered = np.concatenate([positiveFiltered, negativeFiltered])
fpr_filtered, tpr_filtered, thresholds_filtered = roc_curve(y_true_filtered, y_scores_filtered)
auc_filtered = auc(fpr_filtered, tpr_filtered)


# Средний PSNR
mean_psnr = np.mean(psnr)
mean_psnr_filtered = np.mean(psnrFiltered)


# Вывод результатов
print("Без фильтрации:")
print("Средний PSNR:", mean_psnr)
print("AUC:", auc_no_filter)

print("После фильтрации:")
print("Средний PSNR:", mean_psnr_filtered)
print("AUC:", auc_filtered)


with open("experiment_results.csv", "w", newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Фильтр", "Средний PSNR", "AUC"])
    writer.writerow(["Без фильтрации", mean_psnr, auc_no_filter])
    writer.writerow(["unsharp=3:3:-0.25:3:3:-0.25", mean_psnr_filtered, auc_filtered])


plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Latin Modern Roman", "CMU Serif", "Computer Modern Roman", "DejaVu Serif"],
    "mathtext.fontset": "cm",
    "axes.unicode_minus": False,
})

# === Plot ROC Curve ===
plt.figure()

plt.plot(fpr, tpr, label=f'без фильтрации (AUC = {auc_no_filter:.4f})', color='#7f7f7f', linestyle='--')
plt.plot(fpr_filtered, tpr_filtered, label=f'после фильтрации (AUC = {auc_filtered:.4f})', color='#d62728', linestyle='-')

plt.xlabel('Вероятность ложного обнаружения')
plt.ylabel('Вероятность успешного обнаружения')

plt.legend(loc='lower right')
plt.grid(True)

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])

plt.savefig("roc_comparison.png", dpi=300, bbox_inches='tight')
plt.show()
