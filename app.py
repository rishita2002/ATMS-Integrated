from flask import Flask, render_template, request, redirect, url_for,g,send_from_directory
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import sqlite3
import os
import csv
from flask_mail import Mail, Message
from datetime import datetime, timedelta

app = Flask(__name__)

# Function to establish a database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('atms.db')
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        

@app.route('/')
def main_dashboard():
    return render_template("dashboard.html")

@app.route('/analytics')
def dashboard():
    # Fetch data from the database
    #conn = get_db()

    # Load data from CSV
    data = pd.read_csv('mock_data.csv')
    #data = pd.read_sql_query('SELECT * FROM atms', conn)

    visualizations = []

    # Visualization 1: Bar chart for Total Quantity by Product Type
    plt.figure(figsize=(7, 5))
    data.groupby('Product Type')['Quantity'].sum().plot(kind='bar')
    plt.title('Total Quantity by Product Type')
    plt.xlabel('Product Type')
    plt.ylabel('Total Quantity')
    img1 = plot_to_base64(plt)
    visualizations.append(img1)

    # Visualization 2: Scatter plot for Temperature vs. Humidity
    plt.figure(figsize=(7, 5))
    plt.scatter(data['Temperature'], data['Humidity'], alpha=0.5)
    plt.title('Temperature vs. Humidity')
    plt.xlabel('Temperature')
    plt.ylabel('Humidity')
    img2 = plot_to_base64(plt)
    visualizations.append(img2)

    # Visualization 3: Pie chart for Compliance Status
    compliance_counts = data['Compliance Status'].value_counts()
    plt.figure(figsize=(5, 5))
    plt.pie(compliance_counts, labels=compliance_counts.index, autopct='%1.1f%%')
    plt.title('Compliance Status Distribution')
    img3 = plot_to_base64(plt)
    visualizations.append(img3)

    # Visualization 4: Line chart for Quantity over Time
    plt.figure(figsize=(7, 5))
    data['Departure Date'] = pd.to_datetime(data['Departure Date'])
    data.set_index('Departure Date', inplace=True)
    data.resample('M')['Quantity'].sum().plot()
    plt.title('Monthly Total Quantity over Time')
    plt.xlabel('Time')
    plt.ylabel('Total Quantity')
    img4 = plot_to_base64(plt)
    visualizations.append(img4)

    # Visualization 5: Box plot for CO2 Emissions
    plt.figure(figsize=(10, 5))
    data.boxplot(column='CO2 Emissions (in kg)', by='Product Type')
    plt.title('CO2 Emissions by Product Type')
    plt.suptitle('')  # Removes the default title
    plt.xlabel('Product Type')
    plt.ylabel('CO2 Emissions')
    img5 = plot_to_base64(plt)
    visualizations.append(img5)

    # Visualization 6: Histogram for Distance Traveled
    plt.figure(figsize=(7, 5))
    data['Distance Traveled'].hist(bins=20)
    plt.title('Distribution of Distance Traveled')
    plt.xlabel('Distance Traveled (miles)')
    plt.ylabel('Frequency')
    img6 = plot_to_base64(plt)
    visualizations.append(img6)

    # Visualization 7: Correlation Heatmap
    plt.figure(figsize=(8, 6))
    correlation_matrix = data.corr()
    plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='none')
    plt.colorbar()
    plt.title('Correlation Heatmap')
    plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=90)
    plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
    img7 = plot_to_base64(plt)
    visualizations.append(img7)

    # Visualization 8: Time Series of Revenue
    plt.figure(figsize=(7, 5))
    data['Arrival Date'] = pd.to_datetime(data['Arrival Date'])
    data.set_index('Arrival Date', inplace=True)
    data.resample('M')['Revenue'].sum().plot()
    plt.title('Monthly Total Revenue over Time')
    plt.xlabel('Time')
    plt.ylabel('Total Revenue')
    img8 = plot_to_base64(plt)
    visualizations.append(img8)

    # Visualization 9: Bar chart for Quantity by Weather Conditions
    plt.figure(figsize=(7, 5))
    data.groupby('Weather Conditions')['Quantity'].sum().plot(kind='bar')
    plt.title('Total Quantity by Weather Conditions')
    plt.xlabel('Weather Conditions')
    plt.ylabel('Total Quantity')
    img9 = plot_to_base64(plt)
    visualizations.append(img9)

    # Visualization 10: Box plot for Transport Cost by Transportation Mode
    plt.figure(figsize=(10, 5))
    data.boxplot(column='Transport Cost (in dollars)', by='Transportation Mode')
    plt.title('Transport Cost by Transportation Mode')
    plt.suptitle('')  # Removes the default title
    plt.xlabel('Transportation Mode')
    plt.ylabel('Transport Cost')
    img10 = plot_to_base64(plt)
    visualizations.append(img10)

    return render_template('dashboard_analytics.html', plot_url1=img1, plot_url2=img2, plot_url3=img3, plot_url4=img4, plot_url5=img5,
                           plot_url6=img6, plot_url7=img7, plot_url8=img8, plot_url9=img9,plot_url10=img10)

