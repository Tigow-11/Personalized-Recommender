import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
import pickle

# Load your data
courses_df = pd.read_csv("Courses_and_Learning_Material.csv")
ratings_df = pd.read_csv("Learning_Pathway_Index.csv")

# ✅ Rename columns for Surprise
ratings_df = ratings_df.rename(columns={
    'User_ID': 'user_id',
    'Course_ID': 'item_id',
    'Rating': 'rating'
})

# Show for debug
print("🔍 Columns in ratings_df:", ratings_df.columns)
print("📊 Sample ratings:\n", ratings_df.head())

# Surprise Dataset creation
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings_df[['user_id', 'item_id', 'rating']], reader)

# Split & train
trainset, testset = train_test_split(data, test_size=0.2)
model = SVD()
model.fit(trainset)

# Save the model
with open("svd_recommender_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as svd_recommender_model.pkl")
