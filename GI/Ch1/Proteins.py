import sys
sys.path.append(r"..\Ch5")
from NFAbySAT import synthesize
from functools import partial
from FAdo.common import DFAsymbolUnknown

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

def acceptsBy(aut, w):
  try:
    return aut.evalWordP(w)
  except DFAsymbolUnknown:
    return False

S_plus, S_minus = set(Train_pos), set(Train_neg)
k = 1
while True:
  print k,
  A = synthesize(S_plus, S_minus, k)
  if A:
    print findACC(partial(acceptsBy, A))
    print A.dotFormat()
    break
  k += 1
