#Alexandros Georgalli 5135
import heapq
import time

global valid_count
valid_count = 0

def gen_next_male():
    global valid_count
    with open('males_sorted', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            age = int(parts[1])
            marital_status = parts[8]
            if age < 18 or marital_status.startswith(" Married"):
                continue
            valid_count += 1
            yield parts


def gen_next_female():
    global valid_count
    with open('females_sorted', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            age = int(parts[1])
            marital_status = parts[8]
            if age < 18 or marital_status.startswith(" Married"):
                continue
            valid_count += 1
            yield parts


def top_k_join():
    males_gen = gen_next_male()
    females_gen = gen_next_female()

    males_dict = {}
    females_dict = {}
    max_heap = []

    p1_max = p1_cur = p2_max = p2_cur = 0
    counter = 0

    while True:
        if counter % 2 == 0:
            try:
                male = next(males_gen)
            except StopIteration:
                break
            age = int(male[1])
            instance_weight = float(male[25])
            p1_cur = instance_weight
            if p1_cur > p1_max:
                p1_max = p1_cur
            if age not in males_dict:
                males_dict[age] = []
            males_dict[age].append(male)
            if age in females_dict:
                for female in females_dict[age]:
                    score = float(male[25]) + float(female[25])
                    heapq.heappush(max_heap, (-score, male, female))
        else:
            try:
                female = next(females_gen)
            except StopIteration:
                break
            age = int(female[1])
            instance_weight = float(female[25])
            p2_cur = instance_weight
            if p2_cur > p2_max:
                p2_max = p2_cur
            if age not in females_dict:
                females_dict[age] = []
            females_dict[age].append(female)
            if age in males_dict:
                for male in males_dict[age]:
                    score = float(male[25]) + float(female[25])
                    heapq.heappush(max_heap, (-score, male, female))

        T = max((p1_max + p2_cur), (p2_max + p1_cur))

        while len(max_heap) > 0 and -max_heap[0][0] >= T:
            yield heapq.heappop(max_heap)

        counter += 1


def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python meros1.py <K>")
        return

    k = int(sys.argv[1])

    start_time = time.time()

    top_k_gen = top_k_join()

    for i in range(k):
        top_k_result = next(top_k_gen)
        score = -top_k_result[0]
        male_id = top_k_result[1][0]
        female_id = top_k_result[2][0]
        print(f"{i+1}. pair: {male_id},{female_id} score: {score}")

    end_time = time.time() - start_time
    print('Total time:', end_time, 'seconds')
    print('Total valid lines read: ', valid_count)

if __name__ == "__main__":
    main()
