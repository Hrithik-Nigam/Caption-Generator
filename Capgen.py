# We have to clone parrot paraphraser and install protobuf using the pip commands given below from the terminal 
# pip install git+https://github.com/PrithivirajDamodaran/Parrot_Paraphraser.git
# pip install protobuf

def generate(pth):
    import requests
    import json
    import torch
    import warnings
    from parrot import Parrot
    import pandas as pd

    warnings.filterwarnings("ignore")

    endpoint = 'The link for your API inside the resource on Microsoft Azure Cognitive Services.'
    subscription_key = 'Enter the subscription key for your API here'

   
    headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': subscription_key}
    params = {'visualFeatures': 'Description', 'language': 'en'}

  
    imgPath = pth
    img = open(imgPath,'rb').read()

   
    response = requests.post(endpoint + '/vision/v3.2/analyze', headers=headers, params=params, data=img)
    response_json = json.loads(response.text)
   
    caption = response_json['description']['captions'][0]['text']

    if caption == 'graphical user interface':
        cap='Read the text in the image.'

    else:
        cap = caption.capitalize()
    
    def random_state(seed):
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

    parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)
    random_state(1234)

    para_list=[]
    phrases = []
    phrases.append(cap)

    for phrase in phrases:
        para_phrases = parrot.augment(input_phrase=phrase, do_diverse=True)
        for para_phrase in para_phrases:
            temp=para_phrase[0]
            if temp not in para_list:
                para_list.append(temp.capitalize())
    
    return para_list
