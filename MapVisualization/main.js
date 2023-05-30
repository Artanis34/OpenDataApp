import 'leaflet';
import 'leaflet.markercluster';
import 'leaflet.markercluster.placementstrategies';

import '@kalisio/leaflet.donutcluster/src/Leaflet.DonutCluster.css'
import '@kalisio/leaflet.donutcluster/src/Leaflet.DonutCluster.js'

import * as colors from './colors.js';
import { tileLayer } from 'leaflet';
import { valHooks } from 'jquery';
import { drawChart } from './d3handler.js';
 
const params = new Proxy(new URLSearchParams(window.location.search), {
  get: (searchParams, prop) => searchParams.get(prop),
});
// Get the value of "some_key" in eg "https://example.com/?some_key=some_value" //

let mapOptions = {
    center: [46.7135, 7.9706],
    zoom: 9,
    className: 'map-tiles',
}

const mapLightBackground = 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png';
//const mapBackground = 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png';

let map = new L.map('mapid', mapOptions);
var mapLayer = new L.TileLayer(mapLightBackground, {
  maxZoom: 18,
    attribution:'&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',
  });
map.addLayer(mapLayer);


var OpenRailwayMap = L.tileLayer('https://{s}.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png', {
	maxZoom: 18,
	attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Map style: &copy; <a href="https://www.OpenRailwayMap.org">OpenRailwayMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
});
var showRailway = false;

/*Legend specific*/
var legend = L.control({ position: "bottomleft" });

legend.onAdd = function(map) {
  var div = L.DomUtil.create("div", "legend");
  div.innerHTML += "<h4>Legende</h4>";
  div.innerHTML += '<i style="background: red"></i><span>Unvollständig</span><br>';
  div.innerHTML += '<i style="background: green"></i><span>Erfasst</span><br>';
  div.innerHTML += 'Data Timestamp: <b id="timestamp">Unknown</b>';
  return div;
};

legend.addTo(map);


// Create the markercluster
var markers = L.DonutCluster(
    // The first parameter is the standard marker cluster's configuration.
    {
        spiderLegPolylineOptions: { weight: 0 },
        helpingCircles: true,
        clockHelpingCircleOptions:  { fillOpacity: 1, color: 'grey', weight: 0.3 },
        elementsPlacementStrategy: 'one-circle',
        spiderfyDistanceMultiplier: 1.8,

        chunkedLoading: true,
        spiderfyOnMaxZoom: true,
        showCoverageOnHover: false,
        zoomToBoundsOnClick: true,
        reremoveOutsideVisibleBoundsmoveOut: true,
        disableClusteringAtZoom: 18,

    },
    // The second parameter is the donut cluster's configuration.
    {
        // Mandotary, indicates the field to group items by in order to create donut' sections.
        key: 'Status',
        order: colors.color.values,
        // Mandotary, the arc color for each donut section.
        // If array of colors will loop over it to pick color of each section sequentially.
        arcColorDict: colors.color,
        hideLegend: false,
        textClassName: 'donut-text',
        // Optional, the style of the donut
        style: {
            size: 60,
            fill: 'white',
            opacity: 1,
            weight: 3 
        },
        // Function used to customize legend output
        //getLegend: (title, color, percentage, value) => `<spans style='color:black;'>${title}:&nbsp;${parseInt(percentage)}%</span>`
    }
);


var DataCircleMarker = L.CircleMarker.extend({
  options: {
    data: ''
  }
})

function loadMarkers() {

  //var pUrl = "/data/example.geojson";
  var pUrl = "/data/geoData.geojson"
  //var pUrl = "/data/geodata(small).geojson";

  // Use jQuery to load date from GeoJSON file

  $.getJSON(pUrl, function(data) {

    //var dataArray = {'0':0,'1':0,'2':0,'3':0,};

    var geoJsonLayer = L.geoJson(data, {
      filter: function(feature, layer) {
        return filterMarker(feature, layer);
      },
      pointToLayer: function(feature, latlng) {

        //dataArray[feature.properties.status] += 1;

        var label = '<h4>' + feature.properties.Name + '<br>' + feature.properties.Verkehrsmittel +' (' + feature.properties.Bezeichnung + ')</h4>';
            label += feature.properties.Service + '<br>';
            label += latlng.lat + ', ' + latlng.lng + '<br>';

      
        var pMarker = new L.Marker(latlng, {
          title: feature.properties.Name
        });

        pMarker = new DataCircleMarker(latlng, {
          title: feature.properties.Name,
          radius: 11,
          color: '#FFFFFF',
          weight: 2,
          fillOpacity: 0.5,
          //riseOnHover: true,
          status: feature.properties.Status,
          fillColor: colors.color[feature.properties.Status],
          data: feature,
        });
        pMarker.bindPopup(label);
        markers.addLayer(pMarker);

        return pMarker;
      }
    });

    // Add geoJsonLayer to markercluster group

    markers.on('clusterclick', function(a) {
      console.log('Cluster Clicked:' + a);
      console.log(a);
      a.layer.getAllChildMarkers().forEach(element => {
        //console.log(element);
        //element.setZIndexOffset(1000);
      });
    });
    markers.on('click', function(a) {
      console.log('Marker Clicked:' + a);
      updateSelectionView(a);
    });

    /*markers.on('clustermouseover', function(a) {
      
    })*/

    // Add the markercluster group to the map
    map.addLayer(markers);
    drawChart(data);
  });
  
}


