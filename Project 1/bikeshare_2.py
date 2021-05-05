import time
import pandas as pd
from datetime import date
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("please enter the city: ")
    city = city.lower()
    while city not in CITY_DATA:
        city = input("The city you entered is invalid, please enter again")
        city = city.lower()
    filter_criteria = input("Do you want to filter by day or month? ")
    filter_criteria = filter_criteria.lower()
    # get user input for month (all, january, february, ... , june)
    if filter_criteria == 'month':
        month = input("Now please enter your desired month")
        month = month.capitalize()
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        while month not in months:
            month = input("The month you entered is invalid, please enter again")
            month = month.capitalize()
    else: month = 'all'
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_criteria == 'day':
        day = input("Now please enter your desired day")
        day = day.capitalize()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        while day not in days:
            day = input("The day you entered is invalid, please enter again")
            day = day.capitalize()
    else: day = 'all'
    print('-' * 40)
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
    file_to_be_read = CITY_DATA[city]
    df = pd.read_csv(file_to_be_read)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if month != 'all':
        month_no = months.index(month.title()) + 1
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['Months'] = df['Start Time'].dt.month
        df = df[df['Months'] == month_no]
    if day != 'all':
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        # df['Day of Week'] = df['Start Time'].dt.day
        df['Days'] = df['Start Time'].dt.day_name()
        df = df[df['Days'] == day]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Months'] = df['Start Time'].dt.month
    most_common_month_num = df['Months'].mode()[0]
    most_common_month_name = months[most_common_month_num - 1]
    print("Most common month is ", most_common_month_name)
    # display the most common day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Day of Week'] = df['Start Time'].dt.day
    print("most common day of week is, ", df['Day of Week'].mode()[0])
    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start Hour'] = df['Start Time'].dt.hour
    print("most common start hour is ", df['Start Hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("most commonly used start station", df['Start Station'].mode()[0])
    # display most commonly used end station
    print("most commonly used end station", df['End Station'].mode()[0])
    # display most frequent combination of start station and end station trip
    most_freq_comb = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("most frequent combination of start station and end station trip is ", most_freq_comb[0], " and ", most_freq_comb[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = (((df['End Time'].dt.hour) * 60) + (df['End Time'].dt.minute)) - (
                ((df['Start Time'].dt.hour) * 60) + (df['Start Time'].dt.minute))
    # display total travel time
    print("Total travel time in minutes is ", df['Travel Time'].sum())
    # display mean travel time
    print("Mean travel time in minutes is ", df['Travel Time'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    unique_list = df['User Type'].unique()
    usertypes_and_corr_number = {}
    for i in unique_list:
        if i not in usertypes_and_corr_number:
            usertypes_and_corr_number[i] = 0
    for x in df['User Type']:
        usertypes_and_corr_number[x] += 1
    for i in usertypes_and_corr_number:
        print("No of User type ", i, " is : ", usertypes_and_corr_number[i])
    # Display counts of gender
    if 'Gender' in df.columns:
        unique_list_gend = df['Gender'].unique()
        gender_and_corr_number = {}
        for i in unique_list_gend:
            if i not in gender_and_corr_number:
                gender_and_corr_number[i] = 0
        for x in df['Gender']:
            gender_and_corr_number[x] += 1
        for i in gender_and_corr_number:
            print("No of Gender ", i, " : ", gender_and_corr_number[i])

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("Earliest year of birth is ", df['Birth Year'].min())
        print("Most recent year of birth is ", df['Birth Year'].max())
        print("Most common year of birth is ", df['Birth Year'].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
def ask_raw_data(df):
    s=['yes','no']
    itr = True
    counter=0
    while itr:
        if counter==0:
            rd=input("Would you like to see raw data? (yes/no)")
            rd=rd.lower()
        else:
            rd=input("Would you like to see raw data again? (yes/no)")
            rd=rd.lower()
        if rd not in s:
            rd = input("Your input is invalid, please enter yes or no")
            rd = rd.lower()
        if rd =='yes':
            itr=True
            print(df.iloc[counter:counter+5])
            counter+=5
        elif rd == 'no':
            itr=False

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        ask_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thank you, Goodbye")
            break

if __name__ == "__main__":
    main()
