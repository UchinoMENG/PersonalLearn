# Prime算法

1. Prime算法用于求最小生成树的一个算法，今天又看了下这个算法和迪杰斯特拉相同的思路，其实就是最短路径的数组代表的含义是不一样的，其他的算法书写和思想都是差不多的

2. 通用算法

   ```c++
   public void initPrime(){
           fill(double,d+maxv,inf);
           d[0] = 0;
           int ans = 0;
           for(int i = 0;i<n;i++){
               int u = -1,min = inf;
               for(int j = 0;j<n;j++){
                   if(vis[j]==false&&d[j]<min){
                       u = j;
                       min = d[j];
                   }
               }
               if(u==-1){
                   return -1;
               }
           }
           vis[u] = true;
           ans+=d[u];
           for(int i = 0;i<n;i++){
               if(vis[i]==false&&G[u][v]!=inf&&G[u][v]<d[v]){
                   d[v] = G[u][v];
               }
           }
           return ans;
       }
   ```

   

