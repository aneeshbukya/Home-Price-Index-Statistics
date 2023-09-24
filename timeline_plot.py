"""
file: timeline_plot.py
author: Aneesh Bukya  ab5380@g.rit.edu
course: CSCI 141
assignment: Project
date: 11/10/2022
notes: timeline plot file
"""
import numpy.ma as ma
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import copy
import index_tools

def build_plottable_array(xyears, regiondata):
    """
    builds a bridge over the unavailable data gap so that the plotting module can properly plot around the gap
    :param xyears: a list of integer year values
    :param regiondata: a list of AnnualHPI objects.
    :return: An array suitable for plotting with the matplotlib module
    """
    mask_array = ma.array([])
    for idx in range(len(xyears)):
        length = len(mask_array)
        for i in range(len(regiondata)):
            if regiondata[i].year == xyears[idx]:
                mask_array = ma.append(mask_array,regiondata[i].index)
            else:
                continue
        if length == len(mask_array):
            mask_array = ma.append(mask_array,ma.masked)
        else:
            continue
    return mask_array


def filter_years(data,year0,year1):
    """
    filters the AnnualHPI values for all regions so that each list of values contains data for only the span of the
    given years
    :param data: a dictionary mapping from regions to lists of AnnualHPI
    :param year0: the period of interest
    :param year1:  the period of interest
    :return: A dictionary mapping regions to lists of HPI values that are within the year0 to year1 inclusive range
    """
    new_data = {}
    lst = []
    for key in data:
        for i in range(len(data[key])):
            if data[key][i].year >= year0 and data[key][i].year <= year1:
                if new_data.get(key) == None:
                    lst.append(index_tools.AnnualHPI(data[key][i].year, data[key][i].index))
                    new_data[key] = lst
                    lst = []
                else:
                    lst.append(index_tools.AnnualHPI(data[key][i].year, data[key][i].index))
                    new_data[key] += lst
                    lst = []
            else:
                continue
    return new_data

def plot_HPI(data, regionList):
    """
    plots a timeline from point to point over the time period of the data
    :param data: a dictionary mapping a state or zip code to a list of AnnualHPI objects
    :param regionList: a list of key values whose type is string
    """
    mask_array = ma.array([])
    year_lst = []
    start_year = 2020
    end_year = 0
    for key in data:
        if key in regionList:
            for idx in range(len(data[key])):
                if data[key][idx].year < start_year  :
                    start_year = data[key][idx].year
                elif data[key][idx].year > end_year  :
                    end_year = data[key][idx].year
                else:
                    continue
    for year in range(start_year,end_year+1):
        year_lst.append(year)
        mask_array = ma.append(mask_array,year)
    plt.title("Home Price Indices:"+str(start_year)+"-"+str(end_year))
    for val in regionList:
        index_val = build_plottable_array(year_lst,data[val])
        plt.plot(mask_array,index_val,"*",linestyle ="-")
    plt.legend(regionList,loc="upper left")
    plt.show()
    print("Close display window to continue")

def plot_whiskers(data, regionList):
    """
    plots a box and whisker graph from point to point over the time period of the data
    :param data: a dictionary mapping a state or zip code to a list of AnnualHPI objects
    :param regionList: a list of key values whose type is string
    """
    yvals = []
    region_data = []
    for key in regionList:
        for i in range(len(data[key])):
            yvals.append(data[key][i].index)
        region_data.append(yvals)
        yvals = []
    mean = {"marker":"d","markerfacecolor":"red","markeredgecolor":"red"}
    median = dict(color="red")
    box = dict(color="blue")
    whisker = dict(linestyle = "dashed",color = "blue")
    plt.boxplot(region_data, vert=True, showmeans=True,labels = regionList,meanprops=mean,boxprops=box,whiskerprops=whisker,
                medianprops=median)
    plt.title("Home Price Index Comparison. Median is a line. Mean is a diamond")
    plt.show()
    print("Close display window to continue")

def main():
    """
    initializes the code by taking the input from user and displaying the results for the user to view
    """
    tracker = True
    region_lst = []
    file_name = input("Enter house price index filename: ")
    if "state" in file_name:
        start_year = int(input("Enter the start year of the range to plot: "))
        end_year = int(input("Enter the end year of the range to plot: "))
        while tracker == True:
            region_name = input("Enter next region for plots (<ENTER> to stop): ")
            if region_name == "":
                tracker = False
            else:
                region_lst.append(region_name)
        data = index_tools.read_state_house_price_data(file_name)
        annual = index_tools.annualize(data)
        for val in region_lst:
            index_tools.print_range(data, val)
        filter_data = filter_years(annual,start_year,end_year)
        plot_HPI(filter_data,region_lst)
        plot_whiskers(filter_data,region_lst)
    elif "ZIP" in file_name:
        start_year = int(input("Enter the start year of the range to plot: "))
        end_year = int(input("Enter the end year of the range to plot: "))
        while tracker == True:
            region_name = input("Enter next region for plots (<ENTER> to stop): ")
            if region_name == "":
                tracker = False
            else:
                region_lst.append(region_name)
        data = index_tools.read_zip_house_price_data(file_name)
        filter_data = filter_years(data, start_year, end_year)
        plot_HPI(filter_data, region_lst)
        plot_whiskers(filter_data,region_lst)
    else:
        raise FileNotFoundError(file_name, "file not found")
    return
if __name__ == "__main__":
    main()
