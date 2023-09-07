import numpy as np

TEMP_DENSITY = np.reshape([
-25, 1.4224,
-20, 1.3943,
-15, 1.3673,
-10, 1.3413,
-5, 1.3163,
0, 1.2922,
5, 1.2690,
10, 1.2466,
15, 1.2250,
20, 1.2041,
25, 1.1839,
30, 1.1644,
35, 1.1455,
40, 1.1270], (-1, 2))

def movmean(vec, win, centered=False):
    '''
    Function to replicate matlab's movmean()
    vec: the array to compute moving average for
    win: moving average sliding window size
    centered: whether the moving average window is centered (default False)

    '''
    
    if not centered: # trailing moving average
        nwin = np.sum(win)+1
        conv = np.convolve(vec, np.ones(nwin)/nwin, mode='valid')
        front = []
        for k in range(0, len(vec)-len(conv)):
            front.append(np.mean(vec[0:k+1]))
        conv = np.insert(conv, 0, front)

    else: # centered moving average
        nwin = win
        quo, rem = np.divmod(nwin, 2)
        conv = np.convolve(vec, np.ones(nwin)/nwin, mode='valid')
        front = []
        back = []
        for k in range(0, quo):
            front.append(np.mean(vec[0:nwin-quo+k]))
            back.append(np.mean(vec[k-nwin+1:]))

        conv = np.insert(conv, 0, front)
        if rem == 0:
            conv = np.append(conv, back[:-1])
        else:
            conv = np.append(conv, back)

    return conv

def movmean_shift(vec, win, centered=False):
    '''
    Phase-adjusted movmean()
    '''
    conv = movmean(vec, win, centered)
    shiftamnt = int(win/2)
    conv_shift = np.empty_like(conv)
    conv_shift[:] = np.nan
    conv_shift[:len(conv)-shiftamnt] = conv[shiftamnt:]
    return conv_shift

def conv(a, b):
    '''
    Rewritting np.convolve() so that arrays with not all np.nan 
    elements can return non-nan results.
    '''
    signal_length = len(a)
    kernel_length = len(b)
    output_length = signal_length + kernel_length - 1
    output = [0] * output_length

    for i in range(output_length):
        all_nan = True
        for j in range(kernel_length):
            if i-j >= 0 and i-j < signal_length:
                 ss = a[i-j] * b[j]
                 if not np.isnan(ss):
                    output[i] += ss
                    all_nan = False

        if all_nan:
            output[i] = np.nan
    return output

def xcorr(a, b):
    '''
    Computes the cross-correlation of a & b
    '''
    return conv(a, list(reversed(b)))


def temperature2density(temp):
    '''
    Linearly interpolates air density
    '''
    return np.interp(temp, TEMP_DENSITY[:, 0], TEMP_DENSITY[:, 1])



def dragF(v_as, rho=1.2041, area=0.5089, Cd=0.63):
    '''
    v_as: air speed in mps (meters per second)
    rho: air density (default corresponding to 20C)
    Cd: the dimensionless drag constant
    area: frontal area of the biker in m^2
    returns drag force in N (Newtons; kg m/s^2)
    '''
    return 0.5 * Cd * area * np.multiply(rho, np.power(v_as, 2))


def gradeP(dy, dx):
    '''
    Computes grade (rise/run) percentage
    '''
    if dy == 0 and dx == 0:
        return 0
    else:
        return np.divide(dy, dx) * 100


def gravityF(grade, mass):
    '''
    Computes gravity force in N (kg m/s^2)
    '''
    g = 9.8067 # gravity constant in m/s^2
    return mass * g * np.sin(np.divide(np.arctan2(grade, 100), 1))

def roll_resistF(grade, mass, Crr=0.005):
    '''
    Computes the rolling resistance in N (kg m/s^2)
    Crr: dimensionless coef of rolling resistance 
    '''
    g = 9.8067 # gravity constant in m/s^2
    return Crr * mass * g * np.cos(np.arctan2(np.divide(grade, 100), 1))
