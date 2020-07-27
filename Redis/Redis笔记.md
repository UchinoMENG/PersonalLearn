## Redis笔记

#### String类型

1. set key value

2. get key

3. mset key value key value

4. mget key ,key ,key

5. incr key 加一

6. incrby key 步长

7. decr key 减一

8. descby key 步长

9. incrbyfloat key 步长

10. descbyfloat key 步长

11. help @string

    >1. String在redis内部存储的默认就是一个字符串，当遇到增减类操作incr,decr时会转成数值型进行计算
    >2. redis所有的操作是原子性的，采用单线程处理所有业务，命令是一个一个执行的，因此无需考虑并发带来的数据影响
    >3. 注意：按数值进行操作的数据，如果原始数据不能转成数值，或超越了redis数值上限范围，将报错（java中的long型数据最大值，Long.MAX_VALUE）
    >4. redis用于控制数据库主键id,为数据库表主键生成策略，保证数据库表的主键唯一性
    >5. 此方案适用于所有数据库，且支持数据库集群

12. 设置数据具有指定的生命周期

    > setex key seconds value
    >
    > psetex key milliseconds value

    1. redis控制数据的生命周期，通过数据是否失效控制业务行为，适用于所具有时效性限定控制的操作

13. 数据的存数量为512MB

#### hash类型

1. hash类型底层使用哈希表实现数据存储

