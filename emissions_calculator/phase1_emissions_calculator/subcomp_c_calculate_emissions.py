"""
Subcomponent_c code for calcuating emissions reductions (/increases)

"""

import pandas as pd
import numpy as np
from emissions_parameters import EMISSIONS_CHANGEUNITS


#Function to do ResTOU shifting
def shift_hours(dr_hours, hours_to_shift):
    """

    Args:
        dr_hours: Dataframe of the hours for this dr item

        hours_to_shift: Number of hours to by which to shift on either
            side of original hours. (E.g. if shift_hours = 2 and
            dr is implemented 18-21, then hours 16-17 and 22-23 will
            have -1 vals

    Returns:
        dr_hours_out: dataframe containg hours implemented (+1 value) and hours
            shifted to (-1).
    """

    #Baseline hours for newbins is 18-21

    #Get first index in set of 4
    indecies = dr_hours.loc[dr_hours==1].index
    firsts = np.array([])
    first = True
    ind_prev = 0
    for ind in indecies:
        if first:
            firsts = np.append(firsts, np.array([np.floor(ind)]))
            first = False
            ind_prev = ind
        else:
            first = bool(ind-ind_prev > 1)

            ind_prev = ind

    firsts = firsts.astype(int)
    shift_inds_down_2 = firsts - hours_to_shift
    shift_inds_down_1 = firsts - (hours_to_shift-1)
    shift_inds_up_1 = firsts + (hours_to_shift-1)
    shift_inds_up_2 = firsts + hours_to_shift
    indecies = np.append(shift_inds_down_2,shift_inds_down_1)
    indecies = np.append(indecies,shift_inds_up_1)
    indecies = np.append(indecies,shift_inds_up_2)

    dr_product_shifted = dr_hours.copy()
    dr_product_shifted.loc[indecies] = -1

    dr_hours_out = dr_product_shifted.values

    return dr_hours_out


def sort_bins(dr_info, dr_names):
    """
    Args:
        dr_info:
        dr_names:

    Returns:
        out_dict: dictionary with bin number as keys and dr product names as values.
    """
    out_dict = {}

    for dr_name in dr_names:
        bin_name = dr_info.Bin.loc[dr_info.Product == dr_name].values[0]
        if bin_name in list(out_dict.keys()):
            out_dict[bin_name] = out_dict[bin_name]+[dr_name]
        else:
            out_dict[bin_name] = [dr_name]

    return out_dict


def calc_yearly_avoided_emissions(em_rates, dr_hours, dr_potential, dr_product_info):
    """

    This function uses the loaded data and calculated yearly avoided emissions for the new binning
    Args:
        em_rates: baseline emissions rates
        dr_hours: 
        dr_potential:
        dr_product_info
        
    Returs:
        output_dictionary: Dictionary containing keys such as ['newbins_Bin_1_summer'], 
                            or ['oldbins_Bin_3_winter']. Each entry contains a dataframe
                            of avoided annual avoided emissions for each DR product
                            in that binning+season combination.
        

    """

    output_dictionary = {}
    bins = ['oldbins','newbins']
    seasons = [['Winter','Summer'],['Winter','Summer','Fall']]

    em_rates = em_rates.rename({'Report_Month': 'Month', \
                                'Report_Day': 'Day', "Report_Hour": "hourID"}, axis='columns')

    #Get the start and end years and a list of years.
    #These are constant across newbins/oldbins, etc.
    year_start = min(em_rates.Report_Year)
    year_end = max(em_rates.Report_Year)
    years = np.arange(year_start, year_end+1)

    #Loop over old_bins + new_bins
    for i in range(len(bins)):
        binning = bins[i]
        dr_info = dr_product_info[binning]

        for season in seasons[i]:
            #Get a "olbins_summer" type name
            combo_name = binning + "_" + season
            hrs = dr_hours[combo_name]
            pot = dr_potential[combo_name]
            #Grab the names of the DR policies that
            #are actually implemented for this season.
            #This assumes we have the same formatted DF everytime
            dr_list = list(hrs.columns.values[3:])


            bin_dict = sort_bins(dr_info, dr_list)
            #Loop over every bin number
            for bin_num in list(bin_dict.keys()):
                bin_drs = bin_dict[bin_num]
                start_matrix = np.zeros((len(years), len(bin_drs)+1))
                start_matrix[:, 0] = years.astype(int)
                if binning=='newbins':
                    #modify_resTOU_names
                    new_names = ['DVR', 'ResTOU_shift', 'ResTOU_shed']
                    start_matrix = np.zeros((len(years), len(new_names)+1))
                    start_matrix[:, 0] = years.astype(int)
                    yearly_avoided = pd.DataFrame(data = start_matrix, columns=['Year']+new_names)
                else:
                    start_matrix = np.zeros((len(years), len(bin_drs)+1))
                    start_matrix[:, 0] = years.astype(int)
                    yearly_avoided = pd.DataFrame(data = start_matrix, columns=['Year']+bin_drs)

                for dr_name in bin_drs:
                    #rename things so dataframes more easily compared


                    restou_newbins = False
                    #Ok if its new
                    if binning=='newbins':
                        if dr_name == 'ResTOU':
                            restou_newbins = True

                    # Do Shifting if it's a shift product.
                    shift = dr_product_info[binning]['Shift or Shed?'].\
                    loc[dr_product_info[binning].Product==dr_name]
                    shift = shift.iloc[0]


                    if shift == 'Shift':
                        dr_season_hours = shift_hours(hrs[dr_name], 2)
                        if restou_newbins:
                            dr_season_hours_shed = hrs[dr_name]
                            dr_season_hours_shift = shift_hours(hrs[dr_name], 2)

                        else:
                            dr_season_hours = shift_hours(hrs[dr_name], 2)
                    else:
                        dr_season_hours = hrs[dr_name]

                    for year in range(year_start, year_end+1):
                        dr_pot = pot[dr_name].loc[pot.Year==year]
                        short_df = em_rates.loc[em_rates.Report_Year==year]
                        if year%4==0:
                            #There's no DR implemented on leap years, 
                            #so we can ignore that extra time (last 24 entries)
                            short_df = short_df.iloc[:-24]


                        #Multiply baseline emissions by potential for all hours
                        #This should atomatically work correctly if we have -1 values
                        #due to shifting

                        if restou_newbins:
                            out_arr_shift = short_df["Baseline Emissions Rate Estimate"].\
                            values*dr_season_hours_shift*dr_pot.values * EMISSIONS_CHANGEUNITS
                            out_arr_shed = short_df["Baseline Emissions Rate Estimate"].\
                            values*dr_season_hours_shed*dr_pot.values * EMISSIONS_CHANGEUNITS
                            yearly_avoided["ResTOU_shift"].iloc[year-year_start] = out_arr_shift.sum()
                            yearly_avoided["ResTOU_shed"].iloc[year-year_start] = out_arr_shed.sum()

                        else:
                            out_arr = short_df["Baseline Emissions Rate Estimate"].values*dr_season_hours*dr_pot.values
                            out_arr = out_arr * EMISSIONS_CHANGEUNITS
                            yearly_avoided[dr_name].iloc[year-year_start] = out_arr.sum()

                save_name = binning+"_"+bin_num.split()[0]+"_"+bin_num.split()[1]+"_"+season

                output_dictionary[save_name] = yearly_avoided

    return output_dictionary
                
