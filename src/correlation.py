import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df_hist = pd.read_csv('data/processed/cleaned_oscars.csv')
df_wide = df_hist.pivot(index='Year', columns='Category', values='Film')

categories = ['Picture', 'Director', 'Actor', 'Actress', 'SuppActor', 'SuppActress']
df_wide = df_wide[categories]

n_cats = len(categories)
corr_matrix = np.zeros((n_cats, n_cats))

for i in range(n_cats):
    for j in range(n_cats):
        cat1 = categories[i]
        cat2 = categories[j]
        
        matches = (df_wide[cat1] == df_wide[cat2]).astype(int)
        
        corr_matrix[i, j] = matches.mean()

df_corr = pd.DataFrame(corr_matrix, index=categories, columns=categories)

plt.figure(figsize=(8, 6))
sns.heatmap(df_corr, annot=True, cmap='coolwarm', vmin=0, vmax=1)
plt.title("Historical Co-occurrence Matrix (1995-2025)")
plt.show()

df_corr.to_csv('data/processed/correlation_matrix.csv')