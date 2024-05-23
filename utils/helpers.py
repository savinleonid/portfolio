import numpy as np


def diff(self, close_idx=-1, far_idx=-2):
    return self[close_idx] - self[far_idx]


def hist(self):
    _hist = [np.nan]
    for i in range(1, len(self)):
        _hist.append(self[i] - self[i - 1])
    return _hist


def extreme(ema, histogram):
    """Returns closest min or max with its index"""
    start_from = max(np.argwhere(np.isnan(histogram)))[0] + 1
    histogram = histogram[start_from:]  # get rid of nan
    if diff(ema) > 0:
        _max = max(histogram)
        idx_pos = np.where(np.array(histogram) > 0)[0]
        for idx in range(len(histogram) - 1, idx_pos[0], -1):
            if histogram[idx] == _max:
                return idx, _max
    else:
        _min = min(histogram)
        idx_neg = np.where(np.array(histogram) < 0)[0]
        for idx in range(len(histogram) - 1, idx_neg[0], -1):
            if histogram[idx] == _min:
                return idx, _min


def side_checker(stream):
    vse = stream['slow_ema']
    histogram = stream['hist']
    _idx, _extreme = extreme(vse, histogram)
    if _extreme > 0:
        if 90 <= (histogram[-1] / _extreme) * 100:
            return "LONG STRONG"
        elif 90 > ((histogram[-1] / _extreme) * 100) >= 10:
            return "LONG"
        elif 10 > (histogram[-1] / _extreme) * 100 > 5:
            return "LONG ENTERING"
        elif 5 > (histogram[-1] / _extreme) * 100:
            return "CLOSING"
    else:
        if 90 <= (histogram[-1] / _extreme) * 100:
            return "SHORT STRONG"
        elif 90 > ((histogram[-1] / _extreme) * 100) >= 10:
            return "SHORT"
        elif 10 > (histogram[-1] / _extreme) * 100 >= 5:
            return "SHORT ENTERING"
        elif 5 > (histogram[-1] / _extreme) * 100:
            return "CLOSING"


    # if diff(vse) > 0:
    #     return "LONG"
    # elif diff(vse) < 0:
    #     return "SHORT"
    # else:
    #     return "EQUAL"
