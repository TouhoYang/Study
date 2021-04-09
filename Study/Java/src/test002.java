public class test002 {
    public static void main(String[] args) {
        Cat a = new Cat();//新建了一个cat的实例化a
        System.out.println(a.name());//这里的name方法是Animal里面的方法
        Bired b = new Bired();//新建了一个bired实例化b
        System.out.println(b.name());//因为我们在bired类里面修改了name方法，所以优先使用的是我们bired类里面的方法
    }
}
