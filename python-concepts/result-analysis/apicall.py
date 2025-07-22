import requests
import json
from typing import Optional, Dict, Any

class KarunyaExamAPI:
    """
    A Python class to interact with Karunya University's exam results API
    """
    
    def __init__(self):
        self.base_url = "https://web.karunya.edu/exam/exammay25result.asp"
        self.session = requests.Session()
        
        # Set common headers that might be expected
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_exam_results(self, student_id: str, additional_params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Fetch exam results for a given student ID
        
        Args:
            student_id (str): The student ID (like PRK24AD1007)
            additional_params (dict, optional): Any additional form parameters
            
        Returns:
            dict: API response containing exam results or error information
        """
        
        # Form data based on the payload shown in your screenshot
        form_data = {
            't1': student_id,  # Assuming t1 is the student ID field
            't2': '03122003',  # This might be a date or another identifier
            'B1': 'Submit'     # Submit button
        }
        
        # Add any additional parameters if provided
        if additional_params:
            form_data.update(additional_params)
        
        try:
            # Make the POST request
            response = self.session.post(
                self.base_url,
                data=form_data,
                timeout=30
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            return {
                'success': True,
                'status_code': response.status_code,
                'content': response.text,
                'headers': dict(response.headers)
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
    
    def parse_results(self, html_content: str) -> Dict[str, Any]:
        """
        Parse the HTML response to extract exam results
        Note: This is a basic parser - you might need to adjust based on actual HTML structure
        
        Args:
            html_content (str): The HTML response from the API
            
        Returns:
            dict: Parsed results
        """
        try:
            # Basic HTML parsing - you might want to use BeautifulSoup for more complex parsing
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract relevant information (adjust selectors based on actual HTML)
            results = {
                'student_info': {},
                'grades': [],
                'raw_html': html_content
            }
            
            # Add your parsing logic here based on the actual HTML structure
            # Example:
            # tables = soup.find_all('table')
            # for table in tables:
            #     # Extract table data
            #     pass
            
            return results
            
        except ImportError:
            return {
                'error': 'BeautifulSoup not installed. Install with: pip install beautifulsoup4',
                'raw_html': html_content
            }
        except Exception as e:
            return {
                'error': f'Parsing error: {str(e)}',
                'raw_html': html_content
            }

def main():
    """
    Example usage of the Karunya Exam API
    """
    
    # Initialize the API client
    api = KarunyaExamAPI()
    
    # Example student ID (replace with actual student ID)
    student_id = "PRK24AD1007"
    
    print(f"Fetching exam results for student ID: {student_id}")
    print("-" * 50)
    
    # Get exam results
    result = api.get_exam_results(student_id)
    
    if result['success']:
        print("✅ Request successful!")
        print(f"Status Code: {result['status_code']}")
        print(f"Content Length: {len(result['content'])} characters")
        
        # Parse the results
        parsed_results = api.parse_results(result['content'])
        
        if 'error' not in parsed_results:
            print("\n📊 Parsed Results:")
            print(json.dumps(parsed_results, indent=2, default=str))
        else:
            print(f"\n⚠️  Parsing Error: {parsed_results['error']}")
            print("\nRaw HTML Response (first 500 chars):")
            print(result['content'][:500])
    else:
        print("❌ Request failed!")
        print(f"Error: {result['error']}")
        if result['status_code']:
            print(f"Status Code: {result['status_code']}")

if __name__ == "__main__":
    main()