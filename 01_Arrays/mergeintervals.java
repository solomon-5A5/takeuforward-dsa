/*
 * Problem Name: Merge Intervals
 * Link: https://leetcode.com/problems/merge-intervals/description/
 * 
 * Approach: 
 * Time Complexity: O(n log n) - Dominated by sorting the intervals.
 * Space Complexity: O(n) - For the result list.
 */

import java.util.*;
class Solution {
    public int[][] merge(int[][] intervals) {
        int n = intervals.length;

        Arrays.sort(intervals, (a, b) -> a[0] - b[0]);

        List<int[]> ans = new ArrayList<>();

        int start = intervals[0][0];
        int end = intervals[0][1];

        for (int i = 1; i < n; i++) {
            if (end >= intervals[i][0]) {
                end = Math.max(end, intervals[i][1]);
            } else {
                ans.add(new int[] { start, end });
                start = intervals[i][0];
                end = intervals[i][1];
            }
        }
        ans.add(new int[] { start, end });

        return ans.toArray(new int[ans.size()][]);

    }
}
