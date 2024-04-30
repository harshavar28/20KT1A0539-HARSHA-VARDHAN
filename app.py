from flask import Flask, request, render_template
import ml

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        location = request.form.get('location')
        year = int(request.form.get('year'))
        month_str = request.form.get('month')

        # Ensure month input is valid
        if month_str not in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']:
            raise ValueError("Invalid month input")

        # Convert month input to index
        months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        month_index = months.index(month_str)

        # Correctly call predict_rainfall function
        predicted_rainfall = ml.predict_rainfall(location, year, month_index)

        return render_template('results.html', location=location, year=year, month=month_str, predicted_rainfall=predicted_rainfall)
    except ValueError as ve:
        return f"An error occurred: {ve}", 400
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
