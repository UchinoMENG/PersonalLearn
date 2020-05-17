## Fork/Join框架笔记

##### 什么是Fork/join框架

>Fork/Join框架是Java7提供的一个用于并行执行任务的框架，是一个把大任务分割成若干个小任务，最终汇总成每个小任务结果后得到大结果的框架。

##### 举个栗子

>可以计算1+2+3+...+10000,可以分割成10个子任务，每个子任务分别对1000个数进行求和，最终汇总这10个子任务的结果。Fork/Join的运行流程如图所示：
>
>![image-20200514062521430](E:\Typora\upload\image-20200514062521430.png)
>
>其实看到这个和上面的解释之后，我当时就想这TM的不就是归并思想吗，能把归并思想运用到这里是真的nb，写这个框架的人真的是太厉害了。

##### 工作窃取算法

>是指某个线程从其他队列里窃取任务来执行。
>
>把一个比较大的任务分割成许多的若不干扰的，互不依赖的子任务，为了减少线程间的竞争，把这些子任务分别放到不同的队列里，并为每个队列创建一个单独的线程来执行队列里的任务，线程和队列一一对应。
>
>举个栗子：
>
>A线程负责A队列的任务，但是，有的线程把自己队列里的任务干完了，而其他线程对应的队列里还有任务等待处理。干完活的线程与其等着，不如去帮其他线程干活，于是它就去其他线程的队列里窃取一个任务来执行。而在这时，他们会访问同一个队列，所以为了减少窃取任务线程和被窃取任务线程之间的竞争，通常会使用双端队列，被窃取任务的线程永远从双端队列的头部拿任务执行，而窃取任务的线程永远从双端队列的尾部拿任务执行。
>
>![image-20200514063555590](upload\image-20200514063555590.png)

工作窃取算法的优点：

>充分利用线程进行并行计算，减少了线程间的竞争

工作窃取算法的缺点：

>在某些情况下还是存在竞争，比如双端队列里只有一个任务时。并且该算法会消耗了更多的系统资源，比如创建多个线程和多个双端队列。

Fork/join使用两个类来完成以上两件事情。

1. ForkJoinTask：我们使用ForkJoin框架，必须首先创建一个ForkJoin任务。他提供在任务中执行fork()和join()操作的机制。通常情况下，我们不需要直接继承ForkJoinTask类，只需要继承他的子类，提供了以下两个子类：
   1. RecursiveAction:用于没有返回结果的任务
   2. RecusiveTask：用于返回结果的任务。
2. ForkJoinPool:ForkJoinTask需要通过ForkJoinPool来执行



##### 代码：

```java
package com.java并发编程实践;

import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.Future;
import java.util.concurrent.RecursiveTask;

public class ForkJoinTest extends RecursiveTask<Integer> {
    private static final int THRESHOLD = 2;//阈值
    private int start;
    private int end;
    public ForkJoinTest(int start,int end){
        this.start = start;
        this.end = end;
    }
    @Override
    protected Integer compute() {
        int sum = 0;
        boolean canCompute = (end - start) <=THRESHOLD;
        if(canCompute){
            for(int i = start;i<=end;i++){
                sum+=i;
            }
        }
        else{
            int middle = (start+end)/2;
            ForkJoinTest leftTask = new ForkJoinTest(start,middle);
            ForkJoinTest right = new ForkJoinTest(middle+1,end);
            leftTask.fork();
            right.fork();
//            invokeAll(leftTask,right);
            int leftval = leftTask.join();
            int rightval = right.join();
            sum = leftval+rightval;
        }
        return sum;
    }

    public static void main(String[] args) {
        ForkJoinPool forkJoinPool = new ForkJoinPool();
        ForkJoinTest task = new ForkJoinTest(1,4);
        Future<Integer> result = forkJoinPool.submit(task);
        try{
            System.out.println(task.get());
        }
        catch (Exception e){

        }
    }
}

```

运行结果：

10



