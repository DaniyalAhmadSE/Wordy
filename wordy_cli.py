from utils.wordy_api import WordyApi


def launch_cli():
    wordy_api = WordyApi(gui_mode=False)

    print('\nWORDY v1.02\n')

    choice = ''

    while choice != 'q':

        print("\nEnter 1 to search for a word")
        print("Enter 2 to add a word")
        print("Enter q to quit\n")

        choice = input('Enter your choice: ')

        if choice == '1':
            word = input('\nEnter the word you want to search for: ')
            result = wordy_api.search(word)
            print('\n' + result)

        elif choice == '2':
            word = input('\nEnter the word you want to add: ')
            meaning = input('Enter the meaning of the word: ')
            if wordy_api.add(word, meaning):
                print('Word added Successfully')
            else:
                print('Word already exists')

        elif choice == 'q':
            print('\nGoodbye!\n')
            break

        else:
            print('\nInvalid choice\n')


if __name__ == "__main__":
    launch_cli()
