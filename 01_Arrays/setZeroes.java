/**
 * Problem Name: Set Matrix Zeroes
 * Link: https://leetcode.com/problems/set-matrix-zeroes/description/
 * 
 * Approach: We use two arrays to keep track of the rows and columns that need to be zeroed.
 * Time Complexity: O(m*n) - We iterate through the matrix twice.
 * Space Complexity: O(m+n) - We use two arrays to keep track of the rows and columns that need to be zeroed.
 */
class Solution {
    public void setZeroes(int[][] matrix) {
        int m=matrix.length,n=matrix[0].length;
        boolean [] col=new boolean[n];
        boolean[] row=new boolean[m];
        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                if(matrix[i][j]==0){
                    col[j]=true;
                    row[i]=true;
                }
            }
        }
        for(int i=0;i<m;i++)
        for(int j=0;j<n;j++)
        if(col[j]||row[i])
        matrix[i][j]=0;
        
    }
}