def plot_to_base64(plot):
    img = io.BytesIO()
    plot.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.read()).decode()

@app.route('/upload', methods=['POST'])
def upload_data():
    if request.method == 'POST':
        product_name = request.form.get('product-name')
        product_type = request.form.get('product-type')
        origin_location = request.form.get('origin-location')
        destination_location = request.form.get('destination-location')
        transportation_mode = request.form.get('transportation-mode')
        departure_date = request.form.get('departure-date')
        arrival_date = request.form.get('arrival-date')
        distance = request.form.get('distance')
        fuel_consumption = request.form.get('fuel-consumption')
        co2_emissions = request.form.get('co2-emissions')
        transport_cost = request.form.get('transport-cost')
        compliance_status = request.form.get('compliance-status')
        maintenance_status = request.form.get('maintenance-status')
        weather_conditions = request.form.get('weather-conditions')
        route_details = request.form.get('route-details')
        quantity = request.form.get('quantity')
        revenue = request.form.get('revenue')
        temperature = request.form.get('temperature')
        humidity = request.form.get('humidity')
        soil_moisture = request.form.get('soil-moisture')
        pest_incidents = request.form.get('pest-incidents')
        transportation_mode_2 = request.form.get('transportation-mode-2')
        distance_traveled = request.form.get('distance-traveled')
        date = request.form.get('date')
        quarter = request.form.get('quarter')
        year = request.form.get('year')

        # Create a new DataFrame with the form data
        new_data = pd.DataFrame({
            'Product Name': [product_name],
            'Product Type': [product_type],
            'Origin Location': [origin_location],
            'Destination Location': [destination_location],
            'Transportation Mode': [transportation_mode],
            'Departure Date': [departure_date],
            'Arrival Date': [arrival_date],
            'Distance (in miles)': [distance],
            'Fuel Consumption (in gallons)': [fuel_consumption],
            'CO2 Emissions (in kg)': [co2_emissions],
            'Transport Cost (in dollars)': [transport_cost],
            'Compliance Status': [compliance_status],
            'Maintenance Status': [maintenance_status],
            'Weather Conditions': [weather_conditions],
            'Route Optimization Details': [route_details],
            'Quantity': [quantity],
            'Revenue': [revenue],
            'Temperature': [temperature],
            'Humidity': [humidity],
            'Soil Moisture': [soil_moisture],
            'Pest Incidents': [pest_incidents],
            'Transportation Mode (2)': [transportation_mode_2],
            'Distance Traveled': [distance_traveled],
            'Date': [date],
            'Quarter': [quarter],
            'Year': [year]
        })

        # Append the new data to the existing CSV file
        new_data.to_csv("mock_data.csv", mode='a', header=False, index=False)
        print("Data Uploaded Successfully!")

    return redirect(url_for('dashboard'))

