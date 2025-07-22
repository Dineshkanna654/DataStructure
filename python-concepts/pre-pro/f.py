import re
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
    import re
    html_content = re.sub(r'\\(.)', r'\1', html_content)
    
    # Clean up excessive whitespace but preserve intentional spacing
    html_content = re.sub(r'\n\s*\n\s*\n', '\n\n', html_content)  # Max 2 consecutive newlines
    
    return html_content

def format_html_structure(html_content):
    """
    Clean and format HTML with proper structure
    """
    
    # First remove escape characters
    html_content = remove_escape_characters(html_content)
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove CloudFlare script and comments
    for script in soup.find_all('script'):
        if 'cloudflare' in str(script):
            script.decompose()
    
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    
    # Fix DOCTYPE and basic structure
    if not soup.find('!DOCTYPE'):
        doctype = '<!DOCTYPE html>'
    
    # Ensure proper HTML structure
    if not soup.html:
        # Wrap everything in html tag
        new_soup = BeautifulSoup('<!DOCTYPE html><html></html>', 'html.parser')
        html_tag = new_soup.html
        
        # Move head content
        if soup.head:
            html_tag.append(soup.head.extract())
        else:
            head_tag = new_soup.new_tag('head')
            html_tag.append(head_tag)
        
        # Move body content or create body
        if soup.body:
            html_tag.append(soup.body.extract())
        else:
            body_tag = new_soup.new_tag('body')
            # Move all remaining content to body
            for element in list(soup.children):
                if element.name:
                    body_tag.append(element.extract())
            html_tag.append(body_tag)
        
        soup = new_soup
    
    # Add missing meta tags
    head = soup.head
    if not head.find('meta', {'charset': True}):
        meta_charset = soup.new_tag('meta', charset='UTF-8')
        head.insert(0, meta_charset)
    
    if not head.find('meta', {'name': 'viewport'}):
        meta_viewport = soup.new_tag('meta')
        meta_viewport['name'] = 'viewport'
        meta_viewport['content'] = 'width=device-width, initial-scale=1.0'
        head.insert(1, meta_viewport)
    
    # Fix table structure issues
    fix_table_structure(soup)
    
    # Clean up attributes
    clean_attributes(soup)

    
    # Format the output with proper indentation
    formatted_html = soup.prettify()
    
    return formatted_html

def fix_table_structure(soup):
    """Fix common table structure issues"""
    
    # Find tables and fix structure
    for table in soup.find_all('table'):
        # Ensure all rows are properly nested
        rows = table.find_all('tr')
        
        # Check if table has tbody, if not create one
        tbody = table.find('tbody')
        if not tbody and rows:
            tbody = soup.new_tag('tbody')
            table.append(tbody)
            
            # Move rows to tbody (except header rows)
            for i, row in enumerate(rows):
                row.extract()
                tbody.append(row)
        
        # Fix malformed cells
        for row in table.find_all('tr'):
            cells = row.find_all(['td', 'th'])
            for cell in cells:
                # Fix cells that might have broken content
                if cell.string and len(cell.get_text().strip()) == 0:
                    cell.string = ' '

def clean_attributes(soup):
    """Clean up old HTML attributes and convert to modern equivalents"""
    
    # Remove deprecated attributes from body
    body = soup.body
    if body:
        deprecated_attrs = ['leftmargin', 'topmargin', 'marginheight', 'marginwidth', 'bgcolor', 'background']
        for attr in deprecated_attrs:
            if body.has_attr(attr):
                del body[attr]
    
    # Clean up table attributes
    for table in soup.find_all('table'):
        # Convert old attributes to CSS-friendly ones
        old_attrs = ['border', 'cellpadding', 'cellspacing', 'bordercolordark', 'bordercolorlight']
        for attr in old_attrs:
            if table.has_attr(attr):
                del table[attr]
        
        # Add class for styling
        table['class'] = table.get('class', []) + ['formatted-table']
    
    # Clean up font tags - convert to spans with classes
    for font in soup.find_all('font'):
        span = soup.new_tag('span')
        
        # Preserve color
        if font.has_attr('color'):
            span['style'] = f"color: {font['color']};"
        
        # Move content
        span.string = font.get_text()
        font.replace_with(span)

