"""
unisex names

for this challenge, you'll be working with the dataset behind this fivethirtyeight article on common unisex names
in the united states. unisex names are gender-neutral and both boys and girls share these names. you'll start by reading
in the data and iteratively converting the data into more useful representations. at the end of this challenge, you'll
filter the names to the ones at least 1000 people share.
"""

file = open("dq_unisex_names.csv",'r')

data = file.read()

data_list = data.split("\n")

first_five = data_list[:5]

print first_five

string_data = [i.split(",") for i in data_list]

numerical_data = [[i[0],float(i[1])] for i in string_data]

thousand_or_greater = [i[0] for i in numerical_data if i[1] >= 1000]