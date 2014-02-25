# RSA Encryption

## Import(s) ##
import sys, random, pickle

## Util(s) ##
def print_usage( command='' ):
  if command == 'encrypt':
    print 'encrypt <plaintext_filename> <ciphertext_filename>'
  elif command == 'decrypt':
    print 'decrypt <ciphertext_filename> <decrypted_filename>'
  else:
    print 'Usage:'
    print '\tinit - rsa setup, generates rsa.pub and rsa.key as public and private key'
    print '\tencrypt -> takes plaintext_filename, and ciphertext_filename as inputs'
    print '\tdecrypt -> takes ciphertext_filename, and decrypted_filename as inputs '

def miller_rabin_test( a, s, d, n ):
  atop = pow( a, d, n )
  if atop == 1:
    return True
  for i in xrange( s - 1 ):
    if atop == n - 1:
      return True
    atop = ( atop * atop ) % n
  return atop == n - 1

def miller_rabin( n, confidence ):
  d = n - 1
  s = 0
  while d % 2 == 0:
    d >>= 1
    s += 1

  for i in range( confidence ):
    a = 0
    while a == 0:
      a = random.randrange( n )
    if not miller_rabin_test( a, s, d, n ):
      return False
  return True

def euclid_gcd( a, b ):
  if a < b:
    a, b = b, a
  while b != 0:
    a, b = b, a % b
  return a

def ext_euclid( a, b ):
  if b == 0:
    return 1, 0, a
  else:
    x, y, gcd = ext_euclid( b, a % b )
    return y, x - y * ( a // b ), gcd

def inverse_mod( a, m ):
  x, y, gcd = ext_euclid( a, m )
  if gcd == 1:
    return x % m
  else:
    return None

## Class(es) ##
class RSAKey( object ):
  meta = dict()
  primality_confidence = 20

  def gen_keys(self):
    # generate p (nbits-bit prime)
    while 1:
      p = random.getrandbits(256)
      if miller_rabin( p, self.primality_confidence ):
        self.meta.update({'p': p})
        break
    # generate q (256-bit prime)
    while 1:
      q = random.getrandbits(256)
      if miller_rabin( q, self.primality_confidence ):
        self.meta.update({'q': q})
        break
    
    # compute modulus: (p * q)
    modulus = long(self.meta['p'] * self.meta['q'])
    self.meta.update({'modulus': modulus})

    # compute phi: ((p - 1)(q - 1))
    phi = long((self.meta['p'] - 1) * (self.meta['q'] - 1))
    self.meta.update({'phi': phi})

    # choose e s.t 1 < e < phi and euclid_gcd(e, phi) = 1
    while 1:
      while 1:
        e = random.randrange( phi )
        if e == 0: continue
        if euclid_gcd( e, phi ) == 1:
          self.meta.update({'e': e})
          self.meta.update({'pub_key': (modulus, e)})
          break
    
      # compute d:
      d = long(inverse_mod(long(self.meta['e']), phi))
      if d is None: continue
      else:
        self.meta.update({'d': d})
        self.meta.update({'priv_key': (modulus, d)})
        break

    self.store()

  def encrypt(self, plaintext_fn, ciphertext_fn):
    key_handle = open('rsa.pub', 'r')
    pub_key = list(pickle.load(key_handle))
    plaintext_handle = open( plaintext_fn, 'r')
    plaintext = plaintext_handle.read()
    plaintext_handle.close()
    ciphertext = ''
    chunk = ind = 0
    for char in plaintext:
      chunk += ord(char)
      ind = ind + 1
      if ind > 62:
        ciphertext += str(pow(chunk, pub_key[1], pub_key[0])) + '\n'
        chunk = ind = 0
      else:
        chunk *= 256
    if ind > 0:
      ciphertext += str(pow(chunk, pub_key[1], pub_key[0])) + '\n'
    ciphertext_handle = open(ciphertext_fn, 'w')
    ciphertext_handle.write(ciphertext)
    ciphertext_handle.close()
    print 'Wrote encrypted data to: ' + ciphertext_fn

  def decrypt(self, ciphertext_fn, decrypted_fn):
    key_handle = open('rsa.key', 'r')
    priv_key = list(pickle.load(key_handle))
    ciphertext_handle = open(ciphertext_fn, 'r')
    ciphertext = ciphertext_handle.read().split()
    decrypted = ''
    for chunk in ciphertext:
      decrypted_chunk = pow(long(chunk), priv_key[1], priv_key[0])
      decrypted_chars = []
      while decrypted_chunk / 256 > 0:
        decrypted_chars.insert(0, chr(decrypted_chunk % 256))
        decrypted_chunk /= 256
      if decrypted_chunk / 256 == 0:
        if decrypted_chunk > 0:
          decrypted_chars.insert(0, chr(decrypted_chunk))
      if len(decrypted_chars) > 0:
        decrypted += ''.join(decrypted_chars)
    decrypted_handle = open(decrypted_fn, 'w')
    decrypted_handle.write(decrypted)
    decrypted_handle.close()
    print 'Wrote decrypted data to: ' + decrypted_fn

  def store(self):
    handle = open('rsa.pub', 'w')
    pickle.dump(self.meta['pub_key'], handle)
    handle.close()
    handle = open('rsa.key', 'w')
    pickle.dump(self.meta['priv_key'], handle)
    handle.close()
    print 'Wrote generated keys to rsa.pub and rsa.key.'

  def show_keys(self):
    pub_handle = open('rsa.pub', 'r')
    priv_handle = open('rsa.key', 'r')
    pub_key = list(pickle.load(pub_handle))
    priv_key = list(pickle.load(priv_handle))
    print 'Public key: ' + str(pub_key)
    print 'Private key: ' + str(priv_key)

## Main ##
if len(sys.argv) > 1:
  if str(sys.argv[1]) == 'init':
    keys = RSAKey()
    keys.gen_keys()
  elif str(sys.argv[1]) == 'encrypt':
    if len(sys.argv) != 4:
      print 'Invalid number of inputs to encrypt, expects 3, given ' + str(len(sys.argv) - 2)
      print_usage('encrypt')
    else:
      keys = RSAKey()
      keys.encrypt(str(sys.argv[2]), str(sys.argv[3]))
  elif str(sys.argv[1]) == 'decrypt':
    if len(sys.argv) != 4:
      print 'Invalid number of inputs to decrypt, expects 3, given ' + str(len(sys.argv) - 2)
      print_usage('decrypt')
    else:
      keys = RSAKey()
      keys.decrypt(str(sys.argv[2]), str(sys.argv[3]))
  elif str(sys.argv[1]) == 'showkeys':
    keys = RSAKey()
    keys.show_keys()
  else:
    print 'Unrecognized input: ' + str(sys.argv[1])
    print_usage()
    
else:
  print 'Invalid number of inputs'
  print_usage()
