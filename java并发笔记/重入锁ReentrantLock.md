## 重入锁ReentrantLock

1. 重入锁：就是支持重进入的锁，它表示该锁能够支持一个线程对资源的重复加锁。
2. ReentrantLock如果在调用lock方法时，已经获取到锁的线程，能够再次调用lock方法获取锁而不被阻塞。

### 实现重进入

1. 实现重进入，需要解决两个问题：

   1. 线程再次获取锁。

      > 锁需要去识别获取锁的线程是否为当前占据锁的线程，如果是，则再次成功获取。

   2. 锁的最终释放

      > 线程重复了n此获取了锁，随后在第n次释放该锁后，其他线程能够获取到该锁。所得最终释放要求锁对于获取进行计数自增，计数表示当前锁被重复获取的次数，而锁被释放时，计数自减，当计数器等于0时表示锁已经成功释放。

### 代码分析(以nonfairTryAcquire方法为例)

```java
/**
         * Performs non-fair tryLock.  tryAcquire is implemented in
         * subclasses, but both need nonfair try for trylock method.
         */
        final boolean nonfairTryAcquire(int acquires) {
            final Thread current = Thread.currentThread();
            int c = getState();
            if (c == 0) {
                if (compareAndSetState(0, acquires)) {
                    setExclusiveOwnerThread(current);
                    return true;
                }
            }
            else if (current == getExclusiveOwnerThread()) {
                int nextc = c + acquires;
                if (nextc < 0) // overflow
                    throw new Error("Maximum lock count exceeded");
                setState(nextc);
                return true;
            }
            return false;
        }
```

1. 首先看第14行代码，重入锁的秘密就在这实现的

   * 首先它会当前线程是不是独占锁的占有者，如果是的话
     * setState(当前state+1);
     * 返回true
   * 不是的话，直接返回false。

2. 释放锁的时候的代码为:

   ```java
   protected final boolean tryRelease(int releases) {
               int c = getState() - releases;
               if (Thread.currentThread() != getExclusiveOwnerThread())
                   throw new IllegalMonitorStateException();
               boolean free = false;
               if (c == 0) {
                   free = true;
                   setExclusiveOwnerThread(null);
               }
               setState(c);
               return free;
           }
   ```

   1. 请看，第二行和第10行，这里就能明白释放锁的时候会将state减一.
   2. 再看第6-8行，当c=0，它会将AQS中的头结点设为null,然后返回true
   3. 锁释放成功。





参考书籍

《java并发编程的艺术》