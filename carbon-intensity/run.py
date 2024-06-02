import os, requests
from PIL import Image, ImageDraw, ImageFont
import schedule
import time

def text_to_bitmap(text, brightness=255, font_file="lexis.ttf"):
    width=24
    height=12

    # Create a new image with white background
    image = Image.new('1', (width, height), 1)
    draw = ImageDraw.Draw(image)

    font_path = os.path.join(os.path.dirname(__file__), font_file)
    
    font_size = 1
    font = ImageFont.truetype(font_path, font_size)
    
    # Increment the font size until the text size exceeds the image size
    while True:
        font = ImageFont.truetype(font_path, font_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if text_width > width or text_height > height:
            font_size -= 1
            font = ImageFont.truetype(font_path, font_size)
            break
        font_size += 1
    
    # Calculate text position
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw the text onto the image
    draw.text((x, y), text, font=font, fill=0)
    
    # Convert image to a bitmap
    bitmap = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(brightness if image.getpixel((x, y)) == 0 else 0)
        bitmap.append(row)
    
    return bitmap


def get_current_carbon_intensity():
    api_url = "https://api.carbonintensity.org.uk/intensity"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        current_intensity = data['data'][0]['intensity']['actual']

        print(f"Got current carbon intensity: {current_intensity}")

        if current_intensity is None:
            current_intensity = data['data'][0]['intensity']['forecast']
            print("Falling back to forecasted carbon intensity because actual value is null")
        
        return str(current_intensity)
    else:
        print(f"Failed to get current carbon intensity. HTTP code: {response.status_code}")
        return "Error"

def run():
    # Create the base header
    headers = {
        "Authorization": f"Basic {os.environ['AUTH_TOKEN']}"
    }

    # Get basic info from environment
    host = os.getenv('SCREEN_API_HOST')
    app_name = os.getenv('APPLICATION_NAME')
    base_url = f"{host}/api/v1/screen"

    # Get screen info
    screen_info_url = f"{base_url}/application/{app_name}"
    rsp = requests.get(screen_info_url, headers=headers)
    if not rsp.ok:
        print("Failed to get screen info for application... exiting!!!")
        exit(1)

    # Get our screen id from the response
    first_screen = rsp.json()[0]
    screen_id = first_screen['_id']

    print(f"Got screen_id from response: {screen_id}")

    text = get_current_carbon_intensity()

    brightness = 255
    bitmap = text_to_bitmap(text, brightness)

    # Build up the request json
    payload = {
        "animationType": "static",
        "type": "bitmap",
        "value": bitmap,
        "brightness": brightness
    }

    # Try to update
    screen_update_url = f"{base_url}/{screen_id}"
    rsp = requests.patch(screen_update_url, headers=headers, json=payload)
    if not rsp.ok:
        print("Failed updating screen for application")
        print(rsp.json())
        exit(1)

    print(f"Updated Home Pro display with bitmap!")

run() # Run immediately to begin with, then periodically
schedule.every(10).minutes.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)