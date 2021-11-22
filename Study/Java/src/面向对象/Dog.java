public class Dog extends Animal {
    void eat() {//自身的dog。eat方法

        System.out.println("dog : eat");
    }

    void play() {

        System.out.println("dog : play");
    }

    void Test(int a) {//定义自身的eatTest方法，后面有传入一个int a 参数
        if (a == 1) {//对参数进行判断
            this.eat();//调用自身的eat方法：输出dog : eat  this就是代表自身的方法或者自身定义的数据
            this.play();
        } else {
            super.eat();//调用父类的方法输出：animal : eat
            super.play();
        }
    }
}
