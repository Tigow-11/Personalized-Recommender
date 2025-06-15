import pickle
import pandas as pd

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Load user-item matrix if needed
ratings = pd.read_csv("user_course_interactions.csv")

def predict_rating(user_id, item_id):
    pred = model.predict(user_id, item_id)
    return pred.est

# Example usage
if __name__ == "__main__":
    print("Predicted rating:", predict_rating(1, 'CLMML02'))
