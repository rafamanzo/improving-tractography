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

"""Container for FilterMaskNoiseStep class"""

# disable complaints about Module 'numpy' has no 'zeros' member

import sys                    # Makes possible to get the arguments
import os                     # File existence checking
import nibabel as nib         # Lib for reading and writing Nifit1
import numpy as np            # Nibabel is based on Numpy

from src.classes.base.step import Step               # Base class
from src.classes.aux.clustering.fa_dbscan import FADBSCAN
                                                     # Algorithm used for
                                                     #   clustering and noise
                                                     #   reduction

class FAClusteringStep(Step):
    """Applying the DBSCAN algorithm it elimates clusters points
         according to FA values

    """

    def __init__(self):
        self.min_pts = 0
        self.eps = 0
        self.mask_data = []
        self.shape = (0)
        self.clusters = []
        self.maximum_fa_difference = -1.0
        self.tensor_data = [[[]]]
        self.affine = np.eye(4) # pylint: disable-msg=E1101

    def validate_args(self):
        if len(sys.argv) != 6:
            print('This program expects five arguments: tensor file;'+
                  'mask file; DBSCAN eps; DBSCAN min_pts;'+
                  ' maximum FA difference',
                  file=sys.stderr)
            exit(1)
        elif not os.path.isfile(str(sys.argv[1])):
            print('The given tensor file does not exists:\n%s'%
                  str(sys.argv[1]), file=sys.stderr)
            exit(1)
        elif not os.path.isfile(str(sys.argv[2])):
            print('The given mask file does not exists:\n%s'%
                  str(sys.argv[1]), file=sys.stderr)
            exit(1)
        return True

    def load_data(self):
        tensor = nib.load(str(sys.argv[1]))
        self.tensor_data = tensor.get_data()
        self.affine = tensor.get_affine()
        mask = nib.load(str(sys.argv[2]))
        self.mask_data = mask.get_data()
        self.shape = (mask.shape[0], mask.shape[1], mask.shape[2])
        self.eps = int(sys.argv[3])
        self.min_pts = int(sys.argv[4])
        self.maximum_fa_difference = float(sys.argv[5])

    def process(self):
        dbs = FADBSCAN(self.eps, self.min_pts, self.mask_data, self.shape,
                       self.tensor_data, self.maximum_fa_difference)
        self.clusters, _ = dbs.fit()

    def save(self):
            cluster_img = nib.Nifti1Image(
                                    self.__convert_clusters_to_mask(),
                                    self.affine)
            cluster_img.to_filename('fa_clustered_'+
                                          sys.argv[2].split('/')[-1])

    def __convert_clusters_to_mask(self):
        """Gets clusters from DBSCAN and converts them into a mask"""

        mask = np.zeros(self.shape, dtype=np.uint64) # pylint: disable-msg=E1101

        cluster_number = 1
        for cluster in self.clusters:
            for point in cluster:
                mask[point] = cluster_number
            cluster_number += 1

        return mask

