package com.atguigu.boot.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/*@Controller @ResponseBody*/
@RestController
public class HelloContreller {
    @RequestMapping("/hello")
    public String hendle01() {
        return "Hello,Spring Boot 2!";
    }
}