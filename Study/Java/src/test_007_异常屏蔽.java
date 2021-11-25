public class test_007_异常屏蔽 {
//    public static void main(String[] args) {
//        try {
//            Integer.parseInt("abc");
//        } catch (Exception e) {
//            System.out.println("catched");
//            throw new RuntimeException(e);
//        } finally {
//            System.out.println("finally");
//            throw new IllegalArgumentException();
//        }
//    }

    /**
     * catched
     * finally
     * Exception in thread "main" java.lang.IllegalArgumentException
     * 	at test_007_异常屏蔽.main(test_007_异常屏蔽.java:10)
     *
     * 	这说明finally抛出异常后，原来在catch中准备抛出的异常就“消失”了，因为只能抛出一个异常。没有被抛出的异常称为“被屏蔽”的异常（Suppressed Exception）。
     *
     * */

    public static void main(String[] args) throws Exception {
        Exception origin = null;
        try {
            System.out.println(Integer.parseInt("abc"));
        } catch (Exception e) {
            origin = e;
            throw e;
        } finally {
            Exception e = new IllegalArgumentException();
            if (origin != null) {
                e.addSuppressed(origin);
            }
            throw e;
        }
    }

    /**
     * Exception in thread "main" java.lang.IllegalArgumentException
     * 	at test_007_异常屏蔽.main(test_007_异常屏蔽.java:32)
     * 	Suppressed: java.lang.NumberFormatException: For input string: "abc"
     * 		at java.base/java.lang.NumberFormatException.forInputString(NumberFormatException.java:67)
     * 		at java.base/java.lang.Integer.parseInt(Integer.java:668)
     * 		at java.base/java.lang.Integer.parseInt(Integer.java:786)
     * 		at test_007_异常屏蔽.main(test_007_异常屏蔽.java:27)
     *
     * 	当catch和finally都抛出了异常时，虽然catch的异常被屏蔽了，但是，finally抛出的异常仍然包含了它
     *
     * 	通过Throwable.getSuppressed()可以获取所有的Suppressed Exception。
     * 绝大多数情况下，在finally中不要抛出异常。因此，我们通常不需要关心Suppressed Exception
     *
     * */

}