#Route Optimization
# Data for cities in Chhattisgarh with approximate distances
cities_in_chhattisgarh = {
    'Raipur': {'Bhilai': 30, 'Durg': 25, 'Bilaspur': 140, 'Korba': 200, 'Jagdalpur': 300, 'Ambikapur': 350, 'Rajnandgaon': 70, 'Dhamtari': 40, 'Janjgir': 130, 'Mahasamund': 90, 'Balod': 50, 'Bhatapara': 110, 'Mungeli': 140, 'Kanker': 270},
    'Bhilai': {'Durg': 15, 'Bilaspur': 130, 'Korba': 190, 'Jagdalpur': 310, 'Ambikapur': 360, 'Rajnandgaon': 80, 'Dhamtari': 35, 'Janjgir': 120, 'Mahasamund': 95, 'Balod': 55, 'Bhatapara': 115, 'Mungeli': 145, 'Kanker': 275},
    'Durg': {'Bilaspur': 150, 'Korba': 210, 'Jagdalpur': 330, 'Ambikapur': 380, 'Rajnandgaon': 100, 'Dhamtari': 45, 'Janjgir': 130, 'Mahasamund': 100, 'Balod': 60, 'Bhatapara': 120, 'Mungeli': 150, 'Kanker': 280},
    'Bilaspur': {'Korba': 90, 'Ambikapur': 240, 'Rajnandgaon': 180, 'Dhamtari': 110, 'Janjgir': 20, 'Mahasamund': 130, 'Balod': 110, 'Bhatapara': 70, 'Mungeli': 200, 'Kanker': 270},
    'Korba': {'Jagdalpur': 120, 'Ambikapur': 170, 'Rajnandgaon': 250, 'Dhamtari': 190, 'Janjgir': 280, 'Mahasamund': 190, 'Balod': 230, 'Bhatapara': 180, 'Mungeli': 110, 'Kanker': 200},
    'Jagdalpur': {'Ambikapur': 200, 'Rajnandgaon': 420, 'Dhamtari': 330, 'Janjgir': 250, 'Mahasamund': 360, 'Balod': 340, 'Bhatapara': 400, 'Mungeli': 430, 'Kanker': 150},
    'Ambikapur': {'Rajnandgaon': 470, 'Dhamtari': 380, 'Janjgir': 300, 'Mahasamund': 410, 'Balod': 390, 'Bhatapara': 450, 'Mungeli': 480, 'Kanker': 200},
    'Rajnandgaon': {'Dhamtari': 80, 'Janjgir': 160, 'Mahasamund': 170, 'Balod': 150, 'Bhatapara': 210, 'Mungeli': 240, 'Kanker': 370},
    'Dhamtari': {'Janjgir': 60, 'Mahasamund': 50, 'Balod': 70, 'Bhatapara': 90, 'Mungeli': 120, 'Kanker': 250},
    'Janjgir': {'Mahasamund': 70, 'Balod': 90, 'Bhatapara': 50, 'Mungeli': 80, 'Kanker': 210},
    'Mahasamund': {'Balod': 40, 'Bhatapara': 110, 'Mungeli': 140, 'Kanker': 270},
    'Balod': {'Bhatapara': 60, 'Mungeli': 90, 'Kanker': 220},
    'Bhatapara': {'Mungeli': 120, 'Kanker': 250},
    'Mungeli': {'Kanker': 230},
    'Kanker': {}
}


# Function to implement Dijkstra's algorithm
def dijkstra(graph, start, end):
    # Initialization
    unvisited_nodes = set(graph.keys())
    distances = {node: float('infinity') for node in unvisited_nodes}
    distances[start] = 0
    previous_nodes = {node: None for node in unvisited_nodes}

    while unvisited_nodes:
        current_node = min(unvisited_nodes, key=lambda node: distances[node])
        unvisited_nodes.remove(current_node)

        for neighbor, distance in graph[current_node].items():
            potential_distance = distances[current_node] + distance
            if potential_distance < distances[neighbor]:
                distances[neighbor] = potential_distance
                previous_nodes[neighbor] = current_node

    # Reconstructing the path
    path = []
    current = end
    while previous_nodes[current] is not None:
        path.insert(0, current)
        current = previous_nodes[current]
    path.insert(0, start)

    return path, distances[end]

