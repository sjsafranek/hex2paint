# hex2paint
convert hex color code to paint color




# colors = [
#     '#ebe7ce',
#     '#bfcc96',
#     '#5c6b4c',
#     '#2e3641',
#     '#4a303d',
#     '#af7180'
# ]





'''

flask run --reload --host=0.0.0.0


import requests

resp = requests.post('http://localhost:5000/api', json={
    'params': {
        'color': '3D747C',
        'sources': [],
        'matches': 4
    }
})

print(resp.text)


'''