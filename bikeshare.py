import time
import pandas as pd
import numpy as np
import calendar
# Dictionary contains name of files that
# will be used in project
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    cities = ['chicago', 'new york city', 'washington']
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'sunday', 'monday', 'tuesday',
            'wednesday', 'thursday', 'friday', 'saturday']
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(
            'Select city by name to analyze\n1.Chicago\n2.New York City\n3.Washington\n').lower()
        if city not in cities:
            print('>>>> Warning: Enter a valid city name <<<<')
            continue
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            'Select month by name from january until june to filter , or all to apply no month filter\n').lower()
        if month not in months:
            print('>>>> Warning: Enter a valid month name <<<<')
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            'Select one day by name from the week to filter, or "all" to apply no day filter\n').lower()
        if day not in days:
            print('>>>> Warning: Enter a valid day name <<<<')
            continue
        else:
            break

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
    # first we load data file
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month is:\n', calendar.month_name[common_month])

    # TO DO: display the most common day of week
    common_weekday = df['day_of_week'].mode()[0]
    print('Common day of the week:\n', common_weekday)

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Common start hour is:\n', str(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_used_start_station = df['Start Station'].value_counts().head(
        1).idxmax()
    print('Most commonly used start station:\n', most_used_start_station)

    # TO DO: display most commonly used end station
    most_used_end_station = df['End Station'].value_counts().head(1).idxmax()
    print('\nMost commonly used end station:\n', most_used_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    comb = df.groupby(['Start Station', 'End Station']).count()
    print('\nMost common stations Start & End:\n',
          most_used_start_station, ' & ', most_used_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: ', total_travel_time/(24*60*60), ' Days')

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    minutes = mean_travel_time / 60
    print('\nMean travel time: ', minutes, ' Per Minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('Display counts of user types\n', user_types_count)

    # some files have missing data such as (gender and birth year)
    # which will casue error and crash our program
    # so I used exception to avoid the problem
    try:
        # TO DO: Display counts of gender
        gender_count = df['Gender'].value_counts()
        print('\nGender Counts:\n', gender_count)
    except:
        print("\nNo data avaliable for gender in this month")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].mode()[0]
        string = '\nMost common birth year: {}\nMost recent birth year: {}\nEarliest birth year: {}'
        print(string.format(common, recent, earliest))
    except:
        print('\nNo data abaliable for birth year in this month\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def more_row_of_data(df, num_of_rows):
    """Displays more statistics on bikeshare users based on user wish"""
    rows_of_data = df.head(num_of_rows)
    print(rows_of_data)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        row_of_data = df.head()
        print(row_of_data)
        num_of_rows = int(
            input("Want to see more rows? Please enter number of rows you want to see\n"))
        more_row_of_data(df, num_of_rows)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
