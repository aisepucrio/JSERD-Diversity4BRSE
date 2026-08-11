import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os

# Create output directory if it doesn't exist
output_dir = '../../results/RQ6'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df = pd.read_csv("../../data/discrimination_cloud.csv")

text = " ".join(df.iloc[:, 1].dropna().astype(str))

stopwords = set(STOPWORDS)
stopwords.update([
    "a", "an", "and", "the", "to", "of", "in", "for", "on", "with",
    "is", "it", "this", "that", "we", "i", "you", "they",
    "github", "code", "project", "use", "using", "without", "someone",
    "based", "people", "person", "etc", "act","action"
])

wc = WordCloud(
    width=1200,
    height=900,
    background_color="white",
    stopwords=stopwords
).generate(text)

plt.imshow(wc)
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig(f'{output_dir}/discriminationcloud.png', dpi=300, bbox_inches='tight')
plt.show()