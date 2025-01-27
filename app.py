from flask import Flask, render_template, request
import pandas as pd

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
        for i, tweet in tweets_df.iterrows():
            user_score = request.form.get(f"severity_{i}")
            if user_score is not None:
                user_scores.append({"Tweet ID": i, "Tweet Text": tweet["text"], "User Severity Score": int(user_score)})

        # Save all user scores to a CSV file
        pd.DataFrame(user_scores).to_csv("user_scores.csv", index=False)
        return "Thank you for your input! Your scores have been recorded."

    # Add index information to tweets
    tweets_with_indices = [{"index": i, "text": tweet} for i, tweet in enumerate(tweets_df["text"].tolist())]

    return render_template("index.html", tweets=tweets_with_indices)


if __name__ == "__main__":
    app.run(debug=True)
