# oscars-prediction

hi! this is my little oscars prediction project.

i made this to mash together betting odds + old oscar results and see what movies are most likely to win in each main category. it is not a production thing, just a data project that works with csv files and some python scripts.

---

## what this project does (in plain english)

- takes historical oscar winner data
- cleans it to only the categories i care about
- builds a "correlation" matrix for how often categories line up to same film
- takes current odds and turns them into normalized probabilities
- runs monte carlo simulation (10,000 runs)
- outputs a table of win probabilities by film/category
- can draw heatmaps so it's easier to look at

---

## stack / dependencies

python with:

- pandas
- numpy
- matplotlib
- seaborn
- scipy (used in algorithm)

`requirements.txt` has most of these, but if scipy is missing for your environment, install it manually.

example:

```bash
pip install -r requirements.txt
pip install scipy
```

---

## project layout

```text
oscars-prediction/
├── data/
│   ├── raw/
│   │   ├── the_oscar_award.csv
│   │   ├── oscars_nominees.csv
│   │   └── predictions.csv
│   └── processed/
│       ├── cleaned_oscars.csv
│       ├── correlation_matrix.csv
│       ├── oscars.csv
│       └── results.csv
├── src/
│   ├── cleaning.py
│   ├── correlation.py
│   ├── deVig.py
│   ├── algorithm.py
│   └── visualise.py
├── requirements.txt
└── README.md
```

---

## expected input files

### 1) historical data
`data/raw/the_oscar_award.csv`

used by `cleaning.py`.

### 2) current nominees + odds
`data/raw/oscars_nominees.csv`

expected columns:

- `Category`
- `Nominee`
- `Film`
- `Odds`

---

## how to run (important: run in this order)

from project root:

```bash
python src/cleaning.py
python src/correlation.py
python src/deVig.py
python src/algorithm.py
python src/visualise.py
```

### what each script writes

1. `cleaning.py` -> `data/processed/cleaned_oscars.csv`
2. `correlation.py` -> `data/processed/correlation_matrix.csv` (+ heatmap popup)
3. `deVig.py` -> `data/processed/oscars.csv`
4. `algorithm.py` -> `data/processed/results.csv`
5. `visualise.py` -> just visual output from `results.csv`

---

## script notes

### `src/cleaning.py`
- filters to winners only
- maps historical category names to:
  - Picture
  - Director
  - Actor
  - Actress
  - SuppActor
  - SuppActress

### `src/correlation.py`
- pivots historical winners by year
- computes match rate between categories (`same film won both`)
- stores matrix values 0 to 1

### `src/deVig.py`
- converts decimal odds to implied probability (`1/odds`)
- normalizes inside each category so probs sum to 1
- outputs `True_Prob`

### `src/algorithm.py`
- reads de-vigged probs + correlation matrix
- generates correlated noise using cholesky decomposition
- combines market strength + noise score
- picks a winner for each category each simulation
- tallies win rate

### `src/visualise.py`
- heatmap of final results table

---

## known rough edges (yeah there are a few)

- some scripts still use absolute paths from my machine (`/Users/timot/...`), so you may need to switch them to relative paths.
- scripts are not packaged as functions/cli yet, just run top-to-bottom.
- `results.csv` is saved without explicit film name column (row index issue), so keep that in mind when reading it.
- no automated tests yet.

---

## troubleshooting

### matplotlib window does not show
if you're on headless server, plots might not pop up. either:
- skip plotting scripts
- or switch matplotlib backend/save figures instead of `plt.show()`

### module not found
install deps manually:

```bash
pip install pandas numpy matplotlib seaborn scipy
```

### file path errors
make sure you are running commands from repository root and check absolute paths in script files.

---

## ideas for next improvements

- convert absolute paths to relative `pathlib` paths
- refactor scripts into reusable functions
- add one runner script (or makefile)
- add tests for data shape and probability sums
- save chart images to files automatically
- improve docstrings/comments in source

---

## disclaimer

this is a fun forecasting project and not financial advice etc. odds move, nominations change, model assumptions are simplistic, and randomness is involved.

