import requests
from PIL import Image
from io import BytesIO

headers = {
   'x-api-key': '135da4ed-3c90-4ab1-9725-7f62d51cedfe'
}

payload = {
   # 'size': size,
   # 'mime_types': mime_types,
    'order': 'ASC'
   # 'limit': limit,
   # 'page': page,
   # 'category_ids': category_ids,
   # 'format': format
   # 'breed_id': breed_id
}

#returns dict of breed to id mappings
def get_dict_of(type):
   if type == 'breeds' or type == 'categories':
      dict = {}
      try:
         all_of_type = requests.get('https://api.thecatapi.com/v1/' + type, headers = headers).json()
      except: 
         print("Error fetching types")
         exit()
      for i in range (len(all_of_type)):
         dict[all_of_type[i].get('name')] = all_of_type[i].get('id')
      return dict

def set_breed(dict):
   for option in dict.keys():
      print(option)
   chosen_option = input("Pick a breed from the above list: ")
   if chosen_option in dict:
      payload["breed_id"] = dict.get(chosen_option)
   else:
      print("Not a valid choice")
      exit()

def set_category(dict):
   for option in dict.keys():
      print(option)
   chosen_option = input("Pick a category from the above list: ")
   if chosen_option in dict:
      payload['category_ids'] = [dict.get(chosen_option)]
      print("should set payload cateogry")
   else:
      print("Not a valid choice")
      exit()

def search_by_breed():
   dict = get_dict_of('breeds')
   set_breed(dict)

def search_by_category():
   dict = get_dict_of('categories')
   set_category(dict)

def load_page(p, i):
   payload['page'] = p
   try:
      r = requests.get('https://api.thecatapi.com/v1/images/search', headers = headers, params = payload)
   except:
      print("Error fetching next page of images")
   array = r.json()
   print(len(array))

   for j in range (len(array)):
      curr = array[j]
      try: 
         img_r = requests.get(str(curr.get('url')), headers = headers)
         img = Image.open(BytesIO(img_r.content))
         img.save("%scatphoto%d.jpg" % (path, j + i + 1))
      except:
         print("Error fetching images")
   
   #num cats loaded
   return len(array)


def save_cats():
   path = input("Path to the directory where cat photos will be saved (ex. /path/to/my/directory/): ")
   limit = int(input("Limit per page: "))
   payload['limit'] = limit
   by_breed = input("Search by breed? YES or NO: ")
   if by_breed == 'YES':
      search_by_breed()
   else: 
      by_category = input("Search by category? YES or NO: ")
      if by_category  == 'YES':
         search_by_category()

   page = 0
   i = 0
   while load_page(page, i) > 0:
      load_next_page = input("Load next page? YES or NO: ")
      if load_next_page != 'YES':
         break
      else:
         page += 1
         i += limit

option = input("Save cat images (1) or Vote on cats (2)")
if option == '1':
   save_cats()
else:
   exit()


