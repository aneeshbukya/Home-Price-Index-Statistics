"""
file: period_ranking.py
author: Aneesh Bukya  ab5380@g.rit.edu
course: CSCI 141
assignment: Project
date: 11/10/2022
notes: period ranking file
"""
import index_tools

def quarter_data(data, year, qtr):
    """
    sorts a dictionary of list of QuarterHPI objects by its HPI value from high value HPI to low value HPI
    based on a given year and quarter
    :param data: The data is a dictionary mapping a state region to a list of QuarterHPI instances.
    :param year: the year of interest
    :param qtr: the quarter of interest, expressed as an integer between 1 and 4
    :return: A list of (region, HPI) tuples sorted from high value HPI to low value HPI.
    """
    lst = []
    for key in data:
        for i in range(len(data[key])):
            if data[key][i].year == year and data[key][i].qtr == qtr:
                lst_tuple = (key,data[key][i].index)
                lst.append(lst_tuple)
    lst.sort(key=lambda n: n[1], reverse=True)
    return lst

def annual_data(data, year):
    """
    sorts a dictionary of list of AnnualHPI objects by its HPI value from high value HPI to low value HPI
    based on a given year and quarter
    :param data: a dictionary mapping a state or zip code to a list of AnnualHPI objects
    :param year: the year of interest
    :return: A list of (region, HPI) tuples sorted from high value HPI to low value HPI
    """
    lst = []
    for key in data:
        for i in range(len(data[key])):
            if data[key][i].year == year:
                lst_tuple = (key, data[key][i].index)
                lst.append(lst_tuple)
    lst.sort(key=lambda n: n[1], reverse=True)
    return lst

def main():
    """
    initializes the code by taking the input from user and displaying the results for the user to view
    """
    file_name = input("Enter house price index file: ")
    year = int(input("Enter year of interest for house prices: "))
    if "state" in file_name:
        data = index_tools.read_state_house_price_data(file_name)
        annual = index_tools.annualize(data)
        annual_lst = annual_data(annual, year)
    elif "ZIP" in file_name:
        data = index_tools.read_zip_house_price_data(file_name)
        annual_lst = annual_data(data, year)
    else:
        raise FileNotFoundError(file_name, "file not found")
    print()
    index_tools.print_ranking(annual_lst,str(year)+" "+"Annual Ranking")
if __name__ == "__main__":
    main()
