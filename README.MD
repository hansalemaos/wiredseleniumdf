# captures and processes network requests (selenium-wire and undetected-chromedriver) and converts them to pandas DataFrames

## Tested against Windows 10 / Python 3.10 / Anaconda

## pip install wiredseleniumdf



```python

get_driver(save_folder=None, stop_keys="ctrl+alt+e", scan_time=10, **kwargs):
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
	
```

```python

# Download the root certificate https://github.com/wkeeling/selenium-wire/raw/master/seleniumwire/ca.crt and install it - Trusted Root Certification Authorities  

from wiredseleniumdf import get_driver

import random
import requests
import bs4

driver = get_driver(
    save_folder="c:\\requestsdfs",
    stop_keys="ctrl+alt+e",
    scan_time=10,
)
driver.get("https://testpages.eviltester.com/styled/file-upload-test.html")

# The code prints out driver.requests_dfs, which is using a custom WebDriver functionality (selenium-wire)
# to capture and store network request data during the page load.

print(driver.requests_dfs)

# The script retrieves a specific request data frame (POST request) from the
# driver.requests_dfs dictionary using a timestamp (1693779184.1983006) as the key.

df = driver.requests_dfs[1693779184.1983006]  # timestamps used as keys in dict


print(df.iloc[1].to_string())
r"""
id                                                 3810eb8d-ce30-46f6-8cdd-3890728a66de
method                                                                             POST
url                                   https://testpages.eviltester.com/uploads/filep...
headers                               {'Host': 'testpages.eviltester.com', 'Connecti...
_body                                 b'------WebKitFormBoundaryPmEb1NMyJICQA4B5\r\n...
response                                                                         200 OK
date                                                         2023-09-03 19:12:57.084177
ws_messages                                                                          []
cert                                  {'subject': [(b'CN', b'testpages.eviltester.co...
intern_id                                                                             1
cert__subject                                    [(b'CN', b'testpages.eviltester.com')]
cert__serial                                 325007634443972637219049593487986324830598
cert__key                                                                   (RSA, 2048)
cert__signature_algorithm                                    b'sha256WithRSAEncryption'
cert__expired                                                                     False
cert__issuer                          [(b'C', b'US'), (b'O', b"Let's Encrypt"), (b'C...
cert__notbefore                                                     2023-08-28 09:04:49
cert__notafter                                                      2023-11-26 09:04:48
cert__organization                                                                 None
cert__cn                                                    b'testpages.eviltester.com'
cert__altnames                                            [b'testpages.eviltester.com']
headers__x_goog_api_key                                                             NaN
headers__sec_fetch_site                                                             NaN
headers__sec_fetch_mode                                                             NaN
headers__sec_fetch_dest                                                             NaN
headers__user_agent                                                                 NaN
headers__accept_encoding                                                            NaN
headers__accept_language                                                            NaN
headers__Host                                                  testpages.eviltester.com
headers__Connection                                                          keep-alive
headers__Content_Length                                                             619
headers__Cache_Control                                                        max-age=0
headers__sec_ch_ua                    "Chromium";v="116", "Not)A;Brand";v="24", "Goo...
headers__sec_ch_ua_mobile                                                            ?0
headers__sec_ch_ua_platform                                                   "Windows"
headers__Upgrade_Insecure_Requests                                                    1
headers__Origin                                        https://testpages.eviltester.com
headers__Content_Type                 multipart/form-data; boundary=----WebKitFormBo...
headers__User_Agent                   Mozilla/5.0 (Windows NT 10.0; Win64; x64) Appl...
headers__Accept                       text/html,application/xhtml+xml,application/xm...
headers__Sec_Fetch_Site                                                     same-origin
headers__Sec_Fetch_Mode                                                        navigate
headers__Sec_Fetch_User                                                              ?1
headers__Sec_Fetch_Dest                                                        document
headers__Referer                      https://testpages.eviltester.com/styled/file-u...
headers__Accept_Encoding                                              gzip, deflate, br
headers__Accept_Language                                                 en-US,en;q=0.9
"""

wholebody = df.iloc[1]._body
wholeheader = df.iloc[1].headers.copy()
with open(R"C:\newfile.txt", mode="rb") as f: # uploaded file during capturing
    datauploaded = f.read()

# The code reads the contents of another file (the one we want to upload) located at "C:\testfilex.txt" and
#  stores it in the newdata variable.
with open(r"C:\testfilex.txt", mode="rb") as f:
    newdata = f.read()

# The script replaces the request body content again, this time replacing the
# datauploaded with newdata within wholebody. Additionally, it modifies the
# filename part of the request body to include a random number and the text "newfile.txt."
newdata2upload = wholebody.replace(datauploaded, newdata)
newdata2uploadwithnewfilename = newdata2upload.replace(
    b'filename="newfile.txt"',
    b'filename="' + str(random.randint(1000, 2990)).encode() + b"newfile.txt",
)
# The Content-Length header in the wholeheader dictionary is updated to reflect
# the new length of newdata2uploadwithnewfilename.
wholeheader["Content-Length"] = str(len(newdata2uploadwithnewfilename))

# Finally, a POST request is sent to "https://testpages.eviltester.com/uploads/fileprocessor"
# with the modified headers and request body (newdata2uploadwithnewfilename)
res = requests.post(
    "https://testpages.eviltester.com/uploads/fileprocessor",
    headers=wholeheader,
    data=newdata2uploadwithnewfilename,
)


print(bs4.BeautifulSoup(res.text))

"""
<!DOCTYPE html>
<html>
<head>
<title>Uploaded Results Page</title>
<link href="/css/testpages.css" rel="stylesheet"/>
<script src="js/toc.js"></script>
<!-- HEAD -->
</head>
<body>
<div class="left-col" style="float: left"></div>
<div class="page-body">
<div class="navigation">
<div class="page-navigation">
<a href="/styled/index.html">Index</a>
</div>
<div class="app-navigation">
<!-- APPNAVIGATION CONTENT -->
</div>
</div>
<h1>Uploaded File</h1>
<div class="explanation">
<p>You uploaded a file. This is the result.
        </p>
</div>
<div class="centered">
<h2>You uploaded this file:</h2>
<div>
<p id="uploadedfilename">"1901newfile.txt</p>
</div>
<div class="form-label">
<button class="styled-click-button" id="goback" onclick="window.history.back()">Upload Another</button>
</div>
</div>
<div class="page-footer">
<p><a href="https://eviltester.com" rel="noopener noreferrer" target="_blank">EvilTester.com</a>,
            <a href="https://compendiumdev.co.uk" rel="noopener noreferrer" target="_blank">Compendium Developments</a></p>
</div>
</div>
<!-- BODY END -->
<div class="right-col" style="float: right">
<!-- VERTICALADUNIT -->
</div>
</body>
</html>
"""

```