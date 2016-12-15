from sklearn import tree
from sklearn.externals.six import StringIO
from functools import partial

Sigma = set(['N', 'M', 'L', 'K', 'I', 'H', 'W', 'V', 'T', 'S', 'R', 'Q', 'Y', 'G', 'F', 'E', 'D', 'C', 'A', 'P'])
idx = dict(zip(list(Sigma), range(len(Sigma))))

Train_pos = \
['STQIIE', 'STVIIL', 'SDVIIE', 'STVIFE', 'STVIIS', 'STVFIE', 'STVIIN', 'WIVIFF', 'YLNWYQ', 'SFQIYA', \
 'SFFFIQ', 'STFIIE', 'GTFFIN', 'ETVIIE', 'SEVIIE', 'YTVIIE', 'STVIIV', 'SMVLFS', 'STVIYE', 'VILLIS', \
 'SQFYIT', 'SVVIIE', 'STVIII', 'HLVYIM', 'IEMIFV', 'FYLLYY', 'FESNFN', 'TTVIIE', 'STVIIF', 'STVIIQ', \
 'IFDFIQ', 'RQVLIF', 'ITVIIE', 'KIVKWD', 'LTVIIE', 'WVFWIG', 'SLVIIE', 'STVTIE', 'STVIIE', 'GTFNII', \
 'VSFEIV', 'GEWTYD', 'KLLIYE', 'SGVIIE', 'STVNIE', 'GVNYFL', 'STLIIE', 'GTVLFM', 'AGVNYF', 'KVQIIN', \
 'GTVIIE', 'WTVIIE', 'STNIIE', 'AQFIIS', 'SSVIIE', 'KDWSFY', 'STVIIW', 'SMVIIE', 'ALEEYT', 'HYFNIF', \
 'SFLIFL', 'STVIIA', 'DCVNIT', 'NHVTLS', 'EGVLYV', 'VEALYL', 'LAVLFL', 'STSIIE', 'STEIIE', 'STVIIY', \
 'LYQLEN', 'SAVIIE', 'VQIVYK', 'SIVIIE', 'HGWLIM', 'STVYIE', 'QLENYC', 'MIENIQ']
Train_neg = \
['KTVIVE', 'FHPSDI', 'FSKDWS', 'STVITE', 'STVDIE', 'FMFFII', 'YLEIII', 'STVIDE', 'RMFNII', 'ETWFFG', \
 'NGKSNF', 'KECLIN', 'STVQIE', 'IQVYSR', 'AAELRN', 'EYLKIA', 'KSNFLN', 'DECFFF', 'STVPIE', 'YVSGFH', \
 'EALYLV', 'HIFIIM', 'RVNHVT', 'AEVLAL', 'PSDIEV', 'STVIPE', 'DILTYT', 'RETWFF', 'STVIVE', 'KTVIYE', \
 'KLLEIA', 'QPKIVK', 'EECLFL', 'QLQLNI', 'IQRTPK', 'YAELIV', 'KAFIIQ', 'GFFYTP', 'HPAENG', 'KTVIIT', \
 'AARRFF', 'STVIGE', 'LSFSKD', 'NIVLIM', 'RLVFID', 'STVSIE', 'LSQPKI', 'RGFFYT', 'YQLENY', 'QFNLQF', \
 'ECFFFE', 'SDLSFS', 'KVEHSD', 'STVMIE', 'QAQNQW', 'SSNNFG', 'TFWEIS', 'VTLSQP', 'STVIEE', 'TLKNYI', \
 'LRQIIE', 'STGIIE', 'YTFTIS', 'SLYQLE', 'DADLYL', 'SHLVEA', 'SRHPAE', 'KWDRDM', 'FFYTPK', 'STVIQE', \
 'GMFNIQ', 'HKALFW', 'LLWNNQ', 'GSHLVE', 'VTQEFW', 'NIQYQF', 'STMIIE', 'PTEKDE', 'TNELYM', 'LIAGFN', \
 'HAFLII', 'YYTEFT', 'EKNLYL', 'KTVLIE', 'FTPTEK', 'STPIIE', 'STVVIE', 'SGFHPS', 'LFGNID', 'SPVIIE', \
 'STVISE', 'EKDEYA', 'RVAFFE', 'FYTPKT', 'PKIQVY', 'DDSLFF', 'ERGFFY', 'PTVIIE', 'DIEVDL', 'STIIIE']
Test_pos = \
['FTVIIE', 'HQLIIM', 'ISFLIF', 'GTFFIT', 'YYQNYQ', 'HFVWIA', 'NTVIIE', 'SNVIIE', 'MLVLFV', 'YVEYIG', \
 'STVWIE', 'STVIIM', 'EYSNFS', 'SQVIIE', 'SYVIIE', 'FLVHSS', 'NQQNQY', 'QYFNQM', 'DTVIIE', 'VTSTFS', \
 'STVIIT', 'LIFLIV', 'SFVIIE', 'NYVWIV', 'NFGAIL', 'STVIID', 'VTVIIE', 'MTVIIE', 'STVLIE', 'LLYYTE', \
 'QTVIIE', 'KLFIIQ', 'ATVIIE', 'LVEALY', 'TYVEYI', 'RVFNIM', 'NQFIIS', 'STVEIE']
Test_neg = \
['STDIIE', 'LKNGER', 'KAILFL', 'NYFAIR', 'VKWDRD', 'KENIIF', 'WVENYP', 'WYFYIQ', 'VAQLNN', 'DLLKNG', \
 'HLVEAL', 'TAWYAE', 'STAIIE', 'STVGIE', 'ERIEKV', 'EVDLLK', 'STVIIP', 'AINKIQ', 'STTIIE', 'TYQIIR', \
 'MYFFIF', 'TEFTPT', 'NGERIE', 'AENGKS', 'ICSLYQ', 'YASEIE', 'VAWLKM', 'NLGPVL', 'RTPKIQ', 'EHSDLS', \
 'AEMEYL', 'NYNTYR', 'TAELIT', 'HTEIIE', 'AEKLFD', 'LAEAIG', 'STVIME', 'GERGFF', 'VYSRHP', 'YFQINN', \
 'SWVIIE', 'KGENFT', 'STVIWE', 'STYIIE', 'QTNLYG', 'HYQWNQ', 'IEKVEH', 'KMFFIQ', 'ILENIS', 'FFWRFM', \
 'STVINE', 'STVAIE', 'FLKYFT', 'FGELFE', 'STVILE', 'WSFYLL', 'LMSLFG', 'FVNQHL', 'STVIAE', 'KTVIIE', \
 'MYWIIF']

def findACC(f):
  score = 0
  for w in Test_pos:
    if f(w):
      score += 1
  for w in Test_neg:
    if not f(w):
      score += 1
  if score == 0:
    return 0.0
  else:
    return float(score)/float(len(Test_pos) + len(Test_neg))

def accepts(clf, w):
  return clf.predict([map(lambda c: idx[c], list(w))])[0] == 1

X = []
Y = []
for x in Train_pos:
  X.append(map(lambda c: idx[c], list(x)))
  Y.append(1)
for y in Train_neg:
  X.append(map(lambda c: idx[c], list(y)))
  Y.append(0)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
print findACC(partial(accepts, clf))
