import numpy as np

# przeczytaj i wyjeb wszystkie komentarze z ! na początku przed wysłaniem

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
    cs = np.cumsum(sygnal) # ! sumy kumulatywne, najpierw suma 1 el., potem 2, potem 3 itd
    for i in range(len(sygnal)): # ! dobra to jest tak rozjebane, że ci jupytera napiszę
        if i - promien < 0:
            arr = np.append(arr, cs[i + promien] / (i + promien + 1))
        elif i + promien > len(sygnal) - 1:
            arr = np.append(arr, (cs[-1] - cs[i - (promien + 1)]) / (len(sygnal) - i + promien))
        else:
            arr = np.append(arr, np.average(sygnal[i - promien:(i + promien + 1)]))
    return arr



def szukaj_pikow(sygnal, promien, brzegi=True):
    """Szukanie pozycji pików (ekstremów) w sygnale
    Args:
    sygnal (numpy.array): sygnał
    promien (int): promien izolacji piku (otoczenie, w którym
    pik stanowi wartość ekstremalną)
    brzegi (bool): sposób traktowania brzegów zakresu:
    uwzględniane (True, wartość domyślna)
    pomijane (False)
    Returns:
    list: lista pików
    Raises:
    ValueError: jeśli podano ujemny promień
    """
    if promien < 0:
        raise ValueError("Promień nie może być ujemny")
    if promien == 0: # ! kurwa jakis debil jebany pisał to zadanie
        promien += 1
    if len(sygnal) == 0:
        return []
    if promien > len(sygnal) - 1:
        if brzegi is True:
            return np.sort(np.concatenate((np.concatenate((np.argwhere(sygnal == np.amax(sygnal)), np.argwhere(sygnal == np.amin(sygnal)))))))
        else:
            ret = np.sort(np.concatenate((np.concatenate((np.argwhere(sygnal == np.amax(sygnal)), np.argwhere(sygnal == np.amin(sygnal)))))))
            mask = ret > 0
            mask &= ret < len(sygnal) - 1
            return ret[mask]
    arr = np.array([], dtype="int")
    for i in range(1, len(sygnal) - 1):
        if i - promien < 0:
            if sygnal[i] == max(sygnal[0:i + promien]) or sygnal[i] == min(sygnal[0:i + promien]):
                arr = np.append(arr, i)
        elif i + promien > len(sygnal) - 1:
            if sygnal[i] == max(sygnal[i - (promien + 1):-1]) or sygnal[i] == min(sygnal[i - (promien + 1):-1]):
                arr = np.append(arr, i)
        else:
            if sygnal[i] == max(sygnal[i - promien:(i + promien + 1)]) or sygnal[i] == min(sygnal[i - promien:(i + promien + 1)]):
                arr = np.append(arr, i)
    if brzegi is True:
        arr = np.concatenate(([0], arr, [len(sygnal) - 1]))
    return arr