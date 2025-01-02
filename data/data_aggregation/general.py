import pandas as pd
import numpy as np
from datetime import datetime, timedelta

## Create date range
class GeneralData:
    def __init__(self):
        pass
    def gen_lunar_luminosity(self):
        """
        Calculate the Moon's luminosity for every day based on phase dates.
        
        Parameters:
        dates_phases: DataFrame with columns ['Date', 'Phase']
                    - 'Date': Date of the Moon phase
                    - 'Phase': Type of phase ('New', 'FirstQuarter', 'Full', 'ThirdQuarter')
        
        Returns:
        DataFrame with columns ['Date', 'Luminosity']
        """
         # Average length of a lunar month in days
        synodic_period = 29.53
        
        # Sort phases and create a complete date range
        dates_phases['Date'] = pd.to_datetime(dates_phases['Date'])
        dates_phases = dates_phases.sort_values('Date').reset_index(drop=True)
        start_date = dates_phases['Date'].min()
        end_date = dates_phases['Date'].max()
        all_dates = pd.date_range(start_date, end_date)
        
        # Initialize luminosity DataFrame
        luminosity_df = pd.DataFrame({'Date': all_dates})
        
        # Calculate luminosity for each day
        def compute_luminosity(day):
            # Find the closest New Moon
            new_moons = dates_phases[dates_phases['Phase'] == 'New']['Date']
            last_new_moon = new_moons[new_moons <= day].max()
            days_since_new = (day - last_new_moon).days
            
            # Sine wave model for luminosity
            return 0.5 * (1 + np.sin(2 * np.pi * days_since_new / synodic_period))
        
        luminosity_df['Luminosity'] = luminosity_df['Date'].apply(compute_luminosity)
        return luminosity_df
    
    def gen_dates(self):
        date_range = pd.date_range(start='2020-01-01', end='2026-12-31')
        dates_df = pd.DataFrame({
            'DateID':range(len(date_range)),
            'USDate':date_range,
            'LunarLuminosity': [None] * len(date_range)
        })
        
if __name__ == '__main__':
    dat = GeneralData()
    dat.gen_dates()