public class Bired extends Animal{
    public Bired(){

        setName("bired");//通过setName方法给name赋值
    }
    public String name(){//我们这里是重写name（）方法

        return "I am " + getName();
    }
}
