from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        a = p.map(f, [1, 2, 3])

    print(a)