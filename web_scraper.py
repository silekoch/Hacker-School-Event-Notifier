from bs4 import BeautifulSoup
import requests
import os
import pickle
from datetime import datetime

class Event:
    def __init__(self, title: str, datetime: datetime, description: str):
        self.title = title
        self.datetime = datetime
        self.description = description
    
    def __str__(self) -> str:
        return  f'{self.title}: {self.datetime}'

    def __repr__(self) -> str:
        return f'{self.title}, {self.datetime}, {self.description}'

events = set()

url = 'https://hacker-school.de/unterstuetzen/inspirer/checkin-inspirer-yourschool/?formats%5B0%5D=ys'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

def find_events_on_page(soup: BeautifulSoup) -> set:
    event_divs = soup.find_all('div', class_='hs-event')
    events = set()
    for event_div in event_divs:
        title = event_div.find('h3', class_='hs-event-titel').text
        dates_div = event_div.find('div', class_='hs-dates')
        date_and_time = dates_div.find_all('span')[1].text
        course_description = event_div.find('span', class_='hs-curse-discription').text
        events.add(Event(title, date_and_time, course_description))
    return events

# Initialize known_events as an empty set
known_events = set()

# File path where known events are stored
known_events_file_path = 'data/known_events.pkl'

# Check if the file exists
if os.path.exists(known_events_file_path):
    # If the file exists, load the known events from the file
    with open(known_events_file_path, 'rb') as file:
        known_events = pickle.load(file)
found_events = set(find_events_on_page(soup))  # Convert the list of found events to a set

new_events = found_events - known_events  # Find the difference between the found events and known events

# Print the new events
print('\n'.join([str(e) for e in new_events]))

# Update known_events with the new events
known_events.update(new_events)

