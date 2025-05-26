import pandas as pd
from textblob import TextBlob
import os

# Load data
df = pd.read_csv("/Users/casey/Documents/GitHub/NLP sentiment/part_10.csv")

# Define AI and workplace-related terms
ai_terms = ["AI", "artificial intelligence", "machine learning", "automation", "algorithms"]
job_terms = ["job loss", "job displacement", "productivity", "upskilling", "reskilling", "employment", "layoff", "hiring", "labor"]

# Function to analyze sentiment of a text
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity

    # Overall sentiment
    if sentiment_score > 0.1:
        overall_sentiment = "Positive"
    elif sentiment_score < -0.1:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"

    # Workplace sentiment
    lower_text = text.lower()
    ai_near_job = any(ai in lower_text and job in lower_text for ai in ai_terms for job in job_terms)

    if "job loss" in lower_text or "layoff" in lower_text:
        workplace_sentiment = "Negative"
    elif "upskilling" in lower_text or "reskilling" in lower_text or "productivity" in lower_text:
        workplace_sentiment = "Positive"
    else:
        workplace_sentiment = "Neutral"

    # Extract evidence sentences
    sentences = text.split(".")
    evidence = [s.strip() for s in sentences if any(term in s.lower() for term in ai_terms + job_terms)]
    evidence = evidence[:2]  # Max 2

    return {
        "overall_sentiment": overall_sentiment,
        "workplace_sentiment": workplace_sentiment,
        "evidence": evidence,
        "contextual_notes": f"AI terms and job impact terms {'appear close together' if ai_near_job else 'do not co-occur significantly'}."
    }

# Batch processing
batch_size = 20000
total_rows = len(df)

output_folder = "sentiment_batches"
os.makedirs(output_folder, exist_ok=True)

for start in range(0, total_rows, batch_size):
    print(f"Processing rows {start} to {start+batch_size}...")
    batch = df.iloc[start:start+batch_size].copy()

    batch["sentiment_analysis"] = batch["trafilatura_text"].apply(analyze_sentiment)
    batch["overall_sentiment"] = batch["sentiment_analysis"].apply(lambda x: x["overall_sentiment"])
    batch["workplace_sentiment"] = batch["sentiment_analysis"].apply(lambda x: x["workplace_sentiment"])
    batch["evidence"] = batch["sentiment_analysis"].apply(lambda x: x["evidence"])
    batch["contextual_notes"] = batch["sentiment_analysis"].apply(lambda x: x["contextual_notes"])
    batch.drop(columns=["sentiment_analysis"], inplace=True)

    batch.to_csv(f"{output_folder}/sentiment_analysis_batch_10.csv", index=False)

print("All batches processed and saved.")
