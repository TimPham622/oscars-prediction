import pandas as pd
df = pd.read_csv('data/raw/the_oscar_award.csv')

df = df[df['winner'].astype(str) == 'True']
category_map = {
    'BEST PICTURE': 'Picture',
    'OUTSTANDING PRODUCTION': 'Picture',
    'OUTSTANDING PICTURE': 'Picture',
    'OUTSTANDING MOTION PICTURE': 'Picture',
    
    'DIRECTING': 'Director',
    'DIRECTING (Comedy Picture)': 'Director',
    'DIRECTING (Dramatic Picture)': 'Director',
    
    'ACTOR': 'Actor',
    'ACTOR IN A LEADING ROLE': 'Actor',
    
    'ACTRESS': 'Actress',
    'ACTRESS IN A LEADING ROLE': 'Actress',
    
    'ACTOR IN A SUPPORTING ROLE': 'SuppActor',
    'ACTRESS IN A SUPPORTING ROLE': 'SuppActress'
}
df['Category'] = df['category'].str.upper().str.strip().map(category_map)

df = df.dropna(subset=['Category'])

result = df[['year_ceremony', 'Category', 'film']].copy()
result.columns = ['Year', 'Category', 'Film']

custom_order = ['Picture', 'Director', 'Actor', 'Actress', 'SuppActor', 'SuppActress']
result['cat_rank'] = result['Category'].apply(lambda x: custom_order.index(x))

result = result.sort_values(by=['Year', 'cat_rank'], ascending=[False, True])

result = result.drop(columns=['cat_rank'])

print(result.head(10))

result.to_csv('/Users/timot/Documents/oscars-prediction/data/processed/cleaned_oscars.csv', index=False)

