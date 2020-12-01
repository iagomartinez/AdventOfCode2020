import sys

def main():
     with open('../_data/day1_data.txt', 'r',newline='', encoding='utf-8') as f:
        
        nums = []        
        for line in f:
            nums.append(int(line))
        
        for ix in range(0, len(nums)):
            x = nums[ix]
            for iy in range(ix + 1, len(nums)):
                if nums[ix] + nums[iy] == 2020:
                    print(f'Found the two! {nums[ix]} * {nums[iy]} = {nums[ix] * nums[iy]}')
                    break

        for ix in range(0, len(nums)):
            for iy in range(ix + 1, len(nums)):
                for iz in range(iy + 1, len(nums)):
                    if nums[ix] + nums[iy] + nums[iz] == 2020:
                        print(f'Found the three! {nums[ix]} * {nums[iy]} * {nums[iz]} = {nums[ix] * nums[iy] * nums[iz]}')
                        break

if __name__ == '__main__':
    sys.exit(main())