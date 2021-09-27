class Task {
    static boolean f(String inp) {
        /* some code here */
    }
    public static void main(String[] args) {
        System.out.print("> ");
        String inp = System.console().readLine();
        if (f(inp))
            System.out.println("ok!");
    }
}

