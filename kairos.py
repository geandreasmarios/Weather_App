import tkinter as tk
import requests
import datetime
from PIL import Image, ImageTk

BIG_FONT = ("Arial", 32, "bold")
MEDIUM_FONT = ("Arial", 16, "bold")

BACK_COLOR = "#481594"
FRONT_COLOR = "white"
REFRESH_COLOR = "#d47b15"

NEXT_DAYS = 4

GEOLOC_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

WIND_DIRECTIONS = [
    "Βόρειος", 
    "Βορειοανατολικός",
    "Ανατολικός",
    "Νοτιοανατολικός",
    "Νότος",
    "Νοτιοδυτικός",
    "Δυτικός",
    "Βορειοδυτικός"
]

#Αντιστοίχιση καιρικων φαινομενων
WEATHER_DESCRIPTIONS = {
    0  : "Καθαρός Ουρανός ",
    1  : "Κυρίως Καθαρός ",
    2  : "Μερικώς Συννεφιασμένος",
    3  : "Συννεφιά",
    45 : "Ομίχλη",
    48 : "Εναπόθεση Ομίχλης Ριμών",
    51 : "Ψιλοβρέχει",
    53 : "Μέτρια Βροχή",
    55 : "Ψιλόβροχο Πυκνής Εντασης",
    56 : "Παγωμένο Ψιλόβροχο", 
    57 : "Πυκνή Ενταση Ψηχαλας ",
    61 : "Βροχή Ασθενής",
    63 : "Βροχή Μέτρια",
    65 : "Βροχή Εντονης Εντασης",
    66 : "Παγωμένη Βροχή Ελαφρύ",
    67 : "Παγωμένη Βροχή Εντονη Ενταση",
    71 : "Ελαφρα Χιονόπτωση",
    73 : "Μετρια Χιονόπτωση",
    75 : "Χιονόπτωση Εντονης Εντασης",
    77 : "Σπόροι Χιονιού",
    80 : "Ασθενη Βροχή",
    81 : "Βροχές: Μέτριες",
    82 : "Εντονες Βροχοπτωσεις",
    85 : "Μικρές Βροχές Χιονιού",
    86 : "Έντονες Βροχές Χιονιού",
    95 : "Καταιγίδα Ασθενής ή Μέτρια",
    96 : "Ελαφρά Καταιγίδα",
    99 : "Καταιγίδα Με Ισχυρό Χαλάζι"
}

#Αντιστοίχιση καιρικων φαινομενων με icons(Εικονες)
WHEATHER_ICONS = {
    0  : "hlios.png",
    1  : "hlios.png",
    2  : "sunefia.png",
    3  : "sunefia.png",
    45 : "omixlh.png",
    48 : "omixlh.png",
    51 : "psixala.png",
    53 : "psixala.png",
    55 : "broxh.png",
    56 : "xiononero.png", 
    57 : "psixala.png",
    61 : "psixala.png",
    63 : "psixala.png",
    65 : "broxh.png",
    66 : "xiononero.png",
    67 : "xiononero",
    71 : "xioni.png",
    73 : "xioni.png",
    75 : "xioni.png ",
    77 : "xiononero.png",
    80 : "psixala.png",
    81 : "psixala.png",
    82 : "broxh.png",
    85 : "xiononero.png",
    86 : "xioni.png",
    95 : "keravnoi.png",
    96 : "keravnoi.png",
    99 : "keravnoi_broxes_kategida.png"
}
#Οι επιλογες τις λιστας 
POLOIS = (
    "Athens",
    "Patra",
    "Thessaloniki",
    "Aigio"
)

window = tk.Tk()

window.geometry("600x400")
window.config(bg=BACK_COLOR)
window.title("Weather App ")

