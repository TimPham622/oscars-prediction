from scipy.stats import norm
import pandas as pd
import numpy as np

df_corr = pd.read_csv('/Users/timot/Documents/oscars-prediction/data/processed/correlation_matrix.csv', index_col=0)
df_2026 = pd.read_csv('/Users/timot/Documents/oscars-prediction/data/processed/oscars.csv')

n_sims = 10000
films = df_2026['Film'].unique()
categories = ['Picture', 'Director', 'Actor', 'Actress', 'SuppActor', 'SuppActress']

sim_results = {film: {cat: 0 for cat in categories} for film in films}

min_eig = np.min(np.linalg.eigvals(df_corr))
if min_eig < 0:
    df_corr -= 10*min_eig * np.eye(*df_corr.shape)

L = np.linalg.cholesky(df_corr.values)


for s in range(n_sims):
    
    film_scores = {}
    
    for film in films:
        uncorrelated = np.random.normal(0, 1, 6)
        correlated = np.dot(L, uncorrelated)
        
        film_scores[film] = dict(zip(categories, correlated))

    for cat in categories:
        nominees = df_2026[df_2026['Category'] == cat]
        
        best_score = -np.inf
        winner = None
        
        for _, row in nominees.iterrows():
            film = row['Film']
            prob = row['True_Prob']
            
            base_strength = norm.ppf(prob) 
            noise = film_scores[film][cat]
            
            final_score = base_strength + noise
            
            if final_score > best_score:
                best_score = final_score
                winner = film
        
        if winner:
            sim_results[winner][cat] += 1

results_df = pd.DataFrame.from_dict(sim_results, orient='index')
results_df = results_df / n_sims 

results_df = results_df[(results_df.T != 0).any()]
print(results_df.sort_values('Picture', ascending=False).head(10))
results_df.to_csv('/Users/timot/Documents/oscars-prediction/data/processed/results.csv', index=False)