class Task {
    static boolean f(String inp) {
        int sz = inp.length();
        if (sz != 21)
            return false;
        if (!inp.substring(0, 5).equals("flag{"))
            return false;
        if (inp.charAt(sz-1) != '}')
            return false;
        int ch[] = new int[20];
        for (int i=5; i<20; i++) {
            ch[i-5] = (int)inp.charAt(i);
        }
        int s[] = new int[20];
        for (int i=0; i<1234; i++) {
            for (int k=0; k<14; k++) {
                s[k] = ch[k+1];
            }
            int res = s[0]&s[1];
            res = (res+s[3])%256;
            res ^= (s[5]|s[7]);
            res = (res+s[10]+s[11])%256;
            int tmp = res^ch[0];
            for (int k=0; k<14; k++) {
                ch[k] = ch[k+1];
            }
            ch[14] = tmp;
        }
        int res[] = new int[20];
        res[0] = 187;
        res[1] = 169;
        res[2] = 20;
        res[3] = 23;
        res[4] = 100;
        res[5] = 94;
        res[6] = 107;
        res[7] = 117;
        res[8] = 131;
        res[9] = 108;
        res[10] = 239;
        res[11] = 63;
        res[12] = 106;
        res[13] = 112;
        res[14] = 155;
        for (int i=0; i<15; i++) {
            if (ch[i] != res[i])
                return false;
        }
        return true;
    }
    public static void main(String[] args) {
        System.out.print("> ");
        String inp = System.console().readLine();
        if (f(inp))
            System.out.println("ok!");
    }
}
