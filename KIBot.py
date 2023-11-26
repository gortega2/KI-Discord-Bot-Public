import csv
import sys
import pandas as pd
import re
from tabulate import tabulate

command_dict = {'5LP':["Standing LP", "Close LP", "Far LP"], '2LP':['Crouching LP'], '5MP':('Close MP', 'Far MP', "Standing MP"), '2MP':['Crouching MP'],
'5HP':['Close HP', 'Far HP', 'Standing HP'], '2HP':['Crouching HP'], '6LP':["Forward LP"], '6MP':['Forward MP'], '6HP':["Forward HP"], '3HP':["Down-Forward HP"],
'1HP':['Down-Back HP', 'DB HP'], '4LP':['Back LP'], '4MP':['Back MP'], 
'4HP':["Back HP"], '5LK':['Standing LK', 'Close LK', 'Far LK'], '2LK':['Crouching LK'], '5MK':['Standing MK', 'Close MK', 'Far MK'], '2MK':['Crouching MK'], 
'5HK':['Standing HK', 'Close HK', 'Far HK'], '2HK':['Crouching HK'], '3HK':['Down-Forward HK', 'DF+HK'], '4LK':['Back LK'], '4MK':["Back MK"], '4HK':['Back HK'], '6LK':["Forward LK"], '6MK':["Forward MK"],
'6HK':["Forward HK"], 'JLP':["Jumping LP"], "JMP":["Jumping MP"], 'JHP':['Jumping HP'], 'JLK':["Jumping LK"], 'JMK':['Jumping MK'], 'JHK':['Jumping HK'],
'J6MK':["Jumping Forward MK"], 'J2MK':['Jumping Down MK'], 'J6HK':['Jumping Forward HK'], 'J2HK':['Jumping Down HK'], '44':['Backward Run', 'Backward Dash'],
'66':['Forward Dash', 'Forward Run']}

command_regex_pattern = '('+'|'.join(command_dict.keys()) + ')'

numeric_dict ={'J1':'Jumping Down-Back', 'J2':'Jumping Down', 'J3':'Jumping Down-Forward', 'J4':'Jumping Back', 'J6':'Jumping Forward',
               '1':'Down-Back', '2':'Crouching', '3':'Down-Forward', '4':'Back', 'C5':'Close', '5':'Standing', '6':'Forward',
               }

#inv_command_dict = {v: k for k, v in command_dict.items()}
#inv_command_dict = {item: key for key, values in command_dict.items() for item in values}



notation_dict = {('ST', 'FAR', 'FR', 'STAND', 'STANDING'):"Standing", ('CR', 'CROUCH', 'CROUCHING'):'Crouching', ('CL', 'CLOSE'):"Close", 
                 ('J',):'Jumping', ('B', 'BACK'):"Back", ('FOR', 'F', 'FORWARD'):'Forward', ('DF',):'Down-Forward', ('DB',):'Down-Back',
                 ('JD',):'Jumping Down', ('JDF',): 'Jumping Down-Forward', ('JB',):'Jumping Back', ('JDB',):'Jumping Down-Back', 
                 ('JF',):'Jumping Forward'}


abbreviation_dict = {'Standing':"St.", 'Far':'St.', 'Crouching':"Cr.", 'Close':'Cl.', 'Jumping':'J.',
                     'Back':'B.', 'Forward':'F.', 'Down-Forward':'Df.'}

normals_list = ['LP', 'MP', 'HP', 'LK', 'MK', 'HK']

specials_list = ['QCB', 'QCF', 'BF', 'DP', 'DU', '3P', '3K', '2P', '3P']

specials_dict = {'214':'QCB', '236':'QCF', '46':'BF', '623':'DP', '28':'DU'}

character_dict= {('JAPPA', ):'Jago', ('SABRE', 'WULF', 'DOG', 'DOGGO'):'Sabrewulf', ('GLAY', 'COLD_SHOULDER'):'Glacius',
                         ('JHP', 'THUN'):'Thunder', ('SHAGO'):'Shadow_Jago', ('SAD', ):'Sadira', ('ORC', ):'Orchid', ('TJ', 'COMBO'):'TJ_Combo',
                         ('KAN', 'RA',):'Kan_Ra', ('RIP', 'DINO'):'Riptor', ('FRAUD','SAKO'):'Hisako', ('KIM', 'WU'):'Kim_Wu',
                         ('ARBY', ):'Arbiter', ('CARRIED_BALL', ):'Rash', ('RAAM', ):'General_RAAM', ('NOT_BLOCKING', 'EYE', 'DOL'):'Eyedol',
                         }

# Accesses the frame data xls file and then makes a df map from the data
xls = pd.ExcelFile('Killer Instinct Frame Data.xls')
sheet_to_df_map = pd.read_excel(xls, sheet_name=None)
sheet_keys = list(sheet_to_df_map)


