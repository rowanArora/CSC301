import csv

"""
Reads from an existing csv file containing sentiment of a text and the date it was sent.
Stores read data in a formatted list, which can be used for graphing.
(Deprecated, but if someone else is working on this in the future and is using csv files, maybe helpful?)
"""

def read_data(filename: str):
    graph_data = []

    with open(filename, "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            graph_data.append((row[0],  # positive or negative
                            row[1]))    # sentiment value
    
    return graph_data