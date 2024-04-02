# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.


    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import pandas as pd

    df = pd.concat([pd.read_csv("./Data/busdata2022.csv"),pd.read_csv("./Data/busdata2023.csv"),pd.read_csv("./Data/busdata2024.csv")])
    print(df.columns)
    print(df['Saturday - 19:00-23:59'].mean())
    print(df['Saturday - 19:00-23:59'].std())
    #print(df['OperationSince'].unique())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
