from flask import Flask, render_template, request
import pandas as pd
import os
app = Flask(__name__)

# Load the tweets
tweets_file = "Final_Incident_Tweets.csv"  # Ensure the CSV file exists and has the correct column
tweets_df = pd.read_csv(tweets_file)

# Ensure the column name is correct (adjust to match your CSV)
if "text" not in tweets_df.columns:
    raise ValueError("The CSV file must have a column named 'text' containing the tweets.")

# Initialize an empty list to store user inputs
user_scores = []

@app.route("/", methods=["GET", "POST"])
def index():
    global user_scores

    if request.method == "POST":
        # Save user scores submitted from the form
        username = request.form.get("username")  # Capture the user's name
        for i, tweet in tweets_df.iterrows():
            user_score = request.form.get(f"severity_{i}")
            if user_score is not None:
                user_scores.append({
                    "Name": username,
                    "Tweet ID": i,
                    "Tweet Text": tweet["text"],
                    "User Severity Score": int(user_score)
                })

        # Save all user scores to a CSV file
        pd.DataFrame(user_scores).to_csv("user_scores.csv", index=False)
        return "Thank you for your input! Your scores have been recorded."

    # Add index information to tweets
    tweets_with_indices = [{"index": i, "text": tweet} for i, tweet in enumerate(tweets_df["text"].tolist())]

    return render_template("index.html", tweets=tweets_with_indices)


@app.route("/view-scores")
def view_scores():
    try:
        # Read the latest scores from the CSV file
        scores = pd.read_csv("user_scores.csv").to_dict(orient="records")
    except FileNotFoundError:
        # If no scores yet, handle gracefully
        scores = []
    return render_template("view_scores.html", scores=scores)


if __name__ == "__main__":
    # Use the PORT environment variable set by Render, or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
