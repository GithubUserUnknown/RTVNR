from django.shortcuts import render

import pymongo

# MongoDB connection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["carLocation"]
mycol = mydb["location"]

def index(request):
    # Fetch data from MongoDB
    car_locations = list(mycol.find())
    return render(request, 'index.html', {'car_locations': car_locations})

def search_plate(request):
    result = None
    if request.method == 'POST':
        number_plate = request.POST.get('number_plate')
        # Query the database for the number plate, sorted by current_time descending
        result = mycol.find({"recognized_plate": number_plate}).sort("current_time", pymongo.DESCENDING).limit(1)

        # Since find() returns a cursor, we need to convert it to a list and get the first item
        result = list(result)
        if result:
            result = result[0]  # Get the first record from the list

    return render(request, 'search_plate.html', {'result': result})

def car_location_history(request):
    records = []
    if request.method == 'POST':
        number_plate = request.POST.get('number_plate')
        # Query the database for all records for the number plate
        records = list(mycol.find({"recognized_plate": number_plate}).sort("current_time", pymongo.DESCENDING))
        

    return render(request, 'car_location_history.html', {'records': records})
