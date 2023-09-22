from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
model = pickle.load(open('model_L.pkl', 'rb'))

# Mapping
Airline_mapping = {'Air India':[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'GoAir':[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],'IndiGo':[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],'Jet Airways':[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],'Jet Airways Business':[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],'Multiple carriers':[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],'Multiple carriers Premium economy':[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],'SpiceJet':[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],'Trujet':[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],'Vistara':[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],'Vistara Premium economy':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}
Source_mapping = {'Chennai' : [1, 0, 0, 0],'Delhi' : [0, 1, 0, 0],'Kolkata' : [0, 0, 1, 0],'Mumbai' : [0, 0, 0, 1]}
Destination_mapping = {'Cochin' : [1, 0, 0, 0, 0],'Delhi' : [0, 1, 0, 0, 0],'Hyderabad' : [0, 0, 1, 0, 0],'Kolkata' : [0, 0, 0, 1, 0],'New Delhi' : [0, 0, 0, 0, 1]}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extracting values from the form

    Total_Stop = int(request.form['TotalStop'])
    Journey_Day = int(request.form['journeyDay'])
    Journey_Month = int(request.form['journeyMonth'])
    Departure_Hour = int(request.form['depHour'])
    Departure_Minute = int(request.form['depMin'])
    Arrival_Hour = int(request.form['arrivalHour'])
    Arrival_Minute = int(request.form['arrivalMin'])
    Duration_Hours = int(request.form['durationHours'])
    Duration_Minutes = int(request.form['durationMins'])
    Airline = request.form['airline']
    Source = request.form['source']
    Destination = request.form['destination']

    # Get the data based on the selected data

    Airline_data = Airline_mapping.get(Airline, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    Source_data = Source_mapping.get(Source, [0, 0, 0, 0])
    Destination_data = Destination_mapping.get(Destination, [0, 0, 0, 0, 0])

    # Create input array for prediction

    input_data = np.array([[Total_Stop] + [Journey_Day] + [Journey_Month] + [Departure_Hour] + [Departure_Minute] + [Arrival_Hour] + [Arrival_Minute] + [Duration_Hours] + [Duration_Minutes] + Airline_data + Source_data + Destination_data])

    # Predict the price
    predicted_price = model.predict(input_data)

    return render_template('index.html', prediction=f'Predicted Price: {predicted_price[0]:.2f}')

if __name__ == '__main__':
    app.run(debug=True)