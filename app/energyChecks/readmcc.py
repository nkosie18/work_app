# -*- coding: utf-8 -*-
"""
readmcc.py
Created on Fri Aug 01 13:25:39 2021

@author: bez0t
"""


from audioop import bias
import re
import numpy as np
import pandas as pd
from typing import Union
from app.energyChecks.wtscans import XyProfile, PDD
from app.energyChecks.array import STARCHECK, OCT729, OCT1000, OCT1500


def read_file(filepath: str) -> Union[list, STARCHECK, OCT729, OCT1000, OCT1500]:
    """Read a mcc file and create an object from each data part.
    To access the filename in QATrack+ use FILE.name
    
    Only symmetric fields and symmetric offsets are supported.
    
    """
    # default values if information is missing in mcc file.
    offset_in = 0.0
    offset_cr = 0.0
    nominal_fs_in = 100.0
    nominal_fs_cr = 100.0
    scan_depth = 100.0
    ssd = 1000.0
    filter = "FF"
    modality = "X"
    errors =[]

    # list of mcc data objects
    data_obj = []

    with open(filepath) as meas_file:  # elegant way to parse file

        # empty list for data lines "Position\t\tMeasurementValue\t\tReference"
        lines = []
        # mark for data values, they get only edded if copy = true
        copy = False
        # isocenter value for Array files:
        isocenter = 1000.0
        data_type = ""

        for line in meas_file:  # QATrack+ needs "in FILE"
            # strip() removes whitespace characters bevor and after text
            line = line.strip()
            # detect the profile type (profile ore pdd)
            if line.split('=')[0] == "SCAN_CURVETYPE":
                data_type = line.split('=')[1]

            # elektrons or photons?
            if line.split('=')[0] == "MODALITY":
                modality = line.split('=')[1]

            # machine scanned
            if line.split('=')[0] == "LINAC":
                if line.split('=')[1].strip() in ['LINAC 1 ELEKTA', 'L1 ELEKTA VERSA', 'L1 ELEKTA', 'L1 ELEKTA VERSA HD', 'L1', 'ELEKTA L1', 'ELEKTA VERSA L1', 'ELEKTA L1 VERSA', 'ELEKTA L1 VERSA HD', 'ELEKTA LINAC 1']:
                    machine = "L1"
                elif line.split('=')[1].strip() in ['LINAC 2 ELEKTA', 'L2 ELEKTA VERSA', 'L2 ELEKTA', 'L2 ELEKTA VERSA HD', 'L2', 'ELEKTA L2', 'ELEKTA VERSA L2', 'ELEKTA L2 VERSA', 'ELEKTA L2 VERSA HD', 'ELEKTA LINAC 2']:
                    machine = "L2"
                elif line.split('=')[1].strip() in ['LINAC 3 ELEKTA', 'L3 ELEKTA SYNERGY', 'L3 ELEKTA', 'L3 ELEKTA SYNERGY', 'L3', 'ELEKTA L3', 'ELEKTA SYNERGY L3', 'ELEKTA L3 SYNERGY', 'ELEKTA L3 SYNERGY', 'ELEKTA LINAC 3']:
                    machine = "L3"
            
            if line.split('=')[0] == "ENERGY":
                results = line.split('=')[1]
                scan_energy = results.split('.')[0]

            # get field offset information
            if line.split('=')[0] == "COLL_OFFSET_INPLANE":
                offset_in = float(line.split('=')[1])
            if line.split('=')[0] == "COLL_OFFSET_CROSSPLANE":
                offset_cr = float(line.split('=')[1])
                
            # get detector name
            if line.split('=')[0] == "DETECTOR":
                detector = line.split('=')[1]
            
            # get scan offaxis value (useful for starcheck)
            if line.split('=')[0] == "SCAN_OFFAXIS_INPLANE":
                offaxis_in = float(line.split('=')[1])
            if line.split('=')[0] == "SCAN_OFFAXIS_CROSSPLANE":
                offaxis_cr = float(line.split('=')[1])

            # get nominal field/profile size
            if line.split('=')[0] == "FIELD_INPLANE":
                nominal_fs_in = float(line.split('=')[1])
                if nominal_fs_in != 100:
                    errors.append('set-field inplane not 10 x 10')
            if line.split('=')[0] == "FIELD_CROSSPLANE":
                nominal_fs_cr = float(line.split('=')[1])
                if nominal_fs_cr != 100:
                    errors.append('set-field cross_plane not 10 x 10')
            
            # FF or FFF beam
            if line.split('=')[0] == "ENERGY":
                if line.split('=')[1] in ['16.00','110.00' ]:
                    filter1 = "FFF"
            if line.split('=')[0] == "FILTER":
                filter1 = line.split('=')[1]

            # get geometry information
            if line.split("=")[0] == "ISOCENTER":
                isocenter = float(line.split("=")[1])
            if line.split("=")[0] == "SSD":
                ssd = float(line.split("=")[1])
                if ssd != 1000:
                    errors.append('The set SSD not 100 cm')
            if line.split("=")[0] == "SCAN_DEPTH":
                scan_depth = float(line.split("=")[1])

            if line.split("=")[0] == "DETECTOR_HV":
                bias_voltage = float(line.split("=")[1])
            if line.split("=")[0] =='DETECTOR_REFERENCE_HV':
                ref_voltage = float(line.split("=")[1])
                if not ref_voltage == bias_voltage: 
                    errors.append('check your bias voltage')

            

            # find the data block
            if line == "BEGIN_DATA":
                copy = True
            elif line == "END_DATA":
                copy = False
                
                # create object after data block ends
                if data_type == "INPLANE_PROFILE":
                    data = conv_data(lines)
                    data_obj.append(XyProfile(modality, data_type, offset_in,
                                             offaxis_cr, nominal_fs_in, filter,
                                             isocenter, ssd, scan_depth, data))
                    lines = [] # empty line buffer
                
                if data_type == "CROSSPLANE_PROFILE":
                    data = conv_data(lines)
                    data_obj.append(XyProfile(modality, data_type, offset_cr, 
                                             offaxis_in, nominal_fs_cr, filter,
                                             isocenter, ssd, scan_depth, data))
                    lines = [] # empty line buffer
                
                if data_type == "PDD":
                    data = conv_data(lines)
                    energy = scan_energy + modality 

                    data_obj.append(PDD(modality, filter1, machine, energy, data_type, data))


                    # removed: offset, nominal_fs, filter, isocenter, ssd, scan_depth
                    lines = [] # empty line buffer

            elif copy:
                lines.append(line)

    if detector == "STARCHECK":
        return STARCHECK(data_obj)
    elif detector == "OCTAVIUS_729":
        return OCT729(data_obj)
    elif detector == "OCTAVIUS_1000":
        return OCT1000(data_obj)
    elif detector == "OCTAVIUS_1500":
        return OCT1500(data_obj)
    else:
        return data_obj


