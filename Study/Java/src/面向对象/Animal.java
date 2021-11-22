public class Animal {
    //继承
    //编写两个方法，分别是eat和play方法
    void eat() {

        System.out.println("animal : eat");
    }
    void play(){

        System.out.println("animal : play");
    }

    //多态 多态的定义则是使用一个父类实现多个不同类型的动作
    private String name;//private 设置私有的 String 的 变量name 私有属性是无法通过除了get和set以外方法进行调用。
    //get的意思就是获取name 所以这个getName（）方法就是用来获取name的
    public String getName(){

        return name;
    }
    //set的意思就是设置name，所以这个setName（）方法就是用来设置name的
    public void setName(String name ){

        this.name=name;
    }
    //这里我们设置了一个String类型的name方法，返回的值是"animal is " + getName()，这里的getName（）的意思就是通过getName这个方法从Animal这个类里面调用私有属性name。
    public String name(){

        return "animal is " + getName();
    }

}