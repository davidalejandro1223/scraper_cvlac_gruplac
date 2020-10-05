import pandas as pd

def run():
    file_name = 'gruplac.json'
    df = pd.read_json(file_name)
    df.to_excel('gruplac.xlsx')

if __name__ == '__main__':
    run()