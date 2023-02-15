from django.http import HttpResponse
from django.shortcuts import render

import openai as ai

ai.api_key = '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' # replace with your key from earlier
ingridients = [
    ['Говядина', 'Свинина', 'Баранина', 'Курица', 'Индейка', 'Рыба', 'Морепродукты'],
    ['Грибы', 'Огурцы', 'Помидоры', 'Капуста', 'Морковь', 'Баклажан', 'Кабачок'],
    ['Картофель', 'Рис', 'Макароны', 'Яйца', 'Молоко', 'Сыр', 'Сметана']
];

def index(request):
    
    resp = ''  
    for i in range(len(ingridients)):
        for j in range(len(ingridients[i])):
            ingr = request.GET.get("ingredient"+str(i)+str(j),"")
            if ingr != "":
                resp = resp +' ' + ingridients[i][j]
    if resp != "":
        print(resp)
        response = generate_gpt3_response('Придумай рецепт блюда со следующими ингридиентами:' + resp)
        print(response)
        return HttpResponse(f"<h2>"+response+"</h2>")
    else:
        return render(request, 'static/gpt.html')

def generate_gpt3_response(user_text, print_output=False):
    """
    Query OpenAI GPT-3 for the specific key and get back a response
    :type user_text: str the user's text to query for
    :type print_output: boolean whether or not to print the raw output JSON
    """
    
    #print('Sending request')
    completions = ai.Completion.create(
        #engine='text-ada-001',
        engine='text-davinci-003',  # Determines the quality, speed, and cost.
        temperature=0.5,            # Level of creativity in the response
        prompt=user_text,           # What the user typed in
        max_tokens=1024,             # Maximum tokens in the prompt AND response
        n=1,                        # The number of completions to generate
        stop=None,                  # An optional setting to control response generation
    )
    #print('Getting response')

    # Displaying the output can be helpful if things go wrong
    if print_output:
        print(completions)

    # Return the first choice's text
    return completions.choices[0].text