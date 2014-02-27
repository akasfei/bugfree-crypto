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
  [1,1,1,1]
] 
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
] #[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7]

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
def _transform_key(b):
  '''transform the key for each xor'''
  return b[4:]+b[:4]
def _reverse_transform_key(b):
  '''transform the key for each xor'''
  return b[-4:]+b[:-4]
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
def SPN_Bit_Encryption(l_b,_k,f_r=3):
  '''SPN encryption'''
  l_k = list(_k)
  for i in xrange(f_r):
    l_b = _xor(l_b,l_k[:16])
    l_k = _transform_key(l_k)
    l_b = SPN_Block_Substitution(l_b)
    l_b = SPN_Block_Permutation(l_b)
  l_b = _xor(l_b,l_k[:16])
  l_k = _transform_key(l_k)
  l_b = SPN_Block_Substitution(l_b)
  l_b = _xor(l_b,l_k[:16])
  return l_b
def SPN_Bit_Decryption(l_b,_k,f_r=3):
  '''SPN decryption'''
  l_k = list(_k)
  l_k = l_k[16:] + l_k[:16]
  l_b = _xor(l_b,l_k[:16])
  l_k = _reverse_transform_key(l_k)
  l_b = SPN_Reverse_Block_Substitution(l_b)
  l_b = _xor(l_b,l_k[:16])
  l_k = _reverse_transform_key(l_k)
  for i in xrange(f_r):
    l_b = SPN_Block_Permutation(l_b)
    l_b = SPN_Reverse_Block_Substitution(l_b)
    l_b = _xor(l_b,l_k[:16])
    l_k = _reverse_transform_key(l_k)
  return l_b
def test(test_type):
  k_bit = _to_16_bit(random.randint(0,(2**16) - 1)) + _to_16_bit(random.randint(0,(2**16) - 1))
  k_b = list(k_bit)
  print 'Selected key', k_bit
  test_pairs = []
  for i in xrange(10000):
    plain = _to_16_bit(random.randint(0, (2**16) - 1))
    if test_type == 'd':
      plain_a = _xor(plain, [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1])
      test_pairs.append([plain, SPN_Bit_Encryption(plain, k_bit), plain_a, SPN_Bit_Encryption(plain_a, k_bit)])
    else:
      test_pairs.append([plain, SPN_Bit_Encryption(plain, k_bit)])
  count = [[0 for i in xrange((2**4) - 1)]] * ((2**4) - 1)
  for i in xrange(len(test_pairs)):
    if i % 1000 == 0:
      print 'Scanning...', str(i/100), '% complete.'
    p_bit = list(test_pairs[i][0])
    k_bit = list(k_b)

    p_bit = _xor(p_bit, k_bit[:16])
    k_bit = _transform_key(k_bit)
    p_bit = SPN_Block_Substitution(p_bit)
    p_bit = SPN_Block_Permutation(p_bit)

    p_bit = _xor(p_bit, k_bit[:16])
    k_bit = _transform_key(k_bit)
    p_bit = SPN_Block_Substitution(p_bit)
    p_bit = SPN_Block_Permutation(p_bit)

    p_bit = _xor(p_bit, k_bit[:16])
    k_bit = _transform_key(k_bit)
    p_bit = SPN_Block_Substitution(p_bit)
    p_bit = SPN_Block_Permutation(p_bit)

    p_bit = _xor(p_bit, k_bit[:16])
    k_bit = _transform_key(k_bit)
    u4_bit = list(p_bit)
    p_bit = SPN_Block_Substitution(p_bit)
    v4_bit = list(p_bit)
    p_bit = _xor(p_bit, k_bit[:16])
    y_bit = list(p_bit)
    if y_bit != test_pairs[i][1]:
      print 'Encryption failed.', y_bit, test_pairs[i][1]
      return
    for l1 in xrange((2**4) - 1):
      l1_bit = _to_16_bit(l1)[12:16]
      u4_bit[4:8] = _reverse_4_bit_substitution(_xor(l1_bit, y_bit[4:8]))
      if test_type == 'd':
        y_bit_a = list(test_pairs[i][3])
        u4_bit_2_a = _reverse_4_bit_substitution(_xor(l1_bit, y_bit_a[4:8]))
        u4_bit_2_f = _xor(u4_bit[4:8], u4_bit_2_a)
      for l2 in xrange((2**4) - 1):
        l2_bit = _to_16_bit(l1)[12:16]
        u4_bit[12:16] = _reverse_4_bit_substitution(_xor(l2_bit, y_bit[12:16]))
        if test_type == 'l':
          z = test_pairs[i][0][4] + test_pairs[i][0][6] + test_pairs[i][0][7] + u4_bit[5] + u4_bit[7] + u4_bit[13] + u4_bit[15]
          if z % 2 == 0:
            count[l1][l2] += 1
        elif test_type == 'd':
          u4_bit_4_a = _reverse_4_bit_substitution(_xor(l2_bit, y_bit_a[12:16]))
          u4_bit_4_f = _xor(u4_bit[12:16], u4_bit_4_a)
          if (u4_bit_2_f == [0, 1, 1, 0]) and (u4_bit_4_f == [0, 1, 1, 0]):
            count[l1][l2] += 1

  ma = -1
  for l1 in xrange((2**4) - 1):
    for l2 in xrange((2**4) - 1):
      count[l1][l2] = abs(count[l1][l2] - len(test_pairs) / 2)
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
      test(sys.argv[2])
  else:
    print 'python spn.py [encrypt] [decrypt] [test]'