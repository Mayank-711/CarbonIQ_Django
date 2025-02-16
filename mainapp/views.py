from django.shortcuts import render,redirect
from .ml.scripts.predict_co2 import predict_co2_emission
# Create your views here.


def homepage(request):
    return render(request, 'mainapp/homepage.html')



def logtrip(request):
    user = request.user

    if request.method == "POST":
        source_address = request.POST.get("source")
        source_lat = request.POST.get("source_lat")
        source_lng = request.POST.get("source_lng")
        destination_address = request.POST.get("destination")
        dest_lat = request.POST.get("dest_lat")
        dest_lng = request.POST.get("dest_lng")
        mode_of_transport = request.POST.get("mode_of_transport")
        date = request.POST.get("date")
        time_taken = float(request.POST.get("time_taken"))
        electric_vehicle = request.POST.get("electric_vehicle", "No") == "Yes"
        passengers = request.POST.get("passengers", 1)
        api_distance = float(request.POST.get("calculated_distance", "0"))  # in kilometers
        api_duration = float(request.POST.get("calculated_duration", "0"))  # in minutes

        # Debugging logs
        print("==== LOG TRIP DATA ====")
        print("Source:", source_address, "Coordinates:", f"{source_lat}, {source_lng}")
        print("Destination:", destination_address, "Coordinates:", f"{dest_lat}, {dest_lng}")
        print("Mode of Transport:", mode_of_transport)
        print("Electric Vehicle:", electric_vehicle)
        print("Passengers (Before Adjustment):", passengers)
        print("Distance (API):", api_distance, "km, Time Taken (API):", api_duration, "mins")
        print("Time Taken (User Entered):", time_taken, "User:", user)

        # Adjust passenger count for public transport
        public_transports = ["bus", "train", "metro", "actrain", "acbus"]
        if mode_of_transport in public_transports:
            passengers = 0

        # Convert "metro" and "train" to "etrain"
        if mode_of_transport in ["metro", "train"]:
            mode_of_transport = "etrain"

        # Add electric prefix if applicable
        if electric_vehicle and mode_of_transport not in ["actrain", "acbus", "etrain"]:
            mode_of_transport = "e" + mode_of_transport

        # Call the prediction function
        predicted_co2 = get_predictions(mode_of_transport, passengers, api_distance, api_duration,time_taken)

        # Debugging output
        print("Final Mode of Transport:", mode_of_transport)
        print("Passengers (Adjusted):", passengers)
        print(f"Predicted CO2 Emission: {predicted_co2:.2f}g")

        return render(request, 'mainapp/logtrip.html')

    return render(request, 'mainapp/logtrip.html')


def get_predictions(mode_of_transport, passengers, distance, time,time_taken):
    """
    Wrapper function to call the ML model's CO2 emission prediction.
    """

    # Adjust passenger count for electric vehicles
    passengers = float(passengers)
    

    # Call the ML model prediction function
    co2_count = predict_co2_emission(mode_of_transport, passengers, distance, time)
    if mode_of_transport == "ecar":
        new_passengers = passengers/2
        co2_count = co2_count/ new_passengers
    
    if time_taken > time:
        extra_time = float(time_taken) - time
        carbonfootprint_per_min = co2_count / time
        extra_co2 = extra_time * carbonfootprint_per_min
        co2_count += extra_co2
    
    return co2_count


def leaderboards(request):
    return render(request,'mainapp/leaderboards.html')