public class test_006_抛出异常 {
    public static void main(String[] args) {
        try {
            process1();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    static void process1() {
        try {
            process2();
        } catch (NullPointerException e) { //把原始异常一同传入IllegalArgumentException
            throw new IllegalArgumentException(e);
        }
    }
    /**
     * java.lang.IllegalArgumentException: java.lang.NullPointerException
     * 	at test_006_抛出异常.process1(test_006_抛出异常.java:14)
     * 	at test_006_抛出异常.main(test_006_抛出异常.java:4)
     * Caused by: java.lang.NullPointerException
     * 	at test_006_抛出异常.process2(test_006_抛出异常.java:32)
     * 	at test_006_抛出异常.process1(test_006_抛出异常.java:12)
     * 	... 1 more
     * */

//    static void process1() {
//        try {
//            process2();
//        } catch (NullPointerException e) { //拦截了原始异常NullPointerException
//            throw new IllegalArgumentException();
//        }
//    }
    /**
     *java.lang.IllegalArgumentException
     * 	at test_006_抛出异常.process1(test_006_抛出异常.java:22)
     * 	at test_006_抛出异常.main(test_006_抛出异常.java:4)
     * */

    static void process2() { //抛出直接throw 抛出原始异常NullPointerException
        throw new NullPointerException();
    }
}
