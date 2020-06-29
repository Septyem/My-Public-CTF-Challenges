#!/usr/bin/python3
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

class hash_func(nn.Module):
    def __init__(self, input_size=64):
        super(hash_func, self).__init__()
        self.l1 = nn.Conv1d(1, 1, 5, 1, 2)
        self.l2 = nn.Conv1d(1, 1, 3, 1, 1)
        self.l3 = nn.Linear(64, 32)

    def forward(self, input):
        x = F.leaky_relu(self.l1(input), 0.2)
        x = F.leaky_relu(self.l2(x), 0.2)
        x = F.tanh(self.l3(x.view(-1, 64)))
        return x

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

H = hash_func().to(device)
H.load_state_dict(torch.load("./param.pkl",  map_location=device))
H.eval()

def hash(m):
    m = m.ljust(64, b'\x00')
    m = list(map(lambda x:float(x-128)/128, m))
    x = Variable(torch.Tensor(m[:64]).to(device))
    x = x.view(-1, 1, 64)
    res = H(x).tolist()
    #res = bytes(map(lambda x:int(x*128+128), res[0])) # it will always converge to same char :( not used
    bs = map(lambda x:(int(x*32768+32768)//256, int(x*32768+32768)%256), res[0])
    res = bytes([y for x in bs for y in x])
    return res
