import React from 'react';
import { 
  StyleSheet, 
  Text, 
  View,
  Image 
} from 'react-native';
import Constants from 'expo-constants';

export default class App extends React.Component {

  state = {
    percipIntensity: 0,
    percipProbability: 0,
    temperature: 0,
    apparentTemp: 0,
    dewPoint: 0,
    humidity: 0,
    pressure: 0,
    windBearing: 0,
    windSpeed: 0,
    cloudCover: 0,
    uvIndex: 0,
    visibility: 0,
    summary: '',
    image: ''
  }

  fetchData() {
    let doc = require('./assets/test.json');
    this.setState({
      percipIntensity: doc.percipIntensity,
      percipProbability: doc.percipProbability,
      temperature: doc.temperature,
      apparentTemp: doc.apparentTemp,
      dewPoint: doc.dewPoint,
      humidity: doc.humidity,
      pressure: doc.pressure,
      windBearing: doc.windBearing,
      windSpeed: doc.windSpeed,
      cloudCover: doc.cloudCover,
      uvIndex: doc.uvIndex,
      visibility: doc.visibility,
      summary: doc.summary,
    });
  }

  componentWillMount() {
    this.fetchData();
  }

  renderWeatherIcon() {
    return(
      <Image 
        source={require('./assets/sunny_icon.png')}
        style={{ width: 100, height: 100, }}
      />
      
    );
  }

  render() {
    return (
      <View style={styles.container}>
        <View style={{ flex: 1, flexDirection: 'row' }}>
          <View style={{ flex: 2 }}>
            <Text style={{fontSize: 28, fontWeight: 'bold', color: 'white'}}>
              Miami, FL
            </Text>
            <Text style={{fontSize: 24, fontWeight: 'bold', color: 'white'}}>
              {(new Date(Date.now())).toDateString()}
            </Text>
            <Text style={{fontSize: 20, fontWeight: 'bold', color: 'white'}}>
              {this.state.summary}
            </Text>
            <Text style={{fontSize: 18, fontWeight: 'bold', color: 'white'}}>
              Temperature: {this.state.temperature+ " \u2109"}
            </Text>
          </View>
          <View style={{ flex: 1 }}>
           {this.renderWeatherIcon()}
          </View>
        </View>
        <View style={{ flex: 1, flexDirection: 'row' }}>
          <View style={{ flex: 1 }}>
            <Text style={styles.textStyle}>Precipitation: {'\n'}{this.state.percipIntensity} cm</Text>
            <Text style={styles.textStyle}>Wind Speed: {'\n'}{this.state.windSpeed} mph</Text>
            <Text style={styles.textStyle}>Humidity: {'\n'}{this.state.humidity * 100} %</Text>
            <Text style={styles.textStyle}>Pressure: {'\n'}{this.state.pressure} hPa</Text>
          </View>
          <View style={{ flex: 1 }}>
            <Text style={styles.textStyle}>Precipitation Probability: {'\n'}{this.state.percipProbability * 100} %</Text>
            <Text style={styles.textStyle}>Wind Bearing: {'\n'}{this.state.windBearing}</Text>
            <Text style={styles.textStyle}>UV Index: {'\n'}{this.state.uvIndex}</Text>
          </View>
        </View>
        <View style={{ flex: 1 }}/>
        <View style={{ flex: 1 }}/>
      </View>
    );
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
    paddingRight: 10
  },
  textStyle: {
    color: 'white',
    paddingTop: 10
  }
});
