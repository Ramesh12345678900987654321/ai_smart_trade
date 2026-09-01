from flask import Flask, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


API_KEY = "0837f397ad99467ab2d1cf2195caf993"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/news/<company>")
def get_news(company):

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={company}&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"pageSize=10&"
        f"apiKey={API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    if data.get("status") != "ok":
        return jsonify(data)

    news = []

    for article in data.get("articles", []):

        news.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url"),
            "image": article.get("urlToImage"),
            "time": article.get("publishedAt")
        })

    return jsonify(news)


if __name__ == "__main__":
    app.run(debug=True)