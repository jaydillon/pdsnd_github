import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

# Configure filters to apply in front
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str(input('Would you like to see data for Chicago, New York or Washington?\n').lower())
    while city not in CITY_DATA.keys():
        city = str(input('Sorry, it looks like an invalid input. Please try again: Chicago, New York or Washington?\n').lower())

    # TO DO: get user input for month (all, january, february, ... , june)
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    filter_list = ['month', 'weekday', 'both', 'none']
    filter_input = str(input('Would you like to filter the data by month, weekday, both or not at all? Type "none" if you don\'t want to filter anything at all.\n').lower())

    while filter_input not in filter_list:
        filter_input = str(input('Sorry, it looks like an invalid input. Please try again: month, weekday, both or none?\n').lower())

    month = 'all'
    day = 'all'

    if filter_input == 'none':
        month = 'all'
        day = 'all'
    elif filter_input == 'month':
        month = str(input('What month would you like to look at? Jan, Feb, Mar, Apr, May, Jun or all?\n').lower())
        while month not in months:
            month = str(input('Sorry, it looks like an invalid input. Please try again: Jan, Feb, Mar, Apr, May, Jun or all?\n').lower())
    elif filter_input == 'weekday':
        day = str(input('What weekday would you like to look at? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?\n').lower())
        while day not in weekdays:
            day = str(input('Sorry, it looks like an invalid input. Please try again: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?\n').lower())
    elif filter_input == 'both':
        month = str(input('What month would you like to look at? Jan, Feb, Mar, Apr, May, Jun or all?\n').lower())
        while month not in months:
            month = str(input('Sorry, it looks like an invalid input. Please try again: Jan, Feb, Mar, Apr, May, Jun or all?\n').lower())
        day = str(input('What weekday would you like to look at? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?\n').lower())
        while day not in weekdays:
            day = str(input('Sorry, it looks like an invalid input. Please try again: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?\n').lower())

    print('-'*40)
    return filter_input, city, month, day

# Data induction from .csv files
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
    df['weekday'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['weekday'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n\nCalculating The Most Frequent Times of Travel...\n')
    print('-'*40)
    start_time = time.time()

    # TO DO: display the most common month
    most_frequent_month_count = df[df['month'] == df['month'].mode()[0]]['month'].count()
    most_frequent_month = df['month'].mode()[0]
    print('\nThe most popular month is {}, which has {} total counts.'.format(most_frequent_month, most_frequent_month_count))

    # TO DO: display the most common day of week
    most_frequent_weekday_count = df[df['weekday'] == df['weekday'].mode()[0]]['weekday'].count()
    most_frequent_weekday = df['weekday'].mode()[0]
    print('\nThe most popular weekday is {}, which has {} total counts.'.format(most_frequent_weekday, most_frequent_weekday_count))

    # TO DO: display the most common start hour
    most_frequent_hour_count = df[df['hour'] == df['hour'].mode()[0]]['hour'].count()
    most_frequent_hour = df['hour'].mode()[0]
    print('\nThe most popular hour is {}, which has {} total counts.'.format(most_frequent_hour, most_frequent_hour_count))

    print("\nThis took %s seconds. " % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station_count = df[df['Start Station'] == df['Start Station'].mode()[0]]['Start Station'].count()
    popular_start_station = df['Start Station'].mode()[0]
    print('\nThe most popular start station is {}, which has {} total counts.'.format(popular_start_station, popular_start_station_count))

    # TO DO: display most commonly used end station
    popular_start_station_count = df[df['End Station'] == df['End Station'].mode()[0]]['End Station'].count()
    popular_start_station = df['End Station'].mode()[0]
    print('\nThe most popular end station is {}, which has {} total counts.'.format(popular_start_station, popular_start_station_count))

    # TO DO: display most frequent combination of start station and end station trip
    df['Station Pair'] = df['Start Station'] + " - " + df['End Station']
    popular_station_pair_count = df[df['Station Pair'] == df['Station Pair'].mode()[0]]['Station Pair'].count()
    popular_station_pair = df['Station Pair'].mode()[0]
    print('\nThe most popular station pair is {}, which has {} total counts.'.format(popular_station_pair, popular_station_pair_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Trip Duration'] = df['Trip Duration'].astype(np.float64) # Convert data type from int64 to float64 to avoid TypeError using datetime.timedelta
    total_travel_time = str(datetime.timedelta(seconds=df['Trip Duration'].sum()))
    print('\nThe total travel time is {}.'.format(total_travel_time))

    # TO DO: display mean travel time
    avg_travel_time = str(datetime.timedelta(seconds=(df['Trip Duration'].sum()/df['Trip Duration'].count())))
    print('\nThe average travel time is {}.'.format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print('\nThe counts by user types are:')
    print(user_type)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print('\nThe counts by user genders are:')
        print(user_gender)
    else:
        print('\nGender data is not available.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('\nEarliest birth year: {}, \
            \nMost recent birth year: {}, \
            \nMost common birth year: {}.'.format(earliest_birth_year, recent_birth_year, most_common_birth_year))
    else:
        print('\nBirth Year data is not available.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    see_data = str(input('Would you like to see some individual trip data? y/n')).lower()
    while see_data not in ['y', 'n']:
        see_data = str(input('Sorry, I cannot understand you. Would you like to see some individual trip data? Y/N\n').lower())

    i = 0
    while see_data == 'y':
        show_data = df.iloc[i:i+5]
        print(show_data)
        i += 5
        see_data = str(input('Would you like to see some individual trip data? y/n')).lower()
        while see_data not in ['y', 'n']:
            see_data = str(input('Sorry, I cannot understand you. Would you like to see some individual trip data? y/n\n').lower())

def main():
    while True:
        filter_input, city, month, day = get_filters()
        raw_df = load_data(city, month, day)

        time_stats(raw_df)
        station_stats(raw_df)
        trip_duration_stats(raw_df)
        user_stats(raw_df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
