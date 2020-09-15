import re
import os
import time
import json
import requests
import urllib.request

time.sleep(5)

URL = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"

try:
    image_data = json.loads(requests.get(URL).text)
    image_url = 'http://www.bing.com' + image_data['images'][0]['url']
    
    # url for better quality image
    image_download_url = 'http://www.bing.com/hpwp/' + image_data['images'][0]['hsh']
    image_name = image_url[re.search("rb/", image_url).end():re.search('_EN', image_url).start()] + '.jpg'
    
    file_path = os.environ['HOME'] + '/Pictures/Bing_Pic_of_the_Day/' + image_name
    if os.path.exists(file_path) is False:
        try:
            # try downloading by first url(better quality)
            urllib.request.urlretrieve(image_download_url, filename=file_path)
        except urllib.error.HTTPError:
            # if first url fails
            urllib.request.urlretrieve(image_url, filename=file_path)
        image_desc = image_data['images'][0]['copyright']

        command = 'gsettings set org.gnome.desktop.background picture-uri file://'+file_path
        os.system(command)
        notify = 'notify-send -u critical "Wallpaper for the Day updated!" "' + image_desc + '"'
        os.system(notify)
    else:
        # wallpaper alredy updated!!
        notify = 'notify-send -u critical "Bing Wallpaper" "Wallpaper for the day has been updated already!"'
        os.system(notify)

except:
    # If no network connection or sometinh wrong occurs....Who cares ??
    notify = 'notify-send -u critical "Bing Wallpaper" "Wallpaper can\'t be updated!"'
    os.system(notify)
