// csv file we want to load
let filename = 'RandomData/RandTemp.csv';

// all of your code should be inside this command
d3.csv(filename).then(function(loadedData) {
  
  // let's see if our data loaded correctly
  // (and take a peek at how it's formatted)
  console.log(loadedData);
  
  // empty lists for our data and the labels
  let data =   [];
  let labels = [];
  
  // use a for-loop to load the data from the
  // file into our lists
  for (let i=0; i<loadedData.length; i++) {
    console.log(loadedData[i]);
    
    // get the year and mean temp for each listing
    let year =     loadedData[i].time;
    let meanTemp = loadedData[i].Temp;
    console.log(meanTemp);
    
    // add the year to our labels
    if (year % 5 == 0) {
      labels.push(year)
    }
    else {
      labels.push([])
    };
        
    // and mean temp to the data
    data.push(meanTemp);    
  }
  
  // basic line chart settings
  let options = {
    type: 'line',
      
    data: {
      labels: labels,  // the labels we loaded!
      datasets: [{
        data: data,    // the data we loaded!
        fill: false,
        pointRadius: 0,
        pointHoverRadius: 0,
        borderColor: 'rgb(100,100,100)'
      }]
    },
    options: {
    legend: {
      display: false
    },
      
    title: {
      display: true,
      text: 'Temperature (deg C)'
    }
    }
  };
  
  // with all that done, we can create our chart!
  let chart = new Chart(document.getElementById('canvas1'), options);
});
