# This file is part of Improving Tractogrophy
# Copyright (C) 2013 it's respectives authors (please see the AUTHORS file)
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
sys.path.append(sys.path[0][:-18])

import unittest
from unittest.mock import Mock

from src.classes.fa_threshold_map_step import FAThresholdMapStep

class FAThresholdMapStepTestCase(unittest.TestCase):
    def setUp(self):
        self.fa_threshold_map_step = FAThresholdMapStep()

    def test_check_threshold_for(self):
        self.fa_threshold_map_step.threshold = 0.5

        self.assertTrue(self.fa_threshold_map_step.check_for_threshold((1,0,0,0,0,0)))
        self.assertFalse(self.fa_threshold_map_step.check_for_threshold((1,0,0,1,0,1)))