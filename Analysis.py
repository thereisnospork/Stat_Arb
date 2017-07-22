import model as md

asdf = md.get_time_open('aapl',directory='/DJIA_minute')
print(len(asdf))
print(type(asdf))
