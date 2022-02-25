import java.util.Arrays;

public class test_003_数组排序 {
    public static void main(String... args){
        int[] ns = { 28, 12, 89, 73, 65, 18, 96, 50, 8, 36 };
        int[] s = ns;
        // 排序前:
        System.out.println("排序前:"+Arrays.toString(ns));

        //排序:
        for (int i = 0 ; i < ns.length -1 ; i++){
            for (int x = 0 ; x < ns.length -1 -i ; x++){
                if (ns[x] > ns[x+1]){
                    int tmp = ns[x];
                    ns[x] = ns[x+1];
                    ns[x+1] = tmp;
                }
            }
        }
        //排序后:
        System.out.println("排序后:"+Arrays.toString(ns));

        //使用Java内部sort方法进行排序
        Arrays.sort(s);
        System.out.println("sort排序:"+Arrays.toString(s));
    }
}