def conv_data(lines: list) -> pd.DataFrame:
    """Function that converts text lines to numeric data with regular
    expressions and returns a DataFrame
    """

    # \s for unicode (str) patterns, matches whitespace characters
    # \d for unicode (str) patterns, matches decimal digit
    ptw_pattern = re.compile(r'(?P<position>\S+)\s{2}(?P<meas_values>\S+)\s{,2}#*(?P<reference>\S*)')
    data = []
    for line in lines:
        match = ptw_pattern.search(line)
        if match is not None:
            # Create Dict from match and append to data
            data_line = match.groupdict()
            data.append(data_line)

    data = pd.DataFrame(data)  # create DataFrame from list of Dicts
    data = data.apply(pd.to_numeric)  # Convert Strings to np.floats

    return linearize_data(data)


def linearize_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Linearize and upsample the measurement data"""

    # ndarray with 10th mm resolution between first an last measurement
    # position, beginning at the first index (could be smaller than 0!)
    start = dataframe.position[dataframe.first_valid_index()] * 10
    # last index
    stop = dataframe.position[dataframe.last_valid_index()] * 10

    interp_arr = np.arange(start, stop)

    # create dict with single entry to construct dataframe with column names
    dfinter = {"position": interp_arr / 10}
    # convert dict to 1-D dataframe
    dataint = pd.DataFrame(dfinter)

    # connect data frames
    dataint = pd.merge_ordered(dataint, dataframe, on="position",
                                how="outer")
    dataint.meas_values = dataint.meas_values.interpolate()
    #dataint.meas_values = dataint.meas_values.interpolate(method='cubic')

    return dataint

# if __name__ == "__main__":
#     import sys
#     #print(sys.argv[1])
#     mymcc = read_file(sys.argv[1])
#     for i in mymcc:
#         if i.curve_type == "PDD":
#             print(i.calc_pdd())
#         elif i.curve_type == "INPLANE_PROFILE":
#             print(i.calc_profile())
#         elif i.curve_type == "CROSSPLANE_PROFILE":
#             print(i.calc_profile())
