/**
 * Problem Name: Maximum Sub Array
 * Link: https://leetcode.com/problems/maximum-subarray/description/
 * 
 * Approach: Kadane's Algorithm
 * Time Complexity: O(n) - We iterate through the array once.
 * Space Complexity: O(1) - We only use a few variables to keep track of the maximum sum and the current sum.
 */
class Solution {
    public int maxSubArray(int[] nums) {
        int curr=0,max=-100000;
        for(int i=0;i<nums.length;i++){
            curr+=nums[i];
            if(curr>max)
            max=curr;
            if(curr<0)
            curr=0;

        }
        return max;

    }
}