import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# correlation
def plot_correlation(df):
    sns.heatmap(df.corr(), annot=True)

# visualize
# sns.FacetGrid(pd.concat([pd.DataFrame(X_train), pd.Series(y_train, name='target')], axis=1), hue='target').map(plt.scatter, 0, 1).add_legend()
# sns.FacetGrid(pd.concat([pd.DataFrame(X_train), pd.Series(km.labels_, name='labels')], axis=1), hue='labels').map(plt.scatter, 0, 1).add_legend()

# variable distribution
def plot_variable_distribution(df):
    dim = int(np.ceil(df.shape[1]**0.5))
    fig, ax = plt.subplots(dim, dim)
    for i, col in enumerate(df.columns):
        sns.distplot(df[col].fillna(df[col].median()), ax=ax[i//dim][i%dim])

# plot PCA explained_variance_ratio_ for all variables
def plotPCA(X):
    pca = PCA(n_components=X.shape[1])
    pca.fit(X)
    plt.plot(pca.explained_variance_ratio_)
    plt.show()