/**
 * Problem Name: Pascal's Triangle
 * Link: https://leetcode.com/problems/pascals-triangle/description/
 * 
 * Approach: Generate Pascal's Triangle row by row.
 * Time Complexity: O(n^2) - We iterate through each element of the triangle.
 * Space Complexity: O(n^2) - We store the entire triangle.
 */

import java.util.*;
class Solution {
    public List<List<Integer>> generate(int numRows) {
        List<List<Integer>> ls=new ArrayList<>();
        for(int i=0;i<numRows;i++){
            List<Integer> row=new ArrayList<>();
            for(int j=0;j<=i;j++){
                if (j == 0 || j == i) {
                    row.add(1);
                } else {
                    List<Integer> prevRow = ls.get(i - 1);
                    row.add(prevRow.get(j - 1) + prevRow.get(j));
                }
            }
            ls.add(row);

        }
        return ls;
    }
}