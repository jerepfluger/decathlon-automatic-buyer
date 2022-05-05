# Decathlon Automatic Buyer

A simple Python program that allows you to buy a Decathlon item automatically in case you're waiting for it to have availability.
<br> It's mainly intended for buying a bike with N26 virtual card, but you can modify it as needed.
<br> You'll only need to accept the push notification you'll get once there's availability for your product. So you'll be able to leave the program running, do your stuff and just await for a push notification. The program will do the rest.

## Requirements
* Python3
* Pip3
* Selenium
* Geckdriver
* Firefox

### Installing in Windows OS
#### Let's check if Python3 is already installed
Open a command prompt with Administrator privileges
<br> In order to do this just press `Windows+R`. This'll open a "Run" box. Type "cmd" and press `Ctrl+Shift+Enter`.
<br> You'll notice that a windows gets opened. Check if on top of it you are able to read "<b>Administrator: Command Prompt</b>".
<br> Inside the command prompt type
```
python3
```
If you see and output like this, it means it's already installed (you can type `quit()` to exit python3)
```
Python 3.9.10 (main, Jan 15 2022, 11:48:00)
[Clang 13.0.0 (clang-1300.0.29.3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

<br>

#### In case Python3 is NOT installed
Go to https://www.python.org/downloads/windows/ and look for `Latest Python 3 Release - Python 3.xx.x` link (you'll see numbers istead of xx.x, go ahead, click it).
<br> Now, at the end of this page find `Windows installer (64-bit)` (or 32-bit, depending on your operating system).
<br> This'll download a .exe file. Go to your downloads folder and execute it. 
<br>Follow the installation steps (mainly you just need to press 'Next' and that's it). Only thing you need to be aware of is to be sure that 'Add Python 3.xx.x to path' box is checked!
<br> That's it :)

<br>

#### Let's check if pip3 is already installed
Open a command prompt with Administrator privileges
<br> In order to do this just press `Windows+R`. This'll open a "Run" box. Type inn "cmd" and press `Ctrl+Shift+Enter`.
<br> You'll notice that a windows gets opened. Check if on top of it you are able to read "<b>Administrator: Command Prompt</b>".
<br> Inside the command prompt type
```
pip3 -v
```
You should see and output like this
```
Usage:
C:\Python38\python.exe -m pip <command> [options]
Commands:
  install      Install packages.
  download                    Download packages.
  ...
  ...
```
That means pip3 is already installed.

<br>

#### Installing pip3
In the command prompt type `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py` and press Enter
<br> After this type `python3 get-pip.py` and Enter

<br>

#### Installing geckodriver
Go to https://github.com/mozilla/geckodriver/releases and at the end look for `geckodriver-v0.30.0-win64.zip`. Click on it and unzip it.
<br> Execute the file `geckodriver.exe`
<br> After this on the command prompt execute `where python3`. You'll see and output like `C:\Users\SomeName\AppData\Local\Programs\Python\Python310-32\python.exe`
<br> You'll need to copy the file `geckodriver.exe` right next to the `python.exe` of the previous line.

<br>

#### Installing selenium
In the command prompt type `pip3 install selenium`

<br>

#### Install Firefox
https://www.mozilla.org/es-ES/firefox/windows/

## Running the program
In order to run the program, in the command prompt type
```
--link <url> --size <desired_size> --email <decathlon_email_account>  --password <decathlon_password> --region <region> --city <city> --card_number <credit_or_debit_card_number>  --card_expiration_month <expiry_month> --card_expiration_year <expiry_year> --card_secure_code <cvv>
```
For example
```
--link "https://www.decathlon.es/es/p/bicicleta-montana-allmountain-am-100-hardtail/_/R-p-331946" --size "S - 150-164CM" --email "some_email@gmail.com"  --password "StrongPa$$word" --region "Euskadi" --city "City Vitoria (centro ciudad)" --card_number "3435745568760620"  --card_expiration_month "07" --card_expiration_year "2026" --card_secure_code "247"
```

### General Information
You'll need to access manually to Decathlon website and check for data to be correct.
<br> For example, copy the url of the bike you want to buy, be sure what bike size you want and complete with exact information (including whitespaces, dashes, etc). In 'Store pickup' look that the region you want to receive in the product is available. You'll also need to look for the store where you want to pick up the product.
<br> Be sure your billing address is present in your account Profile Setting.
