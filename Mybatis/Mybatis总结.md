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

### 延迟加载

##### 延迟加载：（应用于一对多，多对多，即关联的对象为“多”时）

在真正使用数据时才发起查询，不用的时候不查询，按需加载（懒加载）。

##### 立即加载：（应用于多对一，一对一，即关联的对象为“一”时）

不管用不用，在调用方法的时候就立即执行，马上发起查询。

[https://blog.csdn.net/eson_15/article/details/51669608](Mybatis延迟加载好的博客)



### JDBC编程有哪些不足之处，MyBatis是如何解决这些问题的？

1、数据库链接创建、释放频繁造成系统资源浪费从而影响系统性能，如果使用数据库连接池可解决此问题。

解决：在mybatis-config.xml中配置数据链接池，使用连接池管理数据库连接。

2、Sql语句写在代码中造成代码不易维护，实际应用sql变化的可能较大，sql变动需要改变java代码。

解决：将Sql语句配置在XXXXmapper.xml文件中与java代码分离。

3、向sql语句传参数麻烦，因为sql语句的where条件不一定，可能多也可能少，占位符需要和参数一一对应。

解决： Mybatis自动将java对象映射至sql语句。

4、对结果集解析麻烦，sql变化导致解析代码变化，且解析前需要遍历，如果能将数据库记录封装成pojo对象解析比较方便。

解决：Mybatis自动将sql执行结果映射至java对象。

### Mybatis是否支持延迟加载？如果支持，他的实现原理是什么？

>Mybatis仅支持association关联对象和collection关联集合对象的延迟加载，association指的就是一对一，collection指的就是一对多查询。在Mybatis配置文件中，可以配置是否启用延迟加载lazyLoadingEnabled=true|false。
>
>它的实现原理是，使用CGLIB创建目标对象的代理对象，当调用目标方法时，进入拦截器方法，比如调用a.getB().getName(),拦截器invoke()方法发现a.getB()是null值，那么就会单独发送实现保存好的查询关联对象B对象的sql，把B查询上来，然后调用a,setB(b),于是a对象的b属性就有值了，接着完成a.getB().getName()方法的调用。这就是延迟加载的基本原理。

### #{}和${}的区别

- #{}是占位符，预编译处理；${}是拼接符，字符串替换，没有预编译处理。
- Mybatis在处理#{}时，#{}传入参数是以字符串传入，会将SQL中的#{}替换为?号，调用PreparedStatement的set方法来赋值。
- 在变量替换的时候，#{}对应的变量自动加上单引号' ';而${}对应的变量不会加上单引号
- #{}可以有效的防止SQL注入，提高系统安全性；${}不能防止SQL注入

### 模糊查询like语句该怎么写

（1）’%${question}%’ 可能引起SQL注入，不推荐

（2）"%"#{question}"%" 注意：因为#{…}解析成sql语句时候，会在变量外侧自动加单引号’ '，所以这里 % 需要使用双引号" "，不能使用单引号 ’ '，不然会查不到任何结果。

（3）CONCAT(’%’,#{question},’%’) 使用CONCAT()函数，推荐

（4）使用bind标签

```xml
<select id="listUserLikeUsername" resultType="com.jourwon.pojo.User">
　　<bind name="pattern" value="'%' + username + '%'" />
　　select id,sex,age,username,password from person where username LIKE #{pattern}
</select>

```

