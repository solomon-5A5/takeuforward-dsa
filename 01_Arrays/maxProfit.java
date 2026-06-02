/**
 * Problem Name: Maximum Profit
 * Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/
 * 
 * Approach: Keep track of the minimum element and the maximum profit found so far.
 * Time Complexity: O(n) - We iterate through the array once.
 * Space Complexity: O(1) - We only use a few variables to keep track of the minimum element and the maximum profit.
 */

class Solution {
    public int maxProfit(int[] prices) {
        int min,ans=0;
        min=prices[0];
        for(int i=1;i<prices.length;i++){
            if(prices[i]-min>ans)
            ans=prices[i]-min;
            else if(prices[i]<min)
            min=prices[i];
        }
        return ans;
    }
}