import os
from time import time

import kthread
from kthread_sleep import sleep
from multikeyiterdict import MultiKeyIterDict
import pandas as pd
import seleniumwire.undetected_chromedriver as uc
import keyboard
from a_pandas_ex_dillpickle import pd_add_dillpickle

pd_add_dillpickle()

# trusted root certificate to install
certic = """
-----BEGIN CERTIFICATE-----
MIIFFzCCAv+gAwIBAgIUIUc6dnnqhYX3ZYXQzpZyJ1gtUwcwDQYJKoZIhvcNAQEL
BQAwGzEZMBcGA1UEAwwQU2VsZW5pdW0gV2lyZSBDQTAeFw0xODA3MjAxMDQxMDNa
Fw0yODA3MTcxMDQxMDNaMBsxGTAXBgNVBAMMEFNlbGVuaXVtIFdpcmUgQ0EwggIi
MA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQDKKpm14AHiJb4onGES4Echs2qB
XsfeMAbsA7x4blJkMGyHGx9B8OpXqlRtcNnWD2JGnjc0/k92uuZaV2prDnZwH5Jl
nJSZuGEzUUAnrwhTHTqMhM9pfT8RpltE0lyplQni8rjH5oshBrzzAHILm/iAm1WI
HCFUClQaJ7sVVzAikaPfg4WUXLHP7/AjxIejp/SVI8Ycn1BPIlDwp1pIq4WawJoZ
TZ75GwvsT1ohH4YSRM+BxwBuBUqjusaYJiWwpnR801XV290i3/bBOkS2fEa4+ciS
LEGEi4SaaC6Nhap3sd80npJUQff4ltVGaxX0jCG/zswf2XGEDtsw2FF848KePj4X
Ilgm4xcuhhBvcsgob/bwEvDTrXPk38YQEJEKH8uGf37AOv2TQmqj45WZt7jSZ2YH
ZGn4RunJAO/J7toqJ7upjx66Pq8WkXQ6faSeTNENmXclYPRQFujVbFkECRcOtS6W
fUkHM+tgXHKqSMcfVVp46o/4HfHzoTyvrUDryHJB3h/IrqWK1433rYp3bJzkpjM9
JT71vh6sDo/Ys+4HK5rwrwkeP7b+6dUx1nHOgPX88njVI6cuxnjex6AfSld5d4BH
YZdviXRqCxpiudmnN+cMKAdJgRZFmVNH/djQqtq3y/gmjwKnyW95y3uJu4Xz5+R4
9jhAZGJFiHK/vE+XwwIDAQABo1MwUTAdBgNVHQ4EFgQUPvrTydSlYhMQJy8lvBvh
nLeQsvQwHwYDVR0jBBgwFoAUPvrTydSlYhMQJy8lvBvhnLeQsvQwDwYDVR0TAQH/
BAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAgEAmIvadNtFca9vuMuSewSXHlOd9p7d
9xYkp8Yj5RvFUGL32zYUatH9YsRh5K9Wz5jifjwBLMRDZIm48xhxYjqVvTZoQpL6
Qyzbu2EsRCbmQ+861U4SfcP2uetJuFM6Ug0/CKviyNpUaX/8YWupFXsEiCRJM9pk
sh2b+dqljy9kvrOosfehz8CRbxUfgPsL2IVZa0mHsuOZDa/XHAAW9ns5TdBlFHwo
W/2KDvvPGL/3t7Zah2jwu8D8w397looMXxqyT/DAjH6+bd5Kg/7mELaqbg/pM3EJ
mENd5ButBkhpVbyAKLn7TvpZYSEF/VMNPcZHOKoKrx1utZwLFuVIb07WDMRov0GO
hg/rrIBWvA1ySi/4yrnRDc7GBHSUh0Krx6LLZ/ZtE3j7/4rwj51MwqqNhQrCxGhz
ksqn8V6XY7UUKnlTlAWRyuBLiA+yvf9GdgNJxUblZYMNpPbeLwe2Be/utROuMqwr
G4RA1sfPuEdyfdXB/7c8ViOPxKYFH0POXuwB+Z1JlXDtR8rbjyVPUwqQarAuNIbw
NC8P+GWSzviG544BQyW1xKqLgQcEMSU73icDOOb9COcl1h7URSO9WB6CZXykpQSk
hceDiwojCDsyM84uXyyXKXCRPtseCIRsA1zZwrXU7NDDBXrIC7moVbxkDu2G4V1g
b5JFYe4FNI0yw/o=
-----END CERTIFICATE-----
"""


