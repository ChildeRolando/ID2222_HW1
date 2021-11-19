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

  for j in range(int(r/b)):
    #traverse all rows
    bucket = {}
    for i in range(len(collection)):
      #traverse all columns in a row and hash bands to bucket
      band = collection[i][j*b:j*b+b]
      hashvalue = 1
      for num in band:
        if num:
          hashvalue += num
      hashvalue = int(hashlib.sha256(str(band).encode('utf-8')).hexdigest(), 16)
      if hashvalue in bucket.keys(): 
        bucket[hashvalue].append(i)
      else:
        bucket[hashvalue] = [i]
    
    for value in bucket.values():
      #find candidates from bucket
      candidates = value
      while(len(candidates)>1):
        j = candidates.pop()
        for k in candidates:
          candidatePairs.add(frozenset([j,k]))
  candidatePairs = [set(i) for i in candidatePairs]
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

def signiture_similarity_sort(collection):
  ranking = []
  for i in range(len(collection)):
    s1 = collection[i]
    for j in range(i+1, len(collection)):
      s2 = collection[j]
      ranking.append([compare_signiture(s1,s2), {i,j}])
  rank = sorted(ranking, key=(lambda x:x[0]), reverse=True)
  return rank

if __name__ == "__main__":
  collection = []
  t = 0.6
  with open("data/data.txt", encoding='utf-8') as file:
    rawTexts = file.read().split("\n")
    kShingles = [k_shingle(i) for i in rawTexts]
    collection = [min_hash(i, 200)  for i in kShingles]
    #print_realHashDigit(collection)
  candidatePairs = LSH(collection, t, 8, 200)
  rank = signiture_similarity_sort(collection)
  print("rank:\n",[i for i in rank if i[0]>0.4])
  print("\ncandidatePairs:\n",candidatePairs)