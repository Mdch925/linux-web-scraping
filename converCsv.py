import pandas

# data = pandas.DataFrame({
#     'Name': ['Ali', 'Sara', 'John'],
#     'Age': [20, 22, 21]
# })

# print(data)
# print (dir(pandas))

# print("hello")

my_data = pandas.read_csv("points.txt")

# print(my_data)

my_data.to_csv("points.csv", index=None)
