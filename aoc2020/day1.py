import sys

def main():
     with open('../_data/day1_data.txt', 'r',newline='', encoding='utf-8') as f:
        
        nums = []        
        for line in f:
            nums.append(int(line))
        

if __name__ == '__main__':
    sys.exit(main())