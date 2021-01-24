# Emil's web service for directory listing

This web server lets the caller list the content
of directories and files on the system where the 
service is running.

## Installation
Use python 3 in a virtual environment or otherwise; 
tested with python 3.6 and 3.8

Run `pip install -r requirements.txt` to install aiohttp

## Usage
Run in a terminal:
`python app.py`

## API
### /directory
Payload: `{"path": <valid path to a directory>}`

Return: `{"directory_contents": list}`

List the contents of the directory under path

### /file
Payload: `{"path": <valid path to a text file>}`

Return: `{"file_contents": string}`

Return the contents of the text file in path.

## Reflections & design choices
### Web service framework
aiohttp is my framework of choice; it is minimal and easy to use 
and designed to deal asynchronously with I/O operations.

### Graceful shutdown
aiohttp takes care of this out of the box.

### Error return codes
For the application at hand, I decided that reasonable exceptions are

400 (bad request meaning either that the path is not a directory or 
is a directory, for endpoints `/directory` or `/file` respectively,
or that the file is not a text file.)

403 (forbidden - for simplicity the user can query any file that 
the user running the server can access)

404 (for file not found)

500 (I let the framework handle any outstanding exceptions 
not caught by the handlers)

The exceptions are handled in a middleware, in order to reduce code duplication.
