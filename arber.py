class Arbitrage:
    def __init__(self, bookie, home, draw, away) -> float:
        self.bookie = bookie
        self.home = home
        self.draw = draw
        self.away = away
    def is_possible(home, draw, away):
 
        a_arb_percent = 1/float(home)
        b_arb_percent = 1/float(draw)
        c_arb_percent = 1/float(away)
        ip = a_arb_percent + b_arb_percent + c_arb_percent
        
        if ip > 1:
            pass
            # print(ip)
        else:
            print(f'arbitrage possible: ', ip)
            return ip