def format_html_from_string(html_string, output_file=None):
    """
    Format HTML from string input
    
    Args:
        html_string (str): The HTML content as string
        output_file (str, optional): Output file path. If None, returns formatted string
    
    Returns:
        str: Formatted HTML string
    """
    print("Removing escape characters...")
    print("Formatting HTML structure...")
    formatted_html = format_html_structure(html_string)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(formatted_html)
        print(f"✅ HTML has been formatted and saved as '{output_file}'")
    
    print("\nKey improvements made:")
    print("- Removed escape characters (\\n, \\t, \\r, etc.)")
    print("- Added proper DOCTYPE and HTML5 structure")
    print("- Fixed table formatting and structure")
    print("- Added responsive meta tags")
    print("- Cleaned up deprecated attributes")
    print("- Added modern CSS styling")
    print("- Removed malformed content")
    print("- Improved accessibility and readability")
    
    return formatted_html

def main():
    """Example usage - you can modify this to use your HTML string"""
    
    # Example HTML string (replace this with your actual HTML)
    example_html = """
    <html>\r\n<head>\r\n\r\n<title>KITS Exam - Apr/May 2025 Results</title></head>\r\n<body  leftmargin=0 topmargin=0 marginheight="0" marginwidth="0" style="background-attachment: fixed" bgcolor=#547DEB background="t2.jpg">\r\n\r\n\r\n\r\n<center>\r\n<img src="http://www.karunya.edu/sites/default/files/logo.png.pagespeed.ce.rQZd6s4jcx.png" alt="Porto"></center>\r\n<TABLE WIDTH="87%" BORDER=0 CELLSPACING=1 CELLPADDING=1>\r\n\t<TR>\r\n\r\n\t\t\r\n\t\t<TD width="1044">\r\n\t\t<h2><font color="#0000FF" face="Book Antiqua">Exam Results - Apr/May \r\n\t\t2025 (</font><font face="Book Antiqua" style="font-size: 15pt" color="#008000">All</font><font color="#008000" face="Book Antiqua"><span style="font-size: 15pt"> \r\n\t\tStudents</span></font><font color="#0000FF" face="Book Antiqua">) </font>\r\n\t\t\r\n\t\t</h2>  \r\n\t\t</TD>\r\n\t\t<TD>\r\n\t\t<p align="center"><b><a href="logout_new5.asp">LOGOUT</a></b></TD>\t\t\r\n\t</TR>\r\n</TABLE>\r\n\r\n\r\n\r\n\r\n\r\n\r\n<TABLE border=3 borderColorDark=#c9beb6 
borderColorLight=#000000 cellPadding=1 \r\ncellSpacing=1 width="70%" align=center>\r\n\r\n\t<tr>\r\n\t\t<td ALIGN="middle"><b>REG. NO.</b></td>\r\n\t\t<td ALIGN="middle"><b>NAME</b></td>\r\n\t\t<td ALIGN="middle"><b>COURSE</b></td>\r\n\r\n\t</tr>\r\n\r\n\t<tr>\r\n\t\t<td ALIGN="middle">PRK24AD1007</td>\r\n\t\t<td ALIGN="middle">SANJITH KRISHNA B</td>\r\n\t\t<td ALIGN="middle">M.Sc.&nbsp;&nbsp;Artificial Intelligence and Data Science</td>\r\n\t\r\n\t</tr>\r\n</TABLE>\r\n<CENTER>\r\n<TABLE>\r\n\t<TR>\r\n\t\t<TD>\r\n\t\t\t<table BORDER=1 ALIGN=center>\r\n\t\t\t\t<tr>\r\n\t\t\t\t\t<td WIDTH=150 ALIGN=middle>Credits Earned</td> \r\n\t\t\t\t\t<td WIDTH=150 ALIGN=middle>CGPA</td> \r\n\t\t\t\t</tr>\r\n\t\t\t\t<tr>\r\n\t\t\t\t\t\r\n\t\t\t\t\t<TD ALIGN=middle><FONT COLOR="blue" ><b>47</b></FONT></TD>\r\n\t\t\t\t\t\r\n\t\t\t\t\t<TD ALIGN=middle><FONT COLOR="blue"><b>6.74</b></FONT></TD>\r\n\t\t\t\t\t\r\n\r\n\t\t\t\t</tr>\r\n\t\t\t</table>\r\n\t\t<TD WIDTH=10></TD>\r\n\t\t<TD>\r\n\t\t\t<table BORDER=1 ALIGN=center>\r\n\t\t\t\t<TR>\r\n\t\t\t\t\t<td WIDTH=150 ALIGN=middle>SGPA</td>\r\n\t\t\t\t</TR>\r\n\t\t\t\t<tr>\r\n\t\t\t\t\t\r\n\t\t\t\t\t<TD ALIGN=middle><FONT COLOR="blue"><b>6.54</b></FONT></TD>\r\n\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t</tr>\r\n\t\t\t</table>\r\n\t\t</TD>\r\n\t\t<TD WIDTH=50></TD>\r\n\r\n\t\t<td>\r\n\t\t<table BORDER=1 ALIGN=center>\r\n\t\t\t\t<TR>\r\n\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t\t\r\n\t\t\t\t</tr>\r\n\t\t\t</table>\r\n\r\n\t\t\r\n\t\t\r\n\t\t</td>\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t\t\r\n\t</TR>\r\n</TABLE>\r\n\t\r\n\t\r\n\t\r\n</CENTER>\r\n<small>\r\n\r\n\r\n<!--\r\n<CENTER><FONT size=3><STRONG>\r\n<FONT color=green >Congratulations ! &nbsp;&nbsp;&nbsp; You have cleared all papers !</FONT>  </FONT>\r\n</CENTER></STRONG>\r\n-->\r\n\r\n\r\n<center>\r\n\r\n<TABLE border=3 borderColorDark=#c9beb6 borderColorLight=#000000 cellPadding=1 \r\ncellSpacing=1 width="65%">\r\n\r\n\r\n  <tbody>\r\n\r\n\r\n\r\n\r\n\r\n<tr ALIGN="middle"><td><b>SEM</b></td><td><b>CODE</b></td><td><b>SUBJECT</b></td>\r\n<td><b>GRADE</b></td><td><b><b>CREDIT</b></b></td></tr></B>\r\n\r\n<td align="middle"><font color="black">  2</font></td>\r\n\r\n<td align="middle"><font color="black">  23CA3034</font></td>\r\n\r\n<td> <font color="black"> Data Warehousing and Data Mining Techniques</font></td>\r\n\r\n\r\n<td align="middle"><font color="BLACK">P</font></td>\r\n\r\n\r\n<td align="middle"><font color="black">3</font></td>\r\n\r\n\r\n\r\n<td ALIGN="middle"><font color="black" \r\n      style="COLOR: fuchsia">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align="middle"><font color="black">  2</font></td>\r\n\r\n<td align="middle"><font color="black">  23CA3036</font></td>\r\n\r\n<td> <font color="black"> Data Analytics and Visualization</font></td>\r\n\r\n\r\n<td align="middle"><font color="BLACK">B+</font></td>\r\n\r\n\r\n<td align="middle"><font color="black">3</font></td>\r\n\r\n\r\n\r\n<td ALIGN="middle"><font color="black" \r\n      style="COLOR: fuchsia">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align="middle"><font color="black">  2</font></td>\r\n\r\n<td align="middle"><font color="black">  23CA3038</font></td>\r\n\r\n<td> <font color="black"> Advanced Database Technologies</font></td>\r\n\r\n\r\n<td align="middle"><font color="BLACK">B</font></td>\r\n\r\n\r\n<td align="middle"><font color="black">3</font></td>\r\n\r\n\r\n\r\n<td ALIGN="middle"><font color="black" \r\n      style="COLOR: fuchsia">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align="middle"><font color="black">  2</font></td>\r\n\r\n<td align="middle"><font color="black">  23CA3039</font></td>\r\n\r\n<td> <font color="black"> Human Cd ALIGN="middle"><font color="black" \r\n      style="COLOR: fuchsia">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align="middle"><font color="black">  2</font></td>\r\n\r\n<td align="middle"><font color="black">  23CA3040</font></td>\r\n\r\n<td> <font color="black"> Modelling Techniques in Predictive Analytics</font></td>\r\n\r\n\r\n<td align="middle"><font color="BLACK">B+</font></td>\r\n\r\n\r\n<td align="middle"><font color="black">3</font></td>\r\n\r\n\r\n\r\n<td ALIGN="middle"><font color="black" \r\n      style="COLOR: fuchsia">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align="middle"><font color="black">  2</font></td>\r\n\r\n<td align="middle"><font color="black">  23CA3042</font></td>\r\n\r\n<td> <font color="black"> Internet of Things and Blockchain Technology</font></td>\r\n\r\n\r\n<td align="middle"><font color="BLACK">P</font></td>\r\n\r\n\r\n<td align="middle"><font color="black">3</font></td>\r\n\r\n\r\n\r\n<td ALIGN="middle"><font color="black" \r\n      style="COLOR: fuchsia">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align="middle"><font color="black">  2</font></td>\r\n\r\n<td align="middle"><font color="black">  22MA3001</font></td>\r\n\r\n<td> <font color="black"> Logical Reasoning and Soft Skills</font></td>\r\n\r\n\r\n<td align="middle"><font color="BLACK">Completed</font></td>\r\n\r\n\r\n<td align="middle"><font color="black">0</font></td>\r\n\r\n\r\n\r\n<td ALIGN="middle"><font color="black" \r\n      style="COLOR: fuchsia">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align="middle"><font color="black">  2</font></td>\r\n\r\n<td align="middle"><font color="black">  23CA3035</font></td>\r\n\r\n<td> <font color="black"> Machine Learning Lab</font></td>\r\n\r\n\r\n<td align="middle"><font color="BLACK">B+</font></td>\r\n\r\n\r\n<td align="middle"><font color="black">2</font></td>\r\n\r\n\r\n\r\n<td ALIGN="middle"><font color="black" \r\n      style="COLOR: fuchsia">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n\r\n<td align="middle"><font color="black">  2</font></td>\r\n\r\n<td align="middle"><font color="black">  23CA3037</font></td>\r\n\r\n<td> <font color="black"> Data Analytics and Visualization Lab</font></td>\r\n\r\n\r\n<td align="middle"><font color="BLACK">O</font></td>\r\n\r\n\r\n<td al\n\r\n<td align="middle"><font color="black">  2</font></td>\r\n\r\n<td align="middle"><font color="black">  23CA3041</font></td>\r\n\r\n<td> <font color="black"> Predictive Analytics Lab</font></td>\r\n\r\n\r\n<td align="middle"><font color="BLACK">A+</font></td>\r\n\r\n\r\n<td align="middle"><font color="black">2</font></td>\r\n\r\n\r\n\r\n<td ALIGN="middle"><font color="black" \r\n      style="COLOR: fuchsia">&nbsp; </font></td>\r\n\r\n\r\n</tr>\r\n\r\n \r\n\r\n<center>\r\n<p>\r\n\r\n\r\n\r\n\r\n\r\n<BR></SMALL></TBODY></TABLE>\r\n<SMALL> <FONT color=darkviolet> The information at this site is provided solely for the user\'s immediate information and \r\nwithout warranty of any kind.  <BR>For final and correct data please confirm with the documents signed by the C.O.E.\r\n</FONT></SMALL><BR>\r\n\r\n\r\n\r\n\r\n<p align=right>\r\n\r\n<p align=left>\r\n\r\n<h2 align="center">\r\n<span style="font-size: 15pt">\r\n<i>\r\n&nbsp;<font color="#008000"><a target="_blank" href="CBCSSUPP/home_new.asp">Supplementary \r\n&amp;Photocopy &amp; Revaluation \r\n- <font color="#008000">Registration Link</font></a></font></i><br>\r\n</span>\r\n<font face="Garamond" style="font-size: 13pt; font-weight: 700; font-style:italic; background-color:#FFFF00" color="#008000"><br>\r\n\t\t</font>\r\n\t\t<span style="font-size: 15pt"><br>\r\n&nbsp;</span></h2>\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n</font></b>\r\n\r\n\r\n\r\n\r\n\r\n<hr><center>\r\n\r\n<CENTER>\r\n\r\n\r\n<FONT size=3><BR>You are visitor No.<FONT color=green \r\nface="Comic Sans MS">&nbsp;&nbsp;9861 </FONT>  to this page since \r\n01.07.2025\r\n\r\n<P>\r\n</P></FONT></CENTER></CENTER></H2></H2></u></font>\r\n\r\n\r\n<u>\r\n</FONT>\r\n\t\r\n\r\n<script defer src="https://static.cloudflareinsights.com/beacon.min.js/vcd15cbe7772f49c399c6a5babf22c1241717689176015" integrity="sha512-ZpsOmlRQV6y907TI0dKBHq9Md29nnaEIPlkf84rnaERnq6zvWvPUqr2ft8M1aS28oN72PdrCzSjY4U6VaAw1EQ==" data-cf-beacon=\'{"rayId":"9631adb46ab07f2e","version":"2025.7.0","serverTiming":{"name":{"cfExtPri":true,"cfEdge":true,"cfOrigin":true,"cfL4":true,"cfSpeedBrain":true,"cfCacheStatus":true}},"token":"d649c55a914642f792eb32a3436ff8de","b":1}\' crossorigin="anonymous"></script>\n</body>\r\n</html>
    """
    
    # Format the HTML
    # formatted = format_html_from_string(example_html, 'output.html')
    
    # Or just get the formatted string without saving to file
    formatted = format_html_from_string(example_html)
    print(formatted)

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