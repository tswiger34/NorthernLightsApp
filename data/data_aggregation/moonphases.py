from bs4 import BeautifulSoup
import requests
import pandas as pd

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

    def get_table(self, year):
        url = f"{self.base_url}{year}"
        response = requests.get(url)
        output = response.text
        soup = BeautifulSoup(output, features="lxml")
        tbl = soup.find_all("table")[1]
        df = pd.read_html(str(tbl))[0]
        self.df = df
        
    def clean_data(self, year):
        self.df = self.df.iloc[:-1]
        print(self.df.shape)
        x = 1
        for _, row in self.df.iterrows():
            print("Iterating through row ", x)
            x+=1
            for i in range(1,8,2):
                date = row[i]
                if type(date) == str:
                    date = date.replace(' ', '/')
                    month_code = date.split('/')[0]
                    date = date.replace(month_code, str(self.months.get(month_code)))
                    date = f"{date}/{year}"
                self.dates.append(date)
                print(len((self.dates)))
            for i in range(2,9,2):
                self.times.append(row[i])
            self.phases.extend(['New', 'FirstQuarter', 'Full', 'ThirdQuarter'])
            self.lunations.extend([row[0],row[0],row[0],row[0]])

    def load_data(self):
        new_dict = {
            "Date": self.dates,
            "Time": self.times,
            "Phase": self.phases,
            "Lunation": self.lunations
        }
        new_df = pd.DataFrame(new_dict)
        new_df.dropna(subset=['Date'], inplace=True)
        new_df.to_csv('data/TestCSVs/MoonPhase.csv')

    def main(self):
        for year in self.years:
            self.get_table(year)
            self.clean_data(year)
        self.load_data()
    
if __name__ == "__main__":
    scraper = PhaseScraper()
    scraper.main()
