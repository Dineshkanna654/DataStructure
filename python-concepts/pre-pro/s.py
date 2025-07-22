import re
import json
from bs4 import BeautifulSoup, Comment

def remove_escape_characters(html_content):
    """
    Remove common escape characters and normalize the HTML string
    """
    # Remove Windows line endings and normalize
    html_content = html_content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove common escape sequences
    escape_chars = {
        '\\n': '\n',      # Newline
        '\\t': '\t',      # Tab
        '\\r': '\r',      # Carriage return
        '\\"': '"',       # Escaped quotes
        "\\'": "'",       # Escaped single quotes
        '\\\\': '\\',     # Escaped backslash
        '\\b': '',        # Backspace (remove)
        '\\f': '',        # Form feed (remove)
        '\\v': '',        # Vertical tab (remove)
    }
    
    # Replace escape characters
    for escape_seq, replacement in escape_chars.items():
        html_content = html_content.replace(escape_seq, replacement)
    
    # Remove any remaining backslash followed by non-special characters
    html_content = re.sub(r'\\(.)', r'\1', html_content)
    
    # Clean up excessive whitespace but preserve intentional spacing
    html_content = re.sub(r'\n\s*\n\s*\n', '\n\n', html_content)  # Max 2 consecutive newlines
    
    return html_content

def extract_student_data(html_content):
    """
    Extract student data from HTML and return as JSON structure
    """
    
    # First remove escape characters
    html_content = remove_escape_characters(html_content)
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Initialize result structure
    result = {
        "reg_no": "",
        "name": "",
        "cgpa": 0.0,
        "sgpa": 0.0,
        "credits_earned": 0,
        "non_creds": 0,
        "subjects": []
    }
    
    # Extract basic student info
    try:
        # Find the student info table (first table with REG. NO., NAME, COURSE)
        info_table = soup.find('table', {'width': '70%'}) or soup.find_all('table')[1]
        if info_table:
            rows = info_table.find_all('tr')
            if len(rows) > 1:  # Skip header row
                cells = rows[1].find_all('td')
                if len(cells) >= 2:
                    result["reg_no"] = cells[0].get_text(strip=True)
                    result["name"] = cells[1].get_text(strip=True)
    except Exception as e:
        print(f"Warning: Could not extract student info: {e}")
    
    # Extract CGPA, SGPA, and Credits
    try:
        # Find tables with CGPA and SGPA data
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                for i, cell in enumerate(cells):
                    text = cell.get_text(strip=True).upper()
                    if 'CGPA' in text and i + 1 < len(cells):
                        try:
                            cgpa_text = cells[i + 1].get_text(strip=True)
                            result["cgpa"] = float(re.search(r'[\d.]+', cgpa_text).group())
                        except:
                            pass
                    elif 'SGPA' in text and i + 1 < len(cells):
                        try:
                            sgpa_text = cells[i + 1].get_text(strip=True)
                            result["sgpa"] = float(re.search(r'[\d.]+', sgpa_text).group())
                        except:
                            pass
                    elif 'CREDITS EARNED' in text and i + 1 < len(cells):
                        try:
                            credits_text = cells[i + 1].get_text(strip=True)
                            result["credits_earned"] = int(re.search(r'\d+', credits_text).group())
                        except:
                            pass
    except Exception as e:
        print(f"Warning: Could not extract GPA/Credits: {e}")
    
    # Extract subjects data
    try:
        # Find the subjects table (has SEM, CODE, SUBJECT, GRADE, CREDIT headers)
        subjects_table = None
        for table in soup.find_all('table'):
            header_row = table.find('tr')
            if header_row:
                headers = [td.get_text(strip=True).upper() for td in header_row.find_all(['td', 'th'])]
                if 'CODE' in headers and 'SUBJECT' in headers and 'GRADE' in headers:
                    subjects_table = table
                    break
        
        if subjects_table:
            # The table has malformed structure - subjects are not in proper <tr> tags
            # We need to get all <td> elements and group them manually
            
            all_cells = subjects_table.find_all('td')
            print(f"Found {len(all_cells)} cells in subjects table")
            
            # Skip the header cells (first 5 cells: SEM, CODE, SUBJECT, GRADE, CREDIT)
            header_count = 5
            data_cells = all_cells[header_count:]
            
            non_credit_count = 0
            
            # Group cells into subjects (each subject has 6 cells including the extra fuchsia cell)
            cells_per_subject = 6  # SEM, CODE, SUBJECT, GRADE, CREDIT, + extra cell
            
            for i in range(0, len(data_cells), cells_per_subject):
                if i + 4 < len(data_cells):  # Make sure we have at least 5 cells
                    try:
                        sem = data_cells[i].get_text(strip=True)
                        code = data_cells[i + 1].get_text(strip=True)
                        subject_name = data_cells[i + 2].get_text(strip=True)
                        grade = data_cells[i + 3].get_text(strip=True)
                        credits = data_cells[i + 4].get_text(strip=True)
                        
                        # Skip empty rows
                        if not code or not subject_name:
                            continue
                            
                        # Clean subject name (remove extra whitespace and newlines)
                        subject_name = re.sub(r'\s+', ' ', subject_name).strip()
                            
                        # Convert credits to int, handle special cases
                        try:
                            credits_int = int(credits) if credits.isdigit() else 0
                        except:
                            credits_int = 0
                            
                        # Count non-credit subjects
                        if credits_int == 0 or grade.upper() in ['COMPLETED']:
                            non_credit_count += 1
                        
                        subject_data = {
                            "code": code,
                            "name": subject_name,
                            "grade": grade,
                            "credits": credits_int
                        }
                        
                        result["subjects"].append(subject_data)
                        print(f"Extracted subject: {code} - {subject_name}")
                        
                    except Exception as e:
                        print(f"Warning: Could not parse subject at index {i}: {e}")
                        continue
            
            result["non_creds"] = non_credit_count
            
    except Exception as e:
        print(f"Warning: Could not extract subjects: {e}")
    
    return result

