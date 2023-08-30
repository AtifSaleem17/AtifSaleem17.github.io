# importing libraries
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_score, f1_score, recall_score
import seaborn as sns

# function for model evaluations (confusion metrix, precision, recall, f1 etc)
def model_performance(img_predictions, label_test_set, model_name):
    # Print model name
    print("#############", model_name, "#############")
    # print validation accuraccy
    print("\nAccuracy on validation set: {:.3f}".format(accuracy_score(label_test_set, img_predictions)))
    # classification report
    class_report = classification_report(label_test_set, img_predictions)
    print("\nClassification report : \n", class_report)
    # confusion matrix
    conf_matrix = confusion_matrix(label_test_set, img_predictions)
    print("\nConfusion Matrix : \n", conf_matrix)
    # ploting confusion matrix after converting the values into heatmap
    plt.figure(figsize=(10, 10))
    sns.heatmap(conf_matrix, annot=True, fmt='g', cmap='viridis')
    # saving heatmap
    plt.savefig(model_name + "_CM.jpg")
    plt.tight_layout()
    plt.show()