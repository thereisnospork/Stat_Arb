from bokeh.plotting import figure, output_file, show
import model as md

sym = md.get_time_open('gt',directory='.//DJIA_2016//')
df = md.trade_algo2((.007,.01),sym)

df.to_csv('out.csv')

print(type(df))

plot_title = 'gt_2016'

output_file(plot_title + '.html')
x = df['day']
y = df['money']
p = figure(title=plot_title, x_axis_label = 'days', y_axis_label = 'USD')
p.line(x, y, line_width=1)
p.circle(x , y, fill_color='blue', size=3)

show(p)

