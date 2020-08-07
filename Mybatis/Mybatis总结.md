# Mybatis总结

### Mybatis中的一级缓存

首先mybatis的一级缓存是自动开启的。

缓存的作用是减轻数据库的压力，提高数据库的性能的。Mybatis中提供了一级缓存和二级缓存，先来看两个缓存的示意图：

![image-20200807085736327](https://i.loli.net/2020/08/07/bxd9EeJ5jVYM2nz.png)

从图中可以看出：

>1. 一级缓存是sqlSession级别的缓存。在操作数据库时需要构造sqlsession对象，在对象中有一个数据结构(hashMap)用于存储缓存数据。在不同的sqlsession之间的缓存数据区域是互相不影响。
>2. 二级缓存是mapper级别的缓存，多个sqlsession去操作同一个mapper的sql语句，多个sqlsession可以共用二级缓存，二级缓存是跨sqlsession的
>
>

![image-20200807090349382](https://i.loli.net/2020/08/07/ofDbnJNaLQpGMqe.png)

从图中可以看出：第一次发起查询用户id为1的用户信息，先去找缓存中是否有id为1的用户信息，如果没有，从数据库查询用户信息。得到用户信息，将用户信息存储到一级缓存中。
　　如果中间sqlSession去执行commit操作（执行插入、更新、删除），则会清空SqlSession中的一级缓存，这样做的目的为了让缓存中存储的是最新的信息，避免脏读。
　　第二次发起查询用户id为1的用户信息，先去找缓存中是否有id为1的用户信息，缓存中有，直接从缓存中获取用户信息。

如果是从一级缓存中拿的，则拿到的数据地址是相同的。

#### 二级缓存

Mybatis中的二级缓存是mapper级别的缓存，值得注意的是，不同的mapper都有一个二级缓存，也就是说，不同的mapper之间的二级缓存是互不影响的。

![image-20200807144503991](https://i.loli.net/2020/08/07/qsnt7ml5CW4KLRh.png)

>1. sqlSession1去查询用户id为1的用户信息，查询到用户信息会将查询数据存储到该UserMapper的二级缓存中。
>2. 如果SqlSession3去执行相同 mapper下sql，执行commit提交，则会清空该UserMapper下二级缓存区域的数据。
>3. sqlSession2去查询用户id为1的用户信息，去缓存中找是否存在数据，如果存在直接从缓存中取出数据。

如果是从二级缓存拿的数据，数据的地址是不一样的，因为二级缓存是存的序列化的数据，而不是像一级缓存一样存的是物理地址。