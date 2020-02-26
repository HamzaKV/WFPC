import React from 'react';
import { 
  StyleSheet, 
  Text, 
  View,
  Image,
  Picker,
  Dimensions,
  Platform,
  TouchableOpacity,
  FlatList,
} from 'react-native';
import Constants from 'expo-constants';
import { AppLoading } from 'expo';
import DateTimePickerModal from 'react-native-modal-datetime-picker';

let dataGlobal = null;

export default class App extends React.Component {

  state = {
    time: 0,
    selectedTime: new Date(1514696400000),
    city: 'miami',
    status: false,
    showDatePicker: false,
    dayData: [],
  }

  async fetchData() {
    let dt = new Date(this.state.selectedTime.getFullYear(), this.state.selectedTime.getMonth(), this.state.selectedTime.getDate(), 1, 30, 0);
    this.setState({ status: false });
    await fetch('http://192.168.0.80:8000/?data=fetch&date=' + (dt.getTime()/1000)).then(resp => resp.json()
    ).then(data => {
      dataGlobal = data;
      for(let key in data) {
        let info = data[key];
        if(info.city === this.state.city) {
          this.state.dayData = []
          this.state.dayData.push(info['day0']);
          this.state.dayData.push(info['day1']);
          this.state.dayData.push(info['day2']);
          this.state.dayData.push(info['day3']);
          this.state.dayData.push(info['day4']);
          this.state.dayData.push(info['day5']);
          this.state.dayData.push(info['day6']);
          this.state.dayData.push(info['day7']);
        }
      }
    }).catch(err => console.log(err))
  }

  onDatePress() {
    this.setState({ showDatePicker: true });
  }

  hideDatePicker() {
    this.setState({ showDatePicker: false });
  };

  handleDateConfirm(date) {
    this.setState({ selectedTime: date, showDatePicker: false });
    this.updateView(this.state.city, date);
  };

  handlePicker(itemValue) {
    this.setState({ city: itemValue });
    this.updateView(itemValue, this.state.selectedTime);
  }

  updateView(city, timestamp) {
    // search for city and timestamp if id does not exist then fetch with new params
    let dt = new Date(timestamp.getFullYear(), timestamp.getMonth(), timestamp.getDate(), 1, 30, 0);
    if(dataGlobal != null) {
      let bool = false;
      for(let key in dataGlobal) {
        let info = dataGlobal[key];
        if(info.city === city) {
          for(let i = 0; i < 8; i++) {
            if(Number((info['day'+i]).time) === (dt.getTime()/1000)) {
              bool = true;
              break;
            }
          }
          if(bool) {
            this.state.dayData = []
            this.state.dayData.push(info['day0']);
            this.state.dayData.push(info['day1']);
            this.state.dayData.push(info['day2']);
            this.state.dayData.push(info['day3']);
            this.state.dayData.push(info['day4']);
            this.state.dayData.push(info['day5']);
            this.state.dayData.push(info['day6']);
            this.state.dayData.push(info['day7']);
          }
        }
      }
      if(!bool) {
        this.fetchData();
      }
    }
  }

  renderWeatherIcon(forecast) {
    switch(forecast) {
      case 'Clear':
        return(
          <Image 
            source={require('./assets/sunny_icon.png')}
            style={{ width: 100, height: 100, }}
          />
        );
      case 'Rain':
      case 'Drizzle':
      case 'Possible Drizzle':
      case 'Light Rain':
        return(
          <Image 
            source={require('./assets/rain_icon.png')}
            style={{ width: 100, height: 100, }}
          />
        );
      case 'Humid and Mostly Cloudy':
      case 'Humid and Overcast':
      case 'Mostly Cloudy':
      case 'Overcast':
      case 'Partly Cloudy':
        return(
          <Image 
            source={require('./assets/sunny_cloudy_icon.png')}
            style={{ width: 100, height: 100, }}
          />
        );
      case 'Cloudy':
        return(
          <Image 
            source={require('./assets/cloudy_icon.png')}
            style={{ width: 100, height: 100, }}
          />
        );
      case 'Foggy':
        return(
          <Image 
            source={require('./assets/foggy_icon.png')}
            style={{ width: 100, height: 100, }}
          />
        );
      default:  
        return(
          <Image 
            source={require('./assets/sunny_icon.png')}
            style={{ width: 100, height: 100, }}
          />
        );
    }
  }

