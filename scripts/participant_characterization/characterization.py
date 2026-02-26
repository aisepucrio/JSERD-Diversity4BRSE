import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

# Load data
df = pd.read_csv('../../data/participant-characterization.csv')

# Create folder to save charts
output_dir = '../../results/participant_characterization'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Columns to analyze (excluding ID)
columns_to_analyze = [col for col in df.columns if col != 'ID']

# Style settings
colors = ['#4285F4', '#EA4335', '#FBBC04', '#34A853', '#FF6D01', '#46BDC6', '#7BAAF7', '#F07B72']

# Generate bar charts for each column
for column in columns_to_analyze:
    # Count values and calculate percentages
    value_counts = df[column].value_counts()
    percentages = (value_counts / len(df)) * 100
    
    # Sort to put "Others/I don't know" last
    sorted_indices = []
    others_idx = []
    for idx, label in enumerate(value_counts.index):
        if 'Others' in str(label) or "don't know" in str(label):
            others_idx.append(idx)
        else:
            sorted_indices.append(idx)
    sorted_indices.extend(others_idx)
    
    value_counts = value_counts.iloc[sorted_indices]
    percentages = percentages.iloc[sorted_indices]
    
    # Dynamic figure width based on number of bars
    bar_width = 0.6  # Fixed bar width
    num_bars = len(value_counts)
    fig_width = max(8, num_bars * 1.2)  # At least 8, grows with bars
    
    # Create figure
    fig, ax = plt.subplots(figsize=(fig_width, 6))
    
    # Create vertical bar chart
    bars = ax.bar(
        range(num_bars),
        value_counts.values,
        color=colors[:num_bars],
        width=bar_width
    )
    
    # Configure axes
    ax.set_xticks([])  # Remove x-axis labels
    ax.set_ylabel('Number of Participants', fontsize=14)
    ax.set_ylim(0, 220)  # 200 + padding
    
    # Add values and percentages on bars
    for i, (bar, count, pct) in enumerate(zip(bars, value_counts.values, percentages)):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2, 
            height + 2,
            f'{count}\n({pct:.1f}%)',
            ha='center',
            va='bottom',
            fontsize=12,
            fontweight='bold'
        )
    
    # Create legend with color boxes
    legend_elements = [plt.Rectangle((0,0),1,1, fc=colors[i], edgecolor='black', linewidth=0.5) 
                       for i in range(num_bars)]
    ax.legend(legend_elements, value_counts.index, 
              loc='upper right', 
              fontsize=16,
              frameon=True,
              fancybox=True,
              shadow=True)
    
    # Grid for easier reading
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    
    # Save chart
    filename = f'{output_dir}/{column.replace("/", "-").replace(" ", "_").lower()}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    
    # Close figure to free memory
    plt.close()