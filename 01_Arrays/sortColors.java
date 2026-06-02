/**
 * Problem Name: Sort Array of 0s, 1s and 2s
 * Link: https://leetcode.com/problems/sort-colors/description/
 * 
 * Approach: Dutch National Flag Algorithm
 * Time Complexity: O(n) - We iterate through the array once.
 * Space Complexity: O(1) - We only use a few variables to keep track of the low, mid, and high pointers.
 */
class Solution {
    public void sortColors(int[] nums) {
        int low=0,mid=0,high=nums.length-1,temp;
        while(mid<=high){
            if(nums[mid]==0){
                temp=nums[low];
                nums[low]=nums[mid];
                nums[mid]=temp;
                mid++;
                low++;
            }
            else if(nums[mid]==1)
            mid++;
            else{
                temp=nums[mid];
                nums[mid]=nums[high];
                nums[high]=temp;
                high--;
            }
        }
    }
}