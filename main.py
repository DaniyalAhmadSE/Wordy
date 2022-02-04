from models.wordy import Wordy


def main():
    wordy = Wordy()

    print('\nWORDY v1.02\n')

    choice = ''

    while choice != 'q':

        print("\nEnter 1 to search for a word's meaning")
        print("Enter 2 to add a word to the dictionary")
        print("Enter q to quit\n")

        choice = input('Enter your choice: ')

        if choice == '1':
            word = input('\nEnter the word you want to search for: ')
            result = wordy.search(word)
            if result is not None:
                result.display()
            else:
                print('\nSorry, that word is not in the dictionary.')

        elif choice == '2':
            word = input('\nEnter the word you want to add: ')
            meaning = input('Enter the meaning of the word: ')
            wordy.add(word, meaning)

        elif choice == 'q':
            print('\nGoodbye!\n')
            break

        else:
            print('\nInvalid choice\n')


if __name__ == '__main__':
    main()
