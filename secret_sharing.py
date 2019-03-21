# import modules
import random as rd  # generating random numbers for distributions

# enryption function (additive sharing)
def encrypt(x, Q=None, n_shares=3):
    shares = tuple(rd.randrange(0,Q) for _ in range(n_shares-1))
    return (*shares, ((x - sum(shares)) % Q))

# decryption function
def decrypt(*shares, Q=None):
    return sum(shares) % Q

# addition algorithm
def add(x, y, Q=None):
    # x & y have to have the same number of shares (= length)
    return [(xi + yi) % Q for xi, yi in zip(x,y)]

# substraction algorithm
def sub(x, y, Q=None):
    # x & y have to have the same number of shares (= length)
    return [(xi - yi) % Q for xi, yi in zip(x,y)]

# generate additional independent masks which have a multiplicative relationship
def generate_mul_triple(Q=None, n_shares=3):
    # create triple
    s = rd.randrange(0,Q)
    t = rd.randrange(0,Q)
    st = (s*t)%Q
    
    # create shares
    s = encrypt(s, n_shares=n_shares)
    t = encrypt(t, n_shares=n_shares)
    st = encrypt(st, n_shares=n_shares)
    
    return s,t,st

# multiplication algorithm
def mul(x,y, Q=None):
    # get number of shares
    n_shares = len(x)
    # create triple from trusted party
    s,t,st = generate_mul_triple(n_shares=n_shares)
    
    # create one-time-pad encryptions (each party has a share of each)
    alpha = sum(sub(x,s))
    beta = sum(sub(y,t))
    
    # create z with additive relationship (using indicator function to only add alpha*beta once)
    z = [(st[i] + (alpha * t[i]) + (beta * s[i]) + int(i==0)*(alpha*beta)) % Q for i in range(n_shares)]
    
    return z
