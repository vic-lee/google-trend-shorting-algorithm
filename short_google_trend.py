import numpy as np
import datetime
from zipline.api import order, record, symbol

def initialize(context):
	context.AAPL = symbol('AAPL')
	pass

def handle_data(context, data):
	pass
