import numpy as np
from utils.matfcns import *

# print(TEMP_DENSITY)
PRECISION=4


if __name__ == '__main__':
    assert np.round(temperature2density(12), PRECISION) == 1.238

    v_as=np.array([5, 8, 9])
    rhos=[1.4, 2, 3]
    assert np.round(dragF(v_as[0], rhos[0], area=0.5089), PRECISION) == 5.6106
    assert (np.round(dragF(v_as, area=0.5089), PRECISION) == [4.8255, 12.3534, 15.6347]).all()
    assert (np.round(dragF(v_as, rhos, area=0.63), PRECISION) == [6.9458, 25.4016, 48.2234]).all()

    dx=[1, 10, 100]
    dy=[10, 100, 1000]
    assert (np.round(gradeP(dy, dx), PRECISION) == [1000, 1000, 1000]).all()

    gd=[10, 11, 12] # grade
    mass=95
    assert (np.round(roll_resistF(gd, mass), PRECISION) == [4.6351, 4.6303, 4.6250]).all()

    assert (np.round(gravityF(gd, mass), PRECISION) == [92.7013, 101.8656, 111.0000]).all()

    vec=np.arange(10)
    vec_shift = movmean_shift(vec, 4)
    
    sol = [1., 1.5, 2.0, 3.0, 4.0,  5.0,  6.0,  7.0, np.nan, np.nan]
    assert (np.round(vec_shift[:8], PRECISION) == sol[:8]).all() and np.isnan(vec_shift[8:]).all()


    print('all tests passed')
