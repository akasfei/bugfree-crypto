import sys, random

s_box_in = [
  [0,0,0,0],
  [0,0,0,1],
  [0,0,1,0],
  [0,0,1,1],
  [0,1,0,0],
  [0,1,0,1],
  [0,1,1,0],
  [0,1,1,1],
  [1,0,0,0],
  [1,0,0,1],
  [1,0,1,0],
  [1,0,1,1],
  [1,1,0,0],
  [1,1,0,1],
  [1,1,1,0],
  [1,1,1,1]]
s_box_out = [
  [1,1,1,0],
  [0,1,0,0],
  [1,1,0,1],
  [0,0,0,1],
  [0,0,1,0],
  [1,1,1,1],
  [1,0,1,1],
  [1,0,0,0],
  [0,0,1,1],
  [1,0,1,0],
  [0,1,1,0],
  [1,1,0,0],
  [0,1,0,1],
  [1,0,0,1],
  [0,0,0,0],
  [0,1,1,1]
]
#[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7]

def _to_16_bit(x):
  '''convert an integer to a 16-bit binary representation list'''
  v = map(int,list(bin(x)[2:]))
  return (([0] * (16 - len(v))) + v)
def _to_int(l):
  '''convert a binary representation list to an integer'''
  return int(("0b" + reduce(lambda a,b:a+b,(map(str,l)))),2)
def _xor(a,b):
  '''apply xor on two binary representation lists'''
  return map(lambda a,b:((a+b)%2),a,b)
def _split_blocks(bit_list):
  '''splits 16-bit list in 4, 4-bit blocks'''
  return bit_list[:4],bit_list[4:8],bit_list[8:12],bit_list[12:]
def _permute(L,permutation_mask):
  '''permutes bits of a binary representation list following a permutation rule mask'''
  return [L[i] for i in permutation_mask]
def _4_bit_substitution(b):
  '''replace the s-Box with a 4-bit substition (for encryption)'''
  return s_box_out[s_box_in.index(b)]
def _reverse_4_bit_substitution(b):
  '''replace the s-box with a 4-bit substition (for decryption)'''
  return s_box_in[s_box_out.index(b)]
def SPN_Block_Substitution(b):
  '''s-box phase of the SPN cipher for encryption'''
  return reduce(lambda a,b:a+b,(map(_4_bit_substitution,_split_blocks(b))))
def SPN_Reverse_Block_Substitution(b):
  '''s-box phase of the SPN cipher for decryption'''
  return reduce(lambda a,b:a+b,(map(_reverse_4_bit_substitution,_split_blocks(b))))
def SPN_Block_Permutation(b):
  '''permutation phase of the SPN cipher'''
  bit_permutation_mask = [0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15]
  return _permute(b,bit_permutation_mask)
def SPN_Bit_Encryption(l_b,l_k,FEISTEL_ROUNDS=3):
  '''SPN encryption'''
  l_b = _xor(l_b,l_k)
  for i in xrange(FEISTEL_ROUNDS):
    l_b = SPN_Block_Substitution(l_b)
    l_b = SPN_Block_Permutation(l_b)
    l_b = _xor(l_b,l_k)
  return l_b
def SPN_Bit_Decryption(l_b,l_k,FEISTEL_ROUNDS=3):
  '''SPN decryption'''
  for i in xrange(FEISTEL_ROUNDS):
    l_b = _xor(l_b,l_k)
    l_b = SPN_Block_Permutation(l_b)
    l_b = SPN_Reverse_Block_Substitution(l_b)
  l_b = _xor(l_b,l_k)
  return l_b
def linear_test():
  k = random.randint(0,(2**16) - 1)
  k_bit = _to_16_bit(k)
  print 'Selected key ', k, k_bit
  testPairs = []
  for i in xrange(10000):
    plain = _to_16_bit(random.randint(0, (2**16) - 1))
    testPairs.append([plain, SPN_Bit_Encryption(plain, k_bit)])
  count = [[0 for i in xrange((2**4) - 1)]] * ((2**4) - 1)

  for i in xrange(len(testPairs)):
    if i % 1000 == 0:
      print 'Scanning, ' + str(i / 100) + '% complete.'
    for l1 in xrange((2**4) - 1):
      for l2 in xrange((2**4) - 1):
        p_bit = list(testPairs[i][0])
        p_bit = _xor(p_bit, k_bit)
        p_bit = SPN_Block_Permutation(p_bit)
        p_bit = SPN_Block_Substitution(p_bit)

        p_bit = _xor(p_bit, k_bit)
        p_bit = SPN_Block_Permutation(p_bit)
        p_bit = SPN_Block_Substitution(p_bit)

        p_bit = _xor(p_bit, k_bit)
        p_bit = SPN_Block_Permutation(p_bit)
        p_bit = SPN_Block_Substitution(p_bit)

        p_bit = _xor(p_bit, k_bit)
        u4_bit = list(p_bit)
        p_bit = SPN_Block_Permutation(p_bit)
        v4_bit = list(p_bit)
        y_bit = list(p_bit)

        l1_bit = _to_16_bit(l1)[12:16]
        l2_bit = _to_16_bit(l1)[12:16]

        u4_bit[4:8] = _reverse_4_bit_substitution(_xor(l1_bit, y_bit[4:8]))
        u4_bit[12:16] = _reverse_4_bit_substitution(_xor(l2_bit, y_bit[12:16]))
        
        z = p_bit[4] + p_bit[6] + p_bit[7] + u4_bit[5] + u4_bit[7] + u4_bit[13] + u4_bit[15]
        if z % 2 == 0:
          count[l1][l2] += 1

  ma = -1
  for l1 in xrange((2**4) - 1):
    for l2 in xrange((2**4) - 1):
      count[l1][l2] = abs(count[l1][l2] - len(testPairs) / 2)
      if count[l1][l2] > ma:
        ma = count[l1][l2]
        maxkey = [l1, l2]

  print maxkey

if __name__ == '__main__':
  if len(sys.argv) > 1:
    if sys.argv[1] == 'encrypt':
      if len(sys.argv) != 4:
        print 'python spn.py encrypt <key> <int>'
      print _to_int(SPN_Bit_Encryption(_to_16_bit(int(sys.argv[3])), _to_16_bit(int(sys.argv[2]))))
    elif sys.argv[1] == 'decrypt':
      if len(sys.argv) != 4:
        print 'python spn.py decrypt <key> <int>'
      print _to_int(SPN_Bit_Decryption(_to_16_bit(int(sys.argv[3])), _to_16_bit(int(sys.argv[2]))))
    elif sys.argv[1] == 'test':
      linear_test()
  else:
    print 'python spn.py [encrypt] [decrypt] [test]'