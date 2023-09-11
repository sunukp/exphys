import numpy as np
from src.utils.matfcns import *

PRECISION=4


if __name__ == '__main__':
    assert np.isclose(temperature2density(12), 1.23796)

    v_as=np.array([5, 8, 9])
    rhos=[1.4, 2, 3]
    assert np.isclose(dragF(v_as[0], rhos[0], area=0.5089), 5.6106)
    assert np.allclose(dragF(v_as, area=0.5089), [4.8255, 12.3534, 15.6347])
    assert np.allclose(dragF(v_as, rhos, area=0.63), [6.9458, 25.4016, 48.2234])


    dx=[1, 10, 100, 0, 0]
    dy=[10, 100, 1000, 0, 1]
    gd=gradePrcnt(dy, dx)
    assert np.allclose(gd[:-1], [1000, 1000, 1000, 0])


    gd=[10, 11, 12] # grade
    mass=95
    assert np.allclose(roll_resistF(gd, mass), [4.6351, 4.6303, 4.6250])


    assert np.allclose(gravityF(gd, mass), [92.7013, 101.8656, 111.0000])


    vec=np.arange(10)
    vec_shift = movmean_shift(vec, 4)
    
    sol = [1., 1.5, 2.0, 3.0, 4.0,  5.0,  6.0,  7.0, np.nan, np.nan]
    assert np.allclose(vec_shift[:8], sol[:8])
    assert np.isnan(vec_shift[8:]).all()


    print('all tests passed')
