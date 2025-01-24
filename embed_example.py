import ollama
import numpy as np
from typing import List, Dict
from sklearn.cluster import KMeans

# Sample customer reviews
reviews: List[str] = [
    "The product exceeded my expectations. Great quality!", #positive
    "Absolutely love this! Best purchase I've made all year.", #positive
    "Best product I've ever bought. I'm very happy with it.", #positive
    "My kids absolutely love it", #positive
    "I bought two, no regrets! Cheers!", #positive
    "It's okay, nothing special but does the job.", #neutral
    "It's ok for the price", #neutral
    "It will do the job.", #neutral
    "So far so good", #neutral
    "Terrible customer service. I'm very disappointed.", #negative
    "Faulty product. Had to return it immediately.", #negative
    "I'm very disappointed. The product is not as described and the customer service is terrible.", #negative
    "What a waste of money" #negative
]

# Generate embeddings for reviews
embeddings: List[List[float]] = []
for review in reviews:
    response: Dict = ollama.embeddings(model="nomic-embed-text", prompt=review)
    embeddings.append(response["embedding"])
print("- - - - -")
# Perform K-means clustering to group similar sentiments
kmeans: KMeans = KMeans(n_clusters=3, random_state=42)
clusters: np.ndarray = kmeans.fit_predict(embeddings)

# Analyze cluster centers to determine sentiment mapping
cluster_centers: np.ndarray = kmeans.cluster_centers_
# Calculate average embedding values for each cluster
cluster_averages: List[float] = [np.mean(cluster_centers[i]) for i in range(3)]
# Sort clusters by their average values
sorted_clusters: np.ndarray = np.argsort(cluster_averages)

# Map clusters to sentiments based on their relative positions
sentiment_map: Dict[int, str] = {
    sorted_clusters[2]: "positive",    # Highest average -> positive
    sorted_clusters[0]: "negative",    # Lowest average -> negative
    sorted_clusters[1]: "neutral"      # Middle average -> neutral
}

# Assign sentiments to reviews
sentiments: List[str] = [sentiment_map[cluster] for cluster in clusters]

# Print results
for review, sentiment in zip(reviews, sentiments):
    print(f"Review: '{review}'")
    print(f"Sentiment: {sentiment}\n")