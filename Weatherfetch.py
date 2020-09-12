# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 19:48:24 2019

@author: LENOVO
"""

import requests,bs4,csv,os,pytz
from urllib.request import urlopen
from datetime import datetime

'''Dictionary for storing the weather station details'''
weatherDetailsDictionary={"Temperature":"","Pressure":"","GustSpeed":"","DewPoint":"","Humidity":
    "","PrecRate":"","WindDirection":"","UV":"","SolarRadiation":"","Windspeed":"","Timestamp":""}

'''List for passing the dictionary values in list to the convertToCSV() for creating columns
and storing datas'''
dict_data_list=[]

flag=0    
'''Function for Fetching the Weather Details'''
def fetchWeatherDetails(URL):
    
    '''converting from timezone UTC to EST'''
    u = urlopen('http://just-the-time.appspot.com/')
    timevalue=u.read().strip()
    est=pytz.timezone('US/Eastern')
    utc = pytz.utc
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    new_str = str(timevalue).strip('b')
    EstTime = datetime(int(new_str[1:5]),int(new_str[6:8]), int(new_str[9:11]),int(new_str[12:14]) , int(new_str[15:17]), int(new_str[18:20]), tzinfo=utc)
    print(EstTime.astimezone(est).strftime(fmt))
    try:
        result=requests.get(URL)
        result.raise_for_status()
        
        soup=bs4.BeautifulSoup(result.text,'html.parser')
        
        status=soup.select('#inner-content > section:nth-child(2) > div:nth-child(1) > div > div > div > div > div.dashboard__title.ng-star-inserted > div > span:nth-child(2)')
        if status[0].text.strip()=='Online':
            '''Fetching Temperature'''
            temperature=soup.select('#inner-content > section:nth-child(2) > div:nth-child(1) > div > div > div > div > div:nth-child(2) > div > lib-tile-current-conditions > div > div.module__body > div > div.small-4.columns.text-left.conditions-temp > div.main-temp > lib-display-unit > span > span.wu-value.wu-value-to')
            weatherDetailsDictionary["Temperature"]=temperature[0].text.strip()+" "+"F"
            '''Fetching Pressure'''
            pressure=soup.select("#inner-content > section:nth-child(2) > div:nth-child(1) > div > div > div > div > div:nth-child(2) > div > lib-tile-current-conditions > div > div.module__body > div > div.weather__summary > div:nth-child(3) > div > div.weather__text > lib-display-unit > span > span.wu-value.wu-value-to")
            weatherDetailsDictionary["Pressure"]=pressure[0].text.strip()+" "+"in"
        
            '''Fetching Humidity'''
            humidity=soup.select("#inner-content > section:nth-child(2) > div:nth-child(1) > div > div > div > div > div:nth-child(2) > div > lib-tile-current-conditions > div > div.module__body > div > div.weather__summary > div:nth-child(4) > div > div.weather__text > lib-display-unit > span > span.wu-value.wu-value-to")
            weatherDetailsDictionary["Humidity"]=humidity[0].text.strip()+" "+"%"
            '''Fetching DewPoint'''
            dewPoint=soup.select("#inner-content > section:nth-child(2) > div:nth-child(1) > div > div > div > div > div:nth-child(2) > div > lib-tile-current-conditions > div > div.module__body > div > div.weather__summary > div:nth-child(1) > div > div.weather__text > lib-display-unit > span > span.wu-value.wu-value-to")
            weatherDetailsDictionary["DewPoint"]=dewPoint[0].text.strip()+" "+"F"
            '''Fetching Precipitation Rate'''
            precRate=soup.select("#inner-content > section:nth-child(2) > div:nth-child(1) > div > div > div > div > div:nth-child(2) > div > lib-tile-current-conditions > div > div.module__body > div > div.weather__summary > div:nth-child(2) > div > div.weather__text > lib-display-unit > span > span.wu-value.wu-value-to")
            weatherDetailsDictionary["PrecRate"]=precRate[0].text.strip()+" "+"in/hr"
            '''Fetching Wind Direction'''
            windDirection=soup.select("#inner-content > section:nth-child(2) > div:nth-child(1) > div > div > div > div > div:nth-child(6) > div > lib-tile-wind > div > div.module__body > div > div.small-5.columns > div > div:nth-child(2)")
            weatherDetailsDictionary["WindDirection"]=windDirection[0].text.strip()
            '''Fetching UV details'''
            UV=soup.select("#inner-content > section:nth-child(2) > div:nth-child(1) > div > div > div > div > div:nth-child(2) > div > lib-tile-current-conditions > div > div.module__body > div > div.weather__summary > div:nth-child(6) > div > div.weather__text > lib-display-unit > span > span.wu-value.wu-value-to")
            weatherDetailsDictionary["UV"]=UV[0].text.strip()
            '''Fetching gust speed'''
            gustSpeed=soup.select('#inner-content > section:nth-child(2) > div:nth-child(1) > div > div > div > div > div:nth-child(2) > div > lib-tile-current-conditions > div > div.module__body > div > div:nth-child(3) > div > div.weather__text > lib-display-unit:nth-child(2) > span > span.wu-value.wu-value-to')
            weatherDetailsDictionary["GustSpeed"]=str(gustSpeed[0].text.strip())+" "+"mph"
        
            '''Fetching the Solar Radiation'''
            solarRadiation=soup.select("#inner-content > section:nth-child(2) > div:nth-child(1) > div > div > div > div > div:nth-child(10) > div > lib-tile-solar-radiation > div > div.module__body > div > div.small-5.columns > div > div.weather__text")
            weatherDetailsDictionary["SolarRadiation"]=solarRadiation[0].text.strip()
            '''Fetching the wind speed'''
            windSpeed=soup.select("#inner-content > section:nth-child(2) > div:nth-child(1) > div > div > div > div > div:nth-child(2) > div > lib-tile-current-conditions > div > div.module__body > div > div:nth-child(3) > div > div.weather__text > lib-display-unit:nth-child(1) > span > span.wu-value.wu-value-to")
            weatherDetailsDictionary["Windspeed"]=windSpeed[0].text.strip()+" "+"mph"
            '''Timestamp'''
            weatherDetailsDictionary["Timestamp"]=str(EstTime.astimezone(est).strftime(fmt))
        else:
            '''flag is set if the weather station is offline'''
            
            global flag
            flag=1
    
    except requests.exceptions.ConnectionError:
        print("Connection Error")
    except IndexError:
        print("Index out of bounds")
    
    print("Current Weather Details","\n",'----------------------')
    '''#printing all the current weather details.'''
    for (key,value) in weatherDetailsDictionary.items():
        print(key+":"+value)
    
'''function collecting the data on the CSV file'''
def convertToCSV(csv_file,csv_columns,dict_data,URL):
    exists=os.path.isfile(os.getcwd()+stationid+"WeatherData.csv")
    global filecsv;

    if exists:
        '''If the csv file exists new datas will append to the previous weather details'''        
        with open(os.getcwd()+stationid+"WeatherData.csv") as f:
            filecsv=csv.reader(f)
            count=0
            for line in filecsv:
                #print(line)
                if len(line)==0:
                    continue
                else:
                    if count>0:
                        new_dict={"Temperature":"","Pressure":"","GustSpeed":"","DewPoint":"","Humidity":
    "","PrecRate":"","WindDirection":"","UV":"","SolarRadiation":"","Windspeed":"","Timestamp":""}
                        new_dict["Temperature"]=line[0]
                        new_dict["Pressure"]=line[1]
                        new_dict["GustSpeed"]=line[2]
                        new_dict["DewPoint"]=line[3]
                        new_dict["Humidity"]=line[4]
                        new_dict["PrecRate"]=line[5]
                        new_dict["WindDirection"]=line[6]
                        new_dict["UV"]=line[7]
                        new_dict["SolarRadiation"]=line[8]
                        new_dict["Windspeed"]=line[9]
                        new_dict["Timestamp"]=str(line[10])
                        dict_data.append(new_dict)
                        
                count+=1
                
           
            try:
                '''writing the current as well as previous datas to csv file'''
                
                with open(csv_file, 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    #writer=csv.writer(csvfile)
                    
                    writer.writeheader()
                    for data in dict_data:
                        #print(data)
                        writer.writerow(data)
                    
            
            except (IOError,OSError) :
                print("IOError/OSError")
            
    else:
        ''' It will create a new csv file named as 
        current working directory+stationid+WeatherData.csv and write the data into it '''
        
        print("does not exist")
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    
                writer.writeheader()
                for data in dict_data:
                    #print(data)
                    writer.writerow(data)
                    
            
        except (IOError,OSError) :
                print("IOError/OSError")
        
    return

        
#Input the URL e.g.-http://www.wunderground.com/personal-weather-station/dashboard?ID=IROURKEL4
'''Weather station URL'''
URL="https://www.wunderground.com/dashboard/pws/IROURKEL4"
lastIndex=URL.rfind('/')
stationid=URL[lastIndex+1:]
fetchWeatherDetails(URL)
csv_columns=['Temperature','Pressure',"GustSpeed","DewPoint","Humidity","PrecRate","WindDirection","UV","SolarRadiation","Windspeed","Timestamp"]
current_path=os.getcwd()
csv_file=current_path+stationid+"WeatherData.csv"
dict_data_list=[weatherDetailsDictionary]

'''The convertToCSV function will be called and details in the csv file
 will be reflected only if weather station is online i.e flag = 0'''

if flag==0:
    convertToCSV(csv_file,csv_columns,dict_data_list,URL)
