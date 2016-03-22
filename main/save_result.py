'''
这里用到好多包，具体是什么并不是很清楚，但是需要用到的时候加入 进来就可以了
'''
import matplotlib.pyplot as plt
import numpy as np
import csv
from mpl_toolkits.axes_grid1 import host_subplot  # @UnresolvedImport
import mpl_toolkits.axisartist as AA  # @UnresolvedImport
import matplotlib
from matplotlib.ticker import FuncFormatter

'''
内置一个将涨幅数据显示为百分比的函数
'''
def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'
    
'''
定义一些初始参数
'''    
in_stock = "000626"
year = "2015"
stock_name = ""
x = []
y = []
y2 = []
y3 = []
y4 = []
r = []
c = []
d_date = []
count = 0
file_name = "../csv_files/"+in_stock+".csv"
pic_name = "../img_files/"+in_stock+".png"
try:
    with open(file_name,newline='') as csvfile:  # @UndefinedVariable
        reader = csv.reader(csvfile,delimiter=',',quotechar='|')
        data_list = []
        for row in reader:     
            stock_name = row[1].replace(' ','')       
            read = int(row[4].replace(' ',''))
            tips = int(row[3].replace(' ',''))
            replies = int(row[5].replace(' ',''))
            d_date.append(row[2].replace(' ',''))
            y.append(float(row[6].replace(' ','')))
            y2.append(tips)
            y3.append(read)
            y4.append(replies)
            #先采用一个比较简单的热度衡量方式，平均每帖的阅读数
            hot = read/tips
            r.append(hot)
            c.append(count)
            count = count + 1
    csvfile.close()
    
except FileNotFoundError as e:  # @UndefinedVariable
    print (e)

'''
开始绘制图表
'''    
host = host_subplot(111, axes_class=AA.Axes)
plt.subplots_adjust(right=0.75)
#twinx 方法可以绘制多个Y轴
par1 = host.twinx()
    
host.set_xlabel("日期")
host.set_ylabel("涨幅")
par1.set_ylabel("股吧热度") 

x = np.array(c)
y = np.array(y)

my_xticks = d_date
plt.xticks(x, my_xticks)
#plt.plot(x, y,'r')
plt.title('股票历史涨幅与帖吧热度对比_'+in_stock+"_"+stock_name)# give plot a title
plt.xlabel('日期') # make axis labels
plt.ylabel('涨幅')

p1, = host.plot(x, y,'r',label="涨幅")
p2, = par1.plot(x, r,'b',label="热度")

plt.xticks(rotation=70)
plt.ylim(-0.11, 0.11)
host.set_ylim(-0.11, 0.11)
par1.set_ylim(0,max(r)+max(r)/10)
formatter = FuncFormatter(to_percent)
plt.gca().yaxis.set_major_formatter(formatter)
host.legend()
plt.grid()
host.axis["left"].label.set_color(p1.get_color())
par1.axis["right"].label.set_color(p2.get_color())
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5)
fig.savefig(pic_name, dpi=100)
print ("Image file saved!")
#plt.draw()
#plt.show()