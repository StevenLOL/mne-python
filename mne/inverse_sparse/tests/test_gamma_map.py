# Author: Martin Luessi <mluessi@nmr.mgh.harvard.edu>
#
# License: Simplified BSD

import os.path as op
import numpy as np
from nose.tools import assert_true
from numpy.testing import assert_array_almost_equal

from mne.datasets import testing
from mne import read_cov, read_forward_solution, read_evokeds
from mne.cov import regularize
from mne.inverse_sparse import gamma_map
from mne import pick_types_forward

data_path = testing.data_path()
fname_evoked = op.join(data_path, 'MEG', 'sample',
                       'sample_audvis_trunc-ave.fif')
fname_cov = op.join(data_path, 'MEG', 'sample', 'sample_audvis_trunc-cov.fif')
fname_fwd = op.join(data_path, 'MEG', 'sample',
                    'sample_audvis_trunc-meg-eeg-oct-6-fwd.fif')


def test_gamma_map():
    """Test Gamma MAP inverse"""
    forward = read_forward_solution(fname_fwd, force_fixed=False,
                                    surf_ori=True)
    forward = pick_types_forward(forward, meg=False, eeg=True)
    evoked = read_evokeds(fname_evoked, condition=0, baseline=(None, 0))
    evoked.crop(tmin=0, tmax=0.3)

    cov = read_cov(fname_cov)
    cov = regularize(cov, evoked.info)

    alpha = 0.2
    stc = gamma_map(evoked, forward, cov, alpha, tol=1e-5,
                    xyz_same_gamma=True, update_mode=1)
    # idx = np.argmax(np.sum(stc.data ** 2, axis=1))
    # assert_true(np.concatenate(stc.vertno)[idx] == 96397)
    # XXX fix

    stc = gamma_map(evoked, forward, cov, alpha, tol=1e-5,
                    xyz_same_gamma=False, update_mode=1)
    # idx = np.argmax(np.sum(stc.data ** 2, axis=1))
    # assert_true(np.concatenate(stc.vertno)[idx] == 82010)
    # XXX fix

    # force fixed orientation
    stc, res = gamma_map(evoked, forward, cov, alpha, tol=1e-5,
                         xyz_same_gamma=False, update_mode=2,
                         loose=None, return_residual=True)
    # idx = np.argmax(np.sum(stc.data ** 2, axis=1))
    # assert_true(np.concatenate(stc.vertno)[idx] == 83398)
    # XXX fix

    assert_array_almost_equal(evoked.times, res.times)