var filters = {};
function filterMarker(feature, layer) {
  if (filters.size <= 0) {
    return true;
  }
  for (var key in filters) {
    var filter = filters[key] || '';
    var actual = feature.properties[key];
    //console.log(actual);
    if (filter != '' && actual.toString().toLowerCase() != filter.toString().toLowerCase()) {
      
      return false;
    }
  }

  return true;
  /* if (service != null && service !="") {
    return (feature.properties.service.toLowerCase() == service.toLowerCase());
  } else {
    return true;
  } */
}

function updateFilter() {
  filters = {
    Service: document.getElementById('Service').value,
    Kanton: document.getElementById('Kanton').value,
    Gemeinde: document.getElementById('Gemeinde').value,
    Status: document.getElementById('Status').value,
  };

  //console.log("filter:" + filter['services']);
}

function updateSpecificFilter(filter, value) {
  document.getElementById(filter).value = value.toString();
}

// fetch get parameterss
function fetchGetFilters() {
  if (params.Service != null && params.Service != '') {
    updateSpecificFilter('Service', params.Service);
  }
}
var fUrl = './data/kantonAndService.json'
fetchFilters();
//reloadMap();//fetch filters instead!!!
function fetchFilters() {
  $.getJSON(fUrl, function(data) {

    for (var filter in data) {
      if (filter == "Last_modified") {
        document.getElementById('timestamp').innerHTML = data.Last_modified;
        continue;
      }
      if (filter == "Gemeinde") { continue;}
      var select = document.getElementById(filter);
      for(var key in data[filter]) {
        var opt = document.createElement('option');
        opt.value = data[filter][key];
        opt.innerHTML = data[filter][key];
        select.appendChild(opt);
      }
    }

    fetchGetFilters();
    reloadMap();
  });
}

function bs() {
  updateGemeinde();reloadMap();
}
//add onchange eventlistener to filters
document.getElementById('Service').onchange = reloadMap;
document.getElementById('Status').onchange = reloadMap;
document.getElementById('Gemeinde').onchange = reloadMap;
document.getElementById('Kanton').onchange = bs;
document.getElementById('showOpenRailMap').onchange = reloadMap;



function updateGemeinde() {
  $.getJSON(fUrl, function(data) {

    var selectCanton = document.getElementById('Kanton');
    var selectGemeinde = document.getElementById('Gemeinde');
    //selectGemeinde.value = "";
    selectGemeinde.innerHTML = '<option value="">All</option>';


    for (var Canton in data.Gemeinde) {

      if (selectCanton.value != "" && selectCanton.value != null) {
        if (selectCanton.value != data.Gemeinde[Canton].Kanton) {
          continue;
        }
      }
      for (var gemeinde in data.Gemeinde[Canton].Gemeinden) {
        
        var opt = document.createElement('option');
        opt.value = data.Gemeinde[Canton].Gemeinden[gemeinde];
        opt.innerHTML = data.Gemeinde[Canton].Gemeinden[gemeinde];
        selectGemeinde.appendChild(opt);
        
      }
    }
    updateFilter();

  });
}

function reloadMap() {

  map.removeLayer(markers)
  markers.clearLayers()
  updateFilter();
  updateSelectionView(null);
  //console.log(filters);
  loadMarkers();

  if (document.getElementById('showOpenRailMap').checked) {
    map.addLayer(OpenRailwayMap);
  } else {
    map.removeLayer(OpenRailwayMap);
  }
  
}




function updateSelectionView(marker) {

  if (marker == null) {
    document.getElementById('selectionView').innerHTML = 'No Selection';
    return;
  }

  console.log('selection now: ' + marker.sourceTarget.options.data);
  console.log(marker.sourceTarget.options.data);
  var selection = marker.sourceTarget.options.data;

  if (selection != null) {
    var outputString = "";
    for (var key in selection.properties) {
      outputString += key + ": ";
      if (selection.properties[key] == 99) {
        outputString += 'NaN';
      } else {
        outputString += selection.properties[key];
      }
      outputString += "<br>";
    }
    document.getElementById('selectionView').innerHTML = outputString;
  }
}