# Returns tuple of character and command, raises error if format, char, or command is wrong
# char is a string with the name of the csv file
# command is a list of strings which should match the first column of the csv file depending on move name.
def check_message(char, command):

    char = search_character(char.upper())
    command = search_command_redone(command.upper())
    #command = search_command(command)
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
    special_pattern = r'([qcfbdubp]+)[+]?([23lmh][kp])'
    numeric_pattern = r'([1-9]+)[+]?([23lmh][kp])'
    target_pattern = r'(^[qcfbdubplmhkpx]{2,}[ +>lmhpkx23]+)+'
    num_target_pattern = r'([1-9lmhkpx+]+)'
    command_list = []
    
    #Means that command is not in number notation or invalid. 
    if command == None:
        result = re.search(normal_pattern, message.lower())

        # Regex matches with normal command pattern
        part_1 = None
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
        elif re.search(numeric_pattern, message.lower()) != None and '>' not in message:
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

        #Regex matching with target combos or rekkas using numerical notation
        elif re.search(num_target_pattern, message.lower()) != None:
            test = message.upper()
            result = re.findall(num_target_pattern, message.lower())
            #TODO: 1. Translate all special notations to regular notation
            #TODO: 2. Check for anime normal notation at the start of the string


            #First, sub any anime special notation with normal special notation
            for key, value in specials_dict.items():
                test = re.sub(f'{key}[+]?', f'{value}+', test)

            if re.search(command_regex_pattern, test.upper()) != None:
                split_string = test.split('>')
                part_1 = command_dict.get(split_string[0].upper())
                for x in part_1:
                    command_list.append(f'{x}>{">".join(split_string[1:])}')
            else:
                command_list.append(test)

            return command_list


        else:
            
            raise ValueError(f"Invalid command: {message}")
        
       
    
    else:
        return command

    # Returns a list of strings.   
    return command_list

#Returns tabulated results if specified character and command are found. Otherwise returns an error. 
#TODO: Cleanup Aganos results. Currently lists all frame data of every chunk which clogs results. 

def search_command_redone(command):
    #First, check if the command inputted has a numeric value which indicates it's using anime notation (not [2/3][P/K])
    numeric_pattern = r'[1-9]{2,3}'
    one_digit = r'[J]?[1-9]{1,1}(?![PK])'
    special_pattern = '|'.join(specials_list[0:4])
    normal_pattern = r'[\w]+[.+](?=[\w])'
    result = command

    if re.search(numeric_pattern, result):
        #Replace 2-3 digit notations first
        for key, value in specials_dict.items():
            result = re.sub(f'{key}[+]?', f'{value}+', result)
        
    if re.search(one_digit, result):
        # Replace 1-digit notation after
        for key, value in numeric_dict.items():
            test_pattern = f'{key}(?![PK])'
            result= re.sub(test_pattern, f'{value} ', result)
        
    
    #Format normal notation specialssend_responsepecial}+', result)

    #subsitue abbreivations for full names 
    if re.search(normal_pattern, result):
        for keys, values in notation_dict.items():
            for phrase in keys:
                test_pattern = f'^{phrase}[+.]'
                result = re.sub(test_pattern, f'{values} ', result)

    
    result = re.sub('PPP', '3P', result)
    result = re.sub('PP', '2P', result)
    result = re.sub('KKK', '3K', result)
    result = re.sub('KK', '2K', result)
    return [result]
def findframedata(df_map, command):
    first_column = df_map.columns[0]
    strict = False

    # If true, makes the regex result more strict to filter target combos and such. Not in use currently
    if strict:

        regex_list = []
        first_column = df_map.columns[0]
        for x in command:
            x = "^" + x + "$"
            x = f'^{x}$'
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
    result = df_map[df_map[first_column].str.contains(f'(?i){pattern}', re.IGNORECASE, na=False,)].copy()
    result.reset_index(drop=True, inplace=True)

    #Returns an error if no results are found. Otherwise returns tabulated results. 
    if result.empty:
        print('test')
        raise ValueError('No results found')
    #return tabulate(result[[df_map.columns[0], df_map.columns[2], df_map.columns[3], df_map.columns[4], df_map.columns[6], df_map.columns[7], 
                   #df_map.columns[8]]], headers='keys', tablefmt='simple' ,showindex=False, numalign='right')

    
    #print(abbreivate_response(result))
    abbreivate_response(result)
    #result.rename(columns={result.columns[2]:'SU', result.columns[6]:'OH', result.columns[7]:'OB'}, inplace=True)
    formatted_string = format_response(result)
    return formatted_string
    
    #Old return that formatted results with tabulate
    return tabulate(result[[result.columns[0], result.columns[2], result.columns[6], result.columns[7]]], 
                    headers='keys', tablefmt='simple' ,showindex=False, numalign='right')
    
def get_df(character):
    #df_map = sheet_to_df_map[character]
    
    return sheet_to_df_map[character]


def send_response(char, command):
    character, command = check_message(char, command)
    df = get_df(character)
    print_statement = findframedata(df, command)
    return print_statement


#Abbreviates results from search to better fit mobile and smaller screens
def abbreivate_response(table):
    pattern = r"[ ]+"
    '''
    for row_name in table.iloc[:,0]:
        value = inv_command_dict.get(row_name)
        if value != None:
            #table.at[row_name, 0] = value
            print(table)
            '''

    for i in range(len(table.index)):
        index =  table.iloc[i,0]
        # Remove spaces from results
        index = re.sub(r"[ ]+", '', index)
        for keys, value in abbreviation_dict.items():
                if keys in index:
                    result = re.sub(keys, value, index)
                    table.iloc[i,0] = result
                    break

        #value = inv_command_dict.get(index)
        #if value != None:
            #table.iloc[i,0] = value      
    return table

def format_response(result_df):
    string = f"{result_df.columns[0]}\n"
    for i in range(len(result_df.index)):
        string += f"{result_df.iloc[i,0]}\n"
        string += f"{result_df.columns[2]}: {result_df.iloc[i,2]}\n"
        string += f"{result_df.columns[6]}: {result_df.iloc[i,6]}\n"
        string += f"{result_df.columns[7]}: {result_df.iloc[i,7]}\n"
        string += "\n"
        
    return string

def main():
    

    while True:
        try:
            #character, command = parsemessage_alt(input("Enter character name, space, and then command: "))
            p_input = input("CHAR COMMAND: ").split()
            #print(p_input[0])
            response = send_response(p_input[0], p_input[1])
        except ValueError as err:
            print(type(err))
            print(err)
            continue

        print(response)


# Unhastag this if you want to test commands in the terminal line or in python. 
#main()



