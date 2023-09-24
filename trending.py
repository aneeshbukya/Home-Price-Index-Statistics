"""
file: trending.py
author: Aneesh Bukya  ab5380@g.rit.edu
course: CSCI 141
assignment: Project
date: 11/10/2022
notes: trending file
"""
import index_tools

def cagr(idxlist, periods):
    """
    Computes the compound annual growth rate, CAGR, for a period
    :param idxlist: a 2-item list of [HPI0, HPI1], where HPI0 is the index value of the earlier period
    :param periods: the number (N) of periods (years) between the two HPI values in the list
    :return: A float representing the compound annual growth rate
    """
    idx_zero = idxlist[0]
    idx_one = idxlist[1]
    val = (((idx_one/idx_zero)**(1/periods))-1)*100
    return val

def calculate_trends(data, year0, year1):
    """
    reports the compound average growth rate values
    :param data: a dictionary from region to a list of AnnualHPI
    :param year0: the period of interest
    :param year1: the period of interest
    :return: A list of (region, rate) tuples sorted in descending order by the compound annual growth rate
    """
    lst = []
    val1 = 0
    val2 = 0
    for key in data:
        for i in range(len(data[key])):
            if data[key][i].year == year0:
                val1 = data[key][i].index
            elif data[key][i].year == year1:
                val2 = data[key][i].index
            else:
                continue
        if val1 == 0 or val2 == 0 :
            continue
        else:
            val = cagr([val1,val2],year1-year0)
            lst_tuple = (key,val)
            lst.append(lst_tuple)
            val1 = 0
            val2 = 0
    lst.sort(key=lambda n: n[1], reverse=True)
    return lst

def main():
    """
    initializes the code by taking the input from user and displaying the results for the user to view
    """
    file_name = input("Enter house price index filename: ")
    if "state" in file_name:
        data = index_tools.read_state_house_price_data(file_name)
        annual = index_tools.annualize(data)
    elif "ZIP" in file_name:
        annual = index_tools.read_zip_house_price_data(file_name)
    else:
        raise FileNotFoundError(file_name, "file not found")
    start_year = int(input("Enter start year of interest:"))
    end_year = int(input("Enter ending year of interest:"))
    print()
    index_tools.print_ranking(calculate_trends(annual,start_year,end_year),str(start_year)+"-"+str(end_year)+" Compound Annual Growth Rate")
if __name__ == "__main__":
    main()
