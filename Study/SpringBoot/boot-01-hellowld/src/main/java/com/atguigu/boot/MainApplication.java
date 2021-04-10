package com.atguigu.boot;

import ch.qos.logback.core.db.DBHelper;
import com.atguigu.boot.bean.Pet;
import com.atguigu.boot.bean.User;
import com.atguigu.boot.config.MyConfig;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.SpringBootConfiguration;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.ComponentScan;

import java.time.Period;

/**
 * 主程序类
 * @SpringBootApplication:这是一个SpringBoot应用
 */

@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan("com.atguigu.boot")
public class MainApplication {
    public static void main(String[] args){
        //1.返回我们IOC容器
        ConfigurableApplicationContext run = SpringApplication.run(MainApplication.class,args);

        //2.查看容器里面的组件
        String[] names = run.getBeanDefinitionNames();
        for (String name : names) {
            System.out.println(name);
        }

        //3.从容器中获取组件

        Pet tom01 = run.getBean("tom", Pet.class);
        Pet tom02 = run.getBean("tom", Pet.class);
        System.out.println("组件:" + (tom01 == tom02));

        MyConfig bean = run.getBean(MyConfig.class);
        System.out.println(bean);

        //如果@Configurotion(proxyBeanMethods = true)代理对象调用方法。SpringBoot总会检查这个组件是否在容器中有，如果有就不会新建，包吃组件单实例。
        User user = bean.user01();
        User user02 = bean.user01();
        System.out.println(user == user02);

        User user01 = run.getBean("user01",User.class);
        Pet tom = run.getBean("tom",Pet.class);

        System.out.println ("用户的宠物：" + (user01.getPet() == tom));

        String[] beanNamesForType = run.getBeanNamesForType(User.class);
        System.out.println("=========");
        for (String s : beanNamesForType){
            System.out.println(s);
        }

        DBHelper bean1 = run.getBean(DBHelper.class);
        System.out.println(bean1);

    }
}
