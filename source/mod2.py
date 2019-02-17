PI = 3.141592

class Math:
    def solv(self, r):
        return PI * (r ** 2)

    def sum(self, a, b):
        return a + b

if __name__ == "__main__":
    print(PI)
    a = Math()
    print(a.solv(2))
    print(a.sum(PI, 4.4))