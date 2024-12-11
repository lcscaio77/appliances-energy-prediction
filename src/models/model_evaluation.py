import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import label_binarize
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    auc,
    log_loss,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

def evaluate_model(model, X_test, y_test, classes=None, per_class=True, plot_roc_curve=True, plot_conf_mat=True):
    if classes is None:
        classes = model.classes_
    
    n_classes = len(classes)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    logloss = log_loss(y_test, y_prob)
    precision = precision_score(y_test, y_pred, average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    f1 = f1_score(y_test, y_pred, average='macro')
    roc_auc = roc_auc_score(y_test, y_prob, average='macro', multi_class='ovr')

    print('-'*100 + '\n')

    print(f'Global accuracy : {accuracy}')
    print(f'Global log loss : {logloss}')
    print(f'Global precision : {precision}')
    print(f'Global recall : {recall}')
    print(f'Global F1 score : {f1}')
    print(f'Global ROC-AUC score : {roc_auc}')

    if per_class:
        precision = precision_score(y_test, y_pred, average=None)
        recall = recall_score(y_test, y_pred, average=None)
        f1 = f1_score(y_test, y_pred, average=None)
        roc_auc = roc_auc_score(y_test, y_prob, average=None, multi_class='ovr')

        scores_data = {
            'Precision': precision,
            'Recall' : recall,
            'F1 score' : f1
        }
        if isinstance(classes, dict):
            scores_per_class = pd.DataFrame(scores_data, index=list(classes.values()))
        else:
            scores_per_class = pd.DataFrame(scores_data, index=classes)

        print('\n', scores_per_class)
        
    print('\n' + '-'*100)

    if plot_roc_curve:
        fpr = {}; tpr = {}; roc_auc = {}
        y_test_binarized = label_binarize(y_test, classes=np.arange(n_classes))

        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_test_binarized[:, i], y_prob[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])

        plt.figure(figsize=(8, 6))

        colors = plt.cm.tab20(np.linspace(0, 1, n_classes))
        for i in range(n_classes):
            plt.plot(fpr[i], tpr[i], color=colors[i], lw=2, label=f'{classes[i]} (AUC = {roc_auc[i]:.2f})')

        plt.plot([0, 1], [0, 1], color='gray', linestyle='--')

        plt.title('Courbes ROC Multiclasse (One-vs-Rest)')
        plt.xlabel('Taux de Faux Positifs (FPR)')
        plt.ylabel('Taux de Vrais Positifs (TPR)')
        plt.legend(loc='lower right')
        plt.show()
        
        print('-'*100)
        
    if plot_conf_mat:
        cm = confusion_matrix(y_test, y_pred)

        _, ax = plt.subplots(figsize=(8, 6))
        if isinstance(classes, dict):
            disp_cm = ConfusionMatrixDisplay(cm, display_labels=classes.values())
        else:
            disp_cm = ConfusionMatrixDisplay(cm, display_labels=classes)
        disp_cm.plot(cmap='Blues', ax=ax)
        plt.xticks(rotation=90)
        plt.title('Matrice de confusion')
        plt.show()

        print('-'*100)
