public class test_001_String输入多段文字 { //这个是新版本才有的一个特性，在1.8版本中不能实现，会报错，在使用17版本后可以实现。
    public static void main(String[] args){
        String s = """
                   SELECT * FROM
                     users
                   WHERE id > 100
                   ORDER BY name DESC
                   """;
        System.out.println(s);
    }
}
