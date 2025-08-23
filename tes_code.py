import re
self = "self.dimens = dimens,self.text_on = text_on,self.text_off = text_off,self.text_on  = text_on,self.color_off = color_off,self.color_on = color_on,self.textcoloron = textcoloron,self.textcoloroff = textcoloroff,self.my_border_radius = my_border_radius"
other = self.replace("self","other")


self_waste  = re.findall(r" = \w+",self)
other_waste = re.findall(r" = \w+",other)
for waste in self_waste:
    self=self.replace(waste,"")
for waste in other_waste:
    other=other.replace(waste,"")

self_list = self.split(",")
other_list = other.split(",")

new_code = str()
for a,b in zip(self_list,other_list):
    new_code+=f"{a+b},"
# print(self)

my_dict = {"test":0,"test2":0,"test3":1}
print(not any(my_dict.values()))