@app.route('/route', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get start and end nodes from the form
        start_node = request.form['start_node']
        end_node = request.form['end_node']

        # Calculate the shortest path
        path, distance = dijkstra(cities_in_chhattisgarh, start_node, end_node)

        return render_template('index.html', start=start_node, end=end_node, path=path, distance=distance, cities=cities_in_chhattisgarh.keys())

    return render_template('index.html', start=None, end=None, path=None, distance=None, cities=cities_in_chhattisgarh.keys())

#Inventory Management

# Define the route for adding a new item
@app.route("/add-item", methods=["POST"])
def add_item():
    # Get the product information from the request
    product_name = request.form["product_name"]
    product_quantity = int(request.form["product_quantity"])
    product_price = float(request.form["product_price"])
    product_expiry_date = request.form["product_expiry_date"]

    # Check if the CSV file doesn't exist or is empty
    csv_file = "static/new_inventory.csv"
    csv_file_exists = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0

    # Create a new CSV file or add column headers if it doesn't already exist
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)

        if not csv_file_exists:  # If the file is new or empty, add column headers
            writer.writerow(["product_name", "product_quantity", "product_price", "product_expiry_date"])

        # Write the new item information to the CSV file
        writer.writerow([product_name, product_quantity, product_price, product_expiry_date])

    # Redirect the user back to the main page
    return redirect("/inventory")

@app.route("/remove-item", methods=["POST"])
def remove_item():
    # Get the product name to remove from the form
    product_name_to_remove = request.form.get("product_name")

    # Get the list of items from the CSV file
    items = []

    csv_file = "static/new_inventory.csv"
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        with open(csv_file, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                item = {
                    "product_name": row[0],
                    "product_quantity": int(row[1]),
                    "product_price": float(row[2]),
                    "product_expiry_date": row[3]
                }
                items.append(item)

    # Find and remove the item by the product name
    removed = False
    for item in items:
        if item["product_name"] == product_name_to_remove:
            items.remove(item)
            removed = True
            break

    # If an item was removed, write the updated items back to the CSV file
    if removed:
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["product_name", "product_quantity", "product_price", "product_expiry_date"])
            for item in items:
                writer.writerow([item["product_name"], item["product_quantity"], item["product_price"], item["product_expiry_date"]])

    # Redirect the user back to the main page
    return redirect("/inventory")



# Add a route to serve the CSV file
@app.route('/static/<path:filename>')
def download_file(filename):
    return send_from_directory('static', filename)

# The rest of your Flask code...

# Define the route for seeing all items
@app.route("/inventory")
def see_all_items():
    items = []  # Initialize an empty list

    # Check if the CSV file doesn't exist or is empty
    csv_file = "static/new_inventory.csv"
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        # Open the CSV file and read the data
        with open(csv_file, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                item = {
                    "product_name": row[0],
                    "product_quantity": int(row[1]),
                    "product_price": float(row[2]),
                    "product_expiry_date": row[3]
                }
                items.append(item)

    # Render the template with the list of items
    return render_template("new_inventory.html", items=items)



# Realtime Tracking

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'chdhanlaxmi01@gmail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_PASSWORD'] = 'kieg vkax nbtp hfms'

mail = Mail(app)

@app.route('/track')
def form():
    return render_template('form.html')

