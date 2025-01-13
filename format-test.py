import pandas as pd
import numpy as np
from novem import Plot

def construct_random_matrix(seed):
    # Create base data
    np.random.seed(seed)  # for reproducibility
    rows = 12
    cols = [x for x in range(7)]

    # Generate random numbers
    df = pd.DataFrame(np.random.randint(1, 101, size=(rows, len(cols))), columns=cols)

    # Define column weights for NA distribution
    column_weights = {
        0: 0.05,  # very few NAs
        1: 0.25,  # more NAs
        2: 0.05,
        3: 0.30,  # most NAs
        4: 0.15,
        5: 0.10,
        6: 0.10,
    }

    # Calculate number of NAs (10% of total cells)
    total_nas = int(rows * len(cols) * 0.1)

    # Create weighted position selection
    all_positions = [(col, row) for col in cols for row in range(rows)]
    weights = [column_weights[col] for col, _ in all_positions]

    # Randomly select positions for NAs based on weights
    na_positions = np.random.choice(
        len(all_positions), size=total_nas, replace=False, p=np.array(weights) / sum(weights)
    )

    # Insert NAs
    for idx in na_positions:
        col, row = all_positions[idx]
        df.loc[row, col] = np.nan

    return df


df = construct_random_matrix(44)

# make pct
df /= 1000

plt = Plot('sen-test', type='mtable')
plt.data = df

plt.name = "Cell format experiment"
plt.shared = 'public'
plt.cell.padding = ': : x 2'

# this works
plt.cell.format = """0 : .0f
1: 1: .1%
"""

# this works
plt.cell.format = """1: 1: .1%
0 : .0f
"""

# this works
plt.cell.format =  "0 : .0f"
plt.cell.format += "1: 1: .1%"

# this works
plt.cell.format = "1: 1: .1%"
plt.cell.format +=  "0 : .0f"

print(plt.url)
