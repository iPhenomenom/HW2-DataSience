%matplotlib inline
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns

# Завантаження вмісту сторінки
url = 'https://uk.wikipedia.org/wiki/Населення_України'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Знаходження таблиць на сторінці
tables = soup.find_all('table', {'class': 'wikitable'})

# Виведення першої знайденої таблиці
first_table = tables[6]
dataframe_list = pd.read_html(str(first_table), header=0)
if dataframe_list:
    first_dataframe = dataframe_list[0]

    # Заміна "—" на pd.NA
    first_dataframe.replace("—", pd.NA, inplace=True)

    # Заміна типів колонок (крім "Регіон")
    for column in first_dataframe.columns:
        if column != 'Регіон' and first_dataframe[column].dtype == object:
            first_dataframe[column] = pd.to_numeric(first_dataframe[column], errors='coerce')





    print("Перші рядки таблиці:")
    print(first_dataframe.head())

    # Видалення останнього рядка
    first_dataframe.drop(first_dataframe.index[-1], inplace=True)
    print("Таблиця після видалення останнього рядка:")
    print(first_dataframe)

    # # Заміна відсутніх значень середніми значеннями
    first_dataframe.fillna(first_dataframe.mean(), inplace=True)
    print("Таблиця після заміни відсутніх значень:")
    print(first_dataframe)

    # # Обчислення часток пропусків у кожній колонці
    missing_ratios = first_dataframe.isnull().sum() / len(first_dataframe) * 100
    print("Частки пропусків в кожній колонці:")
    print(missing_ratios)


    # Визначення кількості рядків та стовпців у датафреймі
    num_rows, num_columns = pd.read_html(str(first_table), header=0)[0].shape
    print("Кількість рядків:", num_rows)
    print("Кількість стовпців:", num_columns)

    # Визначення типів стовпців
    column_types = first_dataframe.dtypes
    print("Типи стовпців:")
    print(column_types)

    average_birth_rate_2019 = first_dataframe['2019'].mean()
    regions_above_average = first_dataframe[first_dataframe['2019'] > average_birth_rate_2019]

    list_of_regions_above_average = regions_above_average['Регіон'].tolist()

    print("Список регіонів з народжуваністю вищою за середню у 2019 році:", list_of_regions_above_average)



    max_birth_rate_row = first_dataframe[first_dataframe['2014'] == first_dataframe['2014'].max()]
    region_with_highest_birth_rate = max_birth_rate_row['Регіон'].values[0]

    print("Регіон з найвищою народжуваністю у 2014 році:", region_with_highest_birth_rate)


    # Вибираємо дані для побудови діаграми
    regions = first_dataframe['Регіон']
    birth_rates_2019 = first_dataframe['2019']

    # Побудова стовпчикової діаграми
    plt.figure(figsize=(10, 6))
    plt.bar(regions, birth_rates_2019)
    plt.xlabel('Регіон')
    plt.ylabel('Народжуваність у 2019 році')
    plt.title('Народжуваність по регіонах у 2019 році')
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Показати діаграму
    plt.show()
else:
    print("Таблиця не знайдена")

# Побудова графіка 1: Графік розкиду між двома роками
plt.figure(figsize=(8, 6))
sns.scatterplot(data=first_dataframe, x='2014', y='2019', color='purple')
plt.xlabel('Народжуваність у 2014 році')
plt.ylabel('Народжуваність у 2019 році')
plt.title('Графік розкиду між роками')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()



# Побудова графіка 3: Графік розподілу народжуваності за 2019 рік
plt.figure(figsize=(10, 6))
sns.histplot(data=first_dataframe, x='2019', bins=20, color='orange', kde=True)
plt.xlabel('Народжуваність у 2019 році')
plt.ylabel('Частота')
plt.title('Розподіл народжуваності за 2019 рік')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()