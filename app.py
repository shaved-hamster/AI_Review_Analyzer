
from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Завантаження готової моделі Hugging Face
print("Завантаження AI-моделі...")

classifier = pipeline(
    "text-classification",
    model="Horizon-Labs/multilingual-sentiment-small"
)

print("AI-модель успішно завантажена!")


def analyze_review(text):
    # Аналіз відгуку
    result = classifier(text)[0]

    label = result["label"].lower()

    translations = {
        "positive": "Позитивний",
        "negative": "Негативний",
        "neutral": "Нейтральний"
    }

    return {
        "sentiment": translations.get(label, label),
        "score": round(result["score"] * 100, 2),
        "text": text
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    reviews_text = request.form.get("reviews", "")

    reviews = [
        line.strip()
        for line in reviews_text.splitlines()
        if line.strip()
    ]

    if not reviews:
        return render_template(
            "index.html",
            error="Введіть хоча б один відгук."
        )

    try:
        results = [
            analyze_review(review)
            for review in reviews
        ]

        positive = sum(
            1 for r in results
            if r["sentiment"] == "Позитивний"
        )

        negative = sum(
            1 for r in results
            if r["sentiment"] == "Негативний"
        )

        neutral = sum(
            1 for r in results
            if r["sentiment"] == "Нейтральний"
        )

        statistics = {
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "total": len(results)
        }

        return render_template(
            "index.html",
            results=results,
            statistics=statistics,
            reviews=reviews_text
        )

    except Exception as e:
        return render_template(
            "index.html",
            error=f"Помилка аналізу: {str(e)}",
            reviews=reviews_text
        )


if __name__ == "__main__":
    app.run(debug=True)
