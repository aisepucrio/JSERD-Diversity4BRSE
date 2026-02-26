import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import os

# Create output directory if it doesn't exist
output_dir = '../../results/RQ5'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the CSV file
file_path = "../../data/coding_inclusion_diversity.csv"
df = pd.read_csv(file_path)

t_col = df.iloc[:, 2].dropna()
c_col = df.iloc[:, 3].dropna()

def count_tags(series):
    tags = []
    for cell in series:
        for tag in str(cell).split(","):
            tags.append(tag.strip())
    return pd.Series(tags).value_counts()

# Count categories
t_counts = count_tags(t_col)
c_counts = count_tags(c_col)

# Combine counts
all_counts = pd.concat([t_counts, c_counts]).sort_index()

# Mapping dictionary
label_map = {
    "T1": "Defines diversity only",
    "T2": "Defines inclusion only",
    "T3": "Defines diversity and inclusion separately",
    "T4": "Defines diversity and inclusion complementarly",
    "T5": "Generic or vague definition",
    "T6": "Blank/Out of context",
    "C1": "Demographic representation",
    "C2": "Cognitive or experiential diversity",
    "C3": "Equal opportunity / equity",
    "C4": "Belonging and respect",
    "C5": "Participation and voice",
    "C6": "Organizational practices or policies",
    "C7": "Justice or anti-discrimination framing",
    "C8": "Meritocracy / skills-first framing",
    "C9": "Instrumental or business outcomes",
    "C10": "Hate Comments"
}

# Map codes to descriptions
all_counts.index = all_counts.index.map(lambda x: label_map.get(x, x))

# Colours: T = blue, C = red
colors = [
    "tab:blue" if any(label_map[code].startswith(label_map[code][0]) for code in label_map if label_map[code] == category and code.startswith("T"))
    else "tab:red"
    for category in all_counts.index
]
# Plot
plt.figure(figsize=(12, 6))
bars = plt.barh(all_counts.index, all_counts.values, color=colors)


# Add values at the end of each bar
for bar in bars:
    width = bar.get_width()
    plt.text(
        width,
        bar.get_y() + bar.get_height() / 2,
        f"{int(width)}",
        va="center",
        ha="left",
        fontsize=12
    )

# Legend
legend_elements = [
    Patch(facecolor="tab:blue", label="Type of Definition (T)"),
    Patch(facecolor="tab:red", label="Content of Definition (C)")
]
plt.legend(handles=legend_elements, fontsize='large', loc='upper right')
plt.tick_params(axis='x', labelsize=14)
plt.tick_params(axis='y', labelsize=14)
plt.tight_layout()
plt.savefig(f'{output_dir}/coding_inclusion_diversity.png', dpi=300, bbox_inches='tight')
plt.show()