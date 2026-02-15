import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

results_df = pd.read_csv('/Users/timot/Documents/oscars-prediction/data/processed/results.csv')
plt.figure(figsize=(10, 8))
sns.heatmap(results_df, annot=True, fmt=".1%", cmap="Greens")
plt.title("Monte Carlo Simulation Results: Win Probability per Category")
plt.ylabel("Film")
plt.xlabel("Category")
plt.show()
