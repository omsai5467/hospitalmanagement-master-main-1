# class Solution:
#     def twoSum(self, nums: List[], target: int) -> List[int]:
#       #  print(num)
#         #print(target)
#         j = 0
#         s =[]
#         for i in range(len(nums)-1):
#             a = i+1
#             if nums[j] + nums[a] == target :
#                 s.append(j)
#                 s.append(a)
#                 return [j,a]
#                 break
#             j = a 
#             if nums[j] + nums[i] == target:
#                 return [j,i]
#                 break
        
                
nums = [2,8,7,10,6,0]
target = 12

# for i in range(len(nums)-1):
#     for j in range(i+1,len(nums)):
#         a = i+1
#         if nums[j] + nums [a]==target:
#             print(a,j)
for i in range(len(nums)) :
    for j in range(len(nums)-1):
        if nums[i] + nums[j]==target and i != j:
            print(i,j)
            break
    break
