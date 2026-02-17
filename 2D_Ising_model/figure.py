import matplotlib.pyplot as plt
def figure_adjust(x):
  for ax in plt.gcf().get_axes():
    ax.tick_params(labelsize=x,direction='out',length=8,width=1.5,pad=8)
    ax.spines["top"].set_linewidth(standard)
    ax.spines["bottom"].set_linewidth(standard)
    ax.spines["right"].set_linewidth(standard)
    
    ax.spines["left"].set_linewidth(standard)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times new roman') for label in labels]
    [label.set_weight('normal') for label in labels]
standard = 1

font1 = {'family': 'Times new roman','weight': 'normal','size': 24}
font2 = {'family': 'Times new roman','weight': 'normal','size': 20}
font3 = {'family': 'Times new roman','weight': 'normal','size': 16}
font4 = {'family': 'Times new roman','weight': 'normal','size': 14}