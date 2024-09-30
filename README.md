# Car Website Scraper

A Python-based web scraper that extracts car details from [Cars.com](https://www.cars.com/) using Selenium. The scraper collects information such as car make, model, year, price, and dealer phone number, and saves the data to an Excel file.

## Features

- Automates the browsing of car listings on Cars.com.
- Extracts essential car details including:
  - Car make
  - Car model
  - Year of manufacture
  - Price
  - Dealer phone number
- Saves the extracted data to an Excel file (`cars_data.xlsx`).
- Supports pagination to collect data from multiple pages.

## Requirements

- Python 3.x
- Selenium
- Pandas
- WebDriver Manager
- OpenPyXL

## Installation

1. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```
   
1. Run the scraper:

   ```bash
   python car_scraper.py
   ```
- The scraper will start and navigate to Cars.com, accepting cookies and scraping car details from the listings.
- The extracted data will be saved to an Excel file named cars_data.xlsx in the same directory.