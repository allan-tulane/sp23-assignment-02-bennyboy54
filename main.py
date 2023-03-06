"""
CMPS 2200  Assignment 2.
See assignment-02.pdf for details.
"""
import time


class BinaryNumber:
  """ done """

  def __init__(self, n):
    self.decimal_val = n
    self.binary_vec = list('{0:b}'.format(n))

  def __repr__(self):
    return ('decimal=%d binary=%s' %
            (self.decimal_val, ''.join(self.binary_vec)))


## Implement multiplication functions here. Note that you will have to
## ensure that x, y are appropriately sized binary vectors for a
## divide and conquer approach.
def binary2int(binary_vec):
  if len(binary_vec) == 0:
    return BinaryNumber(0)
  return BinaryNumber(int(''.join(binary_vec), 2))


def split_number(vec):
  return (binary2int(vec[:len(vec) // 2]), binary2int(vec[len(vec) // 2:]))


def bit_shift(number, n):
  # append n 0s to this number's binary string
  return binary2int(number.binary_vec + ['0'] * n)


def pad(x, y):
  # pad with leading 0 if x/y have different number of bits
  # e.g., [1,0] vs [1]
  if len(x) < len(y):
    x = ['0'] * (len(y) - len(x)) + x
  elif len(y) < len(x):
    y = ['0'] * (len(x) - len(y)) + y
  # pad with leading 0 if not even number of bits
  if len(x) % 2 != 0:
    x = ['0'] + x
    y = ['0'] + y
  return x, y


def subquadratic_multiply(x, y):
  ### TODO
  return _subquadratic_multiply(x, y).decimal_val
  pass


  ###
def _subquadratic_multiply(x, y):
  xvec = x.binary_vec
  yvec = y.binary_vec
  if len(xvec) != len(yvec):
    xvec, yvec = pad(xvec, yvec)

  if len(xvec) and len(yvec) <= 1:
    return BinaryNumber(x.decimal_val * y.decimal_val)
  else:
    n = len(xvec)
    x_left, x_right = split_number(xvec)
    y_left, y_right = split_number(yvec)

    xLyL = _subquadratic_multiply(x_left, y_left)
   
    xRyR = _subquadratic_multiply(x_right, y_right)
    
    xL_p_xR = x_left.decimal_val + x_right.decimal_val
    
    yL_p_yR = y_left.decimal_val + y_right.decimal_val
    
        
    xLxR_times_yLyR = _subquadratic_multiply(BinaryNumber(xL_p_xR), BinaryNumber(yL_p_yR))

    z1 = xLxR_times_yLyR.decimal_val - xLyL.decimal_val - xRyR.decimal_val
    z1 = bit_shift(BinaryNumber(z1), n//2).decimal_val
    z2 = xRyR.decimal_val
    z0 = bit_shift(xLyL, n).decimal_val
    sum = z1 + z2 + z0

    return BinaryNumber(sum)


## Feel free to add your own tests here.
def test_multiply():
  assert subquadratic_multiply(BinaryNumber(2), BinaryNumber(2)) == 2 * 2
  assert subquadratic_multiply(BinaryNumber(4), BinaryNumber(2)) == 4 * 2
  assert subquadratic_multiply(BinaryNumber(2), BinaryNumber(3)) == 2 * 3

def time_multiply(x, y, f):
  start = time.time()
  # multiply two numbers x, y using function f
  return (time.time() - start) * 1000


print(time_multiply(2,2,subquadratic_multiply(BinaryNumber(2),BinaryNumber(2))))
print(time_multiply(10,10,subquadratic_multiply(BinaryNumber(10),BinaryNumber(10))))
print(time_multiply(10000,10000,subquadratic_multiply(BinaryNumber(10000),BinaryNumber(10000))))
print(time_multiply(2,200000,subquadratic_multiply(BinaryNumber(2),BinaryNumber(200000))))
print(time_multiply(2000000,20000000,subquadratic_multiply(BinaryNumber(2000000),BinaryNumber(20000000))))
print(time_multiply(9999999999,9999999999,subquadratic_multiply(BinaryNumber(9999999999),BinaryNumber(9999999999))))

