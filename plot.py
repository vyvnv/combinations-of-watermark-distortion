import sys
import csv
import numpy as np
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt



if len(sys.argv) != 6:
    print("`zscores_non_sharped.csv`, `zscores_sharped.csv`, `zscores_min.csv` `zscores_max.csv` `zscores_sum.csv` arguments expected")
    exit(1)

positive = []
negative = []
positiveSharped = []
negativeSharped = []
positiveMin = []
negativeMin = []
positiveMax = []
negativeMax = []
positiveSum = []
negativeSum = []

with open(sys.argv[1]) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        positive.append(float(row[1]))
        negative.append(float(row[2]))

with open(sys.argv[2]) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        positiveSharped.append(float(row[1]))
        negativeSharped.append(float(row[2]))

with open(sys.argv[3]) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        positiveMin.append(float(row[1]))
        negativeMin.append(float(row[2]))

with open(sys.argv[4]) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        positiveMax.append(float(row[1]))
        negativeMax.append(float(row[2]))

with open(sys.argv[5]) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        positiveSum.append(float(row[1]))
        negativeSum.append(float(row[2]))

y_true = np.concatenate([np.ones_like(positive), np.zeros_like(negative)])
y_scores = np.concatenate([positive, negative])
fpr, tpr, thresholds = roc_curve(y_true, y_scores)

y_true_sharped = np.concatenate([np.ones_like(positiveSharped), np.zeros_like(negativeSharped)])
y_scores_sharped = np.concatenate([positiveSharped, negativeSharped])
fpr_sharped, tpr_sharped, thresholds_filtered = roc_curve(y_true_sharped, y_scores_sharped)

y_true_min = np.concatenate([np.ones_like(positiveMin), np.zeros_like(negativeMin)])
y_scores_min = np.concatenate([positiveMin, negativeMin])
fpr_min, tpr_min, thresholds_min = roc_curve(y_true_min, y_scores_min)

y_true_max = np.concatenate([np.ones_like(positiveMax), np.zeros_like(negativeMax)])
y_scores_max = np.concatenate([positiveMax, negativeMax])
fpr_max, tpr_max, thresholds_max = roc_curve(y_true_max, y_scores_max)

y_true_sum = np.concatenate([np.ones_like(positiveSum), np.zeros_like(negativeSum)])
y_scores_sum = np.concatenate([positiveSum, negativeSum])
fpr_sum, tpr_sum, thresholds_sum = roc_curve(y_true_sum, y_scores_sum)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Latin Modern Roman", "CMU Serif", "Computer Modern Roman", "DejaVu Serif"],
    "mathtext.fontset": "cm",
    "axes.unicode_minus": False,
})

# === Plot ROC Curve ===
plt.figure()
plt.plot(fpr, tpr, label=f'без увеличения резкости', color='#7f7f7f', linestyle=(5, (10, 3)))
plt.plot(fpr_sharped, tpr_sharped, label=f'с увеличением резкости', color='#d62728', linestyle='--')
plt.plot(fpr_min, tpr_min, label=f'наименьшее', color='#2ca02c', linestyle='-.')
plt.plot(fpr_max, tpr_max, label=f'наибольшее', color='#9467bd', linestyle=':')
plt.plot(fpr_sum, tpr_sum, label=f'сумма', color='#1f77b4', linestyle='-')

plt.xlabel('Вероятность ложного обнаружения')
plt.ylabel('Вероятность успешного обнаружения')

#plt.plot(fpr, tpr, label=f'without pre-filtering', color='#7f7f7f', linestyle=(5, (10, 3)))
#plt.plot(fpr_sharped, tpr_sharped, label=f'with pre-filtering', color='#d62728', linestyle='--')
#plt.plot(fpr_min, tpr_min, label=f'min', color='#2ca02c', linestyle='-.')
#plt.plot(fpr_max, tpr_max, label=f'max', color='#9467bd', linestyle=':')
#plt.plot(fpr_sum, tpr_sum, label=f'sum', color='#1f77b4', linestyle='-')

#plt.xlabel('FP probability')
#plt.ylabel('TP probability')

plt.legend(loc='lower right')
plt.grid(True)

plt.xlim([0.0, 0.6])   # zoom in on very low FPR range
plt.ylim([0.8, 1.0])  # zoom in on high TPR range

plt.show()
