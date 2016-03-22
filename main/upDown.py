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
from matplotlib.lines import Line2D
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
in_stock = "603010"
year = "2015"
stock_name = ""
x = []
y = []
y2 = []
y3 = []
y4 = []
r = []
c = []
colors = []
d_date = []
count = 0
p_read = 0
d_read = 0
p_hot = 0
d_hot = 0
c1 = 0
c2 = 0
p_acc = 0
file_name = "../csv_files/"+in_stock+".csv"
pic_name = "../img_files/"+in_stock+"_c.png"
try:
    with open(file_name,newline='') as csvfile:  # @UndefinedVariable
        reader = csv.reader(csvfile,delimiter=',',quotechar='|')
        data_list = []
        for row in reader:     
            stock_name = row[1].replace(' ','')       
            read = int(row[4].replace(' ',''))
            tips = int(row[3].replace(' ',''))
            replies = int(row[5].replace(' ',''))
            increase = float(row[6].replace(' ',''))
            if p_read != 0 : d_read = float(read - p_read)/float(p_read)
            p_read = read            
            d_date.append(row[2].replace(' ',''))
            y.append(increase)  
            hot = read/tips
            d_hot = hot - p_hot      
            y3.append(d_read)
            p_hot = hot
            c.append(count)
            count = count + 1
            if d_read * increase <= 0:
                acc_value = 1
                c1 = c1 + 1
            else:
                acc_value = 0
                c2 = c2 + 1            
            if increase > 0:
                color = "#dd6666"
            else:
                color = "#66dd66"
            colors.append(color)        
    csvfile.close()
    
except FileNotFoundError as e:  # @UndefinedVariable
    print (e)
del y[0]
del y3[0]
del d_date[0]
del c[0]
del colors[0]
p_acc = float(c1)/float(c1+c2)
print (p_acc)
    
x = np.array(c)
ind = np.arange(len(c))
width = 0.45  

fig = plt.figure()
ax = fig.add_subplot(111)
par1 = ax.bar(ind+width+0.2, y, 0.2, color=colors)
my_xticks = d_date
plt.xticks(x, my_xticks)
plt.title('股票日涨幅与股吧热度每日变化对比_'+in_stock+"_"+stock_name)# give plot a title
plt.xlabel('日期') # make axis labels
plt.ylabel('涨幅')
plt.grid()
plt.xticks(rotation=70)
plt.ylim(-0.11, 0.11)
formatter = FuncFormatter(to_percent)
plt.gca().yaxis.set_major_formatter(formatter)
ax.add_line(Line2D([0, 1], [0.5, 0.5], transform=ax.transAxes,
                  linewidth=2, color='k'))
ax2 = ax.twinx()
if max(y3) > abs(min(y3)):
    ax2.set_ylim((max(y3)+max(y3)/10)*-1,max(y3)+max(y3)/10)
else:
    ax2.set_ylim((min(y3)+min(y3)/10),(min(y3)+min(y3)/10)*-1) 
par2 = ax2.bar(ind+width, y3, 0.2, color='#b0c4de')
ax2.set_ylabel("股吧热度变化") 
ax2.yaxis.set_major_formatter(formatter)
ax.yaxis.label.set_color('r')
ax2.yaxis.label.set_color('b')
ax.set_xticks(ind+width+(width/2))

fig.set_size_inches(18.5, 10.5)
fig.savefig(pic_name, dpi=100)
print ("Image file saved!")

#plt.tight_layout()
#plt.show()