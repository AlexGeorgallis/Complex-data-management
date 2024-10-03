#Alexandros Georgalli 5135
import heapq
import time

global males_dict
global valid_count
males_dict = {}
valid_count = 0

def gen_next_male():
    global valid_count
    global males_dict

    with open('males_sorted', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            age = int(parts[1])
            marital_status = parts[8]
            if age < 18 or marital_status.startswith(" Married"):
                continue
            else:
                valid_count += 1
                if age not in males_dict:
                    males_dict[age] = []
                males_dict[age].append(parts)
    return males_dict


def gen_next_female(k):
    global valid_count
    with open('females_sorted', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            age = int(parts[1])
            marital_status = parts[8]
            if age < 18 or marital_status.startswith(" Married"):
                continue
            else:
                valid_count += 1
                yield parts


def top_k_join(k):
    global males_dict
    males_dict = gen_next_male()
    females_gen = gen_next_female(k)

    min_heap = []

    for female in females_gen:
        age = int(female[1])
        if age in males_dict:
            for male in males_dict[age]:
                instance_weight_sum = float(male[25]) + float(female[25])
                if len(min_heap) < k:
                    heapq.heappush(min_heap, (instance_weight_sum, male, female))
                else:
                    if instance_weight_sum > min_heap[0][0]:
                        heapq.heappushpop(min_heap, (instance_weight_sum, male, female))

    return sorted(min_heap, reverse=True)


def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <K>")
        return

    k = int(sys.argv[1])

    start_time = time.time()

    top_k_results = top_k_join(k)

    for i, (score, male, female) in enumerate(top_k_results):
        print(f"{i+1}. pair: {male[0]},{female[0]} score: {score}")

    end_time = time.time() - start_time
    print('Total time:', end_time, 'seconds')
    print('Total valid lines read: ', valid_count)

if __name__ == "__main__":
    main()
