from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO
import datetime as dt

class PhaseScraper:
    def __init__(self):
        self.base_url = 'https://www.timeanddate.com/moon/phases/?year='
        self.years = list(range(2020, 2027))
        self.months = {
            'Jan':1,
            'Feb':2,
            'Mar':3,
            'Apr':4,
            'May':5,
            'Jun':6,
            'Jul':7,
            'Aug':8,
            'Sep':9,
            'Oct':10,
            'Nov':11,
            'Dec':12
        }
        self.dates = []
        self.times = []
        self.lunations = []
        self.phases = []
        self.dts = []


    def get_table(self, year):
        url = f"{self.base_url}{year}"
        response = requests.get(url)
        output = response.text
        soup = BeautifulSoup(output, features="lxml")
        tbl = soup.find_all("table")[1]
        df = pd.read_html(StringIO(str(tbl)))[0]
        self.df = df
        
    def clean_data(self, year):
        self.df = self.df.iloc[:-1]
        for _, row in self.df.iterrows():
            for i in range(1,8,2):
                date = row.iloc[i]
                if type(date) == str:
                    date = date.replace(' ', '/')
                    month_code = date.split('/')[0]
                    date = date.replace(month_code, str(self.months.get(month_code)))
                    date = f"{date}/{year}"
                self.dates.append(date)
            for i in range(2,9,2):
                self.times.append(row.iloc[i])
            self.phases.extend(['New', 'FirstQuarter', 'Full', 'ThirdQuarter'])
            self.lunations.extend([row.iloc[0],row.iloc[0],row.iloc[0],row.iloc[0]])
    
    def create_dts(self, df:pd.DataFrame):
        ## Convert to Datetime
        dates = df['Date']
        times = df['Time']
        both = list(zip(dates, times))
        for i in both:
            date = i[0]
            time = i[1]
            if 'am' in time:
                time = time.split()[0]
                if len(time) <= 4:
                    time = f'0{time}'
            elif 'pm' in time:
                nums = time.split()[0]
                hrs, mins = nums.split(':')
                if int(hrs) > 12:
                    hrs = int(hrs) + 12
                else:
                    hrs = int(hrs)
                time = f'{str(hrs)}:{mins}'
            self.dts.append(f'{date} {str(hrs)}:{mins} UTC-08:00')

    def load_data(self):
        new_dict = {
            "Date": self.dates,
            "Time": self.times,
            "Phase": self.phases,
            "Lunation": self.lunations
        }
        new_df = pd.DataFrame(new_dict)
        new_df.dropna(subset=['Date'], inplace=True)
        self.create_dts(new_df)
        new_df['Datetime'] = self.dts
        new_df['Datetime'] = pd.to_datetime(new_df['Datetime'], utc=True)
        new_df['Date'] = new_df['Datetime'].dt.date
        new_df['Time'] = new_df['Datetime'].dt.time
        new_df.to_csv('data/TestCSVs/MoonPhase.csv')

    def main(self):
        for year in self.years:
            self.get_table(year)
            self.clean_data(year)
        self.load_data()

if __name__ == "__main__":
    scraper = PhaseScraper()
    scraper.main()