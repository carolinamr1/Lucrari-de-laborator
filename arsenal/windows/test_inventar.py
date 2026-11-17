"""Teste pentru inventarul Windows."""

from arsenal.windows.inventar import Proces


def test_proces_din_temp_e_suspect():
    proces = Proces(1, "x.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\x.exe")
    assert proces.e_suspect() is True


def test_proces_din_windows_nu_e_suspect():
    proces = Proces(2, "svchost.exe", "SYSTEM", r"C:\Windows\System32\svchost.exe")
    assert proces.e_suspect() is False
