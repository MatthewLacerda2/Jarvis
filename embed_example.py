import ollama
import numpy as np
from sklearn.cluster import KMeans

# Sample customer reviews
reviews = [
    "The product exceeded my expectations. Great quality!",
    "Terrible customer service. I'm very disappointed.",
    "It's okay, nothing special but does the job.",
    "Absolutely love this! Best purchase I've made all year.",
    "Faulty product. Had to return it immediately."
]

# Generate embeddings for reviews
embeddings = []
for review in reviews:
    response = ollama.embeddings(model="nomic-embed-text", prompt=review)
    embeddings.append(response["embedding"])
    print(f"Embedding for review {review}: {response['embedding']}")
print("- - - - -")
# Perform K-means clustering to group similar sentiments
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(embeddings)

# Map clusters to sentiments
sentiment_map = {
    0: "positive",
    1: "negative",
    2: "neutral"
}

# Assign sentiments to reviews
sentiments = [sentiment_map[cluster] for cluster in clusters]

# Prepare a summary for Llama 3.1
summary = "Customer Review Sentiments:\n"
for review, sentiment in zip(reviews, sentiments):
    summary += f"- Review: '{review}'\n  Sentiment: {sentiment}\n"
    print(summary)
print("- - - - -")
# Generate an analysis using Llama 3.1
prompt = f"""Analyze the following customer review sentiments and provide a brief summary:

{summary}

Please include:
1. The overall sentiment distribution
2. Any patterns or trends you notice
3. Recommendations for the business based on these reviews
"""

response = ollama.generate(model="llama3.1", prompt=prompt)
print("- - - - -")
print("Llama 3.1 Analysis:")
print("- - - - -")
print(response['response'])
print("- - - - -")