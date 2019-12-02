#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sept 10 13:11:00 2017

@author: John Funk
"""
import pandas as pd
import numpy as np
import unittest

class Competitors(pd.DataFrame):
    @property
    def _constructor(self):
        return Competitors

    def get_number_of_competitors(self):
        return self.shape[0]



