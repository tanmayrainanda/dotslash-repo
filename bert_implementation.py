import torch
import torch.nn.functional as F
from transformers import BertTokenizer, BertModel
import spacy

# Load Pre-trained BERT Model and Tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

# Predefined Categories with Seed Words
categories = {
    "finance_and_banking": [
        "account", "loan", "credit", "interest", "mortgage"
    ],
    "legal": [
        "court", "lawyer", "contract", "evidence", "trial"
    ],
    "numbers": [
        "one", "hundred", "thousand", "million", "zero"
    ],
    "states_and_cities": [
        "California", "Texas", "New York", "Mumbai", "Sydney"
    ],
    "technical": [
        "algorithm", "circuit", "data", "program", "code"
    ],
    "action": [
        "run", "jump", "write", "speak", "read"
    ],
    "emotion": [
        "joy", "sadness", "anger", "fear", "surprise"
    ],
    "time": [
        "second", "minute", "hour", "day", "year"
    ],
    "people": [
        "teacher", "doctor", "engineer", "child", "parent"
    ],
    "places": [
        "school", "market", "hospital", "park", "beach"
    ],
    "objects": [
        "chair", "table", "pen", "book", "bottle"
    ],
    "food": [
        "pizza", "apple", "bread", "chicken", "rice"
    ],
    "nature": [
        "tree", "mountain", "river", "flower", "cloud"
    ],
    "transportation": [
        "car", "bus", "train", "airplane", "bicycle"
    ],
    "household": [
        "sofa", "lamp", "bed", "mirror", "clock"
    ],
    "event": [
        "wedding", "meeting", "birthday", "concert", "festival"
    ],
    "navigation": [
        "map", "compass", "GPS", "landmark", "route"
    ],
    "sound": [
        "music", "noise", "echo", "ring", "whisper"
    ],
    "animals": [
        "dog", "cat", "elephant", "lion", "bird"
    ],
    "general": [
        "thing", "idea", "concept", "problem", "solution"
    ]
}

nlp = spacy.load("en_core_web_sm")


def lemmatize_sentence(sentence):
    doc = nlp(sentence)
    # Join lemmas into a string instead of returning a list
    return " ".join([token.lemma_ for token in doc if not token.is_stop])


# Step 1: Generate Category Embeddings
def get_category_embeddings(categories):
    category_embeddings = {}
    for category, words in categories.items():
        word_embeddings = []
        for word in words:
            tokens = tokenizer(word, return_tensors="pt", padding=True, truncation=True)
            outputs = model(**tokens)
            word_embedding = outputs.last_hidden_state.mean(dim=1)  # Average embedding
            word_embeddings.append(word_embedding)
        # Average all seed word embeddings for the category
        category_embeddings[category] = torch.stack(word_embeddings).mean(dim=0)
    return category_embeddings


category_embeddings = get_category_embeddings(categories)


# Step 2: Map Words to Categories
def map_words_to_categories(sentence, category_embeddings):
    # Tokenize and get embeddings for the input sentence
    tokens = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**tokens)
    token_embeddings = outputs.last_hidden_state.squeeze(0)  # Remove batch dimension

    # Decode tokens to match embeddings
    decoded_tokens = tokenizer.convert_ids_to_tokens(tokens["input_ids"][0])  # Index batch dimension

    # Map each token to a category
    results = []
    for idx, token in enumerate(decoded_tokens):
        # Skip special tokens like [CLS], [SEP]
        if token not in tokenizer.all_special_tokens:
            token_embedding = token_embeddings[idx]
            # Compute similarity with each category
            similarities = {
                category: F.cosine_similarity(token_embedding, category_embedding.squeeze(0), dim=0).item()
                for category, category_embedding in category_embeddings.items()
            }
            # Assign the token to the category with the highest similarity
            best_category = max(similarities, key=similarities.get)
            results.append(f"{token}_{best_category}")
    return results


# Example Usage
sentence_1 = "Earth's crust and core are essential."
sentence_2 = "I am feeling sad and down today."

print("Results for Sentence 1:")
print(map_words_to_categories(lemmatize_sentence(sentence_1), category_embeddings))

print("\nResults for Sentence 2:")
print(map_words_to_categories(lemmatize_sentence(sentence_2), category_embeddings))
