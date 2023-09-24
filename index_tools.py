"""
file: index_tools.py
author: Aneesh Bukya  ab5380@g.rit.edu
course: CSCI 141
assignment: Project
date: 11/10/2022
notes: index tools file
"""
from dataclasses import dataclass

@dataclass
class QuarterHPI():
    """
    a structure or dataclass that allows us to store info on the year, quarter and index of home prices
    year: an integer representing the year of the index value.
    qtr: an integer representing the quarter of the year.
    index: a float representing the home price index.
    """
    year: int
    qtr: int
    index: float

@dataclass
class AnnualHPI():
    """
    a structure or dataclass that allows us to store info on the year and index of home prices
    year: an integer representing the year of the index value.
    qtr: an integer representing the quarter of the year.
    index: a float representing the home price index.
    """
    year: int
    index: float

def read_state_house_price_data(filepath):
    """
    reads the file and creates a dictionary containing list of QuarterHPI objects
    :param filepath: A string giving the path name of a data file.
    :return: A dictionary mapping state abbreviation strings to lists of QuarterHPI objects.
    """
    data = {}
    lst = []
    with open(filepath) as file:
        new_file = file.readlines()[1:]
        for line in new_file:
            new_line = line.split()
            if new_line[0] == "." or new_line[1] == "." or new_line[2] == "." or new_line[3] == ".":
                print("data unavailable:")
                print(line, "warning: data unavailable in original source.")
                print("")
            else:
                if data.get(new_line[0]) == None:
                    lst.append(QuarterHPI(int(new_line[1]), int(new_line[2]), float(new_line[3])))
                    data[new_line[0]] = lst
                    lst = []
                else:
                    lst.append(QuarterHPI(int(new_line[1]), int(new_line[2]), float(new_line[3])))
                    data[new_line[0]] += lst
                    lst = []
    return data

def read_zip_house_price_data(filepath):
    """
    reads the file and creates a dictionary containing list of AnnualHPI objects
    :param filepath: A string giving the path name of a ZIP5 data file.
    :return: A dictionary mapping zip codes to lists of AnnualHPI objects.
    """
    data = {}
    lst = []
    count = 0
    uncount = 0
    with open(filepath) as file:
        new_file = file.readlines()[1:]
        for line in new_file:
            new_line = line.split()
            if new_line[0] == "." or new_line[1] == "." or new_line[3] == ".":
                uncount += 1
            else:
                if data.get(new_line[0]) == None:
                    lst.append(AnnualHPI(int(new_line[1]), float(new_line[3])))
                    data[new_line[0]] = lst
                    count += 1
                    lst = []
                else:
                    lst.append(AnnualHPI(int(new_line[1]), float(new_line[3])))
                    data[new_line[0]] += lst
                    count += 1
                    lst = []
    print("count:",count,"uncounted:",uncount)
    return data

def index_range(data, region):
    """
    finds and returns the low and high index values of the dataset.
    :param data: the dataset in which we look for the highest and lowest indices
    :param region: key of the dictionary in which we want to find the highest and lowest indices
    :return: A tuple of the *HPI objects that are respectively the low and high index values
    of the dataset
    """
    min_obj = data[region][0]
    max_obj = data[region][0]
    for i in range(len(data[region])):
        if min_obj.index > data[region][i].index:
            min_obj = data[region][i]
        elif max_obj.index < data[region][i].index:
            max_obj = data[region][i]
        else:
            continue
    return min_obj,max_obj

def print_range(data, region):
    """
    Prints the low and high values (range) of the house price index for the given region.
    :param data: the dataset in which we look for the highest and lowest indices
    :param region: key of the dictionary in which we want to find the highest and lowest indices
    """
    min_obj, max_obj = index_range(data, region)
    print("Region:",region)
    print("Low: year/quarter/index: ",min_obj.year,"/",min_obj.qtr,"/",min_obj.index)
    print("High: year/quarter/index: ",max_obj.year,"/",max_obj.qtr,"/",max_obj.index)

