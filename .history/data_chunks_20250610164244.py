import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load cleaned datasets
tds_df = pd.read_csv("cleaned_tds_content.csv")
disc_df = pd.read_csv("cleaned_discourse_posts.csv")

# Prepare combined 'text' field for chunking
tds_df["text"] = tds_df["filename"].fillna("") + "\n" + tds_df["content"].fillna("")
disc_df["text"] = disc_df["topic_title"].fillna("") + "\n" + disc_df["cleaned_content"].fillna("")

# Combine all texts for chunking
combined_texts = pd.concat([tds_df[["text"]], disc_df[["text"]]], ignore_index=True)

# Initialize text splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

# Apply splitting
chunks = []
for row in combined_texts["text"]:
    splits = splitter.split_text(row)
    chunks.extend(splits)

# Convert to DataFrame and save
chunk_df = pd.DataFrame({"chunk": chunks})
chunk_df.to_csv("combined_chunks.csv", index=False)

print(f"✅ Chunking completed. Total chunks: {len(chunk_df)}")
