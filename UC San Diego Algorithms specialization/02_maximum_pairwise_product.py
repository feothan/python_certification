def maximum_pairwise_product(numbers):
    result = 0
    n = len(numbers)
    for i in range(n):
        for j in range(i + 1, n):
            # print(numbers[i], numbers[j])
            # print(numbers[i] * numbers[j])
            if numbers[i] * numbers[j] > result:
                result = numbers[i] * numbers[j]
    return result


if __name__ == '__main__':
    numbers = list(map(int, input().split()))
    result = maximum_pairwise_product(numbers)
    print(result)
