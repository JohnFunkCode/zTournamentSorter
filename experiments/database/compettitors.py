#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sept 10 13:11:00 2017

@author: John Funk
"""
import pandas as pd
import numpy as np
import unittest

class Compettitors(pd.DataFrame):
    def get_number_of_compettotors(self):
        return self.shape[0]



