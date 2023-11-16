#!/usr/bin/env python3
#TODO: Fix unit tests

import unittest

from pandas.core.frame import DataFrame
from KIBot import *
import re

class Testcases(unittest.TestCase):

    def run_test_procedure(test_char, command_test):
        char = search_character(test_char)
        df = get_df(char)
        command = search_command_redone(command_test)

        return findframedata(df, command)

    def test_wrong_format(self):
        testcase = "incorrect string format"
        expected = ValueError
        self.assertRaises(expected, search_command, testcase)

    def test_wrong_character(self):
        testcase = "wrongchar"
        expected = ValueError
        self.assertRaises(expected, search_character, testcase)

    def test_wrong_command(self):
        df = get_df('Jago')
        testcase = "12m1231231k"
        expected = ValueError
        self.assertRaises(expected, send_response, df,testcase)

    
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

    



if __name__ == '__main__':
   unittest.main()