data_fields = {
    'N': {
        'c_p': 0,
        'ss_p': 2,
        'c_w': 20,
        'cb': True,
        'construct': True,
        'ss': True,
        'required': False,
        'duplicates_ok': True,
        'combine': False,
        'value_constraints': False,
        'tooltip': "Specify sample as NORMAL.\nNot required field."
    },
    'Group': {
        'c_p': 1,
        'ss_p': 3,
        'c_w': 60,
        'cb': False,
        'ss_tr': 'Batch',
        'construct': True,
        'ss': True,
        'required': True,
        'duplicates_ok': True,
        'combine': False,
        'value_constraints': False,
        'tooltip': "Specify group that sample belongs to.\nMultiple groups are separated by comma, i.e. 1,2.\nRequired field."
    },
    'Sample_ID': {
        'c_p': 2,
        'ss_p': 0,
        'c_w': 128,
        'cb': False,
        'construct': True,
        'ss': True,
        'required': True,
        'duplicates_ok': False,
        'combine': False,
        'value_constraints': False,
        'tooltip': "Specify Sample_ID.\nMust be unique.\nRequired field."
    },
    'Sample_Name': {
        'c_p': -1,
        'ss_p': 1,
        'c_w': -1,
        'cb': False,
        'construct': False,
        'ss': True,
        'required': False,
        'duplicates_ok': True,
        'combine': False,
        'value_constraints': False
    },
    'Library_ID': {
        'c_p': 4,
        'ss_p': 4,
        'c_w': 128,
        'cb': False,
        'construct': True,
        'ss': True,
        'required': True,
        'duplicates_ok': True,
        'combine': False,
        'value_constraints': False,
        'tooltip': "Specify Library_ID, such as date\nwhen library was made.\nRequired field."

    },
    'Sex': {
        'c_p': 3,
        'ss_p': 5,
        'c_w': 30,
        'cb': False,
        'construct': True,
        'ss': True,
        'required': True,
        'duplicates_ok': True,
        'combine': False,
        'value_constraints': "m,f",
        'tooltip': "Sex of sample, allowed values: m/f.\nRequired field."
    },
    'I5_Index_ID': {
        'c_p': 5,
        'ss_p': 6,
        'c_w': 128,
        'cb': False,
        'construct': True,
        'ss': True,
        'required': False,
        'duplicates_ok': True,
        'combine': False,
        'value_constraints': False,
        'tooltip': "Combination of I5_Index_ID and I7_Index_ID\nmust be unique for each sample.\nNot required field."
    },
    'index2': {
        'c_p': -1,
        'c_w': -1,
        'ss_p': 7,
        'cb': False,
        'construct': False,
        'ss': True,
        'required': False,
        'duplicates_ok': True,
        'combine': False,
        'value_constraints': False
    },
    'I7_Index_ID': {
        'c_p': 6,
        'ss_p': 8,
        'c_w': 128,
        'cb': False,
        'construct': True,
        'ss': True,
        'required': True,
        'duplicates_ok': True,
        'combine': False,
        'value_constraints': False,
        'tooltip': "Combination of I5_Index_ID and I7_Index_ID\nmust be unique for each sample.\nIf I5_Index_ID is not populated I7_Index_ID must be unique.\nRequired field."
    },
    'index': {
        'c_p': -1,
        'ss_p': 9,
        'c_w': -1,
        'cb': False,
        'construct': False,
        'ss': True,
        'required': False,
        'duplicates_ok': True,
        'combine': False,
        'value_constraints': False
    },
    'I7_Index_ID+I5_Index_ID': {
        'c_p': -1,
        'ss_p': -1,
        'c_w': -1,
        'cb': False,
        'construct': False,
        'ss': False,
        'required': True,
        'duplicates_ok': False,
        'combine': "I7_Index_ID,I5_Index_ID",
        'value_constraints': False
    },
    'Definition': {
        'c_p': 8,
        'ss_p': 10,
        'c_w': 128,
        'cb': False,
        'construct': True,
        'ss': True,
        'required': True,
        'duplicates_ok': True,
        'combine': False,
        'value_constraints': False,
        'tooltip': "Analysis_Def specifies definition file containing available\nanalyses (gene sets) under the Analysis field.\nOnly files in the Definition combobox are allowed.\nRequired field."
    },
#    'Panel': {
#        'c_p':-1,
#        'ss_p': 11,
#        'c_w': 128,
#        'cb': False,
#        'construct': False,
#        'ss': True,
#        'required': False,
#        'duplicates_ok': True,
#        'combine': False,
#        'value_constraints': False,
#        'tooltip': "Panel specifies selected panel. contains definition file specifying available\nanalyses (gene sets)under the Analysis field.\nOnly files in the Definition combobox are allowed.\nRequired field."
#    },
    'Method': {
        'c_p': -1,
        'ss_p': 12,
        'c_w': 128,
        'cb': False,
        'construct': False,
        'ss': True,
        'required': False,
        'duplicates_ok': True,
        'combine': False,
        'value_constraints': False
    },
    'Panel': {
        'c_p': 7,
        'ss_p': 13,
        'c_w': 128,
        'cb': False,
        'construct': True,
        'ss': True,
        'required': True,
        'duplicates_ok': True,
        'combine': False,
        'value_constraints': False,
        'tooltip': "Panel specifies selected panel. contains definition file specifying available\nanalyses (gene sets)under the Analysis field.\nOnly files in the Definition combobox are allowed.\nRequired field."
    },
    'Analysis': {
        'c_p': 9,
        'ss_p': 14,
        'c_w': 128,
        'cb': False,
        'construct': True,
        'ss': True,
        'required': True,
        'duplicates_ok': True,
        'combine': False,
        'value_constraints': False,
        'tooltip': "Analysis specifies selected present in selected Definition."
    },
    'Comment': {
        'c_p': 10,
        'ss_p': 15,
        'c_w': 128,
        'cb': False,
        'construct': True,
        'ss': True,
        'required': False,
        'duplicates_ok': True,
        'combine': False,
        'value_constraints': False
    },
}