def print_ranking(data, heading="Ranking"):
    """
    prints the first 10 and last 10 elements in the list
    :param data:  A dictionary mapping regions to lists of HPI objects.
    :param heading: a text message whose default value is “Ranking”
    """
    print(heading)
    print("The Top 10:")
    for i in range(0,10):
        print(i+1," :",data[i])
    print("The Bottom 10:")
    for i in range(10,0,-1):
        print(len(data)-i+1," :",data[-i])

def annualize(data):
    """
    averages lists of QuarterHPI objects to create the lists of AnnualHPI objects
    :param data: A dictionary mapping regions to lists of QuarterHPI objects.
    :return: A dictionary mapping regions to lists of AnnualHPI objects.
    """
    lst = []
    new_data = {}
    annual_index_counter = 0
    counter = 0.0
    for key in data:
        for i in range(len(data[key])):
            if i+1 >= len(data[key]):
                if new_data.get(key) == None:
                    annual_index_counter += data[key][i].index
                    counter += 1
                    lst.append((AnnualHPI(data[key][i].year, (annual_index_counter / counter))))
                    new_data[key] = lst
                    lst = []
                    annual_index_counter = 0
                    counter = 0
                else:
                    annual_index_counter += data[key][i].index
                    counter += 1
                    lst.append((AnnualHPI(data[key][i].year, (annual_index_counter / counter))))
                    new_data[key] += lst
                    lst = []
                    annual_index_counter = 0
                    counter = 0
            elif data[key][i].year == data[key][i+1].year:
                annual_index_counter += data[key][i].index
                counter += 1
            elif annual_index_counter == 0 and counter == 0:
                if new_data.get(key) == None:
                    annual_index_counter += data[key][i].index
                    counter += 1
                    lst.append((AnnualHPI(data[key][i].year, (annual_index_counter/counter))))
                    new_data[key] = lst
                    lst = []
                    annual_index_counter = 0
                    counter = 0
                else:
                    lst.append((AnnualHPI(data[key][i].year, (annual_index_counter/counter))))
                    new_data[key] += lst
                    lst = []
                    annual_index_counter = 0
                    counter = 0

            else:
                annual_index_counter += data[key][i].index
                counter += 1
                if new_data.get(key) == None:
                    lst.append((AnnualHPI(data[key][i].year,(annual_index_counter/counter))))
                    new_data[key] = lst
                    lst = []
                    annual_index_counter = 0
                    counter = 0
                else:
                    lst.append((AnnualHPI(data[key][i].year, (annual_index_counter/counter))))
                    new_data[key] += lst
                    lst = []
                    annual_index_counter = 0
                    counter = 0
    return new_data


def main():
    """
    initializes the code by taking the input from user and displaying the results for the user to view
    """
    tracker = True
    region_lst = []
    file_name = input("Enter house price index file:")
    if "state" in file_name:
        data = read_state_house_price_data(file_name)
    elif "ZIP" in file_name:
        data = read_zip_house_price_data(file_name)
    else:
        raise FileNotFoundError(file_name, "file not found")
    while tracker == True:
        region_name = input("Next region of interest( Hit ENTER to stop):")
        if region_name == "":
            tracker = False
        else:
            region_lst.append(region_name)
    print("="*72)
    for val in region_lst:
        if "state" in file_name:
                print_range(data,val)
                print("Region:", val)
                annual = annualize(data)
                low_val,high_val= index_range(annual,val)
                print("Low: year/index:",low_val.year,"/",low_val.index)
                print("High: year/index:",high_val.year,"/",high_val.index)
                print("Annualized Index Values for",val)
                for i in range(len(annual[val])):
                    print(annual[val][i])
        elif "ZIP" in file_name:
                read_zip_house_price_data(file_name)
                print("Region:", val)
                index_range(data, val)
if __name__ == "__main__":
    main()

