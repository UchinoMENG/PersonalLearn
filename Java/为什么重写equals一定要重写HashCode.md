# 为什么重写equals一定要重写HashCode

1. 其实这个问题我之前好早（大二上学期的时候看核心技术卷一）之前就查了，然而之前好像并没有搞懂，似是而非的就过去了。今天这个问题又出现了，然后我自己想了想，Emmmmm......我不知道，哈哈哈（果然过去的没搞懂，现在一定不懂，今天打算弄懂一些）。

2. 首先equals方法是超类中Object中一个方法

   看一下源码理解一下,并摘录了一下部分解释

   ```java
    /* Note that it is generally necessary to override the {@code hashCode}
        * method whenever this method is overridden, so as to maintain the
        * general contract for the {@code hashCode} method, which states
        * that equal objects must have equal hash codes
        */
   public boolean equals(Object obj) {
           return (this == obj);
       }
   ```

   在官网的解释中，只是说了，必须维持相等的对象必须具有相同的hash codes，至于为什么，在object.equals()方法的解释中我并没有找到（我只看了这个方法，其他的没有看）。唉就假设没有吧，反正我没找到。

   ==号在Java中意味着地址是否相同，意思就是Object的equals比较的是二者在内存中的内存地址是否相同。

3. 重点来了：为什么重写equals一定要重写hashCode方法呢？

   原因是一些需要用到hashcode做比较的一些类，比如HashMap这个类。

   首先我知道HashMap这个类是根据Hash值来决定是否放进桶里的，然后再根据key是否相等来判断是应该覆盖还是创建新的节点（小于8是在链表上创建节点，大于8则在红黑树上创建节点）。

   下面是我在网上摘的一份对put方法的解释（由于自身能力有限，还不足以有能够观看源码的能力）

   [链接为](https://blog.csdn.net/yjp198713/article/details/78971566)

   ```java
    final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
                      boolean evict) {
           Node<K,V>[] tab; Node<K,V> p; int n, i;
           // 步骤①：tab为空则创建数组
           if ((tab = table) == null || (n = tab.length) == 0)
               n = (tab = resize()).length;
           // 步骤②：计算index，并对null做处理 ,(n - 1) & hash 计算数组下标,相关于取模操作但是更快
           //如果tab[i]位置为空,直接new一个node放到该坐标处
           if ((p = tab[i = (n - 1) & hash]) == null)
               tab[i] = newNode(hash, key, value, null);
           //tab[i]处有值,使用拉链法处理冲突数据
           else {
               Node<K,V> e; K k;
                // 步骤③：节点key存在，直接覆盖value
               if (p.hash == hash &&
                   ((k = p.key) == key || (key != null && key.equals(k))))
                   e = p;
                // 步骤④：判断该链表是否为红黑树,如何是,添加红黑树节点
               else if (p instanceof TreeNode)
                   e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
                // 步骤⑤：该链为链表
               else {
                   for (int binCount = 0; ; ++binCount) {
                       if ((e = p.next) == null) {
                           p.next = newNode(hash, key, value, null);
                           //链表长度大于8转换为红黑树进行处理
                           if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                               treeifyBin(tab, hash);
                           break;
                       }
                       // key已经存在直接覆盖value
                       if (e.hash == hash &&
                           ((k = e.key) == key || (key != null && key.equals(k))))
                           break;
                       p = e;
                   }
               }
               if (e != null) { // existing mapping for key
                   V oldValue = e.value;
                   if (!onlyIfAbsent || oldValue == null)
                       e.value = value;
                   afterNodeAccess(e);
                   return oldValue;
               }
           }
           ++modCount;
           // 步骤⑥：超过最大容量 就扩容
           if (++size > threshold)
               resize();
           afterNodeInsertion(evict);
           return null;
       }
   ```

   这样就能够明白许多了。

4. 下面我通过一个例子来验证我上边的解释（假设需求是相同的属性值应该在Map中仅存在一个）

   1. 不重写hashcode()方法

   ```java
   
   
   
   import sun.util.resources.cldr.zh.CalendarData_zh_Hans_HK;
   
   import java.util.HashMap;
   import java.util.Objects;
   import java.util.Scanner;
   
   public class Test {
       private int num ;
       public Test(int num){
           this.num = num;
       }
   
       @Override
       public boolean equals(Object o) {
           if (this == o) return true;
           if (o == null || getClass() != o.getClass()) return false;
           Test test = (Test) o;
           return num == test.num;
       }
   
   //    @Override
   //    public int hashCode() {
   //        return Objects.hash(num);
   //    }
   
       public static void main(String[] args) {
           HashMap<Test,Integer> t = new HashMap<>();
           Test t1 = new Test(1);
           Test t2 = new Test(1);
           System.out.println(t1.hashCode()==t2.hashCode());
           t.put(t1,1);
           t.put(t2,2);
           System.out.println(t.get(t1));
           System.out.println(t.get(t2));
           System.out.println(t.size());
       }
   }
   
   ```

   输出结果为

   >false
   >1
   >2
   >2

   由于t1和t2虽然是含有相同的属性值，但是地址值是完全不同的，因为他们两个是完全不同的对象。如果需求是属性值相同的话，应该在Map中存在一个，那么不重写hashcode是不行的。

   2. 不重写equals方法

      ```java
      import java.util.HashMap;
      import java.util.Objects;
      import java.util.Scanner;
      
      public class Test {
          private int num ;
          public Test(int num){
              this.num = num;
          }
      
      //    @Override
      //    public boolean equals(Object o) {
      ////        if (this == o) return true;
      ////        if (o == null || getClass() != o.getClass()) return false;
      ////        Test test = (Test) o;
      ////        return num == test.num;
      //        return false;
      //    }
      
          @Override
          public int hashCode() {
              return Objects.hash(num);
          }
      
          public static void main(String[] args) {
              HashMap<Test,Integer> t = new HashMap<>();
              Test t1 = new Test(1);
              Test t2 = new Test(1);
              System.out.println(t1.hashCode()==t2.hashCode());
              t.put(t1,1);
              t.put(t2,2);
              System.out.println(t.get(t1));
              System.out.println(t.get(t2));
              System.out.println(t.size());
          }
      }
      
      ```

      >结果为：
      >
      >true
      >
      >1
      >
      >2
      >
      >2

      3. 两个全都重写

      ```java
      import java.util.HashMap;
      import java.util.Objects;
      import java.util.Scanner;
      
      public class Test {
          private int num ;
          public Test(int num){
              this.num = num;
          }
      
          @Override
          public boolean equals(Object o) {
              if (this == o) return true;
              if (o == null || getClass() != o.getClass()) return false;
              Test test = (Test) o;
              return num == test.num;
          }
      
          @Override
          public int hashCode() {
              return Objects.hash(num);
          }
      
          public static void main(String[] args) {
              HashMap<Test,Integer> t = new HashMap<>();
              Test t1 = new Test(1);
              Test t2 = new Test(1);
              System.out.println(t1.hashCode()==t2.hashCode());
              t.put(t1,1);
              t.put(t2,2);
              System.out.println(t.get(t1));
              System.out.println(t.get(t2));
              System.out.println(t.size());
          }
      }
      
      ```

      >结果为：
      >
      >true
      >
      >2
      >
      >2
      >
      >1

      这样需求就达到了。

      ## 总结

      如果需求是属性值相同的对象在类Map中的应该只存在一个，那么就需要重写Hashcode和equals方法。

      

      

      