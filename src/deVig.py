import pandas as pd

df_2026 = pd.read_csv('data/raw/oscars_nominees.csv', encoding='utf-8-sig', skipinitialspace=True)

df_2026.columns = df_2026.columns.str.strip()

print("Columns found:", df_2026.columns.tolist())
df_cols = df_2026.select_dtypes(['object'])
df_2026[df_cols.columns] = df_cols.apply(lambda x: x.str.strip())

df_2026['Implied_Prob'] = 1 / df_2026['Odds']

category_totals = df_2026.groupby('Category')['Implied_Prob'].transform('sum')

df_2026['True_Prob'] = df_2026['Implied_Prob'] / category_totals

print("\nSum of probabilities per category (Should be 1.0):")
print(df_2026.groupby('Category')['True_Prob'].sum())

print("\nTop 5 rows:")
print(df_2026.head())
df_2026.to_csv('/Users/timot/Documents/oscars-prediction/data/processed/oscars.csv', index=False)
