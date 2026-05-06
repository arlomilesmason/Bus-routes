from sklearn.cluster import KMeans


def cluster_time_of_day(freq_df):
    model = KMeans(n_clusters=3, random_state=42)

    freq_df["cluster"] = model.fit_predict(freq_df[["journeys"]])

    return freq_df, model.cluster_centers_
