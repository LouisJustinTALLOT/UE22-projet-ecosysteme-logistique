import ijson
import time

"""
18.765299081802368 s en utilisant directement ijson.parse sur le fichier ouvert     
26.97300958633423  s en lisant le fichier comme string
"""
json_file = "base-sirene.json"
json_shortened_file = "base_sirene_shortened.json"
my_result = "["
with open(json_file, 'r', encoding='utf8') as file:
    json_text = file.read()

    print("là")
    # sirene_objects = ijson.parse(file)
sirene_objects = ijson.parse(json_text)
print("here")
t1 = time.time()

j = 0
# i = 0
for obj in sirene_objects:
    # i += 1

    # if not(i%100000) :
    #     print(i)
    # print(obj)

    if obj == ('item', 'start_map', None):
        my_result += '{'
    elif obj == ('item', 'end_map', None):
        my_result += '},'
        j += 1

    elif obj == ('item', 'map_key', 'fields'):
        my_result += '''"fields":'''

    elif obj == ('item.fields', 'start_map', None):
        my_result += '{'
    elif obj == ('item.fields', 'end_map', None):
        my_result += '},'

    elif (obj[0], obj[1]) == ('item.fields.siret', 'string'):
        my_result += f'''"siret":"{obj[2]}"'''

    elif obj == ('item', 'map_key', 'geometry'):
        my_result += '''"geometry":'''

    elif obj == ('item.geometry', 'start_map', None):
        my_result += '{'
    elif obj == ('item.geometry', 'end_map', None):
        my_result += '}'

    elif obj == ('item.geometry.type', 'string', 'Point'):
        my_result += '''"type":"Point",'''

    elif obj == ('item.geometry', 'map_key', 'coordinates'):
        my_result += '''"coordinates":'''

    elif obj == ('item.geometry.coordinates', 'start_array', None):
        my_result += '['
    elif obj == ('item.geometry.coordinates', 'end_array', None):
        my_result = my_result[:-1]
        my_result += ']'

    elif (obj[0], obj[1]) == ('item.geometry.coordinates.item', 'number'):
        my_result += f'''{obj[2]},'''

    # if i == 379:# 187
    #     break

    if j == 20000:
        break

print(time.time()-t1)
my_result = my_result[:-1]
my_result += "]"
print("writing to file...")
# print(my_result)

with open(json_shortened_file, 'w', encoding='utf8') as file :
    file.write(my_result)

# json_file = "base-sirene.json"
# json_shortened_file = "base_sirene_shortened.json"


# import json

# json_file = "base-sirene.json"
# json_shortened_file = "base_sirene_shortened.json"

# with open(json_file, 'r', encoding='utf8') as file :

#     json_text = file.read()

# print("file read")
# # json_object = json.loads(json_text)
# # print("json object")
# json_object = list(json_text)
# print(json_object[:2])
# print("json dict")
# ## print(len(str(json_object)))
# ## print(json_object[0]['fields'])

# # for i, item in enumerate(json_object):
# #     item['fields'].pop('efetcent', None)
# #     item['fields'].pop('libtu', None)
# #     item['fields'].pop('libreg_new', None)
# #     item['fields'].pop('ind_publipo', None)
# #     item['fields'].pop('tefet', None)
# #     item['fields'].pop('moden', None)
# #     item['fields'].pop('l7_normalisee', None)
# #     item['fields'].pop('comet', None)
# #     item['fields'].pop('rpet', None)
# #     item['fields'].pop('depet', None)
# #     item['fields'].pop('arronet', None)
# #     item['fields'].pop('date_maj', None)
# #     item['fields'].pop('liborigine', None)
# #     item['fields'].pop('libmodet', None)
# #     item['fields'].pop('libtca', None)
# #     item['fields'].pop('libnj', None)
# #     item['fields'].pop('code_section', None)
# #     item['fields'].pop('auxilt', None)
# #     item['fields'].pop('siret', None)
# #     item['fields'].pop('dapet', None)
# #     item['fields'].pop('dcret', None)
# #     item['fields'].pop('categorie', None)
# #     item['fields'].pop('libactivnat', None)
# #     item['fields'].pop('datemaj', None)
# #     item.pop("datasetid", None)
# #     item.pop("recordid", None)
# #     item.pop("record_timestamp", None)


# # print(json_object[0]['fields'])


# # print(len(str(json_object)))


# json_result = json.dumps(json_object)
# print("json result")
# # print(json_result)

# with open(json_shortened_file, 'w', encoding='utf8') as file :
#     file.write(json_result)

# print("done")