@app.route('/status')
def status():
    return render_template('index1.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    '''data = request.get_json()
    checkbox_name = data.get('checkboxName')
    #email = data.get('email')

    if checkbox_name:
        # Add your email sending logic here
        # You can use Flask-Mail or any other library
        email_subject = "Status of Your Order"
        email_recipient = 'ch.shakish13@gmail.com'
        
        msg = Message(email_subject, sender='chdhanlaxmi01@gmail.com', recipients=[email_recipient])
        msg.body = f"Your product '{checkbox_name}'."
        print(msg)
        mail.send(msg)
        return 'Email sent successfully.'
    else:
        return 'Checkbox name address are required.' '''
    try:
        data = request.get_json()
        status = data.get('status')
        
        if status is not None:
            # Customize the email subject and body based on the selected status
            subject = f'Status of your order'
            body = f'Your product {status}.'
            
            msg = Message(subject,sender='chdhanlaxmi01@gmail.com', recipients=['ch.shakish13@gmail.com'])  # Change to the recipient's email
            msg.body = body
            mail.send(msg)
            
            return "Email sent successfully"
        else:
            return "Invalid status data", 400
    except Exception as e:
        return str(e), 500
    
#Pooling
current_running_trucks = [ 
    {'start': 'Raipur', 'end': 'Bilaspur', 'departure_time': '08:00', 'driver': 'Amit', 'truck_number': 'CG 04 7158'},
{'start': 'Durg', 'end': 'Korba', 'departure_time': '10:00', 'driver': 'Rajat', 'truck_number': 'CG 04 6404'},
{'start': 'Bilaspur', 'end': 'Jagdalpur', 'departure_time': '11:30', 'driver': 'Chetan', 'truck_number': 'CG 04 9596'},
{'start': 'Ambikapur', 'end': 'Rajnandgaon', 'departure_time': '13:15', 'driver': 'Sourabh', 'truck_number': 'CG 04 8115'},
{'start': 'Korba', 'end': 'Dhamtari', 'departure_time': '15:00', 'driver': 'Vyapak', 'truck_number': 'CG 04 7516'},
{'start': 'Janjgir', 'end': 'Mahasamund', 'departure_time': '16:45', 'driver': 'Arjun', 'truck_number': 'CG 04 4561'},
{'start': 'Balod', 'end': 'Bhatapara', 'departure_time': '18:30', 'driver': 'Vansh', 'truck_number': 'CG 04 5067'},
{'start': 'Mungeli', 'end': 'Kanker', 'departure_time': '20:15', 'driver': 'Amit', 'truck_number': 'CG 04 1095'},
{'start': 'Bhilai', 'end': 'Ambikapur', 'departure_time': '09:45', 'driver': 'Arjun', 'truck_number': 'CG 04 8129'},
{'start': 'Rajnandgaon', 'end': 'Balod', 'departure_time': '12:15', 'driver': 'Arjun', 'truck_number': 'CG 04 9533'},
{'start': 'Dhamtari', 'end': 'Bhatapara', 'departure_time': '14:30', 'driver': 'Prince', 'truck_number': 'CG 04 8624'},
{'start': 'Mahasamund', 'end': 'Mungeli', 'departure_time': '16:00', 'driver': 'Rahul', 'truck_number': 'CG 04 9121'},
{'start': 'Balod', 'end': 'Kanker', 'departure_time': '17:45', 'driver': 'Arjun', 'truck_number': 'CG 04 9874'},
{'start': 'Bhatapara', 'end': 'Raipur', 'departure_time': '19:30', 'driver': 'Abhishek', 'truck_number': 'CG 04 3786'},
{'start': 'Mungeli', 'end': 'Jagdalpur', 'departure_time': '21:15', 'driver': 'Amit', 'truck_number': 'CG 04 6460'},
{'start': 'Kanker', 'end': 'Durg', 'departure_time': '10:45', 'driver': 'Sonu', 'truck_number': 'CG 04 7630'},
{'start': 'Raipur', 'end': 'Ambikapur', 'departure_time': '12:30', 'driver': 'Vikram', 'truck_number': 'CG 04 2012'}
]

def find_matching_truck(start, end, time):
    time_format = '%H:%M'

    input_time = datetime.strptime(time, time_format)

    for truck in current_running_trucks:
        truck_start_time = datetime.strptime(truck['departure_time'], time_format)

        time_window_start = truck_start_time - timedelta(hours=2)
        time_window_end = truck_start_time + timedelta(hours=2)

        if time_window_start <= input_time <= time_window_end:
            return truck

    return None

def calculate_pooling(start, end, time):
    matching_truck = find_matching_truck(start, end, time)
    if matching_truck:
        check = (
            "Truck number: "+matching_truck['truck_number'] +
            '<br><br>From city: ' + start +
            '<br><br>To: ' + end +
            '<br><br>Time: ' + time +
            '<br><br>With driver: ' + matching_truck['driver']
        )
        return f"<h3>Pooling is available<h3> <br><br>{check}"
    else:
        return "No truck available for pooling right now"




@app.route('/pool', methods=['GET', 'POST'])
def pool():
    if request.method == 'POST':
        # Get start, end, and time from the form
        start_node = request.form['start_node']
        end_node = request.form['end_node']
        departure_time = request.form['departure_time']

        # Perform pooling calculation
        pooling_result = calculate_pooling(start_node, end_node, departure_time)

        return render_template('pool.html', cities=cities_in_chhattisgarh.keys(), result=pooling_result)

    return render_template('pool.html', cities=cities_in_chhattisgarh.keys(), result=None)


if __name__ == '__main__':
    app.run(debug=True)
