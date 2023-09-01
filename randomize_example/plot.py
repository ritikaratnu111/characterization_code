import matplotlib.pyplot as plt
import numpy as np

def bar_graph():
    xaxis_testcases = ["Matrix Mult 16x16", "SOM"]
    yaxis_accuracy_of_model = [92.8, 92.5]
    ground_truth = [100, 100]
    legend = ["Ground Truth", "Accuracy of model"]
    plt.figure(figsize=(10,10))
    plt.bar(xaxis_testcases, yaxis_accuracy_of_model, color = "blue")
    plt.bar(xaxis_testcases, ground_truth, color = "green")
    plt.legend(legend, loc = "upper right")
    plt.title("Energy estimation accuracy of model on DRRA and DiMArch fabric")
    plt.xlabel("Testcases")
    plt.ylabel("Accuracy in percentage")
    plt.xticks(rotation = 45)
    plt.yticks(np.arange(0, 120, 20))
    plt.savefig("bar_graph.png")
    plt.show()
