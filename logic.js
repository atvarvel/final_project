
// Create the tile layer that will be the background of our map
var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "light-v10",
  accessToken: API_KEY
}).addTo(myMap);
 console.log(API_KEY);



/************************* 
 * Event listener code for dropdown
 ***********************/

function processFilters() {
  var review_type = d3.select('#sel-type').node().value;
  var airline = d3.select('#sel-airline').node().value;

  grab_reviews(review_type, airline);
  populateMap(review_type, airline);
}
//grab our review classes 
function grab_reviews(review_type, airline) {
  d3.json(`/api/bandconcerts/${review_type}`).then(data => {
    

    //filteredData = data.filter(d => d['year'] == year);
    console.log(data);
    
    var band_year = data.map(d => 'Year ' + d['year'].toString());
    var band_concerts = data.map(d => d['concerts']);

    var data = [{
      type: 'bar',
      x: band_concerts,
      y: band_year,
      orientation: 'h'
    }];
    
    Plotly.newPlot('band-plot', data);

  });
}

function populateMap(band_name, year){

  var link = `/api/bandyear/${band_name}`



  // // Grabbing our sql data..
  d3.json(link).then(function(response) {


    // clear existing layers if they exist

    try{
      layerGroup.clearLayers();
    }
    catch {
      console.log('No layer group to clear');
    }
    

    var filteredData = response.filter(d => d['year'] == year);

    // var markerclustergroup = L.markerClusterGroup();

    // Creating a layer with the retrieved data
    layerGroup = L.layerGroup().addTo(myMap);

    // //for loop for coordinates
    for (var i = 0; i < filteredData.length; i++) {
      var location = filteredData[i];
      
      //check for location property
      if (location) {
      // Add a new marker to the cluster group and bind a pop-up
       L.marker([location.lat, location.long])
       .bindPopup(`${location.band}<br/>${location.year}<br/>${location.city}`).addTo(layerGroup);
       }
      }
    //myMap.addLayer(markerclustergroup);
    });

    /*
    var markers = L.markerClusterGroup();
    markers.addLayer(L.marker([lat[1], [0]])
            .bindPopup(`${filteredData[i].year}<hr/>${filteredData[i].year}<br/>${filteredData[i].city}`));

    var marker = L.marker([32,-16], {
      draggable: true,
      title: "My First Marker"
    }).addTo(myMap);
    */
}

// // Initialize all of the LayerGroups we'll be using
// // var layers = {
//   // 2005: new L.LayerGroup(),
//   // 2010: new L.LayerGroup(),
//   // 2015: new L.LayerGroup(),
//   // 2019: new L.LayerGroup(),
// // };

// // Create the map with our layers
// // var map = L.map("marker-map", {
//   // center: [42.88, -97.38],
//   // zoom: 5,
//   // layers: [
//     // layers.2005,
//     // layers.2010,
//     // layers.2015,
//     // layers.2019,
//   // ]
// // });
// // 




