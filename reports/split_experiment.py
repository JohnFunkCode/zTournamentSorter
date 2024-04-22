
import pandas as pd

def split_experiment(df, ring_info):
    print(type(ring_info))
    for info in ring_info:
        ring = info.get('ring')
        starting_letter = info.get('startingLetter')
        ending_letter = info.get('endingLetter')
        # Extract the first letter of the 'Last_Name' column
        df['First_Letter'] = df['Last_Name'].str[0]

        # Apply the conditions on the 'First_Letter' column
        df_filtered = df[(df['First_Letter'] >= starting_letter) & (df['First_Letter'] <= ending_letter) | (df['First_Letter'] >= starting_letter.lower()) & (df['First_Letter'] <= ending_letter.lower())]
        # df_filtered = df[(df['First_Letter'] >= starting_letter) & (df['First_Letter'] <= ending_letter) ]

        print(f'Ring {ring} {starting_letter} - {ending_letter}, has {df_filtered.shape[0]} rows')

        print(f'Ring {ring}: {df_filtered.sort_values('Last_Name').to_string()}\n')
    print('Done')



if __name__ == "__main__":
    # create a test data frame with what we will get passed
    columns = ['index', 'First_Name', 'Last_Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
               'Weight',
               'BMI', 'Events', 'Weapons']
    data = [(255, 'Lucas', 'May', 'Male', 'CO- Parker', 10, 'Yellow', 4, 3, '4 ft. 3 in.', 52, 154,
             '2 Events - Forms & Sparring ($75)', 'None'),
            # (195, 'Katie', 'Coleson', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
            #  '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Angela', 'Payne', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Emily', 'Nielsen', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Alec', 'harbaugh', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'MJ', 'Ortiz', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Arav', 'Lukhey', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Jacob', 'Gibberson', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Angelique', 'Hutchins', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Malakai', 'Ruybal', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Visha', 'Hari', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Margaret', 'Buttery', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Constanta', 'Diaz Martinez', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Akshith', 'Naveenkumar', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Kalpak', 'Shankaregowda', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Emerson', 'Colwell', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Jeffery Jr', 'Merriman', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Farah', 'Mohamed-Sadik', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Joshua', 'Betournay', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Anirudh', 'Maheshkumar', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)'),
            (195, 'Maria Jose', 'Acevedo Peck', 'Female', 'CO- Cheyenne Mountain', 12, 'Yellow', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)')]
    df = pd.DataFrame(data, columns=columns)

    ring_info = [{'ring': 1, 'startingLetter': 'A', 'endingLetter': 'H'},
                 {'ring': 1, 'startingLetter': 'I', 'endingLetter': 'P'},
                 {'ring': 2, 'startingLetter': 'Q', 'endingLetter': 'Z'}]

    rings = [info['ring'] for info in ring_info]

    split_experiment(df, ring_info)
