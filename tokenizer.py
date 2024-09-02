import os
import sys

def test():

  print('ordinal of \'h\'')
  print(ord('h'))

  sent = "नमस्ते  means hello in hindi"
  points = [ord(x) for x in sent]
  print(points)


  print('encode in utf-8, bytes: ')
  print(list(sent.encode("utf-8")))


class BasicTokenizer():
  """Tokenize text using Byte-pair encoding (BPE)"""

  def __init__(self):
    self.vocab = {} # to encode text to tokens
    self.token_vocab_map = {} # to decode tokens to text
    self.max_token = 0

  # def train(self, text, vocab_size, verbose=False):
  #   pass

  def encode(self, text):
    # simple let's encode in utf-8
    # return [c for c in text.encode('utf-8')]
    return text.encode('utf-8')


  def decode(self, ids):
    # simple utf-8 decode
    # return ids.decode('utf-8')  
    return ids.decode('utf-8')  


class BytePairTokenizer(BasicTokenizer):
  def __inint__(self):
    super().__init__()

  def add_to_vocab(self, c):
    if c not in self.vocab:
      self.vocab[c] = self.max_token
      self.token_vocab_map[self.max_token] = c
      self.max_token += 1

  def convert_to_tokens(self, text):
    return [self.vocab[c] for c in text]

  def byte_pair_encode_rec(self, tokens):
    byte_pairs = {} # 2 char to count
    locations = {}
    i = 0
    for i in range(len(tokens)-1):
      # pair = str(tokens[i: i+2])
      pair = f"{tokens[i]},{tokens[i+1]}"
      byte_pairs[pair] = byte_pairs.get(pair, 0) + 1
      locs = locations.get(pair)
      if locs is not None and locs[-1] == i-1:
        # if last location is just the previous one
        continue      
      locations.setdefault(pair, []).append(i)



    print(byte_pairs)

    max_count, best_pair = 0, ''
    for pair in byte_pairs:
      if byte_pairs[pair] > max_count:
        best_pair, max_count = pair, byte_pairs[pair]

    # base case, no more to compress
    if max_count == 1:
      print('no more compression todo')
      return tokens
    
    print(best_pair, max_count)
    print(self.vocab)
    print(self.token_vocab_map)
    print(f'add new token to vocab: {best_pair}')
    t1, t2 = best_pair.split(',')
    new_vocab = self.token_vocab_map[int(t1)] + self.token_vocab_map[int(t2)]
    print(f'add new vocab: {new_vocab}')
    self.add_to_vocab(new_vocab)
    print(self.vocab)
    print(self.token_vocab_map)

    # compress the token rep
    print(f'best pair locations: {locations[best_pair]}')
    res = []
    i = 0
    for j in locations[best_pair]:
      print(f'on loc: {j}')
      res.extend(tokens[i:j])
      res.extend([self.max_token-1])
      i = j+2
      print(f'set i to {i}')
    res.extend(tokens[i:])

    print('compressed to: ')
    print(res)

    # return res

    return self.byte_pair_encode_rec(res)

    

  def encode(self, text):
    for c in text:
      self.add_to_vocab(c)

    tokens = self.convert_to_tokens(text)
    print('basic tokens')
    print(tokens)
    return self.byte_pair_encode_rec(tokens)

  def decode(self, tokens: str):
    res = [self.token_vocab_map[tok] for tok in tokens]
    return "".join(res)
    




if __name__ == "__main__":
  print('main')
  print(sys.argv)
  print(len(sys.argv))
  if len(sys.argv) >=2:
    print(sys.argv)
    if sys.argv[1] == "test":
      test()
      exit()
          
  # my_str = "hello, Vancouver"
  my_str = "hello, hello Vancouver"
  # my_str = "aaabdaaabac"
  tok = BytePairTokenizer()
  enc = tok.encode(my_str)
  print('encoding')
  print(enc)
  print(f'len str: {len(my_str)}')
  print(f'len encoding: {len(enc)}')
  print(f'vocab size: {tok.max_token-1}')
  print(f'vocab: {tok.vocab}')
  print(f'token vocab map: {tok.token_vocab_map}')
  dec = tok.decode(enc)
  print(f'decoded: {dec}')
  assert(my_str == tok.decode(enc))
  
