from numpy import array, pi, hstack
from copy import copy

from .simple_arm import SimpleArmEnvironment


def make_arm_config(m_ndims, m_max, s_mins, s_maxs, length_ratio, noise):
    return dict(m_mins=array([-m_max] * m_ndims),
                m_maxs=array([m_max] * m_ndims),
                s_mins=s_mins,
                s_maxs=s_maxs,
                length_ratio=float(length_ratio),
                noise=noise)

low_dim = make_arm_config(3, pi/3, array([-0.5, -1.]), array([1., 1.]), 3, 0.02)
mid_dim = make_arm_config(7, pi/3, array([-0.5, -1.]), array([1., 1.]), 3, 0.02)
hd_dim = make_arm_config(20, pi/12., array([0.2, -0.7]), array([1., 0.7]), 3, 0.02)

environment = SimpleArmEnvironment
configurations = {'low_dimensional': low_dim,
                  'mid_dimensional': mid_dim,
                  'high_dimensional': hd_dim,
                  'default': low_dim}