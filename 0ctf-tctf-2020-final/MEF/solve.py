from Crypto.Util.number import inverse

out = 11804007143439251849628349629375460277798651136608332038133488180610375813979
h = [1]
p = 374144419156711147060143317175368453031918731002211
m = 16077898348258654514826613220527141251832530996721392570130087971041029999399
pi = inverse(p-1, m)
num = 0x142857142857142857

h = (pow(p,num+1,m)-1)*pi%m
flagnum = out^h
print hex(flagnum)


