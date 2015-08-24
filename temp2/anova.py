"""lines = ["the cow ate the grass", "the man ran", 
         "the man ate the cow", "the cow ran over the man"]"""

lines = ['RT @JmeBBK: I call him Oluwababaskepta RT @Iborinho: @JmeBBK Do you call your brother by his name or do you call him Skepta', '@BI_Sports if anyone on the cavs deserves a max besides bron its tristan. No idea what everyone else is thinking.', 'RT @flauntingniall: HE GOES "YOU KNOW HES GUNNA BE A DAD" AND VERY FAINTLY YOU HEAR "NO IM NOT" THIS IS APPARENTLY WHAT HAPPENED http://t.c\u2026','RT @abscbndotcom: On The Wings Of Love August 11, 2015 Teaser: http://t.co/TNstJqyZv2 via @YouTube',  'why have abs when u can have kebabs','RT @CurtisBebro: "i wouldn\'t date a trans woman" boy these women wouldn\'t date you in your dreams http://t.co/PrGZhu2ZDc', 'A bottle fell off my bedside table and I go "OH FUCK YOU, YOU STUPID FUCKING CUNT!" like im so angry bc im tired gn bye outtie']

data = {}
num_tweets = 0 
for i, sentence in enumerate(lines):
    sentence = sentence.lower()
    words = sentence.split()
    num_tweets += 1
    for word in words:
        try:
            data[word]['num'] += 1
        except KeyError:
            data[word] = {'num':1}
        try:
            data[word][i] += 1
        except KeyError:
            data[word][i] = 1

for word in data:
    data[word]['mean'] = float(data[word]['num'])/num_tweets 
    tot = 0
    for i in range(num_tweets):
        temp = 0
        try:
            temp += data[word][i]
        except KeyError:
            pass
        tot += (temp - data[word]['mean'])**2
    data[word]['var'] = (1.0/(num_tweets - 1))*tot

for word in data:
    print word, data[word]['mean'], data[word]['var']

for i in range(num_tweets):
    print i
    words = lines[i].lower().split()
    temp = {}
    for word in words:
        try:
            temp[word] += 1
        except KeyError:
            temp[word] = 1
    for word in temp:
        p = float(temp[word] - data[word]['mean'])/(data[word]['var']**0.5)
        print word, p

    
    
    


    
    
