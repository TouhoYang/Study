public class test_005_异常传播 {
    public static void main(String[] args) {
        try {
            process1();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    static void process1() {
        process2();
    }

    static void process2() {
        Integer.parseInt(null); // 会抛出NumberFormatException
    }
}
/***
 * java.lang.NumberFormatException: Cannot parse null string
 * 	at java.base/java.lang.Integer.parseInt(Integer.java:630)
 * 	at java.base/java.lang.Integer.parseInt(Integer.java:786)
 * 	at test_005_异常传播.process2(test_005_异常传播.java:15)
 * 	at test_005_异常传播.process1(test_005_异常传播.java:11)
 * 	at test_005_异常传播.main(test_005_异常传播.java:4)
 *
 * 	printStackTrace()对于调试错误非常有用，上述信息表示：NumberFormatException是在java.lang.Integer.parseInt方法中被抛出的，从下往上看，调用层次依次是：
 *
 * 1. main()调用process1()；
 * 2. process1()调用process2()；
 * 3. process2()调用Integer.parseInt(String)；
 * 4. Integer.parseInt(String)调用Integer.parseInt(String, int)
 * ***/
