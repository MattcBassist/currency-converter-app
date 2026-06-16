from flask import Flask, render_template, request

app = Flask(__name__)

# Simple hard-coded exchange rates for the coursework currency converter
RATES = {
    "USD": {"GBP": 0.79, "EUR": 0.92},
    "GBP": {"USD": 1.27, "EUR": 1.16},
    "EUR": {"USD": 1.09, "GBP": 0.86}
}


def convert_currency(amount, from_currency, to_currency):
    """Convert an amount from one currency to another."""
    if from_currency == to_currency:
        return round(amount, 2)

    rate = RATES.get(from_currency, {}).get(to_currency)

    if rate is None:
        raise ValueError("Invalid currency selection")

    return round(amount * rate, 2)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        amount_input = request.form.get("amount", "").strip()
        from_currency = request.form.get("from_currency")
        to_currency = request.form.get("to_currency")

        try:
            amount = float(amount_input)

            if amount < 0:
                error = "Please enter a valid number"
            else:
                result = convert_currency(amount, from_currency, to_currency)

        except (ValueError, TypeError):
            error = "Please enter a valid number"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
