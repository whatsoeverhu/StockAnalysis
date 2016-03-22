import matplotlib.pyplot as plt
import numpy as np
import csv
from mpl_toolkits.axes_grid1 import host_subplot  # @UnresolvedImport
import mpl_toolkits.axisartist as AA  # @UnresolvedImport
import matplotlib
from matplotlib.ticker import FuncFormatter

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'
    
    
in_stock = "601766"
year = "2015"
stock_name = ""
x = []
y = []
y2 = []
y3 = []
y4 = []
c = []
d_date = []
count = 0
file_name = "../csv_files/"+in_stock+".csv"
pic_name = "../img_files/"+in_stock+"_d.png"
try:
    with open(file_name,newline='') as csvfile:  # @UndefinedVariable

        reader = csv.reader(csvfile,delimiter=',',quotechar='|')
        data_list = []
        for row in reader:     
            stock_name = row[1].replace(' ','')       
            #data_str = row[0].replace(' ','')+","+row[1].replace(' ','')+","+row[2].replace(' ','')+","+row[3].replace(' ','')+","+row[4].replace(' ','')+","+row[5].replace(' ','')+","+row[6].replace(' ','')     
            #data_list.append(data_str)
            d_date.append(row[2].replace(' ',''))
            y.append(float(row[6].replace(' ','')))
            y2.append(int(row[3].replace(' ','')))
            y3.append(int(row[4].replace(' ','')))
            y4.append(int(row[5].replace(' ','')))
            c.append(count)
            count = count + 1
    csvfile.close()
    
except FileNotFoundError as e:  # @UndefinedVariable
    print (e)
    
host = host_subplot(111, axes_class=AA.Axes)
plt.subplots_adjust(right=0.75)
par1 = host.twinx()
par2 = host.twinx()
par3 = host.twinx()
new_fixed_axis = par2.get_grid_helper().new_fixed_axis
par2.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par2,
                                        offset=(60, 0))
par2.axis["right"].toggle(all=True)

new_fixed_axis2 = par3.get_grid_helper().new_fixed_axis
par3.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par3,
                                        offset=(140, 0))
par3.axis["right"].toggle(all=True)
    
host.set_xlabel("日期")
host.set_ylabel("涨幅")
par1.set_ylabel("发帖量")   
par2.set_ylabel("阅读量")   
par3.set_ylabel("回复量")  

x = np.array(c)
y = np.array(y)
y3 = np.array(y3)
y4 = np.array(y4)

my_xticks = d_date
plt.xticks(x, my_xticks)
#plt.plot(x, y,'r')
plt.title('股票历史涨幅与股吧数据对比_'+in_stock+"_"+stock_name)# give plot a title
plt.xlabel('日期') # make axis labels
plt.ylabel('涨幅')

p1, = host.plot(x, y,'r',label="涨幅")
p2, = par1.plot(x, y2,'b',label="发帖量")
p3, = par2.plot(x, y3,'g',label="阅读量")
p4, = par3.plot(x, y4,'y',label="回复量")

plt.xticks(rotation=70)
plt.ylim(-0.11, 0.11)
host.set_ylim(-0.11, 0.11)
par1.set_ylim(0,max(y2)+max(y2)/10)
par2.set_ylim(0,max(y3)+max(y3)/10)
par3.set_ylim(0,max(y4)+max(y4)/10)
formatter = FuncFormatter(to_percent)
plt.gca().yaxis.set_major_formatter(formatter)
#host.legend()
plt.grid()
host.axis["left"].label.set_color(p1.get_color())
par1.axis["right"].label.set_color(p2.get_color())
par2.axis["right"].label.set_color(p3.get_color())
par3.axis["right"].label.set_color(p4.get_color())
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5)
fig.savefig(pic_name, dpi=100)
print ("Image file saved!")
#plt.draw()
#plt.show()