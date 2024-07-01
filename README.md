# Software Challenge

> BETA Technologies Software Challenge

## Description

The program `main.py` reads and processes data from a csv file of the following form:
Number - Time (ms) - Bus - Direction - Type - ID (hex) - Reserved - Length - D0 - D1 - D2 - D3 - D4 - D5 - D6 - D7

It plots these signals in a series of aligned subplots as follows:
    - Plot 1 shows pitch input, pitch angle, and pitch rate
    - Plot 2 shows roll input, roll angle, and roll rate
    - Plot 3 shows yaw input, yaw angle, and yaw rate
    - Plot 4 shows hover throttle, pusher throttle, and prop spin

## How to use it

1 - Clone the folder `SoftwareChallengeBETA`

2 - Install dependencies: `pip install -r requirements.txt`

3 - Put your csv file into data folder

4 - Run `main.py`: `python main.py`

5 - Enter following informations:
  - The file path (data/name_of_csv_file.csv)
  - First line you want to process (leave blank to process the entire file)
  - Number of lines you want to process (leave blank to process the entire file)