def get_requests_df(driver, scan_time=10, stop_keys="ctrl+alt+e", save_folder=None):
    """
    Capture and Process Network Requests from a Selenium WebDriver Instance.

    This function monitors and captures network requests (with selenium-wire)  made by a Selenium (with undetected-chromedriver)
    WebDriver instance
    during web interactions. It collects request data and organizes it into DataFrames, which
    can be further analyzed or saved to disk.

    Parameters:
    - driver (Selenium WebDriver): The Selenium WebDriver instance to monitor.
    - scan_time (int, optional): The interval in seconds for scanning and capturing requests.
      Defaults to 10 seconds.
    - stop_keys (str, optional): A key combination to stop the request monitoring process.
      Defaults to "ctrl+alt+e".
    - save_folder (str, optional): The folder path where captured request data should be saved
      as DataFrames in pickle format. If None, no data is saved. Defaults to None.

    Returns:
    - resultsdict (dict): A dictionary containing DataFrames of captured request data, indexed
      by timestamps when the data was collected.


    """

    stop = False
    if save_folder:
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

    def stop_recording():
        nonlocal stop
        stop = True

    if stop_keys in keyboard.__dict__["_hotkeys"]:
        keyboard.remove_hotkey(stop_keys)
    keyboard.add_hotkey(stop_keys, stop_recording)

    def _get_requests_df():
        while not stop:
            try:
                while not driver.requests:
                    if stop:
                        return pd.DataFrame()
                    sleep(0.005)
                driver_requests = []
                cox = 0
                while True:
                    if stop:
                        return pd.DataFrame()
                    driver_requests.append(driver.requests[cox])
                    cox += 1
                    l1 = len(driver_requests)
                    l2 = len(driver.requests)
                    if l1 >= l2:
                        del driver.requests
                        break

                for key, item in (
                    MultiKeyIterDict(
                        {i: q.__dict__ for i, q in enumerate(driver_requests)}
                    )
                ).items():
                    alldfs = []
                    for key2, item2 in item.items():
                        try:
                            df = pd.DataFrame(list(item2.nested_items()))
                            alldfs.append(df)
                        except Exception as fe:
                            continue

                finallist = []

                for key, item in (
                    MultiKeyIterDict(
                        {i: q.__dict__ for i, q in enumerate(driver_requests)}
                    )
                ).items():
                    for key2, item2 in item.items():
                        try:
                            finallist.append(
                                pd.DataFrame(list(item2.__dict__())).assign(
                                    **{2: key2, 3: key}
                                )
                            )
                        except Exception as fe:
                            finallist.append(
                                pd.DataFrame([[item2, key2, key]], dtype="object")
                            )
                final2 = []
                co = 0
                for name, group in (pd.concat(finallist, ignore_index=True)).groupby(
                    [2]
                ):
                    final2.append(
                        group.set_index(1)
                        .drop(columns=2)
                        .T.reset_index(drop=True)
                        .assign(intern_id=co)
                    )
                    co = co + 1
                df = pd.concat(final2, ignore_index=True)
                dfheaders = pd.DataFrame()
                try:
                    dfheaders = pd.concat(
                        [
                            pd.DataFrame(df.headers.iloc[h].items())
                            .assign(
                                **{
                                    "newind": lambda x: x.apply(
                                        lambda q: f"headers__{q[0]}", axis=1
                                    ).str.replace("-", "_")
                                }
                            )
                            .set_index("newind")
                            .drop(columns=0)
                            .T
                            for h in range(len(df))
                        ],
                        ignore_index=True,
                    )
                except Exception:
                    pass
                dfa = pd.DataFrame()
                try:
                    dfa = pd.concat(
                        [
                            pd.DataFrame(kj)
                            .assign(
                                newind=lambda x: "cert__"
                                + x[0].apply(str).str.replace("-", "_", regex=False)
                            )
                            .set_index("newind")
                            .drop(columns=0)
                            .T
                            if (kj := df.cert.iloc[fx].items())
                            else (
                                pd.DataFrame(
                                    [[None] * 11],
                                    columns=[
                                        "cert__subject",
                                        "cert__serial",
                                        "cert__key",
                                        "cert__signature_algorithm",
                                        "cert__expired",
                                        "cert__issuer",
                                        "cert__notbefore",
                                        "cert__notafter",
                                        "cert__organization",
                                        "cert__cn",
                                        "cert__altnames",
                                    ],
                                    dtype="object",
                                )
                            )
                            for fx in range(len(df))
                        ],
                        ignore_index=True,
                    )
                except Exception:
                    pass
            except Exception:
                pass
            tsta = time()

            resultsdict[tsta] = pd.concat([df, dfa, dfheaders], axis=1)
            if save_folder:
                fina = (str(tsta) + (18 * "0"))[:18] + ".pkl"
                resultsdict[tsta].to_dillpickle(os.path.join(save_folder, fina))

            sleep(scan_time)

    resultsdict = {}
    t = kthread.KThread(target=_get_requests_df)
    t.daemon = True
    t.start()
    return resultsdict


def get_driver(save_folder=None, stop_keys="ctrl+alt+e", scan_time=10, **kwargs):
    """
    Initialize a Selenium WebDriver Instance (undetected-chromedriver) with Request Monitoring (selenium-wire).

    This function initializes a Selenium WebDriver instance with request monitoring capabilities.
    It allows you to interact with web pages while capturing and processing network requests
    made during the interactions.

    Parameters:
    - save_folder (str, optional): The folder path where captured request data should be saved
      as DataFrames in pickle format. If None, no data is saved. Defaults to None.
    - stop_keys (str, optional): A key combination to stop the request monitoring process.
      Defaults to "ctrl+alt+e".
    - scan_time (int, optional): The interval in seconds for scanning and capturing requests.
      Defaults to 10 seconds.
    - **kwargs: Additional keyword arguments to configure the Selenium WebDriver instance.

    Returns:
    - driver (Selenium WebDriver): An initialized Selenium WebDriver instance with request
      monitoring capabilities.

    Usage:
    1. Call this function to create a WebDriver instance.
    2. The WebDriver instance can be used for web interactions and will automatically
       capture network requests.
    3. Optionally, provide a save folder to save captured data as pickle files.

    Example:
    >>> driver = get_driver(save_folder="request_data", stop_keys="ctrl+alt+e")

    Note:
    - This function combines Selenium WebDriver functionality with request monitoring
      capabilities for advanced web testing and analysis.
    - The request monitoring continues until the specified stop_keys combination is pressed
      or the WebDriver session is closed.
    - Use keyboard shortcuts (stop_keys) to control when to stop request monitoring.


    """
    # Function implementation goes here

    driver = uc.Chrome(**kwargs)
    driver.__dict__["requests_dfs"] = get_requests_df(
        driver, scan_time=scan_time, stop_keys=stop_keys, save_folder=save_folder
    )
    setattr(driver, "requests_dfs", driver.__dict__["requests_dfs"])
    return driver
