# erp-price-scraper
A python script to scrape latest ERP prices from MyTransport.sg

[https://www.mytransport.sg/content/mytransport/home/myconcierge/erprates.html](https://www.mytransport.sg/content/mytransport/home/myconcierge/erprates.html)

## Pre-requisites

- Python 2.7

## Getting started

### Step 1: Open the terminal and clone the repo in the folder of your choice.

```
git clone https://github.com/iewil/erp-price-scraper.git
```

### Step 2: Install python libraries

```
pip install -r requirements.txt
```

### Step 3: Run the script

Data will be saved into the 'data' folder in the root directory.
```
python main.py
```

## References

**Vehicle types available**

- 1: Passenger Cars/Light Goods Vehicles/Taxis
- 2: Motorcycles
- 3: Heavy Goods Vehicles/Small Buses
- 4: Very Heavy Goods Vehicles/Big Buses

**Day types available**

- 0: Weekdays
- 1: Saturday

