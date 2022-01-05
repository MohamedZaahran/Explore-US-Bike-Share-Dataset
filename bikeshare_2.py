import time
import pandas as pd
import numpy as np
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    cities = ["chicago", "new york", "washington"]
    months = ["january", "february", "march", "april", "may", "june", "all"]
    days = ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "all"]
    while True:
            z = False
            city = input("Enter the city name (Chicago, New York or Washington) to get data from:\n").lower()
            for i in cities:
                if city == i:
                    z = True
                    break
            if z == True:
                break
            else:
                print("Invalid input, please try again.")


    # get user input for month (all, january, february, ... , june)
    while True:
            z = False
            month = input("Which month to get data from? January, February, March, April, May, June or All?\n").lower()
            for i in months:
                if month == i:
                    z = True
                    break
            if z == True:
                break
            else:
                print("Invalid input, please try again.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            z = False
            day = input("Which day to get data from? Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or All?\n").lower()
            for i in days:
                if day == i:
                    z = True
                    break
            if z == True:
                break
            else:
                print("Invalid input, please try again.")

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
   # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # filter by month to create the new dataframe
        is_month = df['month']==month
        df = df[is_month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    months = ["january", "february", "march", "april", "may", "june", "all"]
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    Common_Month = df['month'].mode()[0]
    print("Most common month is: {}".format(months[Common_Month - 1].title()))

    # display the most common day of week

    Common_Day = df['day_of_week'].mode()[0]
    print("Most common day is: {}".format(Common_Day))

    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    Common_Start_Hour = df['hour'].mode()[0]
    print("Most common start hour is: {}".format(Common_Start_Hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    Start_Station = df['Start Station'].mode()[0]
    print("The most commonly used start station is: {}".format(Start_Station))

    # display most commonly used end station

    End_Station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station is: {}".format(End_Station))

    # display most frequent combination of start station and end station trip
    
    df['Route'] = df['Start Station'] + "-" + df['End Station']
    x = df['Route'].mode()[0]
    print("The most frequent combination of start station and end station trip: {}".format(x))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    Total_Travel_Time  = df['Trip Duration'].sum()
    print("The total travel time is: {} seconds".format(round(Total_Travel_Time)))
    
    # display mean travel time

    Mean_Travel_Time = df['Trip Duration'].mean()
    print("The mean travel time is: {} seconds".format(round(Mean_Travel_Time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    Count_User_Types = df['User Type'].value_counts()
    print("Counts of user types are:\n\nSubscribers: {}\nCustomers: {}\n".format(Count_User_Types[0], Count_User_Types[1]))

    # Display counts of gender

    if city == 'chicago' or city == 'new york':
        Count_Gender = df['Gender'].value_counts()
        print("Counts of user genders are:\n\nMales: {}\nFemales: {}\n".format(Count_Gender[0], Count_Gender[1]))

    # Display earliest, most recent, and most common year of birth

    if city == 'chicago' or city == 'new york':
        Earliest_Year = int(df['Birth Year'].min())
        print("Earliest year of birth is: {}".format(Earliest_Year))
        
        Recent_Year = int(df['Birth Year'].max())
        print("Most recent year of birth is: {}".format(Recent_Year))
        
        Common_Year = int(df['Birth Year'].mode()[0])
        print("Most common year of birth is: {}".format(Common_Year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(city):
    """Takes the name of the city from get_filters function as input, and returns raw data of the city as chunks of 5 rows depending on the user input."""
    df = pd.read_csv(CITY_DATA[city])
    start = 0
    print("\nDisplaying raw data......\n")
    while True:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            print(df.iloc[start:start+5])
            while True:
                    display = input("Do you wish to view another 5 rows? Yes/No\n").lower()
                    if display == 'yes':
                        start += 5
                        break
                    elif display == 'no':
                        print("\nExiting......\n")
                        break
                    else:
                        print("Invalid input, please try again.")
            if display == 'no':
                break
def main():
    while True:        
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        while True:
            raw = input("\nWould you like to view raw data in chunks of 5 rows? Yes/No\n").lower()
            if raw == 'yes':
                display_raw_data(city)
                break
            elif raw == 'no':
                break
            else:
                print("Invalid input, please try again.")             
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart == 'yes' or restart == 'no':
                break
            else:
                print("Invalid input, please try again.")
        if restart == 'yes':
            continue
        else:
            break
        

if __name__ == "__main__":
	main()