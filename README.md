This script creates a kml file from csv which is generated from slocum glider sbd/tbd files and contains at least date, latitude and longitude.
Many parameters including line/symbol color in kml can be configured through glider.ini

This script works on python2.7.
For Python3, comment out the following line
```
# cfg._interpolation = configparser.ExtendedInterpolation()
```

## Requirements
This script uses the simplekml library. It can be installed with pip.
```
$ pip install simplekml
```

## Note
If a csv file has a header line, change CSV_HEADER YES in glider.ini
Latitude/longitude/date column number start at 1 intead of 0-based index in python. If latitude is in the first column, LAT_COLUMN should be 1.
