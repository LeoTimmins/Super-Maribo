# A list of useful funtions by Leo Timmins

def reverse(array:list):
    # reverses an array
    newArray = []
    for x in range(len(array)):
        newArray.append(array[-1-x])
    return newArray

if __name__ == "__main__":
    print(reverse([1,2,3,4,5,6,7,8,9,10]))