main_frame = None
weather_images = []
city_search_entry = None
#Αναζητηση πολης η χωρας
def create_main_frame(search_city=None):
    global main_frame, weather_images, city_search_entry
   
    if city_search_entry is not None and search_city is None:
        # pare to keimeno apo to label city_search_entry
        # kai balto sth metablhth search_city
        search_city = city_search_entry.get()
        city_search_entry.delete(0, tk.END)

    GEOLOC_API_PARAMS = {"name": search_city, "count": 1}

    geoloc_api_res = requests.get(GEOLOC_API_URL, params=GEOLOC_API_PARAMS)
    geoloc_data = geoloc_api_res.json()
    geoloc_best_result = geoloc_data["results"][0]

    city_name = geoloc_best_result["name"]
    latitude = geoloc_best_result["latitude"]
    longitude = geoloc_best_result["longitude"]

    
    WEATHER_API_PARAMS = {
        "latitude" : format(latitude, ".2f"), 
        "longitude": format(longitude, ".2f"), 
        "current_weather" : "true",
        "timezone": "Europe/Athens",
        "daily" : "weathercode",
        "start_date" : (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
        "end_date": (datetime.date.today() + datetime.timedelta(days=NEXT_DAYS)).strftime("%Y-%m-%d")
    }
    # Παιρνουμε τα δεδομενα καιρου μεσο API απο το διαδυκτιο
    api_res = requests.get(WEATHER_API_URL, params=WEATHER_API_PARAMS)
    weather_data = api_res.json()

    wd = weather_data["current_weather"]["weathercode"]
    ct = round(weather_data["current_weather"]["temperature"])
    wind_dir = weather_data["current_weather"]["winddirection"]
    wind_dir = int((wind_dir + (360 / 16))) % 360 // (360 // 8)

#Δημιουργια Buttons και τακτοποιηση widget
    if main_frame is not None:
        main_frame.destroy()

    main_frame = tk.Frame(window)
    main_frame.config(bg=BACK_COLOR)

    temperature_label = tk.Label(main_frame, text=f"{ct} °C", font=BIG_FONT, justify=tk.RIGHT, bg=BACK_COLOR, fg=FRONT_COLOR)
    temperature_label.pack(anchor=tk.E, padx=5,pady=5)

    city_frame = tk.Frame(main_frame)
    city_frame.config(bg=BACK_COLOR)

    city_label = tk.Label(city_frame, text=f"Πόλη: {city_name.title()}", justify=tk.LEFT, font=MEDIUM_FONT, bg=BACK_COLOR, fg=FRONT_COLOR)
    city_label.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)

    city_search_entry = tk.Entry(city_frame, font=MEDIUM_FONT, bg=BACK_COLOR, fg=FRONT_COLOR)
    city_search_entry.bind("<Return>", create_main_frame)
    city_search_entry.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)

    city_search_button = tk.Button(city_frame, text="Go", font=MEDIUM_FONT, bg=BACK_COLOR, fg=FRONT_COLOR, activebackground ="#d47b15", command=create_main_frame)
    city_search_button.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)

    city_frame.pack(anchor=tk.W, fill=tk.X, padx=5,pady=5)

    dt_now = datetime.datetime.now()
    dt_now_str = dt_now.strftime("%A, %d %B %y %H:%M")
    date_label = tk.Label(main_frame, text=f"Ημερομηνία: {dt_now_str}",justify=tk.LEFT, font=MEDIUM_FONT, bg=BACK_COLOR, fg=FRONT_COLOR)
    date_label.pack(anchor=tk.W, padx=5, pady=5)

    wind_label = tk.Label(main_frame, text=f"Ανεμος: {WIND_DIRECTIONS[wind_dir]}",justify=tk.LEFT, font=MEDIUM_FONT, bg=BACK_COLOR, fg=FRONT_COLOR)
    wind_label.pack(anchor=tk.W,padx=5,pady=5)

    weather_label = tk.Label(main_frame, text=f"Καιρος: {WEATHER_DESCRIPTIONS[wd]}",justify=tk.LEFT, font=MEDIUM_FONT, bg=BACK_COLOR, fg=FRONT_COLOR)
    weather_label.pack(anchor=tk.W,padx=5, pady=5)

    icons_frame = tk.Frame(main_frame)
    icons_frame.config(bg=BACK_COLOR)

    weather_images.clear()

    weather_image = Image.open(f"assets/{WHEATHER_ICONS[wd]}")
    weather_image = ImageTk.PhotoImage(weather_image)
    weather_image_label = tk.Label(icons_frame, image=weather_image, bg=BACK_COLOR)
    weather_image_label.grid(row=1, column=0, sticky=tk.NSEW,padx=5, pady=5)

    il = tk.Label(icons_frame, text="Σήμερα", font=MEDIUM_FONT, bg=BACK_COLOR, fg=FRONT_COLOR)
    il.grid(row=0, column=0, sticky=tk.NSEW)

    weather_images.append(weather_image)

    for column_index, [wd, date_str] in enumerate(zip(weather_data["daily"]["weathercode"], weather_data["daily"]["time"]), start=1):
        wi = Image.open(f"assets/{WHEATHER_ICONS[wd]}")
        wi = ImageTk.PhotoImage(wi)
        weather_image_label = tk.Label(icons_frame, image=wi, bg=BACK_COLOR)
        weather_image_label.grid(row=1, column=column_index, sticky=tk.NSEW,padx=5, pady=5)
        weather_images.append(wi)

        date_dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        day_str = date_dt.strftime("%A")


        il = tk.Label(icons_frame, text=day_str, font=MEDIUM_FONT, bg=BACK_COLOR, fg=FRONT_COLOR)
        il.grid(row=0, column=column_index, sticky=tk.NSEW)

    icons_frame.pack(fill=tk.X, anchor=tk.W, padx=5, pady=5)

    main_frame.pack(fill=tk.BOTH, expand=True)

#Αυτο μας βοηθαει στην επιλογη πολης απο τη λιστα
epilegmenh_polh = tk.StringVar()
epilegmenh_polh.set(POLOIS[-1])
drop = tk.OptionMenu(window, epilegmenh_polh, *POLOIS, command=create_main_frame)
drop.config(font=MEDIUM_FONT, bg=BACK_COLOR, fg=FRONT_COLOR)
drop.pack(side=tk.BOTTOM, anchor=tk.E, padx=5,pady=5)

create_main_frame("Aigio")
#Εδω γινεται η εκκινηση της εφαρμογης
window.mainloop()
