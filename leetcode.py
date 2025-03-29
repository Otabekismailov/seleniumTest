# 1. Two Sum
from itertools import count
from typing import List, Optional

from jinja2.lexer import newline_re


def twoSum(nums: list, target: int) -> [int]:
    if nums is None:
        return nums
    indices = []
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                indices.append(i)
                indices.append(j)
                return indices
    return indices


# 121. Best Time to Buy and Sell Stock
def maxProfit(prices) -> int:
    if not prices:
        return 0
    max_list = 0
    min_list = float('inf')
    for item in prices:
        min_list = min(min_list, item)
        min_ = item - min_list
        max_list = max(max_list, min_)
    return max_list


# print(maxProfit([1, 2, 4]))


def containsDuplicate(nums) -> bool:
    is_bool = False
    nums_len = len(nums)
    diffrence_ = len(set(nums))
    if nums_len != diffrence_:
        is_bool = True
    return is_bool


# print(containsDuplicate([1, 2, 3]))


# 238. Product of Array Except Self


def productExceptSelf(nums):
    nums_len = len(nums)
    new_nums = [1] * nums_len
    for item in range(1, nums_len):
        new_nums[item] = new_nums[item - 1] * nums[item - 1]
    pref = 1
    for i in range(nums_len - 1, -1, -1):
        new_nums[i] *= pref
        pref *= nums[i]
    return new_nums


"""
 :return [24,12,8,6]
"""


# print(productExceptSelf([1, 2, 3, 4]))


# 53. Maximum Subarray


def maxSubArray(nums):
    n = len(nums)
    maxSum = -1e8  # TODO BU  Eng katta manfiy soni olib beradi
    currSum = 0

    for i in range(0, n):
        currSum = currSum + nums[i]
        if (currSum > maxSum):
            maxSum = currSum
        if (currSum < 0):
            currSum = 0

    return maxSum


"""
 :return 6
"""


# print(maxSubArray([-2,1,-3,4,-1,2,1,-5,4]))


def maxProduct(nums) -> int:
    if len(nums) == 0:
        return 0
    n = len(nums)
    maxSum = nums[0]
    minSum = nums[0]
    ns = maxSum
    for i in range(1, n):
        curr = nums[i]
        re = max(curr, maxSum * curr, minSum * curr)
        minSum = min(curr, maxSum * curr, minSum * curr)
        maxSum = re
        ns = max(maxSum, ns)
    return ns


# # [-2,0,-1] [2,3,-2,4] [-3,-1,-1] [2,3,-2,4] [-2,3,-4]
# print(maxProduct([-3,-1,-1]))


# Bosqichlar quyidagicha:

#

# 2 ta ko'rsatkichni, ya'ni past va baland ko'rsatkichni joylashtiring: Dastlab biz ko'rsatkichlarni shunday joylashtiramiz: past birinchi indeksga, yuqori esa oxirgi indeksga ishora qiladi.

# "O'rta" ni hisoblang: Endi tsikl ichida "o'rta" qiymatini quyidagi formuladan foydalanib hisoblaymiz:

# o'rta = (past+yuqori) // 2 ( '//' butun son bo'linishini bildiradi)

# arr[mid] == target ekanligini tekshiring: Agar shunday bo'lsa, indeksni o'rtaga qaytaring.

# Tartiblangan yarmini aniqlang, maqsad qayerda joylashganligini tekshiring va shunga mos ravishda yarmini yo'q qiling:


# 1. if arr[low] <= arr[mid]: Bu shart chap qismning tartiblanganligini ta'minlaydi.


# a. If arr[low] <= target && target <= arr[mid]: Bu maqsadning tartiblangan yarmida ekanligini bildiradi. Shunday qilib, biz o'ng yarmini (yuqori = o'rta-1) yo'q qilamiz.


# b. Aks holda, tartiblangan yarmida maqsad mavjud emas. Shunday qilib, biz bu chap yarmini past = o'rta + 1 qilish orqali yo'q qilamiz.


