import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please choose a city to investigate.  You can search for Chicago, New York City, or Washington.\n").lower()

    while city not in CITY_DATA.keys():
        print('The city you chose is not a valid option.')
        city = input("Please choose a city to investigate.  You can search for \'Chicago\', \'New York City\', or \'Washington\'.\n").lower()

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

    while True:
        month = input('Which month would you like to investigate?  Select \'january\', \'february\', \'march\', \'april\', \'may\', or \'june\'.  You can also search \'all\' to apply no monthly filter.\n').lower()
        if month in months :
            break
        else:
            print('The month you chose was not a valid option.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

    while True:
        day = input('Please choose a day of the week.  You can also select \'all\' to apply no daily filter.\n').lower()
        if day in days:
            break
        else:
            print('The day of week you chose was not valid, please try again.')


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month for bikeshare activity is the {}th'.format(df['month'].mode()[0]))

    # display the most common day of week
    print('The most common day for bikeshare activity is {}'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('The most common hour for bikeshare activity is the {}th'.format(df['hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used station to start a ride is {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used station to end a ride is {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ", " + df['End Station']
    print('The most commonly used route for bikeshare activity is {}'.format(df['route'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time was',(df['Trip Duration'].sum()).round())
    print('seconds.')

    # display mean travel time
    print('The average travel time was',(df['Trip Duration'].mean()).round())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts().to_frame())

    # Display counts of gender
    if city != 'Washington':
        print(df['Gender'].value_counts().to_frame())

    # Display earliest, most recent, and most common year of birth
        print('The oldest bikeshare rider was born in ',int(df['Birth Year'].min()))
        print('The youngest bikeshare rider was born in ',int(df['Birth Year'].max()))
        print('The most common birth year for bikeshare rides was ',int(df['Birth Year'].mode()[0]))

    else:
        print('There is no gender statistics for this city')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    ind = 0
    user_input = input('Would you like to see some raw data, yes or no?  The data will be displayed 5 rows at a time.').lower()
    if user_input not in ['yes', 'no']:
        print('Your input was invalid')
        user_input = input('Would you like to see some raw data, yes or no?  The data will be displayed 5 rows at a time.').lower()
    elif user_input != 'yes':
        print('Ok, no raw data will be displayed')

    else:
        while ind + 5 < df.shape[0]:
            print(df.iloc[ind:ind+5])
            ind += 5
            user_input = input('Would you like 5 more rows of raw data? Please choose yes or no.').lower()
            if user_input != 'yes':
                print('Ok, no additional rows of raw data will be displayed')
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
