import time, string, random, hashlib, bisect, math

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

def LSH(collection, t, b=1, r=100):

  if(len(collection[0])%b or len(collection[0])!=r):
    raise ValueError

  #compute b with t and r
  if b == 1:
    factors = factorization(r)
    b = factors[bisect.bisect_left(factors, 1/-math.log(t, r))]

  candidatePairs = set()

  for i in range(r):
    #traverse all rows
    bucket = {}
    for j in range(int(len(collection[0])/b)):
      #traverse all columns in a row and hash bands to bucket
      band = collection[j*b][i:i+b-1]
      hashvalue = 1
      for k in band:
        if(k):
          hashvalue *= k
      if hashvalue in bucket.keys(): 
        bucket[hashvalue].append(j)
      else:
        bucket[hashvalue] = [j]
    
    for value in bucket.values():
      #find candidates from bucket
      candidates = value
      while(len(candidates)>1):
        j = candidates.pop()
        for k in candidates:
          candidatePairs.add(frozenset([j,k]))

  return candidatePairs

def factorization(num):
  return [i for i in range(1, num) if(num%i == 0)]

def print_realHashDigit(collection):
  """ calculate max and mean hash digit, return with tuple(max, mean)"""
  sum_ = 0
  mean_ = 0
  max_ = 0
  i = 0
  for text in collection:
    for hash_num in text:
      sum_ += hash_num
      i += 1
      if hash_num > max_:
        max_ = hash_num
  mean_ = int(sum_/i)
  print("max:{0}\nmean:{1}".format(max_, mean_))
  return max_, mean_

if __name__ == "__main__":
  collection = []
  with open("data/data.txt", encoding='utf-8') as file:
    collection = [min_hash(k_shingle(i))  for i in file.read().split("\n")]
    #print_realHashDigit(collection)
  candidatePairs = LSH(collection, 0.5)
  print(candidatePairs)