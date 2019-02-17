def sum(a, b):
    return a+b

def safe_sum(a, b):
    if type(a) != type(b):
        print("자료형이 다르므로 계산할 수 없습니다.")
        return
    else:
        result = sum(a, b)

    return result

# main 함수 만들기
if __name__ == "__main__":
    print(sum(3, 4))
    print(safe_sum(3, 4))
    print(safe_sum(3, 'a'))
