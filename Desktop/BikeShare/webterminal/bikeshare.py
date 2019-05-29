import time
import pandas as pd
import numpy as np
import os

# Read the file

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


# in this part getting input from user

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
    while True:
        city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                     'Would you like to see data for chicago, new York, or washington?\n')
        city = city.lower()
        if not city:
            print("Please enter valid input.")
        if city and city not in ('chicago', 'new york city', 'washington'):
            print("Please enter valid input.")
            continue
        if city in ('chicago', 'new york city', 'washington'):
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        time_period = input(
            '\nWould you like to filter the data by month, day, or both? \n')
        time_period = time_period.lower()
        if not time_period:
            print("Please enter valid input.")
            continue
        if time_period and time_period not in ('month', 'day', 'both'):
            print("Please enter valid input.")
            continue
        if time_period in ('month', 'day', 'both'):
            break

    #month control------------------------------------------------------------------------------------
    if time_period == 'month' or time_period=='both':
        day='all'
        while True:
            month = input('Which Month? January February March April May June...\n')
            month = month.lower()
            if not month:
                print("Please enter valid input.")
                continue
            if month and month not in ('january', 'february', 'march', 'april', 'may', 'june'):
                print("Please enter valid input.")
                continue
            if month in ('january', 'february', 'march', 'april', 'may', 'june'):

                break

    #day control---------------------------------------------------------------------------------------
    if time_period == 'day' or time_period=='both':
        month='all'
        while True:
            day = int(input('Which Day?Please type your response as integer(e.g: Sunday=1)\n'))
            if not day:
                print("Please enter valid input.")
                continue
            if day and day >7:
                print("Please enter valid input.")
                continue
            if day <=7:
                break

    if time_period == "": get_filters()
    if city == "": get_filters()
    print('-' * 40)


    return str(city), str(month), str(day)


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df['hours'] = df['Start Time'].dt.hour

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
        df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    arg1: df is string and return string value"""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('display the most common month---->' + str(df['month'].mode()[0]))
    print('Count the most popular month---->' + str(list(df['month'].value_counts())[0]))
    # display the most common day of week
    print('display the most common day of week---->' + str(df['day_of_week'].mode()[0]))
    print('Count the most popular day of week---->' + str(list(df['day_of_week'].value_counts())[0]))
    # display the most common start hour
    print('the most popular hour---->' + str(df['hours'].mode()[0]))
    print('Count the most popular hour---->' + str(list(df['hours'].value_counts())[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popler_StartStations = df['Start Station'].mode()[0]
    print('the most popular start station------->  ' + str(popler_StartStations))
    # display most commonly used end station
    popler_EndStations = df['End Station'].mode()[0]
    print('the most popular End  Station------>   ' + str(popler_EndStations))
    # display most frequent combination of start station and end station trip
    df['period'] = df[['End Station', 'Start Station']].astype(str).sum(axis=1)
    print('the most popular start station and end station----->' + str(df['period'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('-' * 40)
    print('Sum Trip Duration------>' + str(df['Trip Duration'].sum()))
    # display mean travel time
    print('-' * 40)
    print('Average Trip Duration mean-------> ' + str(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Display counts of user types\n' + "-----\n" + str(df['User Type'].value_counts()))
    print('-' * 40)

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Display counts of gender\n' + "------\n" + str(df['Gender'].value_counts()))
        print('-' * 40)
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('most common year of birth------>' + str(pd.to_datetime(df['Birth Year']).dt.year.mode()[0]))
        print('earliest of Birth Year------>' + str(df['Birth Year'].min()))
        print('most recent Birth Year------>' + str(df['Birth Year'].max()))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)


def loadfivedata(count, answer, df):
    while True:
        if "yes" == answer:
            print('  {\n')
            print((df.iloc[count]))
            print('    }\n' + '--------------')
            count = count + 1
            if count % 5 == 0:
                answer = input('\nWould you like to view individual trip data?Type "yes" or "no"\n')

        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        df_new = load_data(city, month, day)
        count = 0
        answer = input('\nWould you like to view individual trip data?Type "yes" or "no"\n')
        loadfivedata(count, answer, df_new)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
