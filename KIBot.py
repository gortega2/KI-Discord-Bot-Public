import csv
import sys
import pandas as pd
import re
from tabulate import tabulate

command_dict = {'5LP':["Standing LP", "Close LP", "Far LP"], '2LP':['Crouching LP'], '5MP':('Close MP', 'Far MP', "Standing MP"), '2MP':['Crouching MP'],
'5HP':['Close HP', 'Far HP', 'Standing HP'], '2HP':['Crouching HP'], '6LP':["Forward LP"], '6MP':['Forward MP'], '6HP':["Forward HP"], '3HP':["Down-Forward HP"],
'1HP':['Down-Back HP', 'DB HP'], '4LP':['Back LP'], '4MP':['Back MP'], 
'4HP':["Back HP"], '5LK':['Standing LK', 'Close LK', 'Far LK'], '2LK':['Crouching LK'], '5MK':['Standing MK', 'Close MK', 'Far MK'], '2MK':['Crouching MK'], 
'5HK':['Standing HK', 'Close HK', 'Far HK'], '2HK':['Crouching HK'], '4LK':['Back LK'], '4MK':["Back MK"], '4HK':['Back HK'], '6LK':["Forward LK"], '6MK':["Forward MK"],
'6HK':["Forward HK"], 'JLP':["Jumping LP"], "JMP":["Jumping MP"], 'JHP':['Jumping HP'], 'JLK':["Jumping LK"], 'JMK':['Jumping MK'], 'JHK':['Jumping HK'],
'J6MK':["Jumping Forward MK"], 'J2MK':['Jumping Down MK'], 'J6HK':['Jumping Forward HK'], 'J2HK':['Jumping Down HK'], '44':['Backward Run', 'Backward Dash'],
'66':['Forward Dash', 'Forward Run']}

notation_dict = {('st', 'far', 'fr', 'stand', 'standing'):["Standing", "Far"], ('cr', 'crouch', 'crouching'):['Crouching'], ('cl', 'close'):["Close"], 
                 ('j'):['Jumping']}

normals_list = ['LP', 'MP', 'HP', 'LK', 'MK', 'HK']

specials_list = ['QCB', 'QCF', 'BF', 'DP', 'DU', '3P', '3K']

specials_dict = {'214':'QCB', '236':'QCF', '46':'BF', '623':'DP', '28':'DU'}

character_dict= {('jappa'):'Jago', ('sabre', 'wulf', 'dog', 'doggo'):'Sabrewulf', ('glay', 'cold_shoulder'):'Glacius',
                         ('jhp', 'thun'):'Thunder', ('shago'):'Shadow_Jago', ('sad'):'Sadira', ('orc'):'Orchid', ('tj', 'combo'):'TJ_Combo',
                         ('kan', 'ra',):'Kan_Ra', ('rip', 'dino'):'Riptor', ('fraud','sako'):'Hisako', ('kim', 'wu'):'Kim_Wu',
                         ('arby'):'Arbiter', ('carried_ball'):'Rash', ('raam'):'General_RAAM', ('not_blocking', 'dol'):'Eyedol'}

# Accesses the frame data xls file and then makes a df map from the data
xls = pd.ExcelFile('Killer Instinct Frame Data.xls')
sheet_to_df_map = pd.read_excel(xls, sheet_name=None)
sheet_keys = list(sheet_to_df_map)


# Returns tuple of character and command, raises error if format, char, or command is wrong
# char is a string with the name of the csv file
# command is a list of strings which should match the first column of the csv file depending on move name.
def check_message(char, command):

    char = search_character(char)
    command = search_command(command)
    return (char, command)

def search_character(message):
    char = None
    index = [i for i, x in enumerate(sheet_keys) if x.casefold() == message.casefold()] 
    if len(index) == 0:  # Means that there was no match for default character names
        for x in character_dict.keys():
            if message in x:
                char = character_dict.get(x)
                return char
            
        if char == None:
            raise ValueError('Invalid Character')
    else:
        char = sheet_keys[index[0]]
    return char

