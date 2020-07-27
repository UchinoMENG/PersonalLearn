# Dijkstra算法

1. 迪杰斯特拉算法

   >用于求点对点的最短路径的算法，个人觉得主要是用了贪心的想法，每次选出最短的路径，算出路径的值。

2. 今天看sp群，看到有些公司让手写了迪杰斯特拉算法，我之前很会这个算法，但我忽然又忘记了，写出来了，今天又做了一下关于点对点最短路径的题，算是自己的一个总结吧

3. **L2-001** **紧急救援** **(25****分****)**

4. 代码

   ```java
   import java.util.*;
   
   public class Main {
   
       private static List<List<Integer>> dest = new ArrayList<>();
       private static int[] cnt ;
       static int[] dis ;
       static List<Integer> rr ;
       static int[] people ;
       static int rel = Integer.MIN_VALUE;
       public static void main(String[] args) {
           Scanner in  = new Scanner(System.in);
          int cn = in.nextInt();
          int num = in.nextInt();
          int st = in.nextInt();
          int end = in.nextInt();
          for(int i = 0;i<cn;i++){
              List<Integer> list = new ArrayList<>();
              dest.add(list);
          }
          people = new int[cn];
          dis = new int[cn];
          for(int i = 0;i<cn;i++){
              people[i] = in.nextInt();
          }
          cnt = new int[cn];
          int[][] to = new int[cn][cn];
          init(to,cn);
          for(int i = 0;i<num;i++){
              int s = in.nextInt();
              int e = in.nextInt();
              to[s][e] = in.nextInt();
              to[e][s] = to[s][e];
          }
          dij(to,cn,st);
          List<Integer> pp = new ArrayList<>();
          //dfs(pp,st,end,people[end]);
           System.out.print(cnt[end]);
           System.out.println(" "+rel);
           for(int i = rr.size()-1;i>=0;i--){
               System.out.print(rr.get(i)+" ");
           }
           System.out.println(end);
           //System.out.println(dis[end]);
       }
       public static void init(int[][] to,int n){
           for(int i = 0;i<n;i++){
               for(int j = 0;j<n;j++){
                   to[i][j] = 501;
               }
           }
       }
       public static void dij(int[][] to,int n,int st){
           boolean[] visit = new boolean[n];
           for(int i = 0;i<n;i++){
               dis[i] = 501;
           }
           dis[st] = 0;
           cnt[st] = 1;
          // System.out.println(visit[0]);
           for(int i = 0;i<n;i++){
               int sign = -1,d = 501;
               for(int j = 0;j<n;j++){
                   if(visit[j]==false&&dis[j]<d){
                       sign = j;
                       d = dis[j];
                   }
               }
               //不连通的话
               if(sign==-1){
                   return ;
               }
               visit[sign] = true;
               for(int j = 0;j<n;j++){
                   if(visit[j]==false&&to[sign][j]!=501){
                       if(dis[sign]+to[sign][j]<dis[j]){
                           dis[j] = dis[sign]+to[sign][j];
                           cnt[j] = cnt[sign];
                           dest.get(j).clear();
                           dest.get(j).add(sign);
                       }
                       else if(dis[sign]+to[sign][j]==dis[j]){
                           cnt[j]+=cnt[sign];
                           dest.get(j).add(sign);
                       }
                   }
               }
           }
       }
       public static void dfs(List<Integer> res,int st,int end,int sum){
           if(st==end){
               if(sum>rel){
                   rel = sum;
                   rr = new ArrayList<>(res);
               }
               return;
           }
           for(int i = 0;i<dest.get(end).size();i++){
               int ss = dest.get(end).get(i);
               res.add(ss);
               dfs(res,st,ss,sum+people[ss]);
               res.remove(res.size()-1);
           }
       }
   }
   ```

   