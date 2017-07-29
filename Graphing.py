from bokeh.plotting import figure, output_file, show
import model as md
import numpy as np

sym = md.get_time_open('dis',directory='.//DJIA_2017//')
df = md.trade_algo2_full_iter([ 0.01,  0.002],sym,panic_stop=60,iter = 200)
df2 = md.trade_algo2_full_iter([ 0.01,  0.002],sym,panic_stop=60,iter = 200)

df.to_csv('out.csv')

print(type(df))

plot_title = '---'

output_file(plot_title + '.html')
x = df['day']
y = df['money']
p = figure(title=plot_title, x_axis_label = 'days', y_axis_label = 'USD')
p.line(x, y, line_width=1)
p.circle(x , y, fill_color='blue', size=3)

show(p)

output_file(plot_title + '.html')
x = df['day']
y = df['money']
p2 = figure(title=plot_title, x_axis_label = 'days', y_axis_label = 'USD')
p2.line(x, y, line_width=1)
p2.circle(x , y, fill_color='blue', size=3)


show(p)
show(p2)
print('up high')
print(np.mean(df['profit']))
print(np.std(df['profit']))
print('down high')


# [ 0.00326624,  0.00032132]