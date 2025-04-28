import numpy as np
import ollama
from sklearn.metrics.pairwise import cosine_similarity

def get_embedding(text):
    """Generate an embedding for the given text using Ollama."""
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)  # Use a model like 'mistral'
    return response["embedding"]  # Extract the embedding vector

def euclidean_sim(vec1, vec2):
    """Compute the Euclidean similarity between two vectors."""
    distance = np.linalg.norm(np.array(vec1) - np.array(vec2))
    similarity = 1 / (1 + distance)  # Convert distance to similarity score
    return similarity

#dot product similarity function
def dot_product_sim(vec1, vec2):
    """Compute the dot product similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def cosine_sim(vec1, vec2):
    """Compute the cosine similarity between two vectors."""
    return cosine_similarity([vec1], [vec2])[0][0]

def are_similar(text1, text2, threshold=0.8):
    """Check if two paragraphs are similar based on embedding similarity."""
    emb1, emb2 = get_embedding(text1), get_embedding(text2)
    similarity = cosine_sim(emb1, emb2)
    return similarity > threshold, similarity

# Example paragraphs
paragraph1 = """You won't believe what happened today! A major event shook the stock market, and analysts are reacting fast."""
paragraph2 = """The stock market experienced a major shift today, causing analysts to respond swiftly to the changes."""

# Compare them
is_similar, similarity_score = are_similar(paragraph1, paragraph2)

# Print results
print(f"Similarity Score: {similarity_score:.4f}")
print("The paragraphs are similar!" if is_similar else "The paragraphs are different.")
