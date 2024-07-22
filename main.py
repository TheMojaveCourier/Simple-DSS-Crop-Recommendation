from flask import Flask, request, render_template, flash, redirect, url_for
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    N = request.form['N']
    P = request.form['P']
    K = request.form['K']
    temperature = request.form['temperature']
    humidity = request.form['humidity']
    ph = request.form['ph']
    rainfall = request.form['rainfall']
    
    # Check for empty values and non-numeric input
    if not N or not P or not K or not temperature or not humidity or not ph or not rainfall:
        flash('All fields are required. Please provide all values.')
        return redirect(url_for('index'))

    if not (re.match(r'^-?\d+(?:\.\d+)?$', N) and re.match(r'^-?\d+(?:\.\d+)?$', P) and 
            re.match(r'^-?\d+(?:\.\d+)?$', K) and re.match(r'^-?\d+(?:\.\d+)?$', temperature) and 
            re.match(r'^-?\d+(?:\.\d+)?$', humidity) and re.match(r'^-?\d+(?:\.\d+)?$', ph) and 
            re.match(r'^-?\d+(?:\.\d+)?$', rainfall)):
        flash('All inputs must be numeric. Please enter valid numbers.')
        return redirect(url_for('index'))
    
    # Convert form data to float
    N = float(N)
    P = float(P)
    K = float(K)
    temperature = float(temperature)
    humidity = float(humidity)
    ph = float(ph)
    rainfall = float(rainfall)
    
    # Create a dictionary of the input features
    features = {
        'N': N,
        'P': P,
        'K': K,
        'temperature': temperature,
        'humidity': humidity,
        'ph': ph,
        'rainfall': rainfall
    }
    
    # Predict crop using the decision tree J48 rules
    def predict_crop(features):
        if features['humidity'] <= 74.829137:
            if features['humidity'] <= 24.969699:
                if features['K'] <= 50:
                    return 'kidneybeans'
                else:
                    return 'chickpea'
            else:
                if features['N'] <= 59:
                    if features['rainfall'] <= 81.985688:
                        if features['rainfall'] <= 59.7598:
                            if features['humidity'] <= 59.966692:
                                return 'mothbeans'
                            else:
                                if features['P'] <= 52:
                                    return 'mothbeans'
                                else:
                                    return 'lentil'
                        else:
                            if features['P'] <= 57:
                                if features['N'] <= 41:
                                    if features['temperature'] <= 32.39524:
                                        return 'mothbeans'
                                    else:
                                        return 'blackgram'
                                else:
                                    return 'blackgram'
                            else:
                                return 'blackgram'
                    else:
                        if features['P'] <= 47:
                            return 'mango'
                        else:
                            return 'pigeonpeas'
                else:
                    if features['rainfall'] <= 112.434969:
                        return 'maize'
                    else:
                        if features['humidity'] <= 70.045567:
                            return 'coffee'
                        else:
                            return 'jute'
        else:
            if features['P'] <= 32:
                if features['N'] <= 60:
                    if features['K'] <= 20:
                        return 'orange'
                    else:
                        if features['temperature'] <= 24.982875:
                            return 'pomegranate'
                        else:
                            return 'coconut'
                else:
                    if features['temperature'] <= 27.003155:
                        return 'watermelon'
                    else:
                        return 'muskmelon'
            else:
                if features['humidity'] <= 90.006217:
                    if features['K'] <= 30:
                        if features['N'] <= 70:
                            return 'mungbean'
                        else:
                            return 'cotton'
                    else:
                        if features['P'] <= 65:
                            if features['rainfall'] <= 197.528258:
                                if features['ph'] <= 6.01248:
                                    return 'rice'
                                else:
                                    if features['temperature'] <= 22.883309:
                                        return 'rice'
                                    else:
                                        if features['P'] <= 36:
                                            if features['rainfall'] <= 179.824894:
                                                return 'jute'
                                            else:
                                                return 'rice'
                                        else:
                                            if features['N'] <= 92:
                                                return 'jute'
                                            else:
                                                if features['rainfall'] <= 180.716828:
                                                    return 'jute'
                                                else:
                                                    return 'rice'
                            else:
                                return 'rice'
                        else:
                            if features['K'] <= 85:
                                return 'banana'
                            else:
                                return 'grapes'
                else:
                    if features['K'] <= 85:
                        return 'papaya'
                    else:
                        return 'apple'
    
    # Get prediction
    prediction = predict_crop(features)
    
    return render_template('result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