# Checks if the command format is valid and returns a list containing string phrases. 
def search_command(message):
    #Different patterns to capture different types of formating/notation. Could be done better but it works
    command = command_dict.get(message.upper())
    normal_pattern = r'([\w]*)\.([23lmh][kp])'
    special_pattern = r'([qcfbdubp]+)\+([23lmh][kp])'
    numeric_pattern = r'([1-9]+)\+([23lmh][kp])'
    target_pattern = r'([qcfbdubplmhkpx]{2,}[ +>lmhpkx23]+)+'
    command_list = []
    
    #Means that command is not in number notation or invalid. 
    if command == None:
        result = re.search(normal_pattern, message.lower())

        # Regex matches with normal command pattern
        if result != None:
            for x in notation_dict.keys():
                if result.group(1).lower() in x:
                    part_1 = notation_dict.get(x)
                    break
            
            if part_1 == None:
                raise ValueError("1st part of command not recognized")
            if result.group(2).upper() in normals_list:
                part_2 = result.group(2).upper()
  
            
            for x in part_1:
                command_list.append(f'{x} {part_2}')
        
        #Regex matches with special commands
        elif re.search(special_pattern, message.lower()) != None:
            command_list.append(message.upper())


        #Regex matches with numerical special commands
        elif re.search(numeric_pattern, message.lower()) != None:
            result = re.search(numeric_pattern, message.lower())

            part1 = specials_dict.get(result.group(1))
            if part1 == None:
                raise ValueError(f"Invalid command: {message}")
            part2 = result.group(2).upper()

            command_list.append(f'{part1}+{part2}')

        #Regex matching with target combos or rekkas
        elif re.search(target_pattern, message.lower()) != None:
            result = re.search(target_pattern, message.lower())

            part1 = result.group(1).upper()
            command_list.append(f'{part1}')
        else:
            raise ValueError(f"Invalid command: {message}")
        
       
    
    else:
        return command

    # Returns a list of strings.   
    return command_list

#Returns tabulated results if specified character and command are found. Otherwise returns an error. 
#TODO: Cleanup Aganos results. Currently lists all frame data of every chunk which clogs results. 
def findframedata(df_map, character, command):
    first_column = df_map.columns[0]
    strict = False

    # If true, makes the regex result more strict to filter target combos and such. Not in use currently
    if strict:

        regex_list = []
        first_column = df_map.columns[0]
        for x in command:
            x = "^" + x + "$"
            regex_list.append(x)
            pattern = r'|'.join(regex_list) #Creates a regex expression
    else:

        # Regular result expression that includes target combos 
        pattern = r'|'.join(command) #Creates a regex expression.

    
    #Creates regex expression that searches the character dataframe.
    pattern = re.sub(r'([+>])', r' *\\\1 *', pattern)
    # This sections drops Enders from appearing on results. May add enders later if specified.
    index = df_map.index[df_map[first_column] == 'Enders'].tolist()[0]
    df_map = df_map.iloc[:index]

    #Returns result from regex pattern, searching the first column for the specified command. 
    result = df_map[df_map[first_column].str.contains(pattern, re.IGNORECASE, na=False,)] 

    #Returns an error if no results are found. Otherwise returns tabulated results. 
    if result.empty:
        raise ValueError('No results found')
    return tabulate(result[[df_map.columns[0], df_map.columns[2], df_map.columns[3], df_map.columns[4], df_map.columns[6], df_map.columns[7], 
                   df_map.columns[8]]], headers='keys', tablefmt='psql' ,showindex=False)
    
def get_df(character):
    #df_map = sheet_to_df_map[character]
    
    return sheet_to_df_map[character]


def send_response(char, command):
    try:
        character, command = check_message(char, command)
    except ValueError as err:
        return err
    
    df = get_df(character)
    try:

        print_statement = findframedata(df, character, command)
    except ValueError as err:
        return err
    return print_statement



def main():
    

    while True:
        try:
            #character, command = parsemessage_alt(input("Enter character name, space, and then command: "))
            p_input = input("CHAR COMMAND: ").split()
            print(p_input[0])
            response = send_response(p_input[0], p_input[1])
        except ValueError as err:
            print(err)
            continue

        print(response)


# Unhastag this if you want to test commands in the terminal line or in python. 
#main()



