# HashMap中的resize方法源码解释

1. 前些天被蘑菇街老哥问到了hashMap源码， 然后让我说一下resize的具体实现，我就简单的说了一下，但是人家要详细的过程，我没说上来，今天准备写一下源码解释，看完之后发现之前没明白，明白了过来，发现真的妙。

2. 源码(一行一行解释的)

   ```java
   final Node<K,V>[] resize() {
           Node<K,V>[] oldTab = table;		//源数组桶	
           int oldCap = (oldTab == null) ? 0 : oldTab.length;	//计算原数组桶中元素的个数
           int oldThr = threshold;		//计算负载个数
           int newCap, newThr = 0;		//初始化定义新负载的容量和个数
           if (oldCap > 0) {		//这个if的分支代表，如果原来的桶容量大于最大容量，则不用扩容，负载容量就设置为最大值即可，并返回
               if (oldCap >= MAXIMUM_CAPACITY) {
                   threshold = Integer.MAX_VALUE;
                   return oldTab;
               }
               else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY &&
                        oldCap >= DEFAULT_INITIAL_CAPACITY)
                   newThr = oldThr << 1; // 如果数组扩容后的二倍比最大容量小，则进行扩容
           }
           else if (oldThr > 0) // initial capacity was placed in threshold
               newCap = oldThr;		//将旧的负载个数赋给新的容量
           else {               // 初始化为零时，先初始化为16，然后负载个数为12
               newCap = DEFAULT_INITIAL_CAPACITY;
               newThr = (int)(DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);
           }
           if (newThr == 0) {//如果new负载个数为0，则进行给新的负载个数赋值
               float ft = (float)newCap * loadFactor;
               newThr = (newCap < MAXIMUM_CAPACITY && ft < (float)MAXIMUM_CAPACITY ?
                         (int)ft : Integer.MAX_VALUE);
           }
           threshold = newThr;		//将当前新的负载个数赋给当前的负载个数，
           @SuppressWarnings({"rawtypes","unchecked"})
               Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
           table = newTab;	//将新的数组赋给当前数组
           if (oldTab != null) {
               for (int j = 0; j < oldCap; ++j) {		//依次遍历桶
                   Node<K,V> e;
                   if ((e = oldTab[j]) != null) {		//如果原来桶下标存在值，并将旧值赋给e
                       oldTab[j] = null;		//将原来的值赋为空，方便gc
                       if (e.next == null)		//如果这个没有下一项，则直接计算下标放在新的桶的下标处
                           newTab[e.hash & (newCap - 1)] = e;
                       else if (e instanceof TreeNode)		//如果是红黑树的话，则插入到树中，这里没看
                           ((TreeNode<K,V>)e).split(this, newTab, j, oldCap);
                       else { // preserve order，这里保证了插入顺序
                           Node<K,V> loHead = null, loTail = null;	//低级链表（低处位置的链表）
                           Node<K,V> hiHead = null, hiTail = null;	//二倍处的链表
                           Node<K,V> next;		
                           do {
                               next = e.next;
                               if ((e.hash & oldCap) == 0) {		//头为空，初始化头，否则插入后面
                                   if (loTail == null)
                                       loHead = e;
                                   else
                                       loTail.next = e;
                                   loTail = e;
                               }
                               else {				//头为空，初始化头，否则插入后面
                                   if (hiTail == null)
                                       hiHead = e;
                                   else
                                       hiTail.next = e;
                                   hiTail = e;
                               }
                           } while ((e = next) != null);
                           if (loTail != null) {		//将低处的node链表插入到这里来
                               loTail.next = null;
                               newTab[j] = loHead;
                           }
                           if (hiTail != null) {		//将二倍处的node链表插入到这里来
                               hiTail.next = null;
                               newTab[j + oldCap] = hiHead;
                           }
                       }
                   }
               }
           }
           return newTab;
       }
   ```

   