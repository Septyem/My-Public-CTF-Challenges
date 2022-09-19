import random

ops = ["add", "mul", "or", "sdiv"]

codes = ""

cnt = 0

expr = "GPR:$r1"
var = "%i"
curops = ops[:]
for i in range(4):
    op = random.sample(curops,1)[0]
    curops.remove(op)
    num = random.randint(0,100)
    codes += "%a{} = {} i64 {}, {}\n".format(cnt, op, var, num)
    expr = "({} {}, {})".format(op, expr, num)
    var = "%a{}".format(cnt)
    cnt += 1
exprs = expr[:]
vartot = var[:]


for j in range(1):
    expr = "GPR:$r{}".format(j+2)
    var = "%i"
    curops = ops[:]
    for i in range(3):
        op = random.sample(curops,1)[0]
        curops.remove(op)
        num = random.randint(0,100)
        codes += "%a{} = {} i64 {}, {}\n".format(cnt, op, var, num)
        expr = "({} {}, {})".format(op, expr, num)
        var = "%a{}".format(cnt)
        cnt += 1

    varnew = "%a{}".format(cnt)
    cnt += 1
    codes += "{} = add i64 {}, {}".format(varnew, vartot, var)
    exprs = "(add {}, {})".format(exprs, expr)
    vartot = varnew[:]

print(codes)
print(exprs)
