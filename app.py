import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Robots.txt Tester</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; }
    form { margin-bottom: 20px; }
    textarea { width: 100%; height: 200px; }
  </style>
</head>
<body>
  <h1>Robots.txt Tester</h1>
  <form method="post" action="/">
    <label for="url">Enter website URL:</label><br>
    <input type="text" id="url" name="url" placeholder="https://www.example.com" required><br><br>
    <button type="submit">Test Robots.txt</button>
  </form>
  {% if result %}
  <h2>Robots.txt Content</h2>
  <textarea readonly>{{ result }}</textarea>
  {% if errors %}
  <h3>Errors</h3>
  <ul>
    {% for error in errors %}
    <li>{{ error }}</li>
    {% endfor %}
  </ul>
  {% endif %}
  {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    errors = []

    if request.method == "POST":
        url = request.form.get("url")
        if not url.startswith("http"):
            url = "http://" + url

        try:
            response = requests.get(url + "/robots.txt")
            response.raise_for_status()
            result = response.text

            # Simple validation checks
            if "User-agent" not in result or "Disallow" not in result:
                errors.append("Missing 'User-agent' or 'Disallow' directives.")
            if result.strip() == "":
                errors.append("Robots.txt file is empty.")
        except requests.RequestException as e:
            errors.append(f"Error fetching robots.txt: {e}")

    return render_template_string(HTML_TEMPLATE, result=result, errors=errors)


if __name__ == "__main__":
    app.run(debug=True)
