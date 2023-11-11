#!/usr/bin/env python3
#TODO: Fix unit tests

import unittest

from pandas.core.frame import DataFrame
from KIBot import *
import re

class Testcases(unittest.TestCase):

    def test_wrong_format(self):
        testcase = "incorrect string format"
        expected = ValueError
        self.assertRaises(expected, search_command, testcase)

    def test_wrong_character(self):
        testcase = "wrongchar"
        expected = ValueError
        self.assertRaises(expected, search_character, testcase)

    def test_wrong_command(self):
        testcase = "12mk"
        expected = ValueError
        self.assertRaises(expected, search_command, testcase)

    
    def test_framedata_search(self):
        testcase = "Jago QCB+HK"
        expected = DataFrame
        command = search_command("QCB+HK")
        char = search_character("Jago")
        df = get_df(char)
        raised = False

        result = findframedata(df, char, command)
        self.assertIsNotNone(result)

    def test_special_notation(self):
        for normal in normals_list:
            for special in specials_list:
                if special == "3K" or special == "3P" or special == "2P" or special == "2K":
                    continue
                testcase = special + "+" + normal
                result = search_command(testcase)
                self.assertIsNotNone(result)

    
    def test_normal_notation(self):
        for normal in command_dict.keys():
            result = search_command(normal)
            self.assertIsNotNone(normal)

    
    def test_char_nicknames(self):
        for tuple in character_dict.keys():
            for nickname in tuple:
                result = search_character(nickname)
                self.assertIsNotNone(result)
    
    def test_target_combo_notation(self):
        for i in range(len(normals_list)):
            for normal in normals_list:
                testcase = f"{normals_list[i]}>{normal}"

                result = search_command(testcase)
                self.assertIsNotNone(testcase)

    def test_rekka_notation(self):

        testcases = []
        
        for normal in normals_list:
            for specials in specials_list:
                if "3P" in specials or "3K" in specials or "2P" in specials or "2K" in specials:
                    continue
                testcases.append(f"{specials}+P > {normal}")
                testcases.append(f'{specials}+P > P > {normal}')
            
        for test in testcases:
            result = search_command(test)
            self.assertIsNotNone(test)

        


    
    def test_char_df_maps(self):
        char_list = ['jago','sabrewulf','glacius', 'thunder', 'shadow_jago', 'sadira', 'orchid', 'spinal', 'fulgore', 'tj_combo', 'maya', 'kan_ra', 'riptor',
                     'omen', 'aganos', 'hisako', 'cinder', 'aria', 'kim_wu', 'tusk', 'arbiter', 'rash', 'mira', 'gargos', 'general_raam', 'eyedol', 'kilgore',
                     'shin_hisako', 'eagle']
        
        for char in char_list:
            char_result = search_character(char)
            df_map = get_df(char_result)
            self.assertIsInstance(df_map, DataFrame)
    
    def test_character_dict(self):
        for tuple in character_dict.keys():
            for nickname in tuple:
                result = search_character(nickname)
                self.assertIsNotNone(result)

    
    #TODO: Write integration test code
    '''
    def test_integration(self):

        test_dictionary = {"Jago":[(19,37), (41,46), (51, 53), (56,58),
                                   (61,63), (66,69), (72, 75), (80,80)]}
        
        for keys, values in test_dictionary.items():
            print(keys, values)
            df_map = get_df(keys)
            for tuple in values:
                for i in range(tuple[0]-1, tuple[1]+1):
                    print(i)
                    s = df_map['Jago']
                    print(df_map.iloc[i, 0])
                    #print(s.iloc[[i]])
                    command = df_map.iloc[i, 0]
                    #print(df_map.iloc[[i]])
                    #print(command)
                    result = findframedata(get_df(keys), keys, [command])
                    print(result)
        return


    
    '''
    '''
    def test_basic(self):
        testcase = "incorrect string format"
        expected = ValueError
        self.assertRaises(expected ,parsemessage, testcase)

    def test_wrong_command(self):
        testcase = 'jago 12mk'
        expected = ValueError
        self.assertRaises(expected, parsemessage, testcase)

    def test_correct_input(self):
        testcase = 'jago 5mk'
        expected = tuple
        #print(parsemessage(testcase))
        self.assertTrue((parsemessage(testcase), expected))


    def test_wrong_char(self):
        testcase = 'fuck 5mk'
        expected = ValueError
        self.assertRaises(expected, parsemessage, testcase)

    def test_df_map(self):
        testcase = 'Jago'
        #expected = type(DataFrame)
        #print()
        #print(expected)
        self.assertFalse(get_df(testcase).empty)

    def test_char_dict(self):
        for char in character_dict.values():
            testcase = char
            self.assertFalse(get_df(testcase).empty)
    
    def test_normal_inputs(self):
        pattern = r'[Jj]*[\d]*([\w]+)'
        for keys, values in command_dict.items():
            #print(keys)
            result = re.search(pattern, keys)
            #print(keys, result, result[1])
            for value in values:
                self.assertTrue(result[1] in value)
                #print(keys, result, result[1], value)
            #self.assertTrue(result in value for value in values)
    
    
    def test_alt_parsemessage(self):
        testcase = 'Jago 5mk'
        expected = tuple
        result = parsemessage_alt(testcase)
        self.assertTrue(result, tuple)

    def test_alt_parsemessage_rekka(self):
        testcase = 'hisako qcf+p > p > HP'
        expected = tuple
        result = parsemessage_alt(testcase)
        self.assertTrue(result, testcase)

    def test_alt_parsemessage_normals(self):
        expected = tuple
        for key in command_dict.keys():
            string = 'Jago '+ key
            self.assertTrue(parsemessage_alt(string), tuple)

    def test_alt_parsemessage_specials(self):
        return
    

    def test_none_return(self):
        testcase = 'jago 4mk'
        expected = type(None)
        #print(parsemessage(testcase))
        tye = type(parsemessage(testcase))
        self.assertTrue(type(parsemessage(testcase) is type(str)))
    '''

if __name__ == '__main__':
   unittest.main()