# rpm-suite
Rudimentary Project Management Tool

### Summary
This is a rudimentary project management tool that allows users to create 
a gantt chart of tasks and their dependencies. 

### Installation
To install the program, download the latest tarball release and run the 
following command from the command line:
```shell
pip install [latest tarball release]
```

### Usage
To run the program, simply run the following command from the command line:
```shell
usage: rpmgantt [-h] [-d DEST_HTML] [-hh HEIGHT] [-wh WIDTH] json

Parses arguments for the Gantt Chart generator.

positional arguments:
  json                  JSON containing the information to be
                        plotted

optional arguments:
  -h, --help            show this help message and exit
  -d DEST_HTML, --dest_html DEST_HTML
                        Destination HTML file to create (default:
                        $HOME/index.html)
  -hh HEIGHT, --height HEIGHT
                        Destination HTML Height (default: 400)
  -wh WIDTH, --width WIDTH
                        Destination HTML Width (default: 800)
                        
```

### Example
Example json configuration can be found in the `examples` directory. The 
user may change the value for each key to their linking, but not the keys 
themselves.

### Dependencies
This project requires the following dependencies:
* Python 3.7+
* pandas
* bokeh


