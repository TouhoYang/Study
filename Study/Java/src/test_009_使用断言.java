public class test_009_使用断言 {
    public static void main(String[] args){
        int x = 1;
        assert x < 0 : "错误,x不小于0";
        System.out.println(x);
    }
}

/**
 * 使用assert的时候,要在idea的Run-Edit Configurations-需要断言的Java文件-Modify options-Add VM options-添加 -ea ,然后保存就可以了.
 * */