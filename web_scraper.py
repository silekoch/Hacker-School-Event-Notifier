from bs4 import BeautifulSoup
import requests
import os
import pickle

class Event:
    def __init__(self, title: str, datetime: str, description: str):
        self.title = title
        self.datetime = datetime
        self.description = description
    
    def __str__(self) -> str:
        return  f'{self.datetime}: {self.title}'

    def __repr__(self) -> str:
        return f'{self.title}, {self.datetime}, {self.description}'
    
    def __hash__(self) -> int:
        return hash((self.title, self.datetime, self.description))
    
    def __eq__(self, other) -> bool:
        return self.title == other.title and self.datetime == other.datetime and self.description == other.description

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

def scrape_hs_website_for_events() -> set:
    found_events = set()
    base_url = 'https://hacker-school.de/unterstuetzen/inspirer/checkin-inspirer-yourschool/?formats%5B0%5D=ys'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    pagination = soup.find('div', class_='hs-event-pagination')
    number_of_pages = int(pagination.find_all('li')[-2].text)

    for i in range(1, number_of_pages + 1):
        page_url = base_url + f'&page={i}'
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        found_events.update(find_events_on_page(soup))
    
    return found_events

def load_events_from_file(file_path: str) -> set:
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    return set()

def save_events_to_file(events: set, file_path: str):
    with open(file_path, 'wb') as file:
        pickle.dump(events, file)

known_events_file_path = 'data/known_events.pkl'
known_events = load_events_from_file(known_events_file_path)
found_events = scrape_hs_website_for_events()

new_events = found_events - known_events

save_events_to_file(found_events, known_events_file_path)
