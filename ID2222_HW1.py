import time, string, random, hashlib, bisect

def k_shingle(text, k=3):
  """ Convert sentense into character ngrams. """
  return sorted([int(hashlib.sha256(text[i:i+k].encode('utf-8')).hexdigest(), 16) % (10**8) for i in range(len(text)-k+1)])

def speed_test():

  # Generate 10000 random strings of length 100.
  sents = [" ".join([''.join(random.choice(string.ascii_uppercase) for j in range(10)) for i in range(100)]) for k in range(100)]

  start = time.time()
  x = [k_shingle(sent, k) for sent in sents]
  print(time.time() - start)

def compare_sets(a, b):
  aSet = set(a)
  bSet = set(b)
  inter = aSet.intersection(bSet)
  union = aSet.union(bSet)
  return len(inter)/len(union)

def min_hash(doc, signitureLen=100, seed=0):
  random.seed(seed)
  randomList = [random.randint(0, 10**8-1) for i in range(signitureLen)]
  signiture = [doc[i]-x if i!=len(doc) else doc[0]-x+10**8 for (i,x) in [(bisect.bisect_left(doc, rand), rand) for rand in randomList]]
  return signiture

def compare_signiture(sigA, sigB):
  iden = 0
  for i in range(len(sigA)):
    if sigA[i] == sigB[i]:
      iden += 1
  return iden/len(sigB)

def compute_loss(trueValue, guess):
  return abs(guess-trueValue)/trueValue

def LSH(collection, t, r=5, b=100):

  if(len(collection[0])%r or len(collection)!=b or len(collection[0])!=0):
    raise ValueError
  
  

if __name__ == "__main__":

  """   k = 6
  sentenceA = 'this is a foo bar sentence and i want to ngramize it'
  sentenceB = 'this are two foo bar sentences and i want to ngramize it'
  sentenceRandomA = ''.join(random.choice(string.ascii_uppercase) for j in range(10000))
  sentenceRandomB = ''.join(random.choice(string.ascii_uppercase) for j in range(10000))
  loss = 0
  for i in range(10000):
    di = compare_sets(k_shingle(sentenceRandomA), k_shingle(sentenceRandomB))
    sig = compare_signiture(min_hash(k_shingle(sentenceRandomA)), min_hash(k_shingle(sentenceRandomB)))
    loss += compute_loss(di, sig)
  loss /= 10000 """
  
  print(loss)