def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def pstdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5

def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0

def findStatistics(dataObj):
    dataObjMean = round(mean(dataObj),3) if len(dataObj) > 0 else float('nan')
    dataObjMin = round(min(dataObj),3) if len(dataObj) > 0 else float('nan')
    dataObjMax = round(max(dataObj),3) if len(dataObj) > 0 else float('nan')
    dataObjStdev = round(pstdev(dataObj),3) if len(dataObj) > 1 else float('nan')
    dataObjMedian = round(median(dataObj),3) if len(dataObj) > 0 else float('nan')
    dataObjMode = round(max(set(dataObj), key=dataObj.count),3) if len(dataObj) > 0 else float('nan')

    return (dataObjMean, dataObjMin, dataObjMax, dataObjStdev, dataObjMedian, dataObjMode)

