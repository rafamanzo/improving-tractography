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

"""Container for IsotropyMapStep class"""

# disable complaints about Module 'numpy' has no 'zeros' member
# pylint: disable-msg=E1101

import sys                    # Makes possible to get the arguments
import os                     # File existence checking
import nibabel as nib         # Lib for reading and writing Nifit1
import numpy as np            # Nibabel is based on Numpy

from src.classes.base.cpu_parallel_step import CPUParallelStep

class IsotropyMapStep(CPUParallelStep):
    """Maps voxels with mean diffusivity lower then a given threshold"""

    def validate_args(self):
        if len(sys.argv) != 4:
            print('This program expects three arguments: tensor file;'+
                  ' mask file; and mean diffusivity threshold.',
                  file=sys.stderr)
            exit(1)
        elif not os.path.isfile(str(sys.argv[1])):
            print('The given tensor file does not exists:\n%s'%
                  str(sys.argv[1]), file=sys.stderr)
            exit(1)
        elif not os.path.isfile(str(sys.argv[2])):
            print('The given mask file does not exists:\n%s'%
                  str(sys.argv[2]), file=sys.stderr)
            exit(1)
        return True

    def load_data(self):
        self.tensor_data = nib.load(str(sys.argv[1])).get_data()
        mask = nib.load(str(sys.argv[2]))
        self.threshold = float(sys.argv[3])
        self.shape = mask.shape
        self.mask_data = mask.get_data()
        self.isotropy_mask = np.zeros(self.shape, dtype=np.int16)

    def __mean_diffusivity(self,tensor):
        """Receives an six element array that represents the tensor matrix of
           a given voxel and returns it's mean diffusivity

        """
        # The sum of the three eigenvalues is equal to the trace of the tensor
        return (tensor[0] + tensor[3] + tensor[5])/3

    def process_partition(self, x_range, y_range, z_range):
        for x in range(x_range[0],x_range[1]):
            for y in range(y_range[0],y_range[1]):
                for z in range(z_range[0],z_range[1]):
                    if self.mask_data[x][y][z]:
                        if (self.__mean_diffusivity(self.tensor_data[x][y][z])
                            <= self.threshold):
                            self.isotropy_mask[x][y][z] = 1

    def save(self):
        isotropy_img = nib.Nifti1Image(self.isotropy_mask, np.eye(4))
        isotropy_img.to_filename('isotropy_mask.nii.gz')
