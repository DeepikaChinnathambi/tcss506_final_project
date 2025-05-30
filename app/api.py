#Ticketmaster API integration logic

import os
import requests
from datetime import datetime
from flask import current_app
from app.models import Event, db

class TicketmasterAPI:
    def __init__(self):
        self.api_key = os.getenv('TICKETMASTER_API_KEY')
        if not self.api_key:
            self.api_key = os.environ.get('TICKETMASTER_API_KEY')
        if not self.api_key:
            raise ValueError("Please set your TICKETMASTER_API_KEY environment variable")
        self.base_url = 'https://app.ticketmaster.com/discovery/v2'

    def search_events(self, keyword=None, city=None, state=None, start_date=None, end_date=None, page=0, size=20):
        """
        Search for events using various filters
        """
        params = {
            'apikey': self.api_key,
            'page': page,
            'size': size,
            'countryCode': 'US',
        }
        
        if keyword:
            params['keyword'] = keyword
        if city:
            params['city'] = city
        if state:
            params['stateCode'] = state
        if start_date:
            params['startDateTime'] = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        if end_date:
            params['endDateTime'] = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        response = requests.get(f"{self.base_url}/events", params=params)
        response.raise_for_status()
        return response.json()

    def get_event_details(self, event_id):
        """
        Get detailed information about a specific event
        """
        params = {'apikey': self.api_key}
        response = requests.get(f"{self.base_url}/events/{event_id}", params=params)
        response.raise_for_status()
        return response.json()

    def save_event_to_db(self, event_data):
        """
        Save or update event information in the database
        """
        try:
            # Extract relevant information from the event data
            event_id = event_data['id']
            name = event_data['name']
            
            # Check if event already exists
            event = Event.query.filter_by(event_id=event_id).first()
            if not event:
                event = Event(event_id=event_id)

            # Update event information
            event.name = name
            event.description = event_data.get('description', '')
            
            dates = event_data.get('dates', {}).get('start', {})
            if dates:
                event.start_date = datetime.fromisoformat(dates.get('dateTime', '').replace('Z', '+00:00'))
            
            if '_embedded' in event_data and 'venues' in event_data['_embedded']:
                venue = event_data['_embedded']['venues'][0]
                event.venue_name = venue.get('name', '')
                event.venue_city = venue.get('city', {}).get('name', '')
                event.venue_state = venue.get('state', {}).get('stateCode', '')

            if 'images' in event_data and event_data['images']:
                event.image_url = event_data['images'][0].get('url', '')

            event.ticket_url = event_data.get('url', '')
            
            if 'priceRanges' in event_data:
                price_range = event_data['priceRanges'][0]
                event.price_range = f"${price_range['min']} - ${price_range['max']}"

            db.session.add(event)
            db.session.commit()
            return event
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error saving event: {str(e)}")
            raise

# Create a singleton instance
ticketmaster_api = TicketmasterAPI()