2. ![image-20200519113356110](https://i.loli.net/2020/05/19/HdMWePfy8bU1VS3.png)

3. hash存储结构优化

   * 如果field数量较少，存储结构优化为类数组结构
   * 如果field数量较多，存储结构使用HashMap结构

4. 添加/修改数据 hset key field value

5. 获取数据

   1. hget key field 
   2. hgetall key

6. 删除数据 hdel key field [field2]

7. 获取哈希表中字段的数量 hlen key

8. 获取哈希表中是否存在指定的字段

   hexists key field

9. hkeys key 所有的field

10. hvals key 所有的value

11. 设置指定字段的是数值数据增加指定范围的值

    1. hincrby key field increment

12. hash类型数据操作的注意事项

    1. hash类型下的value只能存储字符串，不允许存储其他类型数据，不存在嵌套现象。如果数据未获取到，对应的值为nil
    2. 每个hash可以存储2<sup>32</sup>-1个键值对
    3. hash类型十分贴近对象的数据存储形式，并且可以灵活添加删除对象属性。但hash设计初衷不是为了存储大量对象而设计的，切记不可滥用，更不可以将hash作为对象列表使用
    4. hgetall操作可以获取全部属性，如果内部field过多，遍历整体效率就很低，有可能成为数据访问瓶颈。

13. hsetnx key field value 如果不存在这个field则设置，否则什么都不干

#### list类型

1. 数据存储需求：存储多个数据，并对数据进入存储空间的顺序进行区分

2. 需要的存储结构：一个存储空间保存多个数据，且通过数据可以体现进入顺序

3. list类型：保存多个数据，底层是使用**双向链表**存储结构实现

4. List类型数据基本操作（按照双向链表的方式理解）

   > 添加/修改数据
   >
   > lpush key value [value2]...
   >
   > rpush key value [value2]...
   >
   > 获取数据
   >
   > lrange key start stop
   >
   > lindex key index
   >
   > llen key
   >
   > 获取并移除数据
   >
   > lpop key
   >
   > rpop key
   
5. 规定时间内获取并移除数据

   >blpop key (key2) timeout
   >
   >brpop key (key2) timeout

#### set类型

1. 添加数据

   sadd key member1 member2

2. 获取全部数据

   smembers key

3. 删除数据

   srem key memeber1 memeber2

4. 获取集合数据总量

   scard key

5. 判断集合中是否包含指定数据

   sismember key member

6. 随机获取集合中指定数量的数据

   srandmemeber key [count]

7. 随机获取集合中的某个数据并将该数据移除集合

   spop key

8. redis应用于随机推荐类信息检索，例如热点歌单推荐，热点新闻推荐，热卖旅游线路，应用APP推荐等。

9. 求两个集合的交并差

   >sinter key1 key2
   >
   >sunion key1 key2
   >
   >sdiff key1 key2

10. 求两个集合的交、并、差集并存储到指定集合中

    >sinterstore destination key1 key2
    >
    >sunionstore descination key1 key2
    >
    >sdiffstore descination key1 key2

11. 将指定数据从原始集合中移动到目标集合中

    > smove source descination member

12. set的应用实例：

    1. redis应用于同类信息的关联搜索，二度关联搜索，深度关联搜索
    2. 显示公共好友
    3. 显示共同关注
    4. 由用户A出发，获取到好友用户B的好友信息列表

##### sorted_set

1. 添加数据

   zadd key score1 member1 [score2 member2]

2. 获取全部数据

   zrange key start stop [withscores]

   zrevrange key start stop [withscores]

3. 删除数据

   zrem key member [member ... ]

4. 按条件获取数据

   zrangebyscore key min max [withscores] limit

   zrevrangebyscore key max min withscores

5. 条件删除数据

   zremrangebyrank key start stop

   zremrangebyscore key min max

6. 获取集合数据总量

   zcard key

   zcount key min max

7. 集合交，并操作

   zinterstore destination numkeys key [key key key]

   zunionstore descination numkeys key[key key key]

8. 获取数据对应的索引（排名）

   zrank key member

   zrevrank key member

9. score值获取与修改

   zscore key member

   zincrby key increment member

10. redis应用于计数器组合排序功能对应的排名

11. redis应用于定时任务执行顺序管理或任务过期管理

##### key基本操作

1. 删除指定key

   del key

2. 获取key是否存在

   exists key

3. 获取key的类型

   type key

4. 为key设置有效期

   expire key seconds

   pexpire key milliseconds

   expireat key timestamp

   pexpireat key milliseconds-timestamp

5. 获取key的有效时间

   ttl key

   pttl key

6. 切换key从时效性转换为永久性

   persist key

7. 查询key

   keys pattern

   解释pattern 

   1. *匹配任意数量的任意符号
   2. ？匹配一个任意符号
   3. []匹配一个指定符号

8. 为key改名

   rename key newkey

   renamenx key newkey

9. 对所有key排序

   sort  这里排序包括list,set,sorted-set

10. 其他key通用操作

    help @generic

11. 切换数据库

    select index

12. 数据移动（剪切操作）

    move key db

13. 数据清除

    flushdb 清空当前数据库

    flushall 跑路


##### 持久化简介

1. 什么是持久化

   > 利用持久化存储介质将数据进行保存，在特定的时间将保存的数据进行恢复的工作机制称为持久化

2. 为什么要进行持久化

   > 防止数据的意外丢失，确保数据安全性

3. RDB启动方式

   1. 命令:save

   2. 作用：

      手动执行一次保存操作，在用户保存日志的文件夹下生成一个.rdb文件

   3. 注意：save指令的执行会阻塞当前Redis服务器，直到当前RDB过程完成为止，有可能造成长时间阻塞，线上环境下不推荐使用。

4. bgsave

   1. bgsave命令是针对save阻塞问题做的优化。Redis内部所有涉及到RDB操作都采用bgsave的方式，save命令可以放弃使用。
   2. 工作原理
      1. ![](https://i.loli.net/2020/05/20/GHC7MhKPSIkUWwv.png)

5. save second changes

   1. 作用：满足限定时间范围内key的变化数量达到指定数量即可进行持久化

   1. 参数：

      1. second : 监控时间范围

      1. changes:监控key的变化量

   2. 位置在conf文件中进行配置

   3. 这种方式启动后执行的是bgsave操作

6. RDB启动方式对比

   | 方式           | save指令 | bgsave |
   | -------------- | -------- | ------ |
   | 读写           | 同步     | 异步   |
   | 阻塞客户端指令 | 是       | 否     |
   | 额外内存消耗   | 否       | 是     |
   | 启动新进程     | 否       | 是     |

7. RDB总结

   1. RDB优点
      * RDB：RDB是一个紧凑压缩的二进制文件，存储效率较高
      * RDB内部存储的是redis在某个时间点的数据快照，非常适合用于数据备份，全量复制等场景
      * RDB恢复数据的速度要比AOF快的多
      * 应用：服务器中没X小时执行bgsave备份，并将RDB文件拷贝到远程机器中，用于灾难恢复
   2. RDB缺点
      * RDB方式无论是执行指令还是利用配置，无法做到实时持久化，具有较大可能性丢失数据
      * bgsave指令每次运行都要执行fork操作创建子进程，要牺牲掉一些性能
      * Redis的众多版本中未进行RDB文件格式的版本统一，有可能出现个版本服务之间数据格式无法兼容现象

##### AOF

1. 概念

   >AOF持久化：以独立日志的方式记录每次写命令，重启时在重新执行AOF文件中命令达到数据恢复的目的，与RDB相比可以简单描述为改记录数据为记录数据产生的过程

2. 作用

   AOF的主要作用主要是解决了数据持久化的实时性，目前已经是Redis持久化的主流方式

3. AOF写数据的三种策略

   1. always(每次)

      每次写入操作均同步到aof文件，数据零误差，性能较低，不建议使用

   2. everysec(每秒)

      每秒将缓冲区中的指令同步到AOF文件中，数据准确率较高，性能较高，建议使用，也是默认配置

      在系统突然宕机的情况下丢失1秒内的数据

   3. no（系统控制）

      由操作系统控制每次同步到AOF文件的周期，整体过程不可控

4. AOF功能开启

   * 配置

     appendonly yes|no

   * 作用

     是否开启AOF持久化功能，默认为不开启状态

   * 配置

     appendfsync always|everysec|no

   * 作用

     AOF写数据策略

5. AOF重写

   随着命令不断写入AOF，文件会越来越大，为了解决这个问题，Redis引入了AOF重写机制压缩文件体积。AOF文件重写是将Redis进程内的数据转化为写命令同步到AOF文件的过程。简单来说就是将对一个数据的若干条个命令执行结果转化为最终结果数据对应的指令进行记录。

6. AOF重写作用

   * 降低磁盘占用量，提高磁盘利用率
   * 提高持久化效率，降低持久化写，提高IO性能
   * 降低数据恢复用时

7. AOF重写规则

   1. 进程内已超时的数据不再写入文件
   2. 忽略无效指令，重写时使用进程内数据直接生成，这样新的AOF文件只保留最终数据的写入命令
   3. 对同一条数据的多条命令合并为一条命令
      * 为防止数据量过大造成客户端缓冲区溢出，对List，set，hash，zset等类型，每条指令最多写入64个元素

8. AOF重写方式

   1. 手动重写

      >bgrewriteaof

   2. 自动重写

      >auto-aof-rewrite-min-size size
      >
      >auto-aof-rewrite-percentage percentage

9. AOF重写流程

   ![](https://i.loli.net/2020/05/20/pXR5N1S2tUrsHVy.png)

   1. | 持久化方式   | RDB                | AOF              |
      | ------------ | ------------------ | ---------------- |
      | 占用存储空间 | 小（数据级：压缩） | 大（指令集重写） |
      | 存储速度     | 慢                 | 快               |
      | 恢复速度     | 快                 | 慢               |
      | 数据安全性   | 会丢失数据         | 依据策略决定     |
      | 资源消耗     | 高/重量级          | 低/轻量级        |
      | 启动优先级   | 低                 | 高               |

   

10. RDB与AOF的选择

    * RDB与AOF的选择世界上是在做一种权衡，每种都有利弊
    * 如不能承受数分钟以内的数据丢失，对业务数据非常敏感，选用AOF
    * 如能承受数分钟以内的数据丢失，且追求大数据集的恢复速度，先用RDB
    * 灾难恢复选用RDB
    * 双保险策略：同时开启RDB与AOF，重启后，Redis优先选择使用AOF来恢复速度，降低丢失数据的量

##### Redis事务简介

1. 什么是事务

   redis执行指令过程中，多条连续执行的指令被干扰，打断，插队

   redis事务就是一个命令执行的队列，将一系列预定义命令包装秤一个整体（一个队列）。当运行时，一次性按照添加顺序依次执行，中间不会被打断或者干扰

   一个队列中，一次性，顺序性，排他性的执行一系列命令

2. 事务的基本操作

   1. 开启事务

      muti

      作用：设定事务的开启位置，此指令执行后，后续的所有指令均加入到事务中

   2. 执行事务

      exec

      作用：设定事务的结束位置，同时执行事务，与multi成对出现，成对使用

   3. 取消事务

      discard

      作用：终止当前事务的定义，发生在multi之后，exec之前。

3. 基于特定条件的事务执行--锁

   1. 对key添加监视锁，在在执行exec前如果key发生了变化，终止事务执行

      >watch key1 [key2]

   2. 取消对所有key的监视

      >unwatch

4. 基于特定条件的事务执行---分布式锁

   1. 使用setnx设置一个公共锁

      setnx lock-key value

      > 利用setnx命令的返回值特征，有值则返回设置失败，无值则返回设置成功
      >
      > 1. 对于设置成功的，拥有控制权，进行下一步的具体业务操作
      > 2. 对于设置失败的，不具有控制权，排队等待

      操作完毕通过del操作释放锁

5. 基于特定条件的事务执行----分布式锁改良

   1. 使用expire为锁key添加时间限定，到时不释放，放弃锁

      > expire lock-key second
      >
      > pexpire lock-key second

##### 过期数据

1. Redis中的数据特征

   1. redis是一种内存级数据库，所有数据均存放在内存中，内存中的数据可以通过TTL指令获取其状态
      1. * XX：具有时效性的数据
         * -1：永久有效
         * -2：已经过期的数据或 被删除的数据 或未定义的数据

2. 时效性数据的存储结构

   ![](https://i.loli.net/2020/05/21/cfmVAhIbUwpXNuB.png)

3. 数据删除策略

   1. 定时删除

      >* 创建一个定时器，当key设置有过期时间，且过期时间到达时，由定时器任务立即执行对键的删除操作
      >
      >* 优点：节约内存，到时就删除，快速释放掉且不必要的内存占用
      >* 缺点：cpu压力过大，无论cpu此时负载量多高，均占用cpu，会影响redis服务器响应时间和指令吞吐量
      >* 总结：用处理器性能换区存储空间（时间换空间）

   2. 惰性删除

      >* 数据到达过期时间不作处理。等下次访问该数据时
      >  * 如果未过期，返回数据
      >  * 发现已过期，删除，返回不存在
      >* 优点：节约CPU性能，发现必须删除的时候才删除
      >* 缺点：内存压力很大，出现长期占用内存的数据
      >* 总结:用存储空间换取处理器性能（空间换时间）

   3. 定期删除

4. 数据删除策略的目标

   在内存占用与CPU占用之间寻找一种平衡，顾此失彼都会造成整体redis性能的下降，甚至引发服务器宕机或者内存泄露

5. 逐出算法

   > 当新数据进入redis时，如果内存不足怎么办？
   >
   > Redis使用内存存储数据，在执行每一个命令前，会调用freeMemoryIfNeeded()检测内存是否充足，如果内存不满足数据的最低存储要求，redis要临时删除一些数据为当前指令清理存储空间。清理数据的算法称之为逐出算法。

   1. 注意：逐出数据的过程不是100%能够清理出足够的可食用的内存空间，如果不成功则反复执行。当对所有数据尝试完毕后，如果不能够达到内存清理的要求，将会出现错误信息。（OOM）

   2. 最大可使用内存

      maxmemory

      占用物理内存的比例，默认是0，表示不限制，生产环境中根据需求设定，通常在50%以上

   3. 每次选取待删除数据的个数

      maxmemory-sample

      选取数据时并不会全库扫描，导致严重的性能消耗，降低读写性能。因此采用随机获取数据的方式作为待检测删除数据

   4. 删除策略

      maxmemory-policy voliate-lru

      达到最大内存后的，对被挑选出来的数据进行删除的策略

   5. 影响数据逐出的相关配置

      * 检测易失数据（可能会过期的数据级server.db[i].expires）

        1. voliate-lru:挑选最近最少使用的数据淘汰
        2. voliate-lfu:挑选最近使用次数最少的数据淘汰
        3. voliate-ttl:挑选将要过期的数据淘汰
        4. voliate-random:任意选择数据淘汰

      * 检测全库数据（所有数据级server.dp[i].dict）

        1. allkeys-lru:挑选最近最少使用的数据淘汰
        2. allkeys-lfu:挑选最近使用次数最少的数据淘汰
        3. allkeys-random:任意选择数据淘汰

      * 放弃数据驱逐

        no-enviction(驱逐):禁止驱逐数据，会引发OOM

##### Bitmaps

1. 用于存储状态的一个数据结构，以bit位来存储

2. 对指定key按位进行交，并，非，异或操作，并将结果保存到destkey中

   >bitop op destkey key1 [key2...]
   >
   >1. and
   >2. or
   >3. not
   >4. xor

3. 统计指定key中1的数量

   >bitcount key start end

4. 设置某个位为1

   >setbit key index value

5. 获取某个位的状态

   >getbit key index 

##### HyperLogLog

> 在Redis中每个键占用的内容都是12k，理论存储近似接近2<sup>64</sup>值，不管存储的内容是什么。这是一个基于基数估计的算法，只能比较准确的估算出基数，可以使用少量固定的内存去存储并识别集合中的唯一元素，但是这个估算的基数并不一定准确，是一个带有0.81%标准错误的近似值，并且它并不存储数据的内容

1. pfadd

   >将任意数量的元素添加到指定的hyperloglog里面。时间复杂度：每添加一个元素的复杂度为O(1).如果Hyperloglog估计的近似基数在命令执行之后出现了变化，那么返回1，否则返回0.如果命令执行时给定的键不存在，那么程序将先创一个空的Hyperloglog结构，然后在执行命令

   ```
   # 命令格式：PFADD key element [element …]
   # 如果给定的键不存在，那么命令会创建一个空的 HyperLogLog，并向客户端返回 1
   127.0.0.1:6379> PFADD ip_20190301 "192.168.0.1" "192.168.0.2" "192.168.0.3"
   (integer) 1
   # 元素估计数量没有变化，返回 0（因为 192.168.0.1 已经存在）
   127.0.0.1:6379> PFADD ip_20190301 "192.168.0.1"
   (integer) 0
   # 添加一个不存在的元素，返回 1。注意，此时 HyperLogLog 内部存储会被更新，因为要记录新元素
   127.0.0.1:6379> PFADD ip_20190301 "192.168.0.4"
   (integer) 1
   
   ```

2. pfcount

   >当 PFCOUNT key [key …] 命令作用于单个键时，返回储存在给定键的 HyperLogLog 的近似基数，如果键不存在，那么返回 0，复杂度为 O(1)，并且具有非常低的平均常数时间；
   >
   >当 PFCOUNT key [key …] 命令作用于多个键时，返回所有给定 HyperLogLog 的并集的近似基数，这个近似基数是通过将所有给定 HyperLogLog 合并至一个临时 HyperLogLog 来计算得出的，复杂度为 O(N)，常数时间也比处理单个 HyperLogLog 时要大得多。

   ```
   # 返回 ip_20190301 包含的唯一元素的近似数量
   127.0.0.1:6379> PFCOUNT ip_20190301
   (integer) 4
   127.0.0.1:6379> PFADD ip_20190301 "192.168.0.5"
   (integer) 1
   127.0.0.1:6379> PFCOUNT ip_20190301
   (integer) 5
   127.0.0.1:6379> PFADD ip_20190302 "192.168.0.1" "192.168.0.6" "192.168.0.7"
   (integer) 1
   # 返回 ip_20190301 和 ip_20190302 包含的唯一元素的近似数量
   127.0.0.1:6379> PFCOUNT ip_20190301 ip_20190302
   (integer) 7
   
   ```

3. pfmerge

   >**将多个 HyperLogLog 合并（merge）为一个 HyperLogLog，合并后的 HyperLogLog 的基数接近于所有输入 HyperLogLog 的可见集合（observed set）的并集。时间复杂度是 O(N)，其中 N 为被合并的 HyperLogLog 数量，不过这个命令的常数复杂度比较高。** 
   >
   >**命令格式：PFMERGE destkey sourcekey [sourcekey …]，合并得出的 HyperLogLog 会被储存在 destkey 键里面，如果该键并不存在，那么命令在执行之前，会先为该键创建一个空的 HyperLogLog。**

   ```
   127.0.0.1:6379> PFMERGE ip_2019030102 ip_20190301 ip_20190302
   OK
   127.0.0.1:6379> PFCOUNT ip_2019030102
   (integer) 7
   ```

4. 应用场景：

   计算日活，7日活，月活数据，点击量等。

##### GEO

1. 根据坐标求范围内的数据

   ```redis
   georadius key longitude latitude radius m|km|ft
   ```

2. 根据点求范围内数据

   >georadiusbymember key member radius m|km|mi

3. 获取指定点对应的坐标hash值

   ```
   gephash key member [member ...]
   ```

4. 应用：

   radis应用于地理位置计算

##### 主从复制

1. 主从复制即将master中的数据即时、有效的复制到slave中

2. 特征：一个master可以有多个slave，一个slave只对应一个master

3. 职责：

   1. master:
      * 写数据
      * 执行写操作时，将会出现变化的数据自动同步到slave
      * 读数据（可忽略）
   2. slave:
      * 读数据
      * 写数据（禁止）

4. ![](https://i.loli.net/2020/05/21/8MyFDTLj9NvoixQ.png)

5. 主从复制的作用

   1. 读写分离:master写，slave读，提高服务器的读写负载能力
   2. 负载均衡：基于主从结构，配合读写分离，由slave分担master负载，并根据需求的变化，改变slave的数量，通过多个从节点分担数据读取负载，大大提高Redis服务器并发量与数据吞吐量
   3. 故障恢复：当master出现问题时，由slave提供服务，实现快速的故障恢复
   4. 数据冗余：实现数据热备份，是持久化之外的一种数据冗余方式
   5. 高可用基石：基于主从复制，构建哨兵模式与集群，实现Redis的高可用方案。

6. ![](https://i.loli.net/2020/05/21/62DZzxTaGOWmUuS.png)

7. 建立连接阶段工作流程

   1. slave首先发送指令:```slaveif ip pore```

   2. master接收到指令，响应对方

   3. salve保存master的IP与端口

      masterhost

      masterport

   4. slave根据保存的信息创建连接master的socket

   5. 为了保证服务器没掉线，slave会定时周期性发送指令ping

   6. master会响应pong

8. ![](https://i.loli.net/2020/05/21/EmeM8vpZx9n67Nl.png)

9. 主从连接

   1. 方式一：客户端发送命令

      ```slaveof <masterip> <masterport>```

   2. 方式二：启动服务器参数

      ```redis-cli --slaveof <ip> <port> ```

   3. 方式三：服务器配置

      ```slaveof <ip> <port>```

   4. 停用主从复制

      ```slaveof no one```







##### 哨兵简介

> 哨兵是一个分布式系统，用于对主从结构中的每台服务器进行监控，当出现故障时通过投票机制选择新的master并将所有slave连接到新的master。

1. 哨兵的作用

   1. 监控

      >不断的检查master和slave是否正常运行。master存活检测，master与slave运行情况检测

   2. 通知（提醒）

      >当被监控的服务器出现问题时，向其他（哨兵间，客户端）发送通知。

   3. 自动故障转移

      >断开master与slave连接，选取一个slave作为master，将其他slave连接到新的master，并告知客户端新的服务器地址

   4. 注意：

      * 哨兵也是一台redis服务器，只是不提供服务
      * 通常哨兵配置数量为单数

2. 























