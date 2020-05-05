### 自己实现一个CAS（含代码）

1. 概念

   >CAS指令需要有3个操作数，分别是内存位置（V），旧的预期值（A），和新值（B）。CAS指令执行时，当且仅当V符合旧预期值A时，处理器才会用新值B更新V的值，否则他就不执行更新，但是无论是否更新了V的值，都会返回V的旧值，上述的操作是一个原子操作。

2. CAS是一种乐观锁

   > 乐观锁：假设条件一定会成立，他就会不断的去尝试，直到成功为止。

3. 先看一个非锁的代码，多个线程操作一个累加的变量

   ```java
   package com.localhost.深入理解Java虚拟机.example;
   
   import java.util.concurrent.CountDownLatch;
   import java.util.concurrent.TimeUnit;
   
   public class CASDemo {
       //声明一个静态变量
       private static  int count = 0;
       public static void increment()throws Exception{
           TimeUnit.MILLISECONDS.sleep(5);
           count++;
       }
   
       public static void main(String[] args) {
           int ThreadSize = 100;
           int cnt = 10;
           CountDownLatch countDownLatch = new CountDownLatch(ThreadSize);
           long start = System.currentTimeMillis();
           for(int i = 0;i<ThreadSize;i++){
               new Thread(new Runnable() {
                   @Override
                   public void run() {
                       try{
                           for(int i = 0;i<cnt;i++){
                               increment();
                           }
                       }
                       catch (Exception e){
                           e.printStackTrace();
                       }
                       finally {
                           countDownLatch.countDown();
                       }
   
                   }
               }).start();
   
           }
           try{
               //System.out.println("11111111");
               countDownLatch.await();
               //System.out.println("222222222");
           }
           catch (Exception e){
               e.printStackTrace();
           }
           long end = System.currentTimeMillis();
           System.out.println("运行时间为:"+(end-start)+",count = "+count);
       }
   }
   
   ```

   我这显示运行时间为64，count=940,小于1000，这里出现的错误的原因是:count++并不是一个原子操作。

4. 使用CAS实现这个功能

   ```java
   package com.localhost.深入理解Java虚拟机.example;
   
   import java.util.concurrent.CountDownLatch;
   import java.util.concurrent.TimeUnit;
   
   public class CASDemo2 {
       //声明一个静态变量
       private static volatile int count = 0;
       public static  void increment()throws Exception{
           TimeUnit.MILLISECONDS.sleep(5);
           //count++;
           while(!compareAndSwap(getCount(),count+1)){}
       }
       public static synchronized boolean compareAndSwap(int expectValue,int new_value){
           if(getCount()==expectValue){
               count = new_value;
               return true;
           }
           return false;
       }
       public static int getCount(){
           return count;
       }
       public static void main(String[] args) {
           int ThreadSize = 100;
           int cnt = 10;
           CountDownLatch countDownLatch = new CountDownLatch(ThreadSize);
           long start = System.currentTimeMillis();
           for(int i = 0;i<ThreadSize;i++){
               new Thread(new Runnable() {
                   @Override
                   public void run() {
                       try{
                           for(int i = 0;i<cnt;i++){
                               increment();
                           }
                       }
                       catch (Exception e){
                           e.printStackTrace();
                       }
                       finally {
                           countDownLatch.countDown();
                       }
   
                   }
               }).start();
   
           }
           try{
               //System.out.println("11111111");
               countDownLatch.await();
               //System.out.println("222222222");
           }
           catch (Exception e){
               e.printStackTrace();
           }
           long end = System.currentTimeMillis();
           System.out.println("运行时间为:"+(end-start)+",count = "+count);
       }
   }
   
   ```

   我这显示运行时间65，count=1000

