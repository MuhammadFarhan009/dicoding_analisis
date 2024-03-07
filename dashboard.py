import streamlit as st
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


# Load your data
# Assuming df is your DataFrame containing the bike rental data
# Replace this line with your data loading code
data_clean = pd.read_csv("clean_data.csv")

def visualize_air_quality(data, station, year):
    # Function to categorize SO2 values
    def categorize_SO2(value):
        if value < 100:
            return 'Good'
        elif 100 <= value < 200:
            return 'Fair'
        elif 200 <= value < 300:
            return 'Moderate'
        elif 300 <= value < 600:
            return 'Unhealthy'
        else:
            return 'Hazardous'

    # Filter data based on selected station and year
    clean_data_station_year = data[(data['station'] == station) & (data['year'] == year)]

    # Calculate mean for hours
    clean_data_station_year = clean_data_station_year.groupby(['Date', 'day']).agg({'hour': 'mean', 'SO2': 'mean'}).reset_index()

    # Apply SO2 categorization
    clean_data_station_year['SO2_Category'] = clean_data_station_year['SO2'].apply(categorize_SO2)

    # Group by month and SO2 category and calculate count
    grouped_data = clean_data_station_year.groupby([clean_data_station_year['Date'].dt.month, 'SO2_Category']).size().unstack(fill_value=0).reset_index()

    # Rename month numbers to month names
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    grouped_data['Date'] = grouped_data['Date'].map(month_names)

    # Reindex to ensure all categories are present for each month
    grouped_data.set_index(['Date'], inplace=True)
    grouped_data = grouped_data.reindex(columns=['Good', 'Fair', 'Moderate', 'Unhealthy', 'Hazardous'], fill_value=0).reset_index()

    # Melt the dataframe to long format
    grouped_data_melted = pd.melt(grouped_data, id_vars=['Date'], value_vars=['Good', 'Fair', 'Moderate', 'Unhealthy', 'Hazardous'], var_name='SO2_Category', value_name='Count')

    # Plotting stacked bar chart with Plotly
    fig = px.bar(grouped_data_melted, x='Date', y='Count', color='SO2_Category',
                 title=f'Days with Good Air Quality by Month for {station}',
                 labels={'Count': 'Number of Days', 'Date': 'Month'},
                 color_discrete_map={'Good': 'green', 'Fair': 'yellow', 'Moderate': 'orange', 'Unhealthy': 'red', 'Hazardous': 'brown'},
                 barmode='stack')

    # Update layout for better visualization
    fig.update_layout(yaxis_title="Number of Days",
                      xaxis_title="Month",
                      title_x=0.5,
                      plot_bgcolor='rgba(255, 255, 255, 1)')
    
    # Show plot
    st.plotly_chart(fig)

# Function to display the main dashboard page
def show_dashboard():
    st.header("Welcome to Air Quality analisis")
    st.write("You can navigate to different pages using the sidebar.")
    st.header("What I've Already Created" , divider='rainbow')
    st.write("- Saya sudah berhasil membuat visualisasi untuk melihat bagaimana kualitas udara di setiap stasiun sepanjang tahun 2013")
    st.write("- Saya sudah berhasil membuat visualisasi yang menciptakan gambaran yang mengesankan tentang bagaimana kandungan O3 mempengaruhi kondisi suhu pada satu stasiun. Dengan menggunakan grafik yang informatif, kita dapat dengan jelas melihat korelasi antara kandungan O3 dan perubahan suhu. Analisis yang cermat terhadap visualisasi ini memungkinkan untuk memahami bagaimana pola kandungan O3 mempengaruhi suhu secara lokal, memberikan wawasan yang berharga dalam memahami dinamika udara di wilayah tersebut")

# Display the preview of the dataset
def data_preview():
    # st.write("This dashboard will show you statistik in bike rental data.")
    st.header("Preview about dataset: \n", divider='rainbow')
    st.write("\n", data_clean.head(5))
    st.write("Number of rows:", data_clean.shape[0])
    st.write("Number of columns:", data_clean.shape[1])
    st.write("Descriptive Statistics for Numeric Columns:")
    st.write(data_clean.describe())

# Function to create the bar plot for average counts by season


