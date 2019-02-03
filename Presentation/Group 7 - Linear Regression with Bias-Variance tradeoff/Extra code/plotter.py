######################################### Deal with Ipython ###############################################
import sys
from io import StringIO

def ipython_info():
    isIPy = False
    if 'ipykernel' in sys.modules:
        isIPy = True
    return isIPy
class IpyExit(SystemExit):
    """Exit Exception for IPython.

    Exception temporarily redirects stderr to buffer.
    """
    def __init__(self):
        # print("exiting")  # optionally print some message to stdout, too
        # ... or do other stuff before exit
        sys.stderr = StringIO()

    def __del__(self):
        sys.stderr.close()
        sys.stderr = sys.__stderr__  # restore from backup
###########################################################################################################

#TODO COMMENT IN DETAILS

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation as animation
import numpy as np

class Plotter(object):

    #TODO redesign the structure, some static param may be transferred to exact-instance-determined
    isIPy = ipython_info()

    escapeTime = 3000

    colBenchMark = 3

    #TODO del this
    tempTrigger = True

    #TODO implement a save feature
    saveTrigger = False

    def __init__(self,*funcDataTargetParam,**funcsParams):
        #TODO redesign to all dict format and extend it for multi funcs and data in single subplot
        '''
        :param BRACKETfuncBRACKETDataTarget: [[func1,data1,target1],[func2,data2,target2],...] for static plot;
                                              [[data1,target1],[data2,target2]...] for animation plot
                                              you may use *[list]*n for repeated list

        :param funcParams: {plot1:{'func':[step1,step2,...],'param1':[step1,step2,...],...,'paramN':[step1,step2,...]},
                        'plot2':{},...,'plotN':{}}
        '''

        #TODO
        '''
        all the funcs could be a sklearn classifier about x
        step could be different length but should be aligned at 1 step and synchronized
        '''

        plt.close()
        self.funcOrJustDataTargetorAddParam = funcDataTargetParam
        self.funcParams = funcsParams
        self.anim = None
        self.fig = None
        if not funcsParams:
            self.multi_plotter()
        else:
            #TODO enable it
            #self.control()
            self.frameInterval = Plotter.escapeTime // len(self.funcParams['plot1']['func'])#TODO a better speed benchmark
            self.multi_animator()

    def _convert_to_func(self):
        #TODO
        pass

    def _step_align(self):
        #TODO
        pass

    def dynamicCanvas(self):
        #TODO general title
        row = len(self.funcOrJustDataTargetorAddParam) // Plotter.colBenchMark + 1
        col = min(len(self.funcOrJustDataTargetorAddParam), Plotter.colBenchMark)
        return row, col, plt.figure(figsize=(col * 5, row * 5))

    def multi_plotter(self):
        row,col,self.fig = self.dynamicCanvas()
        for i,[func,x,y] in enumerate(self.funcOrJustDataTargetorAddParam):
            x_temp = np.arange(min(x),max(x),0.05).reshape(-1,1)
            #TODO subtitle, label names, range limits, legends
            ax = plt.subplot(row, col, i + 1)
            plt.plot(x,y,'bo',markersize=3)
            plt.plot(x_temp,func(x_temp),'r',linewidth=2)
            #TODO del this
            if Plotter.tempTrigger:
                ax.annotate('train error:{}\ntest error:{}'.format(Plotter.train_error[i],Plotter.test_error[i]),\
                                xy=(0.75, 0.9), xycoords='axes fraction', fontsize=10,\
                                        bbox=dict(facecolor='white', alpha=0.8),\
                                            horizontalalignment='left', verticalalignment='bottom')
        plt.show()

    def multi_animator(self):
        curves=list()
        x_temp=list()
        ax=list()
        an=list()
        row,col,fig = self.dynamicCanvas()
        for n,[x,y] in enumerate(self.funcOrJustDataTargetorAddParam):
            x_temp.append(np.arange(min(x), max(x), 0.05).reshape(-1, 1))
            # TODO subtitle, label names, range limits, legends
            ax.append(plt.subplot(row, col, n + 1))
            if self.funcParams['plot' + str(n + 1)].get('name',None):
                ax[n].set_xlabel(self.funcParams['plot' + str(n + 1)].get('name',None))
            plt.plot(x, y, 'bo', markersize=3)
            curves.append(plt.plot(x_temp[n],self.funcParams['plot'+str(n+1)]['func'][0](x_temp[n]),'r',linewidth=2))
            if len(self.funcParams['plot' + str(n + 1)]) > 1:
                paramStr = ''
                for key in self.funcParams['plot' + str(n + 1)]:
                    if key != 'func':
                        paramStr += '{}:{}\n'.format(key, self.funcParams['plot' + str(n + 1)][key][0])
                an.append(ax[n].annotate(paramStr, xy=(0.75, 0.9), xycoords='axes fraction', fontsize=10,
                                       bbox=dict(facecolor='white', alpha=0.8),
                                       horizontalalignment='left', verticalalignment='bottom'))
            else:
                an.append(None)

        def update(i):
            label = 'Time Step {0}'.format(i)
            plt.suptitle(label)
            for n,curve in enumerate(curves):
                curve[0].set_ydata(self.funcParams['plot'+str(n+1)]['func'][i](x_temp[n]))
                if len(self.funcParams['plot'+str(n+1)])>1:
                    an[n].remove()
                    paramStr = ''
                    for key in self.funcParams['plot'+str(n+1)]:
                        if key != 'func' and key != 'name':
                            paramStr+='{}:{}\n'.format(key,self.funcParams['plot'+str(n+1)][key][i])
                    #TODO shorten to 5 or 6 digits long
                    an[n]=ax[n].annotate(paramStr, xy=(0.75, 0.9), xycoords='axes fraction', fontsize=10,
                                bbox=dict(facecolor='white', alpha=0.8),
                                horizontalalignment='left', verticalalignment='bottom')

        if Plotter.isIPy:
            plt.rcParams["animation.html"] = "jshtml"

        anim = animation(fig, update, frames = range(len(self.funcParams['plot1']['func'])), interval=self.frameInterval)

        if Plotter.isIPy:
            self.anim = anim
        else:
            self.anim = anim
            plt.show()

    #TODO multi-threading
    def control(self):
        while 1:
            if input('Please input q for exit: ') == 'q':
                if not Plotter.isIPy:
                    raise SystemExit
                else:
                    #TODO IpyExit shut whole kernel
                    raise IpyExit
            else:
                print('Input unrecognized, please redo it')