# Java中的值传递

1. 原来以为自己足够明白了Java的值传递，哈哈，今天自己给自己整迷糊了，今天就想写个代码来记录一下哈。

代码

```java
class Student{
    public String name;
    public Student(String name){
        this.name = name;
    }

    @Override
    public String toString() {
        return "Student{" +
                "name='" + name + '\'' +
                '}';
    }
}
public class JavaValuePaseTest {
    public static void main(String[] args) {
        int a= 10;
        int b = 20;
        exchange(a,b);
        System.out.println("a = "+a+", b = "+b);
        Student a1 = new Student("张三");
        Student a2 = new Student("李四");
        exchange1(a1,a2);
        System.out.println(a1);
        System.out.println(a2);
        exchange2(a1,a2);
        System.out.println(a1);
        System.out.println(a2);

    }
    public static void exchange(int a,int b){
        int c = a;
        a = b;
        b = c;
    }
    public static void exchange1(Student a1,Student a2){
        Student c = new Student("");
        c = a1;
        a1 = a2;
        a2 = c;
    }
    public static void exchange2(Student a1,Student a2){
        Student c = new Student("");
        c.name = a1.name;
        a1.name = a2.name;
        a2.name = c.name;
    }
}

```

1. 输出 10 20
2. 输出 张三 李四
3. 输出 李四 张三

分析：

我原来傻傻的竟然以为第二个输出为李四 张三 哈哈，现在终于又明白了，在方法栈中改变了指向，但是没有改变内容，方法栈结束之后，栈中的变量全都消失了。简单的说就是在main方法中的指针并没有改变了指向。但是改变了内容，就变成了另外一种说法了。