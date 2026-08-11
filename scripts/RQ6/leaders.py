import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import os

# Create output directory if it doesn't exist
output_dir = '../../results/RQ4'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the dataset
df = pd.read_csv('../../data/data_leadership.csv')

# Select Likert-scale columns
likert_cols = ['Race/Ethnicity', 'Gender/Sexuality', 'Neurodivergency', 'Disability', 'Elderly']

# Compute normalized counts for each Likert point
likert_counts = df[likert_cols].apply(lambda x: x.value_counts(normalize=True)).fillna(0)

# Ensure the index is ordered 1-4 and convert to percentages
likert_counts = likert_counts.reindex(index=[1, 2, 3, 4])
likert_perc = (likert_counts * 100).T  # transpose so rows are questions

# Split negative (1,2) and positive (3,4) responses
neg = -likert_perc[[1, 2]]
pos = likert_perc[[3, 4]]

# Plot
fig, ax = plt.subplots(figsize=(10,7))

colors = {
    1: "#d90000",  # strongly disagree (red)
    2: "#fc7e7e",  # disagree       (orange)
    3: "#a6d96a",  # agree          (light green)
    4: "#1a9641",  # strongly agree (dark green)
}

# Plot negative responses
offset = np.zeros(len(likert_cols))
for col in [2,1]:
    label = 'Strongly Disagree' if col == 1 else 'Disagree'
    ax.barh(
    likert_cols,
    neg[col],
    left=offset,
    height=0.6,
    label=label,
    color=colors[col])
    offset += neg[col].values

# Plot positive responses
offset = np.zeros(len(likert_cols))
for col in [3, 4]:
    label = 'Agree' if col == 3 else 'Strongly Agree'
    ax.barh(
    likert_cols,
    pos[col],
    left=offset,
    height=0.6,
    label=label,
    color=colors[col])
    offset += pos[col].values



# Add center line and labels
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('% of Respondents')
ax.set_title('Diverging Stacked-Bar Chart of Likert Responses')

legend_handles = [
    Patch(facecolor=colors[1], label='Strongly Disagree'),
    Patch(facecolor=colors[2], label='Disagree'),
    Patch(facecolor=colors[3], label='Agree'),
    Patch(facecolor=colors[4], label='Strongly Agree'),
]
ax.legend(
    handles=legend_handles,
    loc='upper center',
    bbox_to_anchor=(0.5, -0.1),
    ncol=4,
    fontsize=12
)

# after all your plotting, but before plt.tight_layout()/plt.show()
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.margins(x=0.01,y=0.05)
# Invert y-axis to have the first question at the top
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(f'{output_dir}/leadership_level.png', dpi=300, bbox_inches='tight')
plt.show()
