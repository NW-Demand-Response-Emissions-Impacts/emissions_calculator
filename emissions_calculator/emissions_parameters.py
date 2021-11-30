"""
emissions_parameters.py

Defines directories, constants, and file names
for use in the emissions_calculator and subcomponents.
"""

# Import the os module
import os

# Get the Main folder directory, whether user is in Main/ or in Main/emissions_calculator/
CWD = os.getcwd() #gives .../Main/emissions_calculator if run from emissions calculator folder
CALCULATOR_FOLDER = '/emissions_calculator'
MAIN_FOLDER = CWD.split(CALCULATOR_FOLDER, 1)[0]

# Folders within directory
DIR_CALCULATOR = MAIN_FOLDER + CALCULATOR_FOLDER
DIR_DATA_IN = MAIN_FOLDER + '/input_data/'
DIR_EMISSIONS_RATES = DIR_DATA_IN + 'AvoidedEmissionsRates/'
DIR_DR_POTENTIAL_HRS = DIR_DATA_IN + 'DRPotentialandHours/'
DIR_DATA_PROC = MAIN_FOLDER + '/processed_data/'

# Files to input
# The emissions_calculator will run through the old and new bin data
# Users can also just input one file each in DR_HRS_FILES and DR_POTENTIAL_FILES
# Should move these notes to the user guide
EMISSIONS_SCENARIO_LIST = ['Baseline']
#'EarlyCoalRetirement','LimitedMarkets','NoGasBuildLimits',\
#'OrgMarkets','SCC']
#exclude these other scenarios for now
EMISSIONS_RATES_FILES = ['AvoidedEmissionsRate' + x + '.xlsx' for x in EMISSIONS_SCENARIO_LIST]
DR_NAME = ['oldbins','newbins']
DR_HRS_FILES = ['DRHours_' + x + '.xlsx' for x in DR_NAME]
DR_POTENTIAL_FILES = ['DR RPM Inputs_071420.xlsx','DR RPM Inputs_021621_newaMWbins.xlsx']
DR_SEASONS = [['Winter','Summer'],['Winter','Summer','Fall']]
SUBSET_PRODUCTS = [[0],['DVR','ResTOU']] #for newbins, only want to look at these two
SEASONS_ALLDAYS = ['Winter', 'Spring', 'Summer', 'Fall', 'Annual']

# Constants
DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# factor*emissions rates in lbs CO2e/kWh = metric tons CO2e/MWh
EMISSIONS_CHANGEUNITS = .4536
