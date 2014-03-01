# This file is part of Improving Tractogrophy
# Copyright (C) 2013-2014 it's respectives authors (please see the AUTHORS file)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
sys.path.append(sys.path[0][:-17])

import unittest

from src.classes.aux.clustering.tv_dbscan import TVDBSCAN

import numpy as np    # Necessary for assertions

class TVDBSCANTestCase(unittest.TestCase):
    def setUp(self):
        self.shape = (2,2,2)
        self.mask = np.ones(self.shape, dtype=np.int16)
        self.tensor = np.zeros((2,2,2,6), dtype=np.int16)
        self.mask[1][1][1] = 0
        self.max_value_difference = 0.1
        self.tensor_statistics_dbscan = TVDBSCAN(1,1,self.mask, self.shape, self.tensor, self.max_value_difference)

    def test_calculate_value(self):
        error = 0.000000000000001

        self.assertTrue((self.tensor_statistics_dbscan.calculate_value((0,0,0)) - 0.0) <= error)
        