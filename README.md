# msgpack-python

A simple implementation of MessagePack serialization format in Python. This project provides basic functionality to encode JSON data to MessagePack format and decode MessagePack data back to JSON.

## Features

- JSON to MessagePack encoding
- MessagePack to JSON decoding
- Support for basic data types:
  - nil (None)
  - boolean
  - integers
  - floating point numbers
  - strings
  - binary data
  - arrays
  - maps

## Download the Project

Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/kobukuro/msgpack-python.git
cd msgpack-python
```

## Requirements
- Python 3.13 or higher
- No external dependencies required


## Usage

The program can be used to encode JSON to MessagePack or decode MessagePack to JSON from the command line.

### Encoding JSON to MessagePack
#### Windows PowerShell
``` powershell
python main.py -e '{\"name\": \"John\", \"age\": 30}'
```
#### Linux
``` bash
python main.py -e '{"name": "John", "age": 30}'
```
### Decoding MessagePack to JSON
``` bash
python main.py -d 82a46e616d65a44a6f686ea36167651e
```
### Running Tests
The project includes a comprehensive test suite. To run the tests:
``` bash
python -m unittest discover -s tests
```
The test suite covers:
- Nil values
- Booleans
- Integers (positive and negative)
- Floating point numbers
- Strings (including Unicode)
- Binary data
- Arrays
- Maps