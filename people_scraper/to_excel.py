import pandas as pd

def run():
    file_name = 'cvlac.json'
    df = pd.read_json(file_name)
    df.to_excel('cvlac.xlsx')

if __name__ == '__main__':
    run()