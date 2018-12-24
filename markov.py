import re
import random
from collections import defaultdict, deque


class MarkovChain:
    
  def __init__(self, num_key_words = 2):
    #How many words at a time, default 2
    self.num_key_words = num_key_words
    self.dict = defaultdict(list)
    self.regex = re.compile('[,.!;\?\:\-\[\]\n]+')
    self.seeded = False
    self.seed()


  def seed(self, rand_seed=None):
    if self.seeded is not True:
        random.seed()
        self.seeded = True


  def add_string(self, str):
    #Removes punctuation and lowercases
    new_str = self.regex.sub(' ', str).lower()
    tuples = self.generate_tuple_keys(clean_str.split())
    for t in tuples:
      self.dict[t[0]].append(t[1])


  def generate_tuple_keys(self, data):
    if len(data) < self.num_key_words:
      return
    for i in range(len(data) - self.num_key_words):
      yield [ tuple(data[i:i+self.num_key_words]), data[i+self.num_key_words] ]


  def generate_text(self, max_length = 200):
    context = deque()
    output = []
    if len(self.dict) > 0:
      self.seed(rand_seed = len(self.dict))
      idx = random.randint(0, len(self.dict)-1)
      chain_head = list(list(self.dict.keys())[idx])
      context.extend(chain_head)

      while len(output) < (max_length - self.num_key_words):
        next_choices = self.dict[tuple(context)]
        if len(next_choices) > 0:
          next_word = random.choice(next_choices)
          context.append(next_word)
          output.append(context.popleft())
        else:
          break
      output.extend(list(context))
    return output
