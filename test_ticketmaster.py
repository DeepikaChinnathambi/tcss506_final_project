import os
import requests

def test_ticketmaster_connection():
    api_key = os.getenv('TICKETMASTER_API_KEY')
    if not api_key:
        print("TICKETMASTER_API_KEY environment variable not set")
        return

    base_url = "https://app.ticketmaster.com/discovery/v2/events"
    
    # Test parameters
    params = {
        'apikey': api_key,
        'keyword': 'concert',
        'city': 'Seattle',
        'stateCode': 'WA',
        'countryCode': 'US',
        'size': 5
    }
    
    try:
        print("Testing Ticketmaster API connection...")
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        
        if '_embedded' in data and 'events' in data['_embedded']:
            events = data['_embedded']['events']
            print("Successfully retrieved events!")
            print(f"Found {len(events)} events")
            
            # Print details of first event
            if events:
                first_event = events[0]
                print("\nFirst event details:")
                print(f"Name: {first_event['name']}")
                print(f"Date: {first_event['dates']['start'].get('localDate', 'N/A')}")
                print(f"Venue: {first_event['_embedded']['venues'][0]['name']}")
                print(f"Ticket URL: {first_event.get('url', 'N/A')}")
        else:
            print("No events found in the response")
            print("Response structure:", data.keys())
            
    except requests.exceptions.RequestException as e:
        print("API Request Error:", str(e))
    except Exception as e:
        print("Error occurred:", str(e))

if __name__ == "__main__":
    test_ticketmaster_connection() 