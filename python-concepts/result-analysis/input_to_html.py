import requests
import json
import pandas as pd
from typing import List, Dict, Any, Optional
import re
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KarunyaExamAPI:
    """
    Enhanced Python class to interact with Karunya University's exam results API
    with Excel data processing capabilities
    """
    
    def __init__(self, delay_between_requests: float = 1.0):
        self.base_url = "https://web.karunya.edu/exam/exammay25result.asp"
        self.session = requests.Session()
        self.delay_between_requests = delay_between_requests
        
        # Set common headers that might be expected
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://web.karunya.edu/exam/exammay25result.asp'
        })
    
    def parse_excel_data(self, excel_file_path: str) -> List[Dict[str, str]]:
        """
        Parse Excel file to extract registration numbers and DOBs
        Expected format: Column A has Reg_no, Column B has DOB
        
        Args:
            excel_file_path (str): Path to the Excel file
            
        Returns:
            list: List of dictionaries with reg_no and dob
        """
        try:
            # Read the Excel file
            df = pd.read_excel(excel_file_path)
            
            # Print column names for debugging
            logger.info(f"Excel columns: {df.columns.tolist()}")
            
            # Try to find registration number and DOB columns
            reg_col = None
            dob_col = None
            
            # Look for registration number column
            for col in df.columns:
                col_name = str(col).lower()
                if any(keyword in col_name for keyword in ['reg', 'registration', 'student']):
                    reg_col = col
                    break
            
            # Look for DOB column  
            for col in df.columns:
                col_name = str(col).lower()
                if any(keyword in col_name for keyword in ['dob', 'password', 'date of birth']):
                    dob_col = col
                    break
            
            # If not found by name, assume first two columns are reg_no and dob
            if reg_col is None and len(df.columns) >= 1:
                reg_col = df.columns[0]
            if dob_col is None and len(df.columns) >= 2:
                dob_col = df.columns[1]
                
            if reg_col is None:
                logger.error("Could not identify registration number column")
                return []
                
            logger.info(f"Using columns - Reg No: '{reg_col}', DOB: '{dob_col}'")
            
            # Extract data
            student_data = []
            for index, row in df.iterrows():
                print("Rows-------------:", row)
                reg_no = str(row[reg_col]).strip() if pd.notna(row[reg_col]) else ""
                dob = str(row[dob_col]).strip() if pd.notna(row[dob_col]) and dob_col else ""
                
                # Skip empty rows or header rows
                if not reg_no or reg_no.lower() in ['reg.no']:
                    continue
                    
                # Clean up the data
                if reg_no:
                    # Ensure DOB is in correct format (remove any decimal points from pandas)
                    if dob and '.' in dob:
                        dob = dob.split('.')[0]
                    
                    if len(dob) == 7:
                        # If DOB is like 0312203, convert to 03122003
                        dob = '0' + dob
                    
                    student_data.append({
                        'reg_no': reg_no,
                        'dob': dob
                    })
            
            logger.info(f"Extracted {len(student_data)} student records from Excel")
            return student_data
            
        except Exception as e:
            logger.error(f"Error parsing Excel file: {str(e)}")
            return []
    
    def get_exam_results(self, reg_no: str, dob: str) -> Dict[str, Any]:
        """
        Fetch exam results for a given registration number and DOB
        
        Args:
            reg_no (str): Registration number (like PRK24AD1007)
            dob (str): Date of birth in format like 03122003
            
        Returns:
            dict: API response containing exam results or error information
        """
        
        # Form data based on typical form submission
        form_data = {
            't1': reg_no,
            't2': dob,
            'B1': 'Submit'
        }
        
        try:
            # Add delay to be respectful to the server
            time.sleep(self.delay_between_requests)
            
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
                'reg_no': reg_no,
                'dob': dob
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {reg_no}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None,
                'reg_no': reg_no,
                'dob': dob,
                'content': ''
            }
    
    def process_all_students(self, student_data: List[Dict[str, str]], max_workers: int = 3) -> List[Dict[str, Any]]:
        """
        Process all students and get their exam results
        
        Args:
            student_data (list): List of student data with reg_no and dob
            max_workers (int): Maximum number of concurrent requests
            
        Returns:
            list: List of results in the desired format
        """
        results = []
        
        # Use ThreadPoolExecutor for concurrent requests (be careful not to overwhelm the server)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all requests
            future_to_student = {
                executor.submit(self.get_exam_results, student['reg_no'], student['dob']): student
                for student in student_data
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_student):
                student = future_to_student[future]
                try:
                    result = future.result()
                    
                    # Format the result as requested
                    formatted_result = {
                        "reg_no": result['reg_no'],
                        "html_content": result['content']
                    }
                    
                    # Add additional info for debugging if needed
                    if not result['success']:
                        formatted_result["error"] = result.get('error', 'Unknown error')
                        formatted_result["status_code"] = result.get('status_code')
                    
                    results.append(formatted_result)
                    
                    logger.info(f"Processed {student['reg_no']} - Success: {result['success']}")
                    
                except Exception as exc:
                    logger.error(f"Error processing {student['reg_no']}: {str(exc)}")
                    results.append({
                        "reg_no": student['reg_no'],
                        "html_content": "",
                        "error": str(exc)
                    })
        
        return results
    
    def save_results(self, results: List[Dict[str, Any]], output_file: str = "exam_results.json"):
        """
        Save results to a JSON file
        
        Args:
            results (list): List of exam results
            output_file (str): Output file path
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logger.info(f"Results saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")

def main():
    """
    Main function to demonstrate the enhanced API usage
    """
    
    # Initialize the API client
    api = KarunyaExamAPI(delay_between_requests=1.0)  # 1 second delay between requests
    
    print("🎓 Karunya Exam Results Fetcher")
    print("=" * 50)
    
    # Parse from Excel file
    excel_file_path = input("Enter the path to your Excel file (or press Enter for default 'student_data.xlsx'): ").strip()
    if not excel_file_path:
        excel_file_path = 'student_data.xlsx'
    
    print(f"📊 Reading data from: {excel_file_path}")
    student_data = api.parse_excel_data(excel_file_path)
    
    if not student_data:
        print("❌ No student data found. Please check your Excel file format.")
        print("Expected format: Column A = Registration Number, Column B = DOB")
        return
    
    print(f"✅ Found {len(student_data)} students to process")
    
    # Display first few entries for confirmation
    print("\n📋 Sample data:")
    for i, student in enumerate(student_data[:3]):
        print(f"  {i+1}. {student['reg_no']} - DOB: {student['dob']}")
    
    if len(student_data) > 3:
        print(f"  ... and {len(student_data) - 3} more")
    
    # Confirm before proceeding
    proceed = input(f"\n🚀 Proceed to fetch results for {len(student_data)} students? (y/n): ").strip().lower()
    if proceed not in ['y', 'yes']:
        print("Operation cancelled.")
        return
    
    print("\n⏳ Fetching exam results...")
    print("This may take a while depending on the number of students...")
    
    # Process all students
    results = api.process_all_students(student_data, max_workers=2)  # Reduced workers to be respectful
    
    print(f"\n✅ Processing complete! Retrieved {len(results)} results")
    
    # Show summary
    successful = sum(1 for r in results if 'error' not in r or not r.get('error'))
    failed = len(results) - successful
    
    print(f"📊 Summary:")
    print(f"  ✅ Successful: {successful}")
    print(f"  ❌ Failed: {failed}")
    
    # Save results
    output_file = "karunya_exam_results.json"
    api.save_results(results, output_file)
    
    print(f"\n💾 Results saved to: {output_file}")
    print("\n🎉 Done!")
    
    # Display first result as sample
    if results:
        print(f"\n📄 Sample result for {results[0]['reg_no']}:")
        html_preview = results[0]['html_content'][:200] + "..." if len(results[0]['html_content']) > 200 else results[0]['html_content']
        print(f"HTML Content Preview: {html_preview}")

if __name__ == "__main__":
    main()