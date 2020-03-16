import datetime as dt
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}

cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyse.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs


    city = input('Where would you like to see bikeshare data from?\n')
    while city.lower() not in cities:
        city = input('We only have data for Chicago, New York City, and Washington. Pick again\n')

    # asks users how they want to filter the data
    question_options = ['month', 'day', 'both', 'none']
    question = input('Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter.\n')

    # if no answer is provided, the question is repeated.
    while question.lower() not in question_options:
        question = input('Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter.\n')
    else:
        if question.lower() in question_options:
            # filters by month
            if question.lower() == question_options[0]:
                day = 'all'
                month = input('Which month? January, February, March, April, May, or June? Or type "all"\n')
                while month.lower() not in months and month.lower() != 'all':
                    month = input("We only have data for January to June (inclusive). Please select one or type 'all'\n")
            # filters by weekday
            elif question.lower() == question_options[1]:
                month = 'all'
                day = input("Which day of the week (no need to capitalise it!)? Or type 'all'.\n")
                while day.lower() not in months and month.lower() != 'all':
                    day = input("Try again - select a day of the week or type 'all'.\n")
            # filters by month and weekday
            elif question.lower() == question_options[2]:
                month = input('Which month? January, February, March, April, May, or June? Or type "all"\n')
                while month.lower() not in months and month.lower() != 'all':
                    month = input("We only have data for January to June (inclusive). Please select one or type 'all'\n")
                day = input('Which day of the week (no need to capitalise it!)? Or type "all".\n')
                while day.lower() not in days and day.lower() != 'all':
                    day = input("Try again - select a day of the week or type 'all'\n")
            # no filters
            elif question.lower() == question_options[3]:
                month = 'all'
                day = 'all'
    # get user input for day of week (all, monday, tuesday, ... sunday)

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

    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek   # check that this is the right method()

    if month != 'all':
        month = months.index(month.lower()) + 1   # take our month input, and index it to get the integer value provided by datetime()
        df = df[df['month'] == month]

    if day != 'all':
        day = days.index(day.lower())
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    try:
        pop_month = df['month'].mode()[0]
        popular_month = months[pop_month - 1]
        print("The most popular month is: ", popular_month.title())
    except:
        print("Not suitable for your selection.")

    # display the most common day of week
    try:
        pop_day = df['day_of_week'].mode()
        popular_day_of_week = days[pop_day]
        print("The most popular day of the week is: ", popular_day_of_week.title())
    except:
        print("Not suitable for your selection.")

    # display the most common start hour
    try:
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].mode()[0]
        print("The most popular hour is: ", popular_hour)
    except:
        print("Not suitable for your selection.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("The most common Start Station is: ", common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("The most common End Station is: ", common_end)

    # display most frequent combination of start station and end station trip
    common_trip = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("The most common combination of stations is: ", common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_secs = df['Trip Duration'].sum()
    total_travel_time = dt.timedelta(seconds=int(total_secs))
    print("The total travel time was: ", total_travel_time)

    # display mean travel time
    mean_secs= df['Trip Duration'].mean()
    mean_travel_time = dt.timedelta(seconds=int(mean_secs))
    print("The mean travel time was: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(gender)
    except KeyError:
        print("Gender data is not provided.")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print("The earliest year is: ", int(earliest_year))
        print("The most recent year is: ", int(recent_year))
        print("The most common birth year is: ", int(common_year))
    except KeyError:
        print('Birth year data is not provided.')
    finally:
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def raw_stats(df):
    """Asks the user if they want to see raw data"""

    answers = ['yes', 'no']
    # asks the user if they want to see some data

    x = 0
    y = 5

    # asks the user if they want to see more data. Uses slicing to get 5 more rows.

    while True:
        raw = input("Do you want to see the raw data? Enter yes or no?\n")
        if raw not in answers:
            raw = ("Specify yes or no.")
            continue
        while raw.lower() == 'yes':
            print(df[x:y])
            x = x+5
            y = y+5
            raw = input("More data? yes or no.\n")
            continue
        if raw.lower() == 'no':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_stats(df)

        restart = input('\nWould you like to restart the program? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
