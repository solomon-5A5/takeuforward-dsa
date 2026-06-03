/*
 * Problem Name: Rotate Image
 * Link: https://leetcode.com/problems/rotate-image/description/
 * 
 * Approach: Transpose and then reverse each row.
 * Time Complexity: O(n^2) - We iterate through the matrix twice.
 * Space Complexity: O(1) - We modify the matrix in-place.
 */

class Solution {
    public void rotate(int[][] matrix) {
        int n=matrix.length; int temp;
    for(int i=0;i<n-1;i++){
        for(int j=i+1;j<n;j++){
            temp=matrix[i][j];
            matrix[i][j]=matrix[j][i];
            matrix[j][i]=temp;
        }
    }  
    for(int i=0;i<n;i++){
        for(int j=0;j<n/2;j++){
            temp=matrix[i][j];
            matrix[i][j]=matrix[i][n-j-1];
            matrix[i][n-j-1]=temp;
        }
    }   
    }
}
