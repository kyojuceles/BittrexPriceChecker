import json
from bittrex.bittrex import Bittrex

bittrex = Bittrex(None, None);
result = bittrex.get_marketsummary('BTC-NXT');

print(result);


