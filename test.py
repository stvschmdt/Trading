from logger import Logging
from symbol import Symbol
from loader import Loader


print "***** logging test *****"
l = Logging()
l.error("missing symbol")
l.info("missing symbol")
l.refresh("missing symbol")
l.buy("missing symbol")
l.profit("missing symbol")
l.terminate("missing symbol")


print "***** symbol test *****"
s = Symbol('AMD')
s.market_cap()
print s.market_cap
s.earnings_per_share()
print s.eps

print "***** loader test *****"
load = Loader('AMD', '2016-11-01', '2016-11-21')
amd = load.get_data('AMD')
amd.book_value()
print amd.book
print load.data_to_csv('AMD')
