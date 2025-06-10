import pandas as pd

tds_df = pd.read_csv("cleaned_tds_content.csv")
print("TDS CSV columns:", tds_df.columns.tolist())

disc_df = pd.read_csv("cleaned_discourse_posts.csv")
print("Discourse CSV columns:", disc_df.columns.tolist())
