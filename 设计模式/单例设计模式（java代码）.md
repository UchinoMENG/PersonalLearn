# 单例设计模式（java代码）

#### 1. 什么是单例设计模式

单例设计模式是Java中最简单的设计模式之一。这种类型的设计模式属于创建型模式，他提供了一种创建对象的最佳方式。这种模式涉及到一个单一的类，该类负责创建自己的对象，同时确保只有单个对象被创建。这个类提供了一种访问其唯一的对象的方式，可以直接访问，不需要实例化该类的对象。

注意：

* 单例类只能有一个实例
* 单例类必须自己创建自己的唯一实例
* 单例类必须给所有的其他对象提供这一实例

#### 2.单例设计模式的用途

单例模式主要是为了避免因为创建了多个实例造成资源的浪费，且多个实例由于多次调用容易导致结果出现错误，而单例可以保证实例的唯一性。

#### 3.单例设计模式的写法

###### 3.1饿汉式写法

```java
public class Singleton {
	private static Singleton instance=new Singleton();
	private Singleton(){
	
	};
	public static Singleton getInstance(){
		return instance;
	}
}
```

分析：这种写法不管在单线程还是在多线程的环境下，都不会出现错误。

优点：写法简单，在类加载的时候就已经完成了初始化

缺点：容易造成内存的浪费。在类加载的时候就已经初始化完成了。

###### 3.2懒汉式写法（方法上加synchronized）

```java
public class Singleton {
 
	private static Singleton instance=null;
	private Singleton() {};
	public static synchronized Singleton getInstance(){	
		if(instance==null){
			instance=new Singleton();
		}
		return instance;
	}
}
```

分析：这种写法不管在单线程还是在多线程的环境下，都不会出现错误。

缺点：每一次访问都需要同步，会导致效率实在太低了。

###### 3.3DCL写法

```java
public class Singleton {
	private volatile static Singleton instance=null;
	private Singleton() {};
	public static Singleton getInstance(){
		 if (instance == null) {  
	          synchronized (Singleton.class) {  
	              if (instance == null) {  
	            	  instance = new Singleton();  
	              }  
	          }  
	      }  
	      return instance;  
	}
}
```

分析：这种写法不管在单线程还是在多线程的环境下，都不会出现错误。

这里 Singleton一定需要加volatile关键字，原因是防止指令重排以及内容可见性。

1. 首先解释一下创建对象初始化的过程：

   >创建一个类Test，里面有一个成员变量num
   >
   >```
   >public class Test{
   >	int num = 9;
   >}
   >```
   >
   >Test tt = new Test();
   >
   >对象tt创建过程：
   >
   >0. 分配对象的内存空间
   >
   >![image-20200408164217576](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20200408164217576.png)
   >
   >1. 初始化对象
   >
   >   ![image-20200408164241754](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20200408164241754.png)
   >
   >2. 将变量指向内存空间。
   >
   >   ![image-20200408164311826](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20200408164311826.png)
   >
   >

2. 假设不加上volatile

   >由于jvm存在指令重排的优化，存在顺序1和2的颠倒，即先指向内存空间，然后再初始化。
   >
   >0. 分配对象的内存空间
   >
   >![image-20200408164217576](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20200408164217576.png)
   >
   >1. 变量指向内存
   >
   >   ![image-20200408165221165](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20200408165221165.png)
   >
   >2. 对象初始化
   >
   >   ![image-20200408165317056](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20200408165317056.png)
   >
   >   在分析代码：
   >
   >   ```java
   >   public class Singleton {
   >   	private volatile static Singleton instance=null;
   >       int num = 0;//这里加上一个变量
   >   	private Singleton() {};
   >   	public static Singleton getInstance(){
   >   		 if (instance == null) {  
   >   	          synchronized (Singleton.class) {  
   >   	              if (instance == null) {  
   >   	            	  instance = new Singleton();  
   >   	              }  
   >   	          }  
   >   	      }  
   >   	      return instance;  
   >   	}
   >   }
   >   ```
   >
   >   假设线程A，线程B同时访问到getInstance方法，线程A拿到了锁，A一路进行到new对象那，
   >
   >   而创建对象的时候发生了指令重排，进行到了步骤1上，不巧的是B进行到第一个if那，由于instance已经申请到了地址（不为空），所以B直接返回了未初始化的对象（num=0）,导致了错误。（DCL失效）。

3. 加上volatile

   >会防止指令重排，并且可以保证可见性（由于每一个线程都会有自己的一个工作内存，volatile可以立即将自己工作内存的变量写入到主内存中，并且会让其他工作内存中的此变量置为无效），可以很好的防止上述现象的发生。

###### 3.4静态内部类单例模式

1. ```java
   public class Singleton { 
       private Singleton(){
       }
         public static Singleton getInstance(){  
           return SingletonHolder.sInstance;  
       }  
       private static class SingletonHolder {  
           private static final Singleton sInstance = new Singleton();  
       }  
   } 
   
   ```

   分析：写法简单，并且兼顾了懒加载的方式，同时也在单线程和多线程下安全。



#### 如有不对的地方，请指出，我会改正。

### 参考：

<https://blog.csdn.net/itachi85/article/details/50510124>

<https://www.runoob.com/design-pattern/singleton-pattern.html>