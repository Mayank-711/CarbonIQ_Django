from django.shortcuts import render,redirect

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
        time_taken = request.POST.get("time_taken")
        electric_vehicle = request.POST.get("electric_vehicle", "No") == "Yes"
        passengers = request.POST.get("passengers")
        # Fetch calculated distance and time from the frontend API response
        api_distance = request.POST.get("calculated_distance", "0")  # in kilometers
        api_duration = request.POST.get("calculated_duration", "0")  # in minutes

        # Print trip data for debugging
        print("Source Address:", source_address)
        print("Source Coordinates:", f"{source_lat}, {source_lng}")
        print("Destination Address:", destination_address)
        print("Destination Coordinates:", f"{dest_lat}, {dest_lng}")
        print("Mode of Transport:", mode_of_transport)
        print("Date:", date)
        print("Time Taken (User Entered, minutes):", time_taken)
        print("API Calculated Distance (km):", api_distance)
        print("API Calculated Duration (minutes):", api_duration)
        print("Electric Vehicle:", electric_vehicle)
        print("User:",user)
        print("Passengers:",passengers)
        
    return render(request, 'mainapp/logtrip.html')

def leaderboards(request):
    return render(request,'mainapp/leaderboards.html')