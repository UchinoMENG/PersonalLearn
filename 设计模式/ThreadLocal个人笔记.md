## ThreadLocal个人笔记

#### 1.什么是ThreadLocal?

>ThreadLocal这个类能使线程中的某个值与保存值的对象关联起来。ThreadLocal提供了get和set等访问接口或方法，这些方法为每个使用该变量的线程都存有一份独立的副本，因此get总是返回由当前执行线程在调用set时设置的最新值。

#### 2.一个简单的实例

```java
public class ThreadLocalTest {
    private  static ThreadLocal<Integer> t1 = new ThreadLocal<>();
    public static void main(String[] args)throws Exception {
        t1.set(20);
        System.out.println(Thread.currentThread().getName()+": "+t1.get());
        Thread t2 = new Thread(()->{
            System.out.println(Thread.currentThread().getName()+": "+t1.get());
            t1.set(100);
            System.out.println(Thread.currentThread().getName()+": "+t1.get());
        });
        t2.start();
        t2.join();

        System.out.println(Thread.currentThread().getName()+": "+t1.get());
    }
}
```

```
main:20
Thread-0:null
Thread-0:100
main:20
```

从这个结果上就可以看出ThreadLocal为每个使用该变量的线程都存有一份独立的副本，每次获取都是返回当前线程的设置的最新值。

#### 3.看源码

![image-20200409204611521](https://i.loli.net/2020/06/22/KiU1mMhbaDjHITv.png)

> 大概意思就是这个类是一个线程局部变量。在每一个线程中，这些变量不同于其他线程的，每一个线程获取他们自己的，独立变量的副本

###### 1.set方法

```java
public void set(T value) {
    Thread t = Thread.currentThread();	//获取当前的线程
    ThreadLocalMap map = getMap(t);		//传进去当前的线程，获取一个ThreadLocalMap
    if (map != null)
        map.set(this, value);			//将ThreadLocal与value绑定
    else
        createMap(t, value);			//为空，则创建一个ThreadLocalMap
}
```

下面是getMap()方法的源码:

```java
/**
     * Get the map associated with a ThreadLocal. Overridden in
     * InheritableThreadLocal.
     *
     * @param  t the current thread
     * @return the map
     */
    ThreadLocalMap getMap(Thread t) {		//t代表的是当前线程
        return t.threadLocals;
    }
```

在看一下t.threadLocaks返回的是什么,代码如下

```java
   /* ThreadLocal values pertaining to this thread. This map is maintained
     * by the ThreadLocal class. */
    ThreadLocal.ThreadLocalMap threadLocals = null;
```

这代表的是当前线程的一个ThreadLocalMap,那么ThreadLocalMap又是什么.

```java

    static class ThreadLocalMap {

        /**
         * The entries in this hash map extend WeakReference, using
         * its main ref field as the key (which is always a
         * ThreadLocal object).  Note that null keys (i.e. entry.get()
         * == null) mean that the key is no longer referenced, so the
         * entry can be expunged from table.  Such entries are referred to
         * as "stale entries" in the code that follows.
         */
        static class Entry extends WeakReference<ThreadLocal<?>> {
            /** The value associated with this ThreadLocal. */
            Object value;

            Entry(ThreadLocal<?> k, Object v) {
                super(k);
                value = v;
            }
        }
```

ThreadLocalMap是ThreadLocal中的一个内部类，这里面的Entry继承了WeakRefence虚引用，并且使用的是ThreadLocal作为键。

再看一下createMap()方法。

```java
 void createMap(Thread t, T firstValue) {
        t.threadLocals = new ThreadLocalMap(this, firstValue);
    }
```

根据当前线程初始化当前线程的ThreadLocalMap

构造ThreadLocalMap方法为:

```java
ThreadLocalMap(ThreadLocal<?> firstKey, Object firstValue) {
            table = new Entry[INITIAL_CAPACITY];
            int i = firstKey.threadLocalHashCode & (INITIAL_CAPACITY - 1);
            table[i] = new Entry(firstKey, firstValue);
            size = 1;
            setThreshold(INITIAL_CAPACITY);
        }
```

这里又new 了一个Entry来进行设置键值对。

仔细阅读源码之后，就会看懂这个图了。

原理图就是这样

![ThreadLocal原理](https://i.loli.net/2020/06/22/yWUmp6MKaBje2ot.jpg)

2.get方法

```java
public T get() {
        Thread t = Thread.currentThread();
        ThreadLocalMap map = getMap(t);
        if (map != null) {
            ThreadLocalMap.Entry e = map.getEntry(this);
            if (e != null) {
                @SuppressWarnings("unchecked")
                T result = (T)e.value;
                return result;
            }
        }
        return setInitialValue();
    }
```

get方法其实就是从map中取当前线程中的threadLocal中存的值。（因为一个线程中可以有多个ThreadLocal，并且Entry的键值为ThreadLocal）。

#### 4关于内存泄露的问题

之前我首先是看马士兵老师视频才知道的这方面的知识。这里的ThreadLocal是弱引用指向的，那什么是弱引用的。根据《深入浅出Java虚拟机》，

> 弱引用：用来描述非必须对象的，被弱引用关联的对象只能生存到下一次垃圾收集发生之前。当垃圾收集器工作时，无论当前内存是否足够，都会回收掉只被弱引用关联的对象。

那内存泄露指的是什么呢？

>是指当ThreadLocal没有被指向时，发生了GC,会导致key为null（ThreadLocal被回收，ThreadLocal关联的线程共享变量还存在）。

解决方法：

> 可以通过threadLocal.remove方法来清除线程共享变量即可