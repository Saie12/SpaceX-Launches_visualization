from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", launches=launches)

@app.template_filter("date_only")
def date_only_filter(s):
    date_object = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_object.date()

def fetch_spacex_launches():
    url = "https://api.spacexdata.com/v4/launches"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return []

def categorize_launches(launches):
    successful = list(filter(lambda x: x["success"] and not x["upcoming"], launches))
    failed = list(filter(lambda x: not x["success"] and not x["upcoming"], launches))
    upcoming = list(filter(lambda x: x["upcoming"], launches))

    return {
        "successful": successful,
        "failed": failed,
        "upcoming": upcoming
    }

launches = categorize_launches(fetch_spacex_launches())

if __name__ == "__main__":
    app.run(debug=True)

# List of online image URLs
image_urls = [
    "https://c4.wallpaperflare.com/wallpaper/18/491/722/technology-spacex-falcon-9-lift-off-wallpaper-preview.jpg",
    "https://c4.wallpaperflare.com/wallpaper/459/777/198/heat-fire-rocket-spacex-booster-hd-wallpaper-preview.jpg",
    "https://c4.wallpaperflare.com/wallpaper/769/114/520/falcon-heavy-spacex-rocket-astronautics-wallpaper-preview.jpg",
    "https://c4.wallpaperflare.com/wallpaper/559/647/739/5c1cc0125bccc-wallpaper-preview.jpg",
    "https://c1.wallpaperflare.com/preview/987/704/26/atlantis-space-shuttle-rocket-launch-pad-thumbnail.jpg"
    # Add more image URLs as needed
]

# Generate dynamic CSS for background image slideshow
css_rule = """
@keyframes slideshow {
"""
for i, url in enumerate(image_urls):
    css_rule += f"  {i * (100 / len(image_urls))}% {{ background-image: url('{url}'); }}\n"
css_rule += "}"

# Write the generated CSS rule to a CSS file
with open("static/css/background_slideshow.css", "w") as css_file:
    css_file.write(css_rule)
