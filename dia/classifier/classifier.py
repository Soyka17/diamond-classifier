from dataclasses import dataclass
from dia.parsers import parsers
import numpy as np


@dataclass
class Stage:
    def __init__(self, t, v, dt, dv):
        self.target = t
        self.value = v
        self.target_delta = dt
        self.value_delta = dv
        self.result = 0


def get_classifiers():
    result = {
        "colorless": colorless_checker,
        "pink": pink_checker
    }
    return result


def colorless_checker(lst):
    nat_res = __nat_colorless_checker(lst)
    result = {
        "P(hpht)": __hpht_colorless_checker(lst),
        "P(cvd)": __cvd_colorless_checker(lst),
        "P(nat_IaAB)": nat_res[0],
        "P(nat_IIa)": nat_res[1],
        "P(nat_IaA)": nat_res[2]
    }
    return result


def __hpht_colorless_checker(lst):
    """
    stage 1 x:30-50 | y:6000-8000  /  13000-15000
    stage 2 x:50-70 | y:6000-8000  /  14000-16000
    stage 3 x:80-90 | y:9200-12000 /  19000-21000
    """
    stages = [0, 0, 0]

    peaks_lst = parsers.parse_peaks(lst)

    for x in peaks_lst:
        if (30 <= x <= 50) and not stages[0]:
            if (6000 < lst[x] < 8000) or (13000 < lst[x] < 15000):
                stages[0] = 1
        if (50 <= x <= 70) and not stages[1]:
            if (6000 < lst[x] < 8000) or (14000 < lst[x] < 16000):
                stages[1] = 1
        if (80 <= x <= 90) and not stages[2]:
            if (9200 < lst[x] < 12000) or (19000 < lst[x] < 21000):
                stages[2] = 1

    return sum(stages) / 3


def __nat_colorless_checker(lst):
    """
    del_x = 3
    del_y = 1250
    STAGE 1: x: 11+-del | y: 5900 +- del | 16300 +- del
    STAGE 2: x: 25+-del | y: 8900 +- del | 23700 +- del
    STAGE 3: x: 35+-del | y: 11200 +- del | 30000 +- del
    STAGE 4: x: 49+-del | y: 11200 +- del | 30000 +- del
    STAGE 5: x: 76+-del | y: 8900 +- del | 23700 +- del

    Nat IaA has one peak at the coordinates
    х: 100-150
    y: 16000-20000

    :return: [P(IaAB), P(IIa), P(IaA)]
    """
    targets = [11, 25, 35, 49, 76]
    valuesI = [5900, 8900, 11200, 11200, 8900]
    valuesII = [16300, 23700, 30000, 30000, 23700]
    stagesI = [0, 0, 0, 0, 0]
    stagesII = [0, 0, 0, 0, 0]
    DELTA_X = 3
    DELTA_Y = 1250

    peaks_lst = parsers.parse_peaks(lst)

    # Determine the probability for IaAB and IIa types
    for x in peaks_lst:
        for i, t in enumerate(targets):
            if t - DELTA_X <= x <= t + DELTA_X:
                if not stagesI[i]:
                    stagesI[i] = __checker(lst, x, valuesI[i], DELTA_Y)
                if not stagesII[i]:
                    stagesII[i] = __checker(lst, x, valuesII[i], DELTA_Y)

    # Determine the probability for IaA type
    x, y = __anti_aliasing(lst, 5)
    peaks = parsers.parse_peaks(y)
    is_IaA_peak = False
    is_another_peak = False
    for i in peaks:
        if __checker(x, i, 125, 25):
            if __checker(y, i, 18000, 2000):
                is_IaA_peak = True
        elif y[i] > 5000:
            is_another_peak = True

    p_IaAB = (sum(stagesI) / len(stagesI))
    p_IIa = (sum(stagesII) / len(stagesII))
    p_IaA = 1.0 if is_IaA_peak and not is_another_peak else 0.0

    return [p_IaAB, p_IIa, p_IaA]


def __cvd_colorless_checker(lst):
    """
    STAGE 1: x: 5+-2 | y: 29000 +- 2000
    STAGE 2: x: 35+-10 | y: 35000 +- 1000
    STAGE 3: x: 54+-3 | y: 37000 +- 1000
    STAGE 4: x: 86+-3 | y: 49500 +- 2000

    :return: P(CVD)
    """

    stages = [
        Stage(5, 29000, 2, 2000),
        Stage(35, 35000, 10, 1000),
        Stage(54, 37000, 3, 1000),
        Stage(86, 49500, 3, 2000)
    ]

    return __stage_checker(lst, stages)

def pink_checker(lst):
    """
    CVD:
        STAGE 1: x: 172+-4 | y: 35000 +- 4000
        STAGE 2: x: 185+-4 | y: 29000 +- 3000
        STAGE 3: x: 217+-4 | y: 38000 +- 1000
    Nat_IaAB:
        STAGE 1: x: 172+-4 | y: 24000 +- 4000
        STAGE 2: x: 187+-4 | y: 22000 +- 3000
        STAGE 3: x: 243+-4 | y: 31000 +- 1000
    HPHT:
        STAGE 1: x: 172+-4 | y: 13330 +- 4000
        STAGE 2: x: 185+-4 | y: 10000 +- 3000
        STAGE 3: x: 217+-4 | y: 12000 +- 1000

    :param lst:
    :return: [P(hpht), P(cvd), P(nat_IaAB)]
    """

    cvd_stages = [
        Stage(172, 35000, 4, 4000),
        Stage(185, 29000, 4, 3000),
        Stage(217, 38000, 4, 1000),
    ]

    nat_IaAB_stages = [
        Stage(172, 24000, 4, 4000),
        Stage(187, 22000, 4, 3000),
        Stage(243, 31000, 4, 1000),
    ]

    hpht_stages = [
        Stage(172, 13300, 4, 4000),
        Stage(185, 10000, 4, 3000),
        Stage(217, 12000, 4, 1000),
    ]

    result = {
        "P(cvd)": __stage_checker(lst, cvd_stages),
        "P(nat_IaAB)": __stage_checker(lst, nat_IaAB_stages),
        "P(hpht)": __stage_checker(lst, hpht_stages),
    }

    return result


def __stage_checker(lst, stages):
    peaks_lst = parsers.parse_peaks(lst)

    for x in peaks_lst:
        for s in stages:
            if s.target - s.target_delta <= x <= s.target + s.target_delta:
                if not s.result:
                    s.result = __checker(lst, x, s.value, s.value_delta)

    result = 0
    for i in stages:
        result += i.result

    return result / len(stages)


def __checker(lst, x, target, delta_y):
    if target - delta_y < lst[x] < target + delta_y:
        return 1
    return 0


def __anti_aliasing(lst, win):
    """
    Graph smoothing function using np.convolve
    :param lst:
    :param win: sliding window for smoothing
    :return filtered_x, filtered_y:
    """

    x = np.array([i for i in range(len(lst))])
    filt = np.ones(win) / win
    mov = win // 2
    filt_x = x[mov:-mov]
    filt_y = np.convolve(lst, filt, mode='same')[mov:-mov]

    return filt_x, filt_y
