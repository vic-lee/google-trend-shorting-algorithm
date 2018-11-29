# This algorithm recreates the algorithm presented in
# "Quantifying Trading Behavior in Financial Markets Using Google Trends"
# Preis, Moat & Stanley (2013), Scientific Reports
# (c) 2013 Thomas Wiecki, Quantopian Inc.

import numpy as np
import datetime
# Average over 5 weeks, free parameter.
delta_t = 5

def initialize(context):
    # This is the search query we are using, this is tied to the csv file.
    context.query = 'debt'
    # User fetcher to get data. I uploaded this csv file manually, feel free to use.
    # Note that this data is already weekly averages.
    fetch_csv('https://gist.github.com/twiecki/5629198/raw/6247da04bacebcd6334a4b91ed21f14483c6d4d0/debt_google_trend',
              date_format='%Y-%m-%d',
              symbol='debt',
    )
    context.sec_id = 8554
    context.security = sid(8554) # S&P5000

def handle_data(context, data):
    c = context
  
    if c.query not in data[c.query]:
        return
   
    # Extract weekly average of search query.
    indicator = data[c.query][c.query]
    
    # Buy and hold strategy that enters on the first day of the week
    # and exits after one week.
    if data[c.security].dt.weekday() == 0: # Monday
        # Compute average over weeks in range [t-delta_t-1, t[
        mean_indicator = mean_past_queries(data, c.query)
        if mean_indicator is None:
            return

        # Exit positions
        amount = c.portfolio['positions'][c.sec_id].amount
        order(c.security, -amount)

        starting_cash = context.portfolio.starting_cash # initial deposit (never changes)
        pnl = context.portfolio.pnl # profit & loss (updated at the start of handle_data)
        market_value = starting_cash + pnl # current market value (cash +/- profit & loss)
        margin_cash = market_value / .5 # available buying power (based on 50% margin)
        bet_size = margin_cash * .75 # risk 75% of available margin

        if market_value > 0:
            # Long or short depending on whether debt search frequency
            # went down or up, respectively.
            if indicator > mean_indicator:
                order(c.security, -bet_size/data[c.sec_id].price)
            else:
                order(c.security, bet_size/data[c.sec_id].price)
        
# If we want the average over 5 weeks, we'll have to use a 6
# week window as the newest element will be the current event.
@batch_transform(window_length=delta_t+1, refresh_period=0)
def mean_past_queries(data, query):
    # Compute mean over all events except most current one.
    return data[query][query][:-1].mean()