import sqlite3

def read_from_database():
    connection = sqlite3.connect('pv_results.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM max_power_results')
    results = cursor.fetchall()
    connection.close()

    return results

def main():
  
    results_from_db = read_from_database()
    for result in results_from_db:
        temperature, radiation, max_power = result
        print(f'Temperature: {temperature}, Radiation: {radiation}, Max Power: {max_power:.2f} W')

if __name__ == '__main__':
    main()