print("Hello, fellow Arber")
a = input("cote Home: ")
b = input("cote Draw: ")
c = input("cote Away: ")

a_arb_percent = 1/float(a)
b_arb_percent = 1/float(b)
c_arb_percent = 1/float(c)
ip = a_arb_percent + b_arb_percent + c_arb_percent


if ip > 1:
    print('no arbitrage possible')
    print(ip)
else:
    print('possible arbitrage \n')
    print(ip)
    bet = input('your bet: ')
    bet = float(bet)
    arb_profit = (bet/float(ip)) - bet
    print(arb_profit)
    profit_percent = (((bet + arb_profit) - bet)/bet) * 100
    print(f'profit in % : ', profit_percent)
    
    a_individual_bet = (bet*a_arb_percent)/ip
    b_individual_bet = (bet*b_arb_percent)/ip
    c_individual_bet = (bet*c_arb_percent)/ip
    
    print(a_individual_bet)
    print(b_individual_bet)
    print(c_individual_bet)
    print(a_individual_bet+b_individual_bet+c_individual_bet)