def html_to_json(html_string, output_file=None):
    """
    Convert HTML to JSON format
    
    Args:
        html_string (str): The HTML content as string
        output_file (str, optional): Output file path. If None, returns JSON string
    
    Returns:
        str: JSON formatted string
    """
    print("Removing escape characters...")
    print("Extracting student data...")
    
    student_data = extract_student_data(html_string)
    
    # Convert to JSON
    json_output = json.dumps(student_data, indent=2, ensure_ascii=False)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(json_output)
        print(f"✅ Data extracted and saved as '{output_file}'")
    
    print("\n📊 Extraction Summary:")
    print(f"- Student: {student_data['name']} ({student_data['reg_no']})")
    print(f"- CGPA: {student_data['cgpa']}, SGPA: {student_data['sgpa']}")
    print(f"- Credits Earned: {student_data['credits_earned']}")
    print(f"- Total Subjects: {len(student_data['subjects'])}")
    print(f"- Non-Credit Subjects: {student_data['non_creds']}")
    
    return json_output

def main():
    """Example usage"""
    
    # Your actual HTML string
    example_html = """
    <html>\r\n<head>\r\n\r\n<title>KITS Exam - Apr/May 2025 Results</title></head>\r\n<body  leftmargin=0 topmargin=0 marginheight=\"0\" marginwidth=\"0\" style=\"background-attachment: fixed\" bgcolor=#547DEB background=\"t2.jpg\">\r\n\r\n\r\n\r\n<center>\r\n<img src=\"http://www.karunya.edu/sites/default/files/logo.png.pagespeed.ce.rQZd6s4jcx.png\" alt=\"Porto\"></center>\r\n<TABLE WIDTH=\"87%\" BORDER=0 CELLSPACING=1 CELLPADDING=1>\r\n\t<TR>\r\n\r\n\t\t\r\n\t\t<TD width=\"1044\">\r\n\t\t<h2><font color=\"#0000FF\" face=\"Book Antiqua\">Exam Results - Apr/May \r\n\t\t2025 (</font><font face=\"Book Antiqua\" style=\"font-size: 15pt\" color=\"#008000\">All</font><font color=\"#008000\" face=\"Book Antiqua\"><span style=\"font-size: 15pt\"> \r\n\t\tStudents</span></font><font color=\"#0000FF\" face=\"Book Antiqua\">) </font>\r\n\t\t\r\n\t\t</h2>  \r\n\t\t</TD>\r\n\t\t<TD>\r\n\t\t<p align=\"center\"><b><a href=\"logout_new5.asp\">LOGOUT</a></b></TD>\t\t\r\n\t</TR>\r\n</TABLE>\r\n\r\n\r\n\r\n\r\n\r\n\r\n<TABLE border=3 borderColorDark=#c9beb6 borderColorLight=#000000 cellPadding=1 \r\ncellSpacing=1 width=\"70%\" align=center>\r\n\r\n\t<tr>\r\n\t\t<td ALIGN=\"middle\"><b>REG. NO.</b></td>\r\n\t\t<td ALIGN=\"middle\"><b>NAME</b></td>\r\n\t\t<td ALIGN=\"middle\"><b>COURSE</b></td>\r\n\r\n\t</tr>\r\n\r\n\t<tr>\r\n\t\t<td ALIGN=\"middle\">PRK24AD1007</td>\r\n\t\t<td ALIGN=\"middle\">SANJITH KRISHNA B</td>\r\n\t\t<td ALIGN=\"middle\">M.Sc.&nbsp;&nbsp;Artificial Intelligence and Data Science</td>\r\n\t\r\n\t</tr>\r\n</TABLE>\r\n<CENTER>\r\n<TABLE>\r\n\t<TR>\r\n\t\t<TD>\r\n\t\t\t<table BORDER=1 ALIGN=center>\r\n\t\t\t\t<tr>\r\n\t\t\t\t\t<td WIDTH=150 ALIGN=middle>Credits Earned</td> \r\n\t\t\t\t\t<td WIDTH=150 ALIGN=middle>CGPA</td> \r\n\t\t\t\t</tr>\r\n\t\t\t\t<tr>\r\n\t\t\t\t\t\r\n\t\t\t\t\t<TD ALIGN=middle><FONT COLOR=\"blue\" ><b>47</b></FONT></TD>\r\n\t\t\t\t\t\r\n\t\t\t\t\t<TD ALIGN=middle><FONT COLOR=\"blue\"><b>6.74</b></FONT></TD>\r\n\t\t\t\t\t\r\n\r\n\t\t\t\t</tr>\r\n\t\t\t</table>\r\n\t\t<TD WIDTH=10></TD>\r\n\t\t<TD>\r\n\t\t\t<table BORDER=1 ALIGN=center>\r\n\t\t\t\t<TR>\r\n\t\t\t\t\t<td WIDTH=150 ALIGN=middle>SGPA</td>\r\n\t\t\t\t</TR>\r\n\t\t\t\t<tr>\r\n\t\t\t\t\t\r\n\t\t\t\t\t<TD ALIGN=middle><FONT COLOR=\"blue\"><b>6.54</b></FONT></TD>\r\n\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t</tr>\r\n\t\t\t</table>\r\n\t\t</TD>\r\n\t\t<TD WIDTH=50></TD>\r\n\r\n\t\t<td>\r\n\t\t<table BORDER=1 ALIGN=center>\r\n\t\t\t\t<TR>\r\n\t\t\t\t\t<td WIDTH=150 ALIGN=middle>Non Academic Credits Earned</td>\r\n\t\t\t\t</TR>\r\n\t\t\t\t<tr>\r\n\t\t\t\t\t<TD ALIGN=middle><FONT COLOR=\"blue\"><b>1</b></FONT></TD>\r\n\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t</tr>\r\n\t\t\t</table>\r\n\r\n\t\t\r\n\t\t\r\n\t\t</td>\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t</TR>\r\n</TABLE>\r\n\t\r\n\t\r\n\t\r\n</CENTER>\r\n<small>\r\n\r\n\r\n<!--\r\n<CENTER><FONT size=3><STRONG>\r\n<FONT color=green >Congratulations ! &nbsp;&nbsp;&nbsp; You have cleared all papers !</FONT>  </FONT>\r\n</CENTER></STRONG>\r\n-->\r\n\r\n\r\n<center>\r\n\r\n<TABLE border=3 borderColorDark=#c9beb6 borderColorLight=#000000 cellPadding=1 \r\ncellSpacing=1 width=\"65%\">\r\n\r\n\r\n  <tbody>\r\n\r\n\r\n\r\n\r\n\r\n<tr ALIGN=\"middle\"><td><b>SEM</b></td><td><b>CODE</b></td><td><b>SUBJECT</b></td>\r\n<td><b>GRADE</b></td><td><b><b>CREDIT</b></b></td></tr></B>\r\n\r\n<td align=\"middle\"><font color=\"black\">  2</font></td>\r\n\r\n<td align=\"middle\"><font color=\"black\">  23CA3034</font></td>\r\n\r\n<td> <font color=\"black\"> Data Warehousing and Data Mining Techniques</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"BLACK\">P</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">3</font></td>\r\n\r\n\r\n\r\n<td ALIGN=\"middle\"><font color=\"black\" \r\n      style=\"COLOR: fuchsia\">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">  2</font></td>\r\n\r\n<td align=\"middle\"><font color=\"black\">  23CA3036</font></td>\r\n\r\n<td> <font color=\"black\"> Data Analytics and Visualization</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"BLACK\">B+</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">3</font></td>\r\n\r\n\r\n\r\n<td ALIGN=\"middle\"><font color=\"black\" \r\n      style=\"COLOR: fuchsia\">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">  2</font></td>\r\n\r\n<td align=\"middle\"><font color=\"black\">  23CA3038</font></td>\r\n\r\n<td> <font color=\"black\"> Advanced Database Technologies</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"BLACK\">B</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">3</font></td>\r\n\r\n\r\n\r\n<td ALIGN=\"middle\"><font color=\"black\" \r\n      style=\"COLOR: fuchsia\">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">  2</font></td>\r\n\r\n<td align=\"middle\"><font color=\"black\">  23CA3039</font></td>\r\n\r\n<td> <font color=\"black\"> Human Centered Computing</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"BLACK\">B+</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">3</font></td>\r\n\r\n\r\n\r\n<td ALIGN=\"middle\"><font color=\"black\" \r\n    
  style=\"COLOR: fuchsia\">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">  2</font></td>\r\n\r\n<td align=\"middle\"><font color=\"black\">  23CA3040</font></td>\r\n\r\n<td> <font color=\"black\"> Modelling Techniques in Predictive Analytics</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"BLACK\">B+</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">3</font></td>\r\n\r\n\r\n\r\n<td ALIGN=\"middle\"><font color=\"black\" \r\n      style=\"COLOR: fuchsia\">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">  2</font></td>\r\n\r\n<td align=\"middle\"><font color=\"black\">  23CA3042</font></td>\r\n\r\n<td> <font color=\"black\"> Internet of Things and Blockchain Technology</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"BLACK\">P</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">3</font></td>\r\n\r\n\r\n\r\n<td ALIGN=\"middle\"><font color=\"black\" \r\n      style=\"COLOR: fuchsia\">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">  2</font></td>\r\n\r\n<td align=\"middle\"><font color=\"black\">  22MA3001</font></td>\r\n\r\n<td> <font color=\"black\"> Logical Reasoning and Soft Skills</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"BLACK\">Completed</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">0</font></td>\r\n\r\n\r\n\r\n<td ALIGN=\"middle\"><font color=\"black\" \r\n      style=\"COLOR: fuchsia\">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">  2</font></td>\r\n\r\n<td align=\"middle\"><font color=\"black\">  23CA3035</font></td>\r\n\r\n<td> <font color=\"black\"> Machine Learning 
Lab</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"BLACK\">B+</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">2</font></td>\r\n\r\n\r\n\r\n<td ALIGN=\"middle\"><font color=\"black\" \r\n      style=\"COLOR: fuchsia\">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">  2</font></td>\r\n\r\n<td align=\"middle\"><font color=\"black\">  23CA3037</font></td>\r\n\r\n<td> <font color=\"black\"> Data Analytics and Visualization Lab</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"BLACK\">O</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">2</font></td>\r\n\r\n\r\n\r\n<td ALIGN=\"middle\"><font color=\"black\" 
\r\n      style=\"COLOR: fuchsia\">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">  2</font></td>\r\n\r\n<td align=\"middle\"><font 
color=\"black\">  23CA3041</font></td>\r\n\r\n<td> <font color=\"black\"> Predictive Analytics Lab</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"BLACK\">A+</font></td>\r\n\r\n\r\n<td align=\"middle\"><font color=\"black\">2</font></td>\r\n\r\n\r\n\r\n<td ALIGN=\"middle\"><font color=\"black\" \r\n      style=\"COLOR: fuchsia\">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n \r\n\r\n<center>\r\n<p>\r\n\r\n\r\n\r\n\r\n\r\n<BR></SMALL></TBODY></TABLE>\r\n<SMALL> <FONT color=darkviolet> The information at this site is provided solely for the user's immediate information and \r\nwithout warranty of any kind.  <BR>For final and correct data please confirm with the documents signed by the C.O.E.\r\n</FONT></SMALL><BR>\r\n\r\n\r\n\r\n\r\n<p align=right>\r\n\r\n<p align=left>\r\n\r\n<h2 align=\"center\">\r\n<span style=\"font-size: 15pt\">\r\n<i>\r\n&nbsp;<font color=\"#008000\"><a target=\"_blank\" href=\"CBCSSUPP/home_new.asp\">Supplementary \r\n&amp;Photocopy &amp; Revaluation \r\n- <font color=\"#008000\">Registration Link</font></a></font></i><br>\r\n</span>\r\n<font face=\"Garamond\" style=\"font-size: 13pt; font-weight: 700; font-style:italic; background-color:#FFFF00\" color=\"#008000\"><br>\r\n\t\t</font>\r\n\t\t<span style=\"font-size: 15pt\"><br>\r\n&nbsp;</span></h2>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n</font></b>\r\n\r\n\r\n\r\n\r\n\r\n<hr><center>\r\n\r\n<CENTER>\r\n\r\n\r\n<FONT size=3><BR>You are visitor No.<FONT color=green \r\nface=\"Comic Sans MS\">&nbsp;&nbsp;9967 </FONT>  to this page since \r\n01.07.2025\r\n\r\n<P>\r\n</P></FONT></CENTER></CENTER></H2></H2></u></font>\r\n\r\n\r\n<u>\r\n</FONT>\r\n\t\r\n\r\n<script defer src=\"https://static.cloudflareinsights.com/beacon.min.js/vcd15cbe7772f49c399c6a5babf22c1241717689176015\" integrity=\"sha512-ZpsOmlRQV6y907TI0dKBHq9Md29nnaEIPlkf84rnaERnq6zvWvPUqr2ft8M1aS28oN72PdrCzSjY4U6VaAw1EQ==\" data-cf-beacon='{\"rayId\":\"9632e399fdc87f8a\",\"version\":\"2025.7.0\",\"serverTiming\":{\"name\":{\"cfExtPri\":true,\"cfEdge\":true,\"cfOrigin\":true,\"cfL4\":true,\"cfSpeedBrain\":true,\"cfCacheStatus\":true}},\"token\":\"d649c55a914642f792eb32a3436ff8de\",\"b\":1}' crossorigin=\"anonymous\"></script>\n</body>\r\n</html>
    """
    
    # Extract data and convert to JSON
    json_result = html_to_json(example_html, 'student_data.json')
    
    print("\n" + "="*50)
    print("JSON OUTPUT:")
    print("="*50)
    print(json_result)

if __name__ == "__main__":
    # Install required package if not available
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("Installing required package: beautifulsoup4")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
        from bs4 import BeautifulSoup
    
    main()