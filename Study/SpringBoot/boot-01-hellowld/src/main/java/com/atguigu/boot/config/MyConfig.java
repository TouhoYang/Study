package com.atguigu.boot.config;


import ch.qos.logback.core.db.DBHelper;
import com.atguigu.boot.bean.Pet;
import com.atguigu.boot.bean.User;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

/**
 * 1.配置类里面使用@Bean标注在方法上给容器注册组件，默认也是单实例的
 * 2.配置类本身也是组件
 * 3.proxyBeanMethods:代理bean的方法
 * Full(proxyBeanMethods = true)
 * Lite(proxyBeanMethods = false)轻量级
 * 组建
 *
 * @Import({Pet.class,User.class, DBHelper.class})
 *      给容器中自动创建出这两个类型的组件
 */

@Import({Pet.class,User.class, DBHelper.class})
@Configuration(proxyBeanMethods = true)//告诉SpringBoot这是一个配置类 == 配置文件
public class MyConfig {

    /**
     * 外部无论对配置类中的这个组件注册方法调用多少次，获取的都是之前注册容器中的单实例对象
     */

    @Bean //给容器中添加组件，以方法名作为组件的id，返回类型就是组件类型，返回的值就是组件在容器中的实例。
    public User user01() {
        User zhangsan = new User("张三", 18);
        //user组件依赖了Pet组件
        zhangsan.setPet(tomcatPet());
        return zhangsan;
    }

    @Bean("tom")//把组件名称重命名为tom
    public Pet tomcatPet() {
        return new Pet("tomcat");
    }

}
