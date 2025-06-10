import json
import pandas as pd
import re
from bs4 import BeautifulSoup


with open("discourse_posts.json", "r") as f:
    data = json.load(f)


df = pd.DataFrame(data)


df["content"] = df["cooked"].apply(lambda x: BeautifulSoup(x, "html.parser").get_text())


df["created_at"] = pd.to_datetime(df["created_at"])
df["updated_at"] = pd.to_datetime(df["updated_at"])


df = df[df["content"].str.strip().astype(bool)]
df = df[df["content"].str.len() > 10]


df.drop_duplicates(subset=["id"], inplace=True)


def clean_text(text):
    text = re.sub(r"http\S+", "", text)           
    text = re.sub(r"[^a-zA-Z\s]", "", text)       
    text = re.sub(r"\s+", " ", text)             
    return text.lower().strip()

df["cleaned_content"] = df["content"].apply(clean_text)


df.to_csv("cleaned_discourse_posts.csv", index=False)