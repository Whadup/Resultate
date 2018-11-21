
"""
Computes a histrogram for the 9th layer of pretrained AlexNet, that computes 256 convolutions resulting 
in a layer of size 256x13x13.
We have computed the first 12k eigenvalues "exactly" using ARPACK

Small spikes have been amplified in amplitude for visual clarity
"""
import numpy as np
import sys

data = np.genfromtxt(sys.argv[1],delimiter=",")
specialFirstBar = False
if "-f-" in sys.argv[1]:
	specialFirstBar = True
bins=data[:,0].flatten()
weights=data[:,1].flatten()
numBins = data.shape[0]
step = bins[1]
if specialFirstBar:
	step = bins[6]-bins[5]
weightsA = numBins * [0]
weightsB = numBins * [0]
x=0
for i in range(numBins-1,-1,-1):
	# print(i)
	if x+weights[i]<=1000:
		x+=weights[i]
		weightsB[i] = weights[i]
		weightsA[i] = 0
	elif x>=1000:
		weightsA[i] = weights[i]
	elif x+weights[i]>1000:
		weightsA[i] = weights[i]
		#weightsB[i] = 1000-x
		#weightsA[i] = weights[i]-weightsB[i]
		x=1000
# for i in range(numBins):
# 	if weightsB[i]>0:
# 		print(100/(weightsB[i]**0.8))
# 		weightsB[i]*=100/(weightsB[i]**0.8)

pattern = """
\\documentclass[border=10pt]{{standalone}}
\\usepackage{{pgfplots}}
\\pgfplotsset{{compat=1.14}}
\\pgfplotsset{{width=14cm,height=7cm}}
\\begin{{document}}
\\begin{{tikzpicture}}
\\begin{{axis}}[
		%ybar stacked,
	 bar width={width:.2f},
	 bar shift = {shift:.2f},
	 ymax={height},
	 tick label style={{/pgf/number format/fixed}},
	 scaled ticks = false,
	 enlarge x limits={{0.05}},
	 enlarge y limits={{0.01}},
	%nodes near coords,
		xlabel={{Eigenvalue}},
		ylabel={{Count}},
		xtick={{{ticks}}},
		x tick label style={{rotate=45,anchor=east}},
		area style,
		xtick pos=left,
		ytick pos=left,
		xtick align=outside,
		% every axis plot/.append style={{draw=none}}
		]
"""
secondLargest = max(weights[1:])
sizeHeuristic = 1.25 if secondLargest/weights[0]>0.1 else 3.5
print(pattern.format(width=step,shift=step/2.0,height=int(sizeHeuristic*secondLargest),ticks=str([float("{0:.2f}".format(x)) for x in bins[::numBins//10]]+[bins[-1]+step])[1:-1]))


if specialFirstBar:
	
	stri = "\\addplot+[ybar,bar width={},bar shift={}] plot coordinates {{".format(bins[1],bins[1]/2.0)
	for i in range(5):
		stri+="({0:.2f}".format(bins[i])+","+str(int(weightsA[i])) + ") "
	stri+= "};"#"({0:.2f}".format(bins[numBins])+",0) };"
	print(stri)
	print("\pgfplotsset{cycle list shift=-1}")

# print(sizeHeuristic)

stri = "\\addplot+[ybar stacked] plot coordinates {"
for i in range(5 if specialFirstBar else 0,numBins):
	stri+="({0:.2f}".format(bins[i])+","+str(int(weightsA[i])) + ") "
stri+= "};"#"({0:.2f}".format(bins[numBins])+",0) };"
print(stri)


stri = "\\addplot+[ybar stacked] plot coordinates {"
for i in range(5 if specialFirstBar else 0,numBins):
	stri+="({0:.2f}".format(bins[i])+","+str(int(weightsB[i])) + ") "
stri+= "};"#"({0:.2f}".format(bins[numBins])+",0) };"
print(stri)
print("""
	\\node at (axis cs:0,{}) [anchor=north west] {{---{:,}}};

\\end{{axis}}
\\end{{tikzpicture}}
\\end{{document}}
""".format(int(sizeHeuristic*secondLargest),int(weights[0])))
# import matplotlib
# matplotlib.use('pgf')
# pgf_with_pdflatex = {
#     "pgf.texsystem": "pdflatex",
#     "pgf.preamble": [
#          r"\usepackage[utf8x]{inputenc}",
#          r"\usepackage[T1]{fontenc}",
#          r"\usepackage{cmbright}",
#          ]
# }
# matplotlib.rcParams.update(pgf_with_pdflatex)  
# print(weightsA)
# print(weightsB)
# print([float("{0:.2f}".format(x)) for x in bins[::5]])
# print(sum(weightsA),sum(weightsB),sum(weightsB)+sum(weightsA),sum(weights))
# from brokenaxes import brokenaxes
# import matplotlib.pyplot as plt

# import seaborn as sns
# sns.set(style="white", palette="muted", color_codes=True)
# fig,ax=plt.subplots()
# #boost spikes for visual clarity
# #bax = brokenaxes(ylims=((0,6000),(36000,38000)),hspace=.1)
# # sns.rugplot(top[-800:],height=0.01,kwargs = {"col":1})
# for i in range(numBins):
# 	if weightsB[i]>0:
# 		print(100/(weightsB[i]**0.8))
# 		weightsB[i]*=100/(weightsB[i]**0.8)
# plt.hist([bins[:-1],bins[:-1]], bins=bins, weights=[weightsA,weightsB],stacked=True);
# plt.savefig('exactHistogram.pdf')
# customTicks = [x+step/2 for (i,x) in enumerate(bins[:-1]) if weightsB[i]>0]
# locs=list(ax.get_xticks())
# labels = [ w.get_text() for w in ax.get_xticklabels()]
# print(locs,labels)

# plt.xticks(locs[1:-1]+customTicks,labels[1:-1]+["" for x in customTicks])
# plt.tick_params(axis='x', color=sns.color_palette().as_hex()[1], direction='in', length=4, width=1)

# # sns.distplot([bins[:-1],bins[:-1]], bins=numBins,hist_kws={"bins":bins, "weights":[weightsA,weightsB],"stacked":True}, kde=False, rug=True)
# plt.savefig('exactHistogram.pgf')