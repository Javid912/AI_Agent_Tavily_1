import os
from tavily import TavilyClient
from typing import List, Dict
from tabulate import tabulate

# Initialize Tavily client
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")  # Get API key from environment variable
if not TAVILY_API_KEY:
    print("Error: TAVILY_API_KEY environment variable not set")
    exit(1)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

class InstagramLeadGenerator:
    def __init__(self):
        self.client = tavily_client

    def generate_leads(self, niche: str, location: str = None) -> List[Dict]:
        """
        Generate Instagram leads based on niche and location
        """
        search_query = f"instagram accounts {niche}"
        if location:
            search_query += f" in {location}"
        
        try:
            response = self.client.search(query=search_query)
            instagram_accounts = []
            
            # Process each result
            for result in response.get('results', []):
                if 'instagram.com' in result.get('url', '').lower():
                    instagram_accounts.append({
                        'url': result.get('url'),
                        'title': result.get('title'),
                        'snippet': result.get('snippet')
                    })
            
            return instagram_accounts[:30]  # Limit to 30 results
        except Exception as e:
            print(f"Error during search: {e}")
            return []

if __name__ == "__main__":
    generator = InstagramLeadGenerator()
    
    # Get user input
    niche = input("Enter the niche (e.g., fitness, food, travel): ").strip()
    location = input("Enter location (optional - press enter to skip): ").strip()
    
    # Validate input
    if not niche:
        print("Error: Niche is required")
        exit(1)
    
    location = location if location else None
    print(f"\nSearching for {niche} Instagram accounts{' in ' + location if location else ''}...")
    
    results = generator.generate_leads(niche, location)
    
    if results:
        # Prepare data for table
        table_data = [[i+1, result['title'], result['url']] 
                     for i, result in enumerate(results)]
        
        # Print table
        print("\nFound Instagram Accounts:")
        print(tabulate(table_data, 
                      headers=['#', 'Account', 'URL'],
                      tablefmt='grid'))
    else:
        print("\nNo Instagram accounts found.")