def plot_monthly_average_concentrations(data_clean, year, station):
    # Ensure data_clean has a datetime index
    data_clean['datetime'] = pd.to_datetime(data_clean[['year', 'month', 'day', 'hour']])
    data_clean.set_index('datetime', inplace=True)

    # Filter data for the specified year and station
    data_filtered = data_clean[(data_clean.index.year == year) & (data_clean['station'] == station)]

    # Calculate monthly average for TEMP and O3
    monthly_avg_TEMP = data_filtered['TEMP'].resample('M').mean()
    monthly_avg_O3 = data_filtered['O3'].resample('M').mean()

    # Plot the time series
    plt.figure(figsize=(10, 5))
    plt.plot(monthly_avg_TEMP.index, monthly_avg_TEMP, label='TEMP', color='blue')
    plt.plot(monthly_avg_O3.index, monthly_avg_O3, label='O3', color='red')
    plt.title(f'Monthly Average Concentrations at {station} (Year {year})')
    plt.xlabel('Date')
    plt.ylabel('Concentration')
    plt.legend()
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot()  

# Function to display the page for average counts by season
def show_season_counts():
    data_clean['Date'] = pd.to_datetime(data_clean[['year', 'month', 'day']])
    

    st.title('Kualitas udara di setiap stasiun sepanjang tahun')
    
    

    # Station selection dropdown    
    station = st.selectbox('Select Station', ['Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong'])

    # Year selection
    # selected_year = st.sidebar.slider('Select Year', min_value=2013, max_value=2016, value=2013, step=1)
    selected_year = st.slider('Select Year', min_value=2013, max_value=2016, value=2013)
    # station = st.selectbox('Select Station', data_clean['station'].unique())


    # Visualize air quality
    visualize_air_quality(data_clean, station, selected_year)
    # visualize_air_quality(data_clean, 'Dongsi', 2013)
    st.subheader('Berdasarkan analisis data yang dilakukan, dapat disimpulkan:')
    st.write("Udara di setiap statiun sangat baik. Namun terdapat beberapa hari yang memiliki kualitas udaranya fair dan hazardous di sepanjang tahun 2013. Untuk kualitas udara fair masih sangat wajar dikarenakan sangat mungkin terjadinya lonjakan kadar SO2 di udara sedangkan untuk kualitas udara hazardous terjadi dikarenakan ada beberapa data pada column SO2 memiliki nilai yang sangat besar sehingga mempengaruhi rata rata konsentrasi SO2 di udara.")


# Streamlit app
def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # df_filtered = df[(df['dteday'] >= '2012-01-01') & (df['dteday'] <= '2012-12-21')]
    st.sidebar.title('Navigation')
    page = st.sidebar.selectbox("Select a page", ["Dashboard", "kondisi temperature", "Kualitas udara di setiap stasiun"])

    if page == "Dashboard":
        show_dashboard()
        data_preview()
        
    elif page == "kondisi temperature":
        st.title("kandungan O3 terhadap kondisi temperature")


        # Streamlit UI
        station = st.selectbox('Select Station', data_clean['station'].unique())
        year = st.slider('Select Year', min_value=2013, max_value=2016, value=2013)

        # Call the function to plot the data
        plot_monthly_average_concentrations(data_clean, year, station)
        
        st.subheader('Berdasarkan analisis data yang dilakukan, dapat disimpulkan:')
        st.write("dapat kita liat bahwasanya setiap naiknya konsentrasi O3 akan mempengaruhi kenaikan suhu atau temperature pada statiun Aotizhongxin. Namun terdapat perbedaaan saat bulan 6 dan 7 dimana penurunan konsentrasi O3 tidak membuat suhu menurun. Hal ini sesuai dengan korelasi antara 'TEMP' and 'O3' yang hanya berkisar 0.53. korelasi positif menandakan hubungan satu variabel meningkat jika variabel lainnya meningkat, atau satu variabel menurun sementara yang lainnya juga menurun dan Korelasi 0.53 artinya mereka memiliki hubungan yang tidak sangat kuat tetapi tetap mampu saling mempengaruhi")

            

    elif page == "Kualitas udara di setiap stasiun":

        show_season_counts()

if __name__ == "__main__":
    main()
