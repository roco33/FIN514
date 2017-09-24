# -*- coding: utf-8 -*-

import numpy as np
import math
from scipy.stats import norm
import matplotlib.pyplot as plt


# 1.
# a. calculate the B-S value of the put

S0 = 100
K = 105
r = 0.01
div = 0
sigma = 0.3
T = 1

d1 = 1 / (math.sqrt(T)) * (math.log(S0/K) + ((r - div) + sigma**2 / 2) * T)
d2 = d1 - sigma * math.sqrt(T)

P = norm.cdf(-d2) * K * math.exp(-r*T) - norm.cdf(-d1) * S0


# b.
# CCR

P1 = np.array([])

def CCR(S0, K, r, div, sigma, T, N, method):
    delta = T/N
    VStock = np.zeros((601,601))
    VOption = np.zeros((601,601))
    if method == 'CCR':
        u = math.exp(sigma * math.sqrt(delta))
        d = 1/u
        
    qu = (math.exp(r*delta) - d)/(u - d)
    qd = 1 - qu
    j = N
    for i in range(j+1):
        VStock[j,i] = S0 * u**i * d ** (N - i)
        VOption[j,i] = max(K - VStock[j,i], 0)
    for j in range(N-1,-1,-1):
        for i in range(j,-1,-1):
            VOption[j,i] = math.exp(-r * delta) * (qu * VOption[j+1,i+1] +
                   qd * VOption[j+1,i])

    return VOption[0,0]


for N in range(50,501):
    P1.append(CCR(S0,K,r,div,sigma,T,N))

plt.plot(np.arange(50,501), P1-P)
plt.show()


# c.
# R&B

P2 = list()

def RB(S0,K,r,div,sigma,T,N):
    delta = T/N
    u = math.exp((r-div-0.5*sigma**2)*delta+sigma*math.sqrt(delta))
    d = math.exp((r-div-0.5*sigma**2)*delta-sigma*math.sqrt(delta))
    qu = (math.exp(r*delta) - d)/(u - d)
    qd = 1 - qu
    VStock = np.zeros((601,601))
    VOption = np.zeros((601,601))
    j = N
    for i in range(j+1):
        VStock[j,i] = S0 * u**i * d ** (N - i)
        VOption[j,i] = max(K - VStock[j,i], 0)
    for j in range(N-1,-1,-1):
        for i in range(j,-1,-1):
            VOption[j,i] = math.exp(-r * delta) * (qu * VOption[j+1,i+1] +
                   qd * VOption[j+1,i])

    return VOption[0,0]


for N in range(50,501):
    P2.append(RB(S0,K,r,div,sigma,T,N))

plt.plot(np.arange(50,501), P2-P)
plt.show()


# d.
# L&R

P3 = list()

def LR(S0,K,r,div,sigma,T,N):
    delta = T/N
    d1 = 1 / (math.sqrt(T)) * (math.log(S0/K) + ((r - div) + sigma**2 / 2) * T)
    d2 = d1 - sigma * math.sqrt(T)
    k = 1 if d2 > 0 else -1
    l = 1 if d1 > 0 else -1
    q = 1/2 + k * math.sqrt(1/4-1/4*math.exp(-(d2/(N+1/3))**2*(N+1/6)))
    q_star = 1/2 + l * math.sqrt(1/4-1/4*math.exp(-(d1/(N+1/3))**2*(N+1/6)))
    u = math.exp((r-div)*delta)*q_star/q
    d = (math.exp((r-div)*delta)-q*u)/(1-q)
    qu = (math.exp(r*delta) - d)/(u - d)
    qd = 1 - qu
    VStock = np.zeros((601,601))
    VOption = np.zeros((601,601))
    j = N
    for i in range(j+1):
        VStock[j,i] = S0 * u**i * d ** (N - i)
        VOption[j,i] = max(K - VStock[j,i], 0)
    for j in range(N-1,-1,-1):
        for i in range(j,-1,-1):
            VOption[j,i] = math.exp(-r * delta) * (qu * VOption[j+1,i+1] +
                   qd * VOption[j+1,i])

    return VOption[0,0]

for N in range(50,501):
    P3.append(LR(S0,K,r,div,sigma,T,N))

plt.plot(np.arange(50,501), P3-P)
plt.show()


# e.
N = np.array([25, 50, 100, 150, 200, 250])

P4 = np.array([])
P5 = np.array([])

for n in N:
    P4 = np.append(P4,CCR(S0,K,r,div,sigma,T,n))
    P5 = np.append(P5,CCR(S0,K,r,div,sigma,T,2*n))


plt.plot(N,P4-P,label="simple lattic")
plt.plot(N,(P4*N-P5*2*N)/(-N)-P, label="extapolating")
plt.show()


N1 = np.array([51, 101, 151, 201, 251])

P6 = np.array([])
P7 = np.array([])

for n in N1:
    P6 = np.append(P6,LR(S0,K,r,div,sigma,T,n))
    P7 = np.append(P7,LR(S0,K,r,div,sigma,T,2*(n-1)-1))

plt.plot(N1,P6-P,N1,P7-P)
plt.show()


# 2.
# a. memory error
#def CCRA(S0,K,r,div,sigma,T,N):
#    delta = T/N
#    u = math.exp(sigma * math.sqrt(delta))
#    d = 1/u
#    qu = (math.exp(r*delta) - d)/(u - d)
#    qd = 1 - qu
#    VStock = np.zeros((5000,5000))
#    VOption = np.zeros((5000,5000))
#    j = N
#    for i in range(j+1):
#        VStock[j,i] = S0 * u**i * d ** (N - i)
#        VOption[j,i] = max(K - VStock[j,i], 0)
#    for j in range(N-1,-1,-1):
#        for i in range(j,-1,-1):
#            VOption[j,i] = max(math.exp(-r * delta) * (qu * VOption[j+1,i+1] +
#                   qd * VOption[j+1,i]),0)
#
#    return VOption[0,0]
#
## initial position
#N = 500
#m = 1
#PA = np.zeros((5000))
#
#PA[0] = CCRA(S0,K,r,div,sigma,T,N)
#N = N + 500
#
#while True:
#    PA[m] = CCRA(S0,K,r,div,sigma,T,N)
#    if abs(PA[m] - PA[m-1]) < 0.0000001:
#        break
#    m = m + 1
#    N = N + 500
    
