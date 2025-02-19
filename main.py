import pandas as pd # Required to handle excel file and edit it
import isodate  # Required for parsing ISO 8601 durations
from googleapiclient.discovery import build # Gives access to use API
from video_id import all_video_content_id_s  # Importing list of video id's from another video_id .py

API_KEY = "" # You Tube API key ( ❗PLACE YOURS❗ )
CHANNEL_ID = "UCMdN6_SvFFQZZiC_fNfCk3A" # ID of the channel that we want to scrape
youtube = build("youtube", "v3", developerKey=API_KEY) # Initializing You Tube API

def get_video_details(video_ids): # Creating function to fetch data from the list
    all_video_data = [] # Creating empty list for fetched video id's

    for i in range(0, len(video_ids), 50):  # YouTube API allows 50 videos per request
        request = youtube.videos().list( # Request to You Tube video list
            part="snippet,contentDetails,statistics", # Part is snippet, contentDetails, statistics
            id=",".join(video_ids[i:i+50]) # Creating comma seperated string from a list of video id's
        )
        response = request.execute() # Executes the API request and retrieves YouTube's JSON response

        for video in response.get("items", []): # Loops through videos; avoids errors if "items" is missing
            try: # Tries...
                duration = isodate.parse_duration(video["contentDetails"]["duration"]).total_seconds() # YouTube's API provides ISO 8601 formatted duration (PT5M30S → 5 minutes 30 seconds) Converts this ISO 8601 into python timedelta and extracts time duration in seconds
                data = { # It collect all informations into a structured format
                    "Video Title": video["snippet"]["title"], # Fetch video title from response
                    "Video Length (seconds)": duration, # Fetch video length from response
                    "Upload Date and Time": video["snippet"]["publishedAt"], # Fetching uploaded time from response
                    "View Count": int(video["statistics"].get("viewCount", 0)), # Fetching view count from response
                    "Like Count": int(video["statistics"].get("likeCount", 0)), # Fetching like count from response
                    "Comment Count": int(video["statistics"].get("commentCount", 0)), # Fetching comment count from response
                    "Description": video["snippet"]["description"], # Fetching description from response
                    "Tags": ", ".join(video["snippet"].get("tags", [])), # Fetching tags from response
                    "Thumbnail URL": video["snippet"]["thumbnails"]["high"]["url"], # Fetching Thumbnail URL from response
                    "Category": video["snippet"]["categoryId"] # Fetching Category from response
                }
                all_video_data.append(data) 
            except Exception as e: # Catches errors (e.g., missing fields) and prevents script from crashing
                print(f"⚠️ Error processing video {video['id']}: {e}") # Print any error into terminal, because of {e}

    return all_video_data # Returns the all_video_data list, which contains dictionaries of video details

video_data = get_video_details(all_video_content_id_s) # Runs the code and fetches video details. Returned list is stored in video_data

df = pd.DataFrame(video_data) # This two code lines is used for saving video data into (.xlsx) Excel file
output_file = r"C:\Users\user\Desktop\excel's\youtube_videos.xlsx" # We gave path, where to save the Excel file
df.to_excel(output_file, index=False)

print(f"✅ Data saved to {output_file}") # Prints success message into Terminal