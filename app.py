from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Home route to render your HTML file
@app.route('/')
def home():
    return render_template('index.html')

# Route to calculate queueing theory parameters
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get input data from the request (JSON format expected)
        data = request.json

        # Extract required inputs
        arrival_rate = float(data.get('arrival_rate'))  # Lambda (λ)
        service_rate = float(data.get('service_rate'))  # Mu (μ)

        # Basic validation
        if service_rate <= arrival_rate:
            return jsonify({"error": "System is unstable. Service rate must be greater than arrival rate."}), 400

        # Calculations for M/M/1 queue
        traffic_intensity = arrival_rate / service_rate  # ρ
        avg_number_in_system = traffic_intensity / (1 - traffic_intensity)  # L
        avg_time_in_system = 1 / (service_rate - arrival_rate)  # W
        avg_number_in_queue = traffic_intensity**2 / (1 - traffic_intensity)  # Lq
        avg_time_in_queue = traffic_intensity / (service_rate - arrival_rate)  # Wq

        # Return results as JSON
        return jsonify({
            "traffic_intensity": traffic_intensity,
            "avg_number_in_system": avg_number_in_system,
            "avg_time_in_system": avg_time_in_system,
            "avg_number_in_queue": avg_number_in_queue,
            "avg_time_in_queue": avg_time_in_queue
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