# 2. Aks holda, o'ng yarmi tartiblangan bo'lsa:
# a. If arr[mid] <= target && target <= arr[high]: Bu maqsadning tartiblangan o'ng yarmida ekanligini bildiradi. Shunday qilib, biz chap yarmini yo'q qilamiz (past = o'rta + 1).
# b. Aks holda, bu tartiblangan yarmida maqsad mavjud emas. Shunday qilib, biz bu o'ng yarmini yuqori = o'rta-1 qilish orqali yo'q qilamiz.
# Bir marta, "o'rta" maqsadni ko'rsatsa, indeks qaytariladi.
# Bu jarayon halqa ichida bo'ladi va pastadir xochlar baland bo'lguncha pastadir davom etadi. Agar indeks topilmasa, biz -1 ni qaytaramiz.


class So:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1


# obj = So()
# # [4, 5, 6, 7, 0, 1, 2]
# print(obj.search([1, 3], 0))


def moveZeroes(nums: List[int]):
    new = []

    for index in range(len(nums) - 1, -1, -1):
        if nums[index] == 0:
            new.append(nums[index])
            nums.remove(nums[index])
    nums.extend(new)
    return nums


# print(moveZeroes([0, 1, 0, 3, 12]))
# 20. Valid Parentheses
def isValid(s: str) -> bool:
    # ke_1 = s.count('(', ) + s.count('{') + s.count('[') + s.count(']', ) + s.count('}') + s.count(')')
    stack = []
    for c in s:
        if c in ['(', '{', '[']:
            stack.append(c)
        elif c == ')' and len(stack) != 0 and stack[-1] == '(':
            stack.pop()
        elif c == '}' and len(stack) != 0 and stack[-1] == '{':
            stack.pop()
        elif c == ']' and len(stack) != 0 and stack[-1] == '[':
            stack.pop()
        else:
            return False
    return stack == []


# print(isValid("(){}}{"))


def isPalindrome(s: str) -> bool:
    r = ''
    for i in s.lower():
        if i.isalnum():
            r += i
    return r.startswith(r[::-1])


# print(isPalindrome("A man, a plan, a canal: Panama"))
# print(isPalindrome("0P"))
# print(isPalindrome("race a car"))


# 88. Merge Sorted Array
def merge(nums1: List[int], m: int, nums2: List[int], n: int):
    new = nums1.copy()
    nums1.clear()
    nums1.extend(new[:m])
    nums1.extend(nums2[:n])
    nums1.sort()


# nums1 = [1]
# m = 1
# nums2 = []
# n = 0
# print(merge(nums1, m, nums2, n))


class LinkenList:
    def __init__(self):
        self.head = None

    class Node:
        def __init__(self, val=0):
            self.val = val
            self.next = None
            self.end = None

    def append(self, data):
        new_node = self.Node(data)
        if not self.head:
            self.head = new_node
            self.end = new_node
            return
        # self.end.next = new_node
        # self.end = new_node

        #  BU SEKIN ISHLAY ANCHA
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def reverse(self):
        prev = None
        curr = self.head
        while curr:
            next_node = curr.next

            curr.next = prev

            prev = curr

            curr = next_node

        self.head = prev

    def hasCycle(self) -> bool:
        fast = self.head
        while fast and fast.next:
            self.head = self.head.next
            fast = fast.next.next
            if self.head is fast:
                return True
        return False

    def removeNthFromEnd(self, n: int):
        curr,res = self.head,self.head
        count = 0
        while curr.next:
            count += 1
            curr = curr.next
            if count == n:
                if res.next.next is not None:
                 curr.next = res.next.next
            elif count != n:
                return []
        self.head.next = res.next



    def print_list(self):
        current = self.head
        while current:
            print(current.val, end=" ")
            current = current.next
        print()

    def print_to_list(self):
        result = []
        current = self.head

        while current:
            result.append(current.val)
            current = current.next
        return result


# Input data
lists = [1,2]

n = 1
# Create and populate the linked list
obj = LinkenList()
for val in lists:
    obj.append(val)

# obj.append()
# Print the original list
print("Original Linked List:")
obj.print_list()


obj.removeNthFromEnd(2)
# Reverse the linked list
# obj.reverse()
# print(obj.hasCycle())
# Print the reversed list as a Python list
print("Reversed List as Python List:")
print(obj.print_to_list())
