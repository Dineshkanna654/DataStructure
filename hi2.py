import requests
import json
import os
from typing import Optional, Dict, Any
from datetime import datetime
from bs4 import BeautifulSoup

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
                'reg_no': student_id,
                'html_content': response.text,
                'status_code': response.status_code
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'reg_no': student_id,
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
    
    def get_results_for_multiple_students(self, student_ids: list) -> list:
        """
        Fetch exam results for multiple student IDs
        
        Args:
            student_ids (list): List of student IDs
            
        Returns:
            list: List of dictionaries with reg_no and html_content for successful requests
        """
        
        results = []
        
        print(f"Processing {len(student_ids)} student IDs...")
        print("-" * 50)
        
        for i, student_id in enumerate(student_ids, 1):
            print(f"Processing {i}/{len(student_ids)}: {student_id}")
            
            result = self.get_exam_results(student_id)
            
            if result['success']:
                # Add to results list with the required format
                results.append({
                    'reg_no': result['reg_no'],
                    'html_content': result['html_content']
                })
                print(f"✅ Success - HTML content retrieved")
            else:
                print(f"❌ Failed - Error: {result['error']}")
            
            print()
        
        return results

def html_to_json_beautifulsoup(html_content):
    """
    Parse HTML and extract structured data using BeautifulSoup
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract student information
    student_data = {}
    
    # Get student basic info from the first table
    main_table = soup.find('table', {'width': '70%'})
    if main_table:
        rows = main_table.find_all('tr')
        if len(rows) > 1:  # Skip header row
            cells = rows[1].find_all('td')
            if len(cells) >= 3:
                student_data['registration_number'] = cells[0].get_text(strip=True)
                student_data['name'] = cells[1].get_text(strip=True)
                student_data['course'] = cells[2].get_text(strip=True)
    
    # Extract CGPA and SGPA information
    cgpa_tables = soup.find_all('table', {'border': '1'})
    for table in cgpa_tables:
        rows = table.find_all('tr')
        if len(rows) >= 2:
            headers = [th.get_text(strip=True) for th in rows[0].find_all('td')]
            values = [td.get_text(strip=True) for td in rows[1].find_all('td')]
            
            for header, value in zip(headers, values):
                if 'Credits Earned' in header:
                    try:
                        student_data['credits_earned'] = int(value)
                    except ValueError:
                        student_data['credits_earned'] = value
                elif 'CGPA' in header:
                    try:
                        student_data['cgpa'] = float(value)
                    except ValueError:
                        student_data['cgpa'] = value
                elif 'SGPA' in header:
                    try:
                        student_data['sgpa'] = float(value)
                    except ValueError:
                        student_data['sgpa'] = value
    
    # Extract subject grades
    subjects = []
    grade_table = soup.find('table', {'width': '65%'})
    if grade_table:
        rows = grade_table.find_all('tr')
        for row in rows[1:]:  # Skip header row
            cells = row.find_all('td')
            if len(cells) >= 5:
                subject = {
                    'semester': cells[0].get_text(strip=True),
                    'code': cells[1].get_text(strip=True),
                    'subject': cells[2].get_text(strip=True),
                    'grade': cells[3].get_text(strip=True),
                    'credit': cells[4].get_text(strip=True)
                }
                subjects.append(subject)
    
    student_data['subjects'] = subjects
    
    return student_data

def process_all_results(results):
    """
    Process all HTML results and convert them to JSON format
    
    Args:
        results (list): List of dictionaries with 'reg_no' and 'html_content'
        
    Returns:
        list: List of processed student data in JSON format
    """
    processed_results = []
    
    for result in results:
        try:
            # Parse HTML content for each student
            student_data = html_to_json_beautifulsoup(result['html_content'])
            
            # Add registration number if not already present
            if 'registration_number' not in student_data:
                student_data['registration_number'] = result['reg_no']
            
            processed_results.append(student_data)
            print(f"✅ Successfully processed: {result['reg_no']}")
            
        except Exception as e:
            print(f"❌ Error processing {result['reg_no']}: {str(e)}")
            # Add error information to results
            processed_results.append({
                'registration_number': result['reg_no'],
                'error': str(e),
                'raw_html': result['html_content'][:200] + "..." if len(result['html_content']) > 200 else result['html_content']
            })
    
    return processed_results

def save_results_to_file(processed_results, filename='exam_results.json'):
    """
    Save processed results to a JSON file
    
    Args:
        processed_results (list): List of processed student data
        filename (str): Output filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(processed_results, f, indent=2, ensure_ascii=False)
        print(f"✅ Results saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving to file: {str(e)}")

def main():
    """
    Example usage of the Karunya Exam API for multiple students
    """
    
    # Initialize the API client
    api = KarunyaExamAPI()
    
    # Multiple students - replace with actual student IDs
    student_ids = [
        "PRK24AD1007",
        # Add more student IDs here
        # "PRK24AD1008",
        # "PRK24AD1009",
    ]
    
    print(f"Processing multiple students:")
    print("=" * 60)
    
    # Get HTML results for all students
    results = api.get_results_for_multiple_students(student_ids)
    
    if not results:
        print("❌ No results retrieved. Check student IDs and network connection.")
        return []
    
    print(f"\n📊 Retrieved {len(results)} successful results")
    print("=" * 60)
    
    # Process all HTML content to JSON
    print("\nProcessing HTML to JSON:")
    print("-" * 30)
    processed_results = process_all_results(results)
    
    # Display first result as example
    if processed_results:
        print("\n📋 Sample processed result:")
        print("-" * 30)
        print(json.dumps(processed_results[0], indent=2, ensure_ascii=False))
        
        # Save all results to file
        save_results_to_file(processed_results)
    
    return processed_results

if __name__ == "__main__":
    main()