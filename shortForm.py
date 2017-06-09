w_dic = {'example': 'eg', 'Example': 'eg', 'important': 'imp', 'Important': 'Imp',
             'mathematics': 'math', 'Mathematics': 'Math', 'algorithm': 'algo',
             'Algorithm': 'Algo', 'frequency': 'freq', 'Frequency': 'Freq', 'input': 'i/p',
             'Input': 'i/p', 'output': 'o/p', 'Output': 'o/p', 'software': 's/w', 'Software': 's/w',
             'hardware': 'h/w', 'Hardware': 'h/w', 'network': 'n/w', 'Network': 'n/w', 'machine learning': 'ML',
             'machine Learning': 'ML', 'Machine learning': 'ML', 'Machine Learning': 'ML', 'Data Mining': 'DM',
             'Data mining': 'DM', 'data Mining': 'DM', 'data mining': 'DM', 'database': 'DB', 'Database': 'DB',
             'management': 'mgmt', 'Management': 'mgmt', 'Artificial Intelligence': 'AI', 'artificial Intelligence': 'AI',
             'Artificial intelligence': 'AI', 'artificial intelligence': 'AI', 'laptop': 'LP', 'Computer Science': 'CS'}

def shortF(text):
    def replace_all(text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
            print (text)
        return text



    text = replace_all(text, w_dic)

    # print result
    return text

