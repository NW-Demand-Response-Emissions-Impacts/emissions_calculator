"""
emissions_calculator.py

Runs all subcomponents to output processed emissions impacts data
for the dashboard.
"""

from subcomp_a_organize_data import subcomp_a_runall
from subcomp_b_process_emissions_factors import subcomp_b_runall
from subcomp_d_output_data \
        import output_avg_emissions_rates, output_dr_hours, output_dr_potential

# File information to be updated by data analyst users
emissions_scenario_list = ['Baseline']
#'EarlyCoalRetirement','LimitedMarkets','NoGasBuildLimits',\
#'OrgMarkets','SCC']
#exclude these other scenarios for now
emissions_rates_files = ['AvoidedEmissionsRate' + x + '.xlsx' for x in emissions_scenario_list]
EMISSIONS_YEAR = 2022 #year to show emissions rates for gen pub
dr_name = ['oldbins','newbins']
dr_hrs_files = ['DRHours_' + x + '.xlsx' for x in dr_name]

# For each plan in dr_name, list the DR potential file,
# seasons with DR hours, and the subset of products to include
# ([0] for all products)
dr_potential_files = ['DR RPM Inputs_071420.xlsx','DR RPM Inputs_021621_newaMWbins.xlsx']
dr_seasons = [['Winter','Summer'],['Winter','Summer','Fall']]
subset_products = [[0],['DVR','ResTOU']] #for newbins, only want to look at these two

# Read files and create dataframes
print('Running subcomponent a')
emissions_rates_df_out, dr_hours_df_dict_out, \
dr_potential_df_dict_out, dr_product_info_df_dict_out = \
        subcomp_a_runall(emissions_rates_files, emissions_scenario_list, \
                        dr_hrs_files, dr_name, dr_seasons, dr_potential_files, subset_products)

# Calculate average hourly emissions rates for dashboard
print('Running subcomponent b')
df_seasonal_ave, df_annual_ave, df_oneyear_seasonal_ave = \
                        subcomp_b_runall(dr_name, dr_seasons, emissions_scenario_list,\
                                emissions_rates_df_out, dr_hours_df_dict_out, EMISSIONS_YEAR)

# Calculate emissions impacts

# Output csv files for dashboard
print('Running subcomponent d')
output_avg_emissions_rates(df_seasonal_ave, df_annual_ave, df_oneyear_seasonal_ave, EMISSIONS_YEAR)
output_dr_hours(dr_hours_df_dict_out)
output_dr_potential(dr_potential_df_dict_out, dr_product_info_df_dict_out)
    