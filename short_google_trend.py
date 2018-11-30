import numpy as np
import datetime
from zipline.api import order, record, symbol

'''
Algorithm description: 

This algorithm shorts the stock market based on how frequent negative keywords 
are searched on Google.

Detailed Algorithm:

Prior-week search frequency
Avg search frequency (look-back window or full history)

- every Monday
  - if prior-week search frequency > avg search frequency
    - short asset
  - if prior-week search frequency < avg search frequency
    - long asset
- every Friday
  - close all positions

Variations on algorithm:
1. look back window for avg search frequency
2. starting capital
3. general index / industry-specific indices paired 
    with industry-specific search terms

Note: 
Only use search query data at (t - 1) to avoid look-ahead bias.

'''

def initialize(context):
	context.AAPL = symbol('AAPL')
	pass

def handle_data(context, data):
	pass
