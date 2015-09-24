#!/bin/env python
"""
Name:      csv2kml_gliders.py
Author:    shinichi.kobara@gcoos.org
Created:   2013-07-22
Modified:  2015-09-22
Inputs:    csv file with date, latitude, longitude
           configuration in glider.ini
Outputs:   kml file with time track and a line path
           file name: Glider_ORGANIZATION_VEHICLE_MISSION-DATE.kml
Notes:     This script requires simplekml library and CONFIG file
           under the same directory
simplekml: http://www.simplekml.com/en/latest/
           pip install simplekml
"""

from future import standard_library
standard_library.install_aliases()

import os
import time
import csv
from simplekml import Kml, Snippet

import configparser


def write_track_kml(csvreader):
    """
    Inputs: csv contains lon/lat
    Output:	glider track kml file
    """
    coord = []
    timerange = []

    lat_f = int(cfg.get(section1, 'LAT_COLUMN'))
    lon_f = int(cfg.get(section1, 'LON_COLUMN'))
    date_f = int(cfg.get(section1, 'DATE_COLUMN'))
    date_fmt = cfg.get(section1, 'DATE_FORMAT')
    kml_dir = cfg.get(section1, 'KML_DIR')
    mission_date = cfg.get(section1, 'MISSION_START_DATE')
    organization = cfg.get(section1, 'ORGANIZATION')
    vehicle_name = cfg.get(section1, 'VEHICLE_NAME')
    kml_title = cfg.get(section1, 'KML_DOC_TITLE')
    kml_lookat_lon = float(cfg.get(section1, 'KML_LOOKAT_LON'))
    kml_lookat_lat = float(cfg.get(section1, 'KML_LOOKAT_LAT'))
    kml_lookat_range = float(cfg.get(section1, 'KML_LOOKAT_RANGE'))
    kml_cdata_title = cfg.get(section1, 'KML_CDATA_TITLE')
    plot_url = cfg.get(section1, 'PLOT_URL')
    plot_width = int(cfg.get(section1, 'PLOT_WIDTH'))
    plot_height = int(cfg.get(section1, 'PLOT_HEIGHT'))
    plot_temp = cfg.get(section1, 'PLOT_TEMP')
    plot_oxyg = cfg.get(section1, 'PLOT_OXYG')
    plot_sali = cfg.get(section1, 'PLOT_SALI')
    plot_chlo = cfg.get(section1, 'PLOT_CHLO')
    plot_cdom = cfg.get(section1, 'PLOT_CDOM')
    icon_url = cfg.get(section1, 'ICON_URL')
    icon_normal_scale = cfg.get(section1, 'ICON_NORMAL_SCALE')
    icon_normal_color = cfg.get(section1, 'ICON_NORMAL_COLOR')
    icon_normal_width = cfg.get(section1, 'ICON_NORMAL_WIDTH')
    icon_highlight_url = cfg.get(section1, 'ICON_HIGHLIGHT_URL')
    icon_highlight_scale = cfg.get(section1, 'ICON_HIGHLIGHT_SCALE')
    icon_highlight_color = cfg.get(section1, 'ICON_HIGHLIGHT_COLOR')
    icon_highlight_width = cfg.get(section1, 'ICON_HIGHLIGHT_WIDTH')
    path_line_color = cfg.get(section1, 'PATH_LINE_COLOR')
    path_line_width = int(cfg.get(section1, 'PATH_LINE_WIDTH'))

    csvheader = cfg.get(section1, 'CSV_HEADER')
    if csvheader == "YES":
        csvreader.next()
    else:
        pass

    for row in csvreader:
        coord.append((row[lon_f - 1], row[lat_f - 1], 0.0))  # -1 for python order
        timestamp = time.strptime(row[date_f - 1], date_fmt)
        kmltime = time.strftime("%Y-%m-%dT%H:%M:%SZ", timestamp)  # KML requires specific time format
        timerange.append(kmltime)  # time stamp

    # This constructs the KML document from the CSV file.
    kml = Kml(name="%s %s" % (organization, vehicle_name))
    doc = kml.newdocument(name='%s' % kml_title, snippet=Snippet(timerange[0]))
    doc.lookat.gxtimespan.begin = timerange[0]
    doc.lookat.gxtimespan.end = timerange[-1]
    doc.lookat.longitude = kml_lookat_lon
    doc.lookat.latitude = kml_lookat_lat
    doc.lookat.range = kml_lookat_range
    # Create a folder
    ge_dir = doc.newfolder(name='Tracks')
    # Create a schema for extended data: heart rate, cadence and power
    schema = kml.newschema()

    # Create a new track in the folder
    trk = ge_dir.newgxtrack(name='%s %s' % (organization, vehicle_name))
    desc1 = "<![CDATA[\n%s<br />\n<br />\n" % kml_cdata_title
    desc2 = "<a href='%s/glider.html' target='_blank'>Link to Plot</a><br />\n" % plot_url
    desc_temp = "<img src='%s/%s' height='%d' width='%d' /><br />\n" % (plot_url, plot_temp, plot_height, plot_width)
    desc_oxyg = "<img src='%s/%s' height='%d' width='%d' /><br />\n" % (plot_url, plot_oxyg, plot_height, plot_width)
    desc_sali = "<img src='%s/%s' height='%d' width='%d' /><br />\n" % (plot_url, plot_sali, plot_height, plot_width)
    desc_chlo = "<img src='%s/%s' height='%d' width='%d' /><br />\n" % (plot_url, plot_chlo, plot_height, plot_width)
    desc_cdom = "<img src='%s/%s' height='%d' width='%d' /><br />\n" % (plot_url, plot_cdom, plot_height, plot_width)
    desc3 = "]]>\n"
    trk.description = desc1 + desc2 + desc_temp + desc_oxyg + desc_sali + desc_chlo + desc_cdom + desc3
    # Apply the above schema to this track
    trk.extendeddata.schemadata.schemaurl = schema.id
    # Add all information to the track
    trk.newwhen(timerange)  # Each item in the give nlist will become a new <when> tag
    trk.newgxcoord(coord)  # Ditto

    # Style
    trk.stylemap.normalstyle.iconstyle.icon.href = icon_url
    trk.stylemap.normalstyle.iconstyle.scale = icon_normal_scale
    trk.stylemap.normalstyle.linestyle.color = icon_normal_color
    trk.stylemap.normalstyle.linestyle.width = icon_normal_width
    trk.stylemap.highlightstyle.iconstyle.icon.href = icon_highlight_url
    trk.stylemap.highlightstyle.iconstyle.scale = icon_highlight_scale
    trk.stylemap.highlightstyle.linestyle.color = icon_highlight_color
    trk.stylemap.highlightstyle.linestyle.width = icon_highlight_width

    # Create a path line
    gpath = kml.newlinestring(name="%s %s" % (organization, vehicle_name))
    gpath.description = trk.description
    gpath.timespan.begin = timerange[0]
    gpath.timespan.end = ""
    gpath.coords = coord
    gpath.style.linestyle.color = path_line_color
    gpath.style.linestyle.width = path_line_width

    # Check if KML Directory exists
    if not os.path.exists(kml_dir):
        os.makedirs(kml_dir)

    # Save the KML
    kml.save("%s/Glider_%s_%s_%s.kml" % (kml_dir, organization, vehicle_name, mission_date))
    print("Glider_%s_%s_%s.kml created in '%s' folder" % (organization, vehicle_name, mission_date, kml_dir))


if __name__ == '__main__':
    # get CONFIG info
    cfg = configparser.ConfigParser()
    #cfg._interpolation = configparser.ExtendedInterpolation()  # comment out if py3
    cfg.read('glider.ini')
    section1 = cfg.sections()[0]
    # get deployment status
    DEPLOYED = int(cfg.get(section1, 'DEPLOYED'))
    if DEPLOYED == 1:
        CSV_DIR = cfg.get(section1, 'DEPLOYED_CSV_DIR')
    else:
        CSV_DIR = cfg.get(section1, 'POSTMISSION_CSV_DIR')

    try:
        source = open("%s/%s" % (CSV_DIR, cfg.get(section1, 'CSV_FILE_NAME')), 'r')
    except IOError:
        print("The file does not exist, existing gracefully")
    # read csv file
    rdr = csv.reader(source)
    # generate kml
    write_track_kml(rdr)
    source.close()