import java.io.*;
import java.util.*;

public class KnapsackSolution {
    
    private static int solve(int s, int[] v, int[] w) {
        int m = v.length;
        int[][] d = new int[s+1][m];
        for(int i = 1; i < s+1; i++){
            for(int j = 0; j < m ; j++){
                int var1 = 0;
                if(i - w[j] >= 0 ){
                    if(j-1 < 0){
                        var1 = v[j];
                    } else {
                        var1 = d[i-w[j]][j-1] + v[j];    
                    }
                }
                int var2 = 0;
                if(j - 1 >= 0){
                    var2 = d[i][j-1];
                }
                d[i][j] = Math.max(var1, var2);
            }
        }
        return d[s][m-1];
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int numTestCases = sc.nextInt();
        for(int i =0 ; i < numTestCases; i++){
            int s = sc.nextInt();
            int n = sc.nextInt();
            int[] v = new int[n];
            int[] w = new int[n];
            for(int j = 0; j < n; j++){
                w[j] = sc.nextInt();
                v[j] = sc.nextInt();
            }
            int ans = solve(s,v,w);
            System.out.println(ans);
        }
    }
}