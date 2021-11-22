public class 面向对象_1 {
    public static void main(String[] args) {
        Animal a = new Animal();
        Animal b = new Animal();//第一个Animal，意识是使用Animall这个class，第二个new就是代表我新建了一个Animal（）这个玩意儿，然后复制给了a
        String c = new String("fine");//我们一般都写成String c = "fine"
        a.eat();
        a.play();
        b.eat();
        System.out.println(c);
        Dog d = new Dog();
        d.Test(1);
        d.Test(2);
        boolean e = a instanceof Dog;//a 是不是 Dog 的子类 或者说 a 是不是 Dog 的对象 中间的instanceof是一个判断一个对象是否为一个类的实例，也可以用来判断是否为接口的实例
        boolean f = a instanceof Animal;//如果是的话就返回ture 否的话返回false
        System.out.println(e);
        System.out.println(f);
    }
}