  renderPicker() {
    if(Platform.OS === 'android') {
      return(
        <Picker 
          style={styles.pickerStyle} 
          itemStyle={styles.pickerItemStyle} 
          selectedValue={this.state.city} 
          onValueChange={this.handlePicker.bind(this)}
        >
          <Picker.Item label='Miami, FL' value='miami' />
          <Picker.Item label='BelleGlade, FL' value='BelleGlade' />
          <Picker.Item label='BonitaSprings, FL' value='BonitaSprings' />
          <Picker.Item label='CapeCoral, FL' value='CapeCoral' />
          <Picker.Item label='Goodland, FL' value='Goodland' />
          <Picker.Item label='HomesteadAirReserveBase, FL' value='HomesteadAirReserveBase' />
          <Picker.Item label='Immokalee, FL' value='Immokalee' />
          <Picker.Item label='KingsPoint, FL' value='KingsPoint' />
          <Picker.Item label='LehighAcres, FL' value='LehighAcres' />
          <Picker.Item label='LibertyPoint, FL' value='LibertyPoint' />
          <Picker.Item label='Turkeyfoot, FL' value='Turkeyfoot' />
          <Picker.Item label='WestPalmBeach, FL' value='WestPalmBeach' />
        </Picker>
      );
    } else if(Platform.OS === 'ios') {
      return(
        <Picker 
          style={styles.pickeriosStyle} 
          itemStyle={styles.pickeriosItemStyle} 
          selectedValue={this.state.city} 
          onValueChange={this.handlePicker.bind(this)}
        >
          <Picker.Item label='Miami, FL' value='Miami' />
          <Picker.Item label='BelleGlade, FL' value='BelleGlade' />
          <Picker.Item label='BonitaSprings, FL' value='BonitaSprings' />
          <Picker.Item label='CapeCoral, FL' value='CapeCoral' />
          <Picker.Item label='Goodland, FL' value='Goodland' />
          <Picker.Item label='HomesteadAirReserveBase, FL' value='HomesteadAirReserveBase' />
          <Picker.Item label='Immokalee, FL' value='Immokalee' />
          <Picker.Item label='KingsPoint, FL' value='KingsPoint' />
          <Picker.Item label='LehighAcres, FL' value='LehighAcres' />
          <Picker.Item label='LibertyPoint, FL' value='LibertyPoint' />
          <Picker.Item label='Turkeyfoot, FL' value='Turkeyfoot' />
          <Picker.Item label='WestPalmBeach, FL' value='WestPalmBeach' />
        </Picker>
      );
    }
  }

  render() {
    if(this.state.status) {
      return (
        <View style={styles.container}>
          <View style={{ flex: 1 }}>
            {this.renderPicker()}
            <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
              <Text style={{fontSize: 24, fontWeight: 'bold', color: 'white'}}>
                {(new Date(this.state.selectedTime)).toDateString()}
              </Text>
              <TouchableOpacity onPressIn={this.onDatePress.bind(this)} style={styles.buttonStyle}>
                <Text style={styles.buttonTextStyle}>Change Date</Text>
              </TouchableOpacity>
              <DateTimePickerModal
                date={this.state.selectedTime}
                isVisible={this.state.showDatePicker}
                mode="date"
                onConfirm={this.handleDateConfirm.bind(this)}
                onCancel={this.hideDatePicker.bind(this)}
              />
            </View>
          </View>
          <View style={{ flex: 3 }}>
            <FlatList
              data={this.state.dayData}
              renderItem={({ item }) => {
                return (
                  <View style={styles.listItemViewer}>
                    <View style={{ flex: 1, flexDirection: 'row' }}>
                      <View style={{ flex: 1 }}>
                        <Text style={{fontSize: 20, fontWeight: 'bold', color: 'white', flex: 1}}>
                          {item.forecast}
                        </Text>
                        <Text style={{fontSize: 14, color: 'white', flex: 1}}>
                          {(new Date(Number(item.time) * 1000)).toDateString()}
                        </Text>
                      </View>
                      <View style={{ flex: 1 }}>
                        {this.renderWeatherIcon(item.forecast)}
                      </View>
                    </View>
                    <View style={{ flex: 4 }}>
                      <Text style={styles.textStyle}>Precipitation: {Math.round(Number(item.precipIntensity) * 10000)/10000} cm</Text>
                      <Text style={styles.textStyle}>Wind Speed: {Math.round(Number(item.windSpeed) * 10000)/10000} mph</Text>
                      <Text style={styles.textStyle}>Humidity: {Math.round(Number(item.humidity) * 1000000)/10000} %</Text>
                      <Text style={styles.textStyle}>Pressure: {Math.round(Number(item.pressure) * 10000)/10000} hPa</Text>
                      <Text style={styles.textStyle}>Precipitation Probability: {Math.round(Number(item.precipProbability) *1000000)/10000} %</Text>
                      <Text style={styles.textStyle}>Wind Bearing: {Math.round(Number(item.windBearing) * 10000)/10000}</Text>
                    </View>
                  </View>
                );
              }}
              keyExtractor={(item) => item.time}
              horizontal
            />
          </View>
        </View>
      );
    } else {
      return (
        <View style={styles.container}>
          <AppLoading
            startAsync={this.fetchData.bind(this)}
            onFinish={() => this.setState({ status: true })}
            onError={console.warn}
          />
        </View>
      );
    }
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: Constants.statusBarHeight,
    backgroundColor: '#03b6fc',
    paddingTop: 20,
    paddingBottom: 20,
    paddingLeft: 10,
    paddingRight: 10,
  },
  pickerStyle: {
    width: Dimensions.get('screen').width-20,
    borderColor: 'black',
    borderWidth: 5,
    color: 'white',
  },
  pickerItemStyle: {
    width: Dimensions.get('screen').width-20
  },
  pickeriosStyle: {
    backgroundColor: 'white',
    height: 120,
    width: Dimensions.get('screen').width-20
  },
  pickeriosItemStyle: {
    fontSize: 22,
    height: 120,
    width: Dimensions.get('screen').width-20
  },
  textStyle: {
    color: 'white',
    paddingTop: 10
  },
  buttonTextStyle: {
    alignSelf: 'center',
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    paddingTop: 10,
    paddingBottom: 10
  },
  buttonStyle: {
    alignSelf: 'stretch',
    backgroundColor: '#1991EB', //nice blue color, changed to grey with #8a8c91
    borderRadius: 5,
    borderWidth: 1,
    borderColor: '#1991EB',
    alignItems: 'center',
    justifyContent: 'center',
    opacity: 1
  },
  listItemViewer: {
    borderWidth: 1,
    flex: 1,
    padding: 5,
    margin: 10
  }
});
