// g++ -O3 solve.cpp
#include<iostream>
#include<fstream>
#include<random>
#include<unordered_map>
#include<stdint.h>
#include<stdio.h>

using namespace std;

uint64_t pt[16777777];
uint64_t ct[16777777];
uint64_t pti[16777777];
uint64_t P = 247359019496198933UL;
uint64_t C = 223805275076627807UL;
uint64_t M = 1UL<<60;

uint64_t modinv(uint64_t u, uint64_t v) {
    uint64_t inv, u1, u3, v1, v3, t1, t3, q;
    int iter;
    /* Step X1. Initialise */
    u1 = 1;
    u3 = u;
    v1 = 0;
    v3 = v;
    /* Remember odd/even iterations */
    iter = 1;
    /* Step X2. Loop while v3 != 0 */
    while (v3 != 0)
    {
        /* Step X3. Divide and "Subtract" */
        q = u3 / v3;
        t3 = u3 % v3;
        t1 = u1 + q * v1;
        /* Swap */
        u1 = v1; v1 = t1; u3 = v3; v3 = t3;
        iter = -iter;
    }
    /* Make sure u3 = gcd(u,v) == 1 */
    if (u3 != 1)
        return 0;   /* Error: No inverse exists */
    /* Ensure a positive result */
    if (iter < 0)
        inv = v - u1;
    else
        inv = u1;
    return inv;
}

uint64_t mulmod(uint64_t a, uint64_t b, uint64_t mod) {
    __uint128_t ax = a;
    __uint128_t bx = b;
    ax *= bx;
    return ax%mod;
}

static std::random_device rd; 
static std::mt19937 rng(rd());
static std::uniform_int_distribution<uint64_t> uid(0,std::numeric_limits<uint64_t>::max());

uint64_t rndd() {
    return uid(rng)%P;
}

unordered_map<uint64_t, uint64_t> stat;
unordered_map<uint64_t, uint64_t>::iterator it;
uint64_t K0, K1;

int main() {
    ifstream fin("res");
    for (long i=0; i<16777216; i++) {
        fin>>pt[i]>>ct[i];
        pti[i] = modinv(pt[i], P);
    }
    fin.close();
    puts("go");
    int iter = 0;
    uint64_t d;
    bool found = false;
    while (!found) {
        cout<<"iter: "<<iter<<endl;
        iter++;
        d = rndd();
        //d = 190570034347447822L;
        stat.clear();
        for (long i=0; i<16777216; i++) {
            uint64_t f = mulmod(mulmod(d, pti[i], P), C, M);
            uint64_t val = mulmod(ct[i], f, P);
            it = stat.find(val);
            if (it != stat.end()) {
                uint64_t pt0 = it->second;
                cout<<pt0<<" "<<pt[i]<<" "<<d<<endl;
                uint64_t pt0i = modinv(pt0, P);
                K0 = mulmod(mulmod(d, pt0i, P), pti[i], P);
                uint64_t v1 = mulmod(K0, pt[i], P);
                uint64_t v2 = mulmod(v1, C, M);
                K1 = mulmod(ct[i], modinv(v2, P), P);
                cout<<K0<<" "<<K1<<endl;
                found = true;
            }
            stat[val] = pt[i];
        }
    }
    return 0;
}
