import pandas as pd


# File ID obtained from the Google Drive sharing link
file_id = '1JMYqXipZpz9Y5-vyxvLEO2Y1sRBxqu-U'
url = f'https://drive.google.com/uc?id={file_id}'

# Reading the CSV file
data = pd.read_csv(url)


# # Прочитати файл
# data = pd.read_csv('2017_jun_final.csv')

# Вивести перші декілька рядків
print(data.head())

# Розмір таблиці
print("Розмір таблиці:", data.shape)

# Типи стовпців
print("Типи стовпців:")
print(data.dtypes)

# Частка пропусків у кожному стовпці
missing_percentages = data.isnull().sum() / len(data) * 100
print("Частка пропусків у кожному стовпці:")
print(missing_percentages)
#
# Видалити стовпці з пропусками, крім "Язык.программирования"
data_cleaned = data.dropna(subset=['Язык.программирования'], inplace=False)

print(data_cleaned)

# Частка пропусків після видалення
missing_percentages_cleaned = data_cleaned.isnull().sum() / len(data_cleaned) * 100
print("Частка пропусків після видалення:")
print(missing_percentages_cleaned)

# # Видалити рядки з пропусками
# data_cleaned = data_cleaned.dropna()
# print(data_cleaned)

# Розмір після видалення рядків
print("Розмір після видалення рядків:", data_cleaned.shape)
#
# Відібрати дані для Python
python_data = data_cleaned[data_cleaned['Язык.программирования'] == 'Python']
print(python_data)
#
# Розмір таблиці python_data
print("Розмір таблиці python_data:", python_data.shape)
#
# Групування за стовпцем "Посада"
grouped_data = data_cleaned.groupby('Должность')
# Агрегація мінімальної та максимальної зарплати за посадою
aggregated_data = grouped_data.agg({'Зарплата.в.месяц': ['min', 'max']})
print(aggregated_data)


# Функція для обчислення середньої зарплати
def fill_avg_salary(group):
    avg_salary = group['Зарплата.в.месяц'].mean()
    group['avg'] = avg_salary  # Додати стовпчик "avg" до групи
    return group


# Додати новий стовпчик "avg"
data_cleaned_with_avg = grouped_data.apply(fill_avg_salary)


# Описова статистика для нового стовпчика
print(data_cleaned_with_avg['avg'].describe())
#
# Зберегти дані у CSV файл
data_cleaned_with_avg.to_csv('data_with_avg.csv', index=False)
