import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats


def plot_frequency(freq_df, path):
    plt.figure()
    sns.lineplot(data=freq_df, x="hour", y="journeys")
    plt.title("Hourly Frequency")
    plt.savefig(path)
    plt.close()


def plot_normal_distribution(freq_df, path):
    data = freq_df["journeys"]

    mean = data.mean()
    std = data.std()

    x = np.linspace(mean - 3*std, mean + 3*std, 100)
    y = stats.norm.pdf(x, mean, std)

    plt.figure()
    plt.hist(data, bins=10, density=True)
    plt.plot(x, y)

    plt.title("Normal Distribution")
    plt.savefig(path)
    plt.close()


def plot_clusters(freq_df, path):
    plt.figure()
    sns.scatterplot(data=freq_df, x="hour", y="journeys", hue="cluster")
    plt.title("Clustered Demand")
    plt.savefig(path)
    plt.close()