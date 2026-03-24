import math

def q():
    return 2.302585092994046/400.0

def gRD(RD):
    return 1/math.sqrt(1+(3*(q()**2))*((RD**2) / (math.pi**2)))

def Es(gRDj,r,rj):
    return 1/(1+(10**(0-(gRDj*(r-rj)/400))))