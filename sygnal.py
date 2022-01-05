import numpy as np

def wygladz(sygnal, promien):
    """Wygładzanie sygnału filtrem uśredniającym.
    Uwaga! Wartości na brzegach zakresu są wygładzane we fragmencie okna
    znajdującym się nad zakresem, np. dla promienia 1 (długość okna 3):
    [ 1 2 6 4 5]
    [ 1.5 ]
    [ 3 ]
    [ 4 ]
    [ 5 ]
    [ 4.5 ]
    Args:
    sygnal (numpy.array): sygnał
    promien (int): promien uśredniania (długość okna = 2 x promien + 1)
    Returns:
    numpy.array: wygładzony sygnał
    Raises:
    ValueError: jeśli podano ujemny promień
    """
    if promien < 0:
        raise ValueError("Promień nie może być ujemny")
    arr = np.array([], dtype="float_")
    w = 2 * promien + 1
    if w > len(sygnal) and len(sygnal) > 0:
        return np.mean(sygnal)
    cs = np.cumsum(sygnal)
    for i in range(len(sygnal)):
        if i - promien < 0:
            arr = np.append(arr, cs[i + promien] / (i + promien + 1))
        elif i + promien > len(sygnal) - 1:
            arr = np.append(arr, (cs[-1] - cs[i - (promien + 1)]) / (len(sygnal) - i + promien))
        else:
            arr = np.append(arr, np.average(sygnal[i - promien:(i + promien + 1)]))
    return arr


# tu była druga funkcja ale sobie poszła, pytać priv
