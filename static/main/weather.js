// dom elements
var weather = $(".weather"),
  brightness = $(".brightness"),
  bgColor = $(".color"),
  forecast = $(".forecast"),
  currentClasses,
  currentTemp;

var days = ["Sun", "Mon", "Tues", "Wed", "Thur", "Fri", "Sat"];

var weatherData = [[new Date().getTime() / 1000, 33, "partly-cloudy-day"]];

var forecastData = [
  [1376978400, 25.5, "snow"],
  [1377064800, 37, "rain"],
  [1377151200, 34.4, "clear-day"],
  [1377237600, 40.4, "sleet"],
];

var renderForecast = function (data) {
  console.log(data);
  forecast.empty();
  _.each(_.first(data, 3), function (item) {
    var classes = iconClasses[item[2].toLowerCase()];
    var wrapper = createElement("div", "forecast-item");
    _.each(classes, function (className) {
      wrapper.append(createElement("i", "icon-" + className));
    });
    wrapper.append(createElement("div", "temp", (+item[1]).toFixed() + "°"));
    wrapper.append(
      createElement("div", "day", days[new Date(item[0] * 1000).getDay()])
    );
    forecast.append(wrapper);
  });
};

var renderWeather = function (temp, conditions) {
  var classes = iconClasses[conditions.toLowerCase()];

  // Transistion in new Icons if needed
  if (classes !== currentClasses) {
    _.each($(".weather i"), function (elem) {
      $(elem).removeClass("scaleUp").addClass("scaleDown");
    });

    _.each(classes, function (className) {
      weather.append(createElement("i", "scaleUp icon-" + className));
    });
  }

  //First Load
  if (!currentTemp) {
    setTemp(temp, "scaleUp");
  }
  //New Data
  else if (currentTemp !== temp) {
    setTemp(temp, "moveFromTopFade");
  }

  setBackground(temp);

  currentTemp = temp;
  currentClasses = classes;
};

var setBackground = function (temp, time) {
  var bgElem = createElement("div");
  if (temp >= 90) {
    bgElem.addClass("hot");
  } else if (temp >= 65) {
    bgElem.addClass("warm");
  } else if (temp >= 32) {
    bgElem.addClass("cold");
  } else {
    bgElem.addClass("freezing");
  }

  bgColor.append(bgElem);
};

var setBrightness = function (hour) {
  var brightnessClass;

  if (hour < 5 || hour > 21) {
    brightnessClass = "night";
  } else if (hour < 7 || hour > 18) {
    brightnessClass = "sun";
  } else {
    brightnessClass = "day";
  }

  brightness.removeClass("day sun night").addClass(brightnessClass);
};

var setTemp = function (temp, className) {
  $(".temp")
    .removeClass("moveFromBottomFade scaleUp")
    .addClass("moveToBottomFade");
  weather.append(createElement("div", "temp " + className, temp + "°"));
};

var createElement = function (tagName, className, text) {
  return $("<" + tagName + ">")
    .addClass(className)
    .text(text);
};

var iconClasses = {
  "clear-day": ["sun"],
  "clear-night": ["moon"],
  rain: ["basecloud", "rainy"],
  snow: ["basecloud", "snowy"],
  sleet: ["basecloud", "sleet"],
  wind: ["basecloud", "windy"],
  fog: ["mist"],
  cloudy: ["cloud"],
  "partly-cloudy-day": ["sunny-cloud", "sunny-cloud-sunny"],
  "partly-cloudy-night": ["sunny-cloud", "sunny-cloud-night"],
};

$("body").addClass("loaded");
var currentWeather = _.map(weatherData[0], function (d) {
  if (typeof d === "object") {
    return d.value;
  }
  return d;
});

var currentHour = new Date(currentWeather[0] * 1000).getHours();
renderWeather((+currentWeather[1]).toFixed(), currentWeather[2]);
setBrightness(currentHour);
renderForecast(forecastData);

window.setTimeout(function () {
  renderWeather(97, "clear-day");
}, 4.5e3);

window.setTimeout(function () {
  renderWeather(74, "clear-night");
}, 3e3);

window.setTimeout(function () {
  renderWeather(62, "rain");
}, 6e3);

window.setTimeout(function () {
  renderWeather(27, "snow");
}, 1.5e3);
