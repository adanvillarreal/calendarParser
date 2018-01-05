# calendarParser
Get ITESM's student calendar in Google Calendar.

## Getting Started

### Prerequisites
To install the required modules, run the following lines in a terminal
```
pip install --upgrade scrapy
pip install --upgrade twisted
pip install --upgrade pyopensslpip install --upgrade google-api-python-client
```
### Usage
Execute the file `calendarParser.py` with two arguments: email and password.
E.g.
```
python calendarParser.py 'a01234567@itesm.mx' 'password'
```
A browser window will show up asking for permission to access your calendar. 

## Author
Adan Villarreal

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
