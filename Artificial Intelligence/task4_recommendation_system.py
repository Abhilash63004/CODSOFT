"""
CODSOFT AI Internship - Task 4: Recommendation System
Suggests movies to users based on collaborative filtering and content-based filtering.
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# ─────────────────────────────────────────────
# SAMPLE DATASET
# ─────────────────────────────────────────────

# Movies with genres and tags
movies_data = {
    "movie_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "title": [
        "The Dark Knight", "Inception", "Interstellar", "The Matrix",
        "Avengers: Endgame", "Forrest Gump", "The Shawshank Redemption",
        "Pulp Fiction", "The Godfather", "Toy Story"
    ],
    "genres": [
        "Action Crime Drama", "Action Sci-Fi Thriller", "Sci-Fi Drama Adventure",
        "Sci-Fi Action", "Action Adventure Sci-Fi", "Drama Romance",
        "Drama", "Crime Thriller Drama", "Crime Drama", "Animation Comedy Family"
    ]
}

# User ratings (user_id → movie_id → rating out of 5)
ratings_data = {
    "user_id": [1,1,1,1,1, 2,2,2,2,2, 3,3,3,3,3, 4,4,4,4,4, 5,5,5,5,5],
    "movie_id": [1,2,3,5,8, 1,3,4,6,9, 2,3,5,7,10, 1,4,6,8,9, 2,3,5,7,8],
    "rating":   [5,4,5,3,4, 4,5,5,2,5, 5,4,4,5,3,  3,5,4,5,4, 4,5,5,3,4]
}

movies_df = pd.DataFrame(movies_data)
ratings_df = pd.DataFrame(ratings_data)


# ─────────────────────────────────────────────
# 1. CONTENT-BASED FILTERING
# ─────────────────────────────────────────────

def content_based_recommendations(movie_title: str, top_n: int = 5) -> pd.DataFrame:
    """
    Recommend movies similar to the given movie based on genre/content similarity.
    Uses TF-IDF vectorization + cosine similarity.
    """
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(movies_df["genres"])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Find index of the given movie
    idx_series = movies_df[movies_df["title"].str.lower() == movie_title.lower()].index
    if idx_series.empty:
        print(f"  ⚠️  Movie '{movie_title}' not found in database.")
        return pd.DataFrame()

    idx = idx_series[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [(i, s) for i, s in sim_scores if i != idx][:top_n]

    rec_indices = [i for i, _ in sim_scores]
    result = movies_df.iloc[rec_indices][["title", "genres"]].copy()
    result["similarity_score"] = [round(s, 3) for _, s in sim_scores]
    return result.reset_index(drop=True)


# ─────────────────────────────────────────────
# 2. COLLABORATIVE FILTERING (User-Based)
# ─────────────────────────────────────────────

def collaborative_recommendations(user_id: int, top_n: int = 5) -> pd.DataFrame:
    """
    Recommend movies to a user based on ratings from similar users.
    Uses user-user cosine similarity.
    """
    # Build user-movie rating matrix
    user_movie_matrix = ratings_df.pivot_table(
        index="user_id", columns="movie_id", values="rating"
    ).fillna(0)

    if user_id not in user_movie_matrix.index:
        print(f"  ⚠️  User {user_id} not found.")
        return pd.DataFrame()

    # Compute cosine similarity between users
    user_sim = cosine_similarity(user_movie_matrix)
    user_sim_df = pd.DataFrame(
        user_sim,
        index=user_movie_matrix.index,
        columns=user_movie_matrix.index
    )

    # Get similar users (excluding self)
    similar_users = user_sim_df[user_id].drop(user_id).sort_values(ascending=False)

    # Movies already rated by this user
    rated_movies = set(ratings_df[ratings_df["user_id"] == user_id]["movie_id"])

    # Score unrated movies using weighted average of similar users' ratings
    scores = {}
    for other_user, sim_score in similar_users.items():
        other_ratings = ratings_df[ratings_df["user_id"] == other_user]
        for _, row in other_ratings.iterrows():
            mid = row["movie_id"]
            if mid not in rated_movies:
                scores[mid] = scores.get(mid, 0) + sim_score * row["rating"]

    if not scores:
        print("  ⚠️  No recommendations found (user may have rated all movies).")
        return pd.DataFrame()

    # Sort by score and return top N
    top_movies = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    rec_ids = [mid for mid, _ in top_movies]
    rec_scores = [round(score, 3) for _, score in top_movies]

    result = movies_df[movies_df["movie_id"].isin(rec_ids)][["title", "genres"]].copy()
    score_map = dict(zip(rec_ids, rec_scores))
    result["predicted_score"] = result["movie_id"].map(score_map) if "movie_id" in result.columns else rec_scores
    # Re-attach movie_id for mapping
    result2 = movies_df[movies_df["movie_id"].isin(rec_ids)].copy()
    result2["predicted_score"] = result2["movie_id"].map(score_map)
    result2 = result2.sort_values("predicted_score", ascending=False)
    return result2[["title", "genres", "predicted_score"]].reset_index(drop=True)


# ─────────────────────────────────────────────
# 3. HYBRID RECOMMENDATION
# ─────────────────────────────────────────────

def hybrid_recommendations(user_id: int, top_n: int = 5) -> pd.DataFrame:
    """
    Combines collaborative filtering + content-based filtering.
    First gets collaborative recommendations, then re-ranks using content similarity.
    """
    collab = collaborative_recommendations(user_id, top_n=top_n * 2)
    if collab.empty:
        return pd.DataFrame()

    # Use user's highest-rated movie as seed for content filtering
    user_ratings = ratings_df[ratings_df["user_id"] == user_id]
    if user_ratings.empty:
        return collab.head(top_n)

    top_rated_id = user_ratings.sort_values("rating", ascending=False).iloc[0]["movie_id"]
    top_rated_title = movies_df[movies_df["movie_id"] == top_rated_id]["title"].values[0]

    content = content_based_recommendations(top_rated_title, top_n=top_n * 2)
    if content.empty:
        return collab.head(top_n)

    # Merge results — prioritize overlap
    collab_titles = set(collab["title"])
    content_titles = set(content["title"])
    overlap = collab_titles & content_titles

    hybrid = []
    for title in list(overlap)[:top_n]:
        row = movies_df[movies_df["title"] == title].iloc[0]
        hybrid.append({"title": row["title"], "genres": row["genres"], "method": "Hybrid ✅"})

    # Fill remaining from collab
    for _, row in collab.iterrows():
        if len(hybrid) >= top_n:
            break
        if row["title"] not in [h["title"] for h in hybrid]:
            hybrid.append({"title": row["title"], "genres": row["genres"], "method": "Collaborative"})

    return pd.DataFrame(hybrid)


# ─────────────────────────────────────────────
# MAIN DEMO
# ─────────────────────────────────────────────

def display_df(df: pd.DataFrame):
    if df.empty:
        print("  No results.\n")
    else:
        print(df.to_string(index=False))
        print()


def main():
    print("=" * 60)
    print("  🎬  CodSoft AI Internship - Recommendation System  🎬")
    print("=" * 60)

    # ── Content-Based ──
    print("\n📽️  [1] CONTENT-BASED: Movies similar to 'Inception'")
    print("-" * 60)
    result = content_based_recommendations("Inception", top_n=5)
    display_df(result)

    print("📽️  [1] CONTENT-BASED: Movies similar to 'The Godfather'")
    print("-" * 60)
    result = content_based_recommendations("The Godfather", top_n=5)
    display_df(result)

    # ── Collaborative ──
    print("👤  [2] COLLABORATIVE: Recommendations for User 1")
    print("-" * 60)
    result = collaborative_recommendations(user_id=1, top_n=5)
    display_df(result)

    print("👤  [2] COLLABORATIVE: Recommendations for User 3")
    print("-" * 60)
    result = collaborative_recommendations(user_id=3, top_n=5)
    display_df(result)

    # ── Hybrid ──
    print("🔀  [3] HYBRID: Recommendations for User 2")
    print("-" * 60)
    result = hybrid_recommendations(user_id=2, top_n=5)
    display_df(result)

    # ── Interactive ──
    print("=" * 60)
    print("  🎯  INTERACTIVE MODE")
    print("=" * 60)
    while True:
        print("\nOptions:")
        print("  1. Content-based (by movie title)")
        print("  2. Collaborative (by user ID)")
        print("  3. Hybrid (by user ID)")
        print("  4. Exit")
        choice = input("\nYour choice: ").strip()

        if choice == "1":
            print("Available movies:", ", ".join(movies_df["title"].tolist()))
            title = input("Enter movie title: ").strip()
            display_df(content_based_recommendations(title))
        elif choice == "2":
            uid = int(input("Enter user ID (1-5): ").strip())
            display_df(collaborative_recommendations(uid))
        elif choice == "3":
            uid = int(input("Enter user ID (1-5): ").strip())
            display_df(hybrid_recommendations(uid))
        elif choice == "4":
            print("Goodbye! 🎬")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
