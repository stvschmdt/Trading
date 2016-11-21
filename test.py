from logger import Logging
from symbol import Symbol

l = Logging()
l.error("missing symbol")
l.info("missing symbol")
l.refresh("missing symbol")
l.buy("missing symbol")
l.profit("missing symbol")
l.terminate("missing symbol")


s = Symbol('AMD')
s.market_cap()
print s.market_cap
s.earnings_per_share()
print s.eps
