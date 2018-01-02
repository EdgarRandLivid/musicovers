#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# general
import re
import os
import glob
import pandas as pd
import numpy as np
from os.path import join
import datetime

#specific
import pygal


# ===============================
# Parameters
# ===============================


workdir = "/media/christof/data/repos/dh-trier/musicovers"
sourcedatafile = join(workdir, "6FO-daten", "6FO-001.csv") 
targetdatafile = join(workdir, "XEV-daten", "XEV-001.svg") 
docfile = join(workdir, "XEV-daten", "XEV-001.txt")



# ===============================
# Functions
# ===============================


def load_data(sourcedatafile):
    """
    Load the features and metadata from CSV
    https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html#pandas.read_csv
    """
    with open(sourcedatafile, "r") as infile:
        data = pd.read_csv(infile, sep=";", encoding="utf8", index_col=False)
        return data


def get_metadata(data): 
    """
    From the data table, extract the list of genre labels. 
    """
    genres = list(data["genre"])
    print("genres:", len(set(genres)), set(genres))
    return genres


def get_featurematrix(coverdata): 
    histmax = list(coverdata.loc[:,"histmax"])
    histmed = list(coverdata.loc[:,"histmed"])
    histstd = list(coverdata.loc[:,"histstd"])
    featurematrix = [[m,n,o] for m,n,o in zip(histmax, histmed, histstd)]
    print("feature examples:", featurematrix[0:3])
    return featurematrix


def make_scatterplot(genres, featurematrix, targetdatafile):
    plot = pygal.XY(
        title="Cover features",
        x_title = "feature 1 (hist_argmax)",
        y_title = "feature 2 (hist_median)",
        stroke=False,
        logarithmic=False,
        show_legend = False)
    for i in range(0,15):
        if genres[i] == "hip-hop":
            color = "blue"
        elif genres[i] == "country":
            color = "red"
        elif genres[i] == "pop":
            color = "green"
        plot.add(
            genres[i],
            [{
                "value" : (featurematrix[i][0], featurematrix[i][1]),
                "label" : genres[i],
                "color" : color},
             ])
    plot.render_to_file(targetdatafile)


# ===============================
# Documentation functions
# ===============================


def get_timestamp(): 
    timestamp = datetime.datetime.now()
    timestamp = re.sub(" ", "_", str(timestamp))
    timestamp = re.sub(":", "-", str(timestamp))
    timestamp, milisecs = timestamp.split(".")
    return timestamp


def write_docfile(sourcedatafile, targetdatafile, docfile):
    operations = "operations = visualize the feature distribution."
    sourcestring = "sourcedata = " + str(os.path.basename(sourcedatafile))
    targetstring = "targetdata = " + str(os.path.basename(targetdatafile))
    scriptstring = "script = " + str(os.path.basename(__file__))
    timestamp = "timestamp = " + get_timestamp()
    doctext = "==9EV==\n" + sourcestring + "\n" + targetstring + "\n" + scriptstring + "\n" + operations + "\n" + timestamp + "\n" 
    with open(docfile, "w") as outfile:
        outfile.write(doctext)


# ===============================
# Main
# ===============================


def main(sourcedatafile, targetdatafile, docfile): 
    """
    Visualize the feature distribution.
    """
    data = load_data(sourcedatafile)
    genres = get_metadata(data)
    featurematrix = get_featurematrix(data)
    make_scatterplot(genres, featurematrix, targetdatafile)
    write_docfile(sourcedatafile, targetdatafile, docfile)

main(sourcedatafile, targetdatafile, docfile)
































