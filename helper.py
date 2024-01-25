import pandas as pd
import config

def append_to_excel(filename, data, sheet_name='Sheet1'):
    """
    Append data to an existing Excel file.

    :param filename: str, the path to the Excel file
    :param data: DataFrame or dict, the new data to append
    :param sheet_name: str, the name of the sheet to append to (default is 'Sheet1')
    """
    print('filename: ', filename)
    print('writing started...')
    # Try to open the existing Excel file
    try:
        # Read the existing data
        existing_data = pd.read_excel(filename, sheet_name=sheet_name, engine='openpyxl')
    except FileNotFoundError:
        # If the file does not exist, create an empty DataFrame
        existing_data = pd.DataFrame()

    # Convert the new data to a DataFrame if it is not already one
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    # Append the new data
    updated_data = existing_data._append(data, ignore_index=True)

    # Write the updated DataFrame back to the Excel file
    with pd.ExcelWriter(filename, mode='w', engine='openpyxl') as writer:
        updated_data.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print('writing finished...')

# Example usage
# new_data = {'column1': [1, 2, 3], 'column2': ['A', 'B', 'C']}
# append_to_excel(config.xlsx_path, new_data)



def backup_append_to_csv(filename, data):
    """
    Append data to an existing CSV file.

    :param filename: str, the path to the CSV file
    :param data: DataFrame or dict, the new data to append
    """
    print('filename: ', filename)
    print('writing to backup csv started...')

    # Convert the new data to a DataFrame if it is not already one
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    # Append the new data to the CSV file
    # If the file does not exist, it will be created
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        data.to_csv(f, header=f.tell()==0, index=False)

    print('writing to backup csv finished...')


def append_to_csv(filename, data):
    """
    Append data to an existing CSV file.

    :param filename: str, the path to the CSV file
    :param data: DataFrame or dict, the new data to append
    """
    print('filename: ', filename)
    print('writing started...')

    # Convert the new data to a DataFrame if it is not already one
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    # Append the new data to the CSV file
    # If the file does not exist, it will be created
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        data.to_csv(f, header=f.tell()==0, index=False)

    print('writing finished...')

# Example usage
# new_data = {'column1': [1, 2, 3], 'column2': ['A', 'B', 'C']}
# append_to_csv(config.csv_path, new_data)
