import zad1
import pytest
import csv
import numpy as np


def test_normalize_simple():
    """ Test funkcji normalize dla przykładowej listy wartości"""
    x = zad1.normalize([-7, 0, 9, 65, -7, -1, 2.3, 8])
    assert all(x <= 1) and all(x >= 0)


def test_normalize_inputs():
    """ Test funkcji normalize - sprawdzenie złego
    typu argumentu wejściowego"""
    with pytest.raises(TypeError):
        zad1.normalize("test")


def test_normalize_empty_list():
    """ Test funkcji normalize - sprawdzenie złego argumentu - pusta lista"""
    with pytest.raises(ValueError):
        zad1.normalize([])


def test_read_ecg_signal_not_found():
    """ Test funkcji read_ecg_signal - nie znaleziono pliku"""
    with pytest.raises(FileNotFoundError):
        zad1.read_ecg_signal("nieistniejący_plik.csv")


def test_read_ecg_signal_wrong_extension():
    """ Test funkcji read_ecg_signal - złe rozszerzenie pliku"""
    with pytest.raises(TypeError):
        zad1.read_ecg_signal("nieistniejący_plik.dat")


def test_read_ecg_signal_simple():
    """ Test funkcji read_ecg_signal - sprawdzenie czy wczytywane
    wartości w środku listy mają typ float"""
    x = zad1.read_ecg_signal("signal.csv")
    assert all([isinstance(i, float) for i in x])


@pytest.fixture
def sample_ecg_signal():
    with open('sample_ecg.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            sample_ecg = line
        sample_ecg = [float(k) for k in sample_ecg]
    return sample_ecg


def test_find_r_waves_simple(sample_ecg_signal):
    """ Test funkcji test_find_r_waves_simple - sprawdzenie czy wartości
    wykrytych załamków R są w dobrym miejscu"""
    signal, peaks = zad1.find_r_waves(sample_ecg_signal)
    dist = [peaks[i] - peaks[i - 1] for i in range(1, len(peaks) - 1)]
    assert all(np.array(dist) >= 200)


def test_moving_average_typical():
    x = zad1.moving_average([1, 2, 3, 4, 5], 3)
    assert all(x == [2, 3, 4])


def test_moving_average_window():
    x = zad1.moving_average([2, 7], 5)
    assert all(x == [1.8, 1.8, 1.8, 1.8])


def test_moving_average_wrong_type():
    """ Test funkcji moving_average - sprawdzenie złego typu
    argumentu wejściowego"""
    with pytest.raises(TypeError):
        zad1.moving_average("kot", 5)

def test_moving_average_wrong_type2():
    """ Test funkcji moving_average - sprawdzenie złego typu
    argumentu wejściowego 2"""
    with pytest.raises(TypeError):
        zad1.moving_average([1, 2, 3], 1.5)

def test_moving_average_empty_list():
    """ Test funkcji moving_average - sprawdzenie argumentu
    wejściowego - pusta lista"""
    with pytest.raises(ValueError):
        zad1.moving_average([], 4)
