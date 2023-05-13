import 'leaflet';
import 'leaflet.markercluster';

import '@kalisio/leaflet.donutcluster/src/Leaflet.DonutCluster.css'
import '@kalisio/leaflet.donutcluster/src/Leaflet.DonutCluster.js'

import * as fct from './functions.js';
//import { CircleMarker } from 'leaflet';
 

let mapOptions = {
    center: [46.7135, 7.9706],
    zoom: 9,
    className: 'map-tiles'
}


let map = new L.map('mapid', mapOptions);

let layer = new L.TileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}{r}.png');
map.addLayer(layer);

/* var markers = L.markerClusterGroup({
  spiderfyOnMaxZoom: true,
  showCoverageOnHover: false,
  zoomToBoundsOnClick: true,
  reremoveOutsideVisibleBoundsmoveOut: true,
}); */

// Create the markercluster
var markers = L.DonutCluster(
    // The first parameter is the standard marker cluster's configuration.
    {
        chunkedLoading: true,
        spiderfyOnMaxZoom: true,
        showCoverageOnHover: false,
        zoomToBoundsOnClick: true,
        reremoveOutsideVisibleBoundsmoveOut: true,

    },
    // The second parameter is the donut cluster's configuration.
    {
        // Mandotary, indicates the field to group items by in order to create donut' sections.
        key: 'status',
        order: ['1', '2', '3', '0'],
        // Mandotary, the arc color for each donut section.
        // If array of colors will loop over it to pick color of each section sequentially.
        arcColorDict: {
            1: 'red',
            2: 'orange',
            3: 'green',
            4: 'gray'
        },
        hideLegend: false,
        textClassName: 'donut-text',
        // Optional, the style of the donut
        style: {
            size: 60,
            fill: 'white',
            opacity: .5,
            weight: 14
        },
        // Function used to customize legend output
        getLegend: (title, color, percentage, value) => `<span>${title}:&nbsp;${percentage}%</span>`
    }
);



var example = "/example.geojson";
var pUrl = "/data/geodata.geojson";

// Use jQuery to load date from GeoJSON file
$.getJSON(pUrl, function(data) {
  var geoJsonLayer = L.geoJson(data, {
    filter: function(feature, layer) {
      return true;
      return (feature.properties.status == "1");
    },
    pointToLayer: function(feature, latlng) {
      var label = '<h4>' + feature.properties.name + '<br>Status: ' + feature.properties.status + '</h4>';
          label += feature.properties.address + '<br>';
          label += latlng + '<br>';

     
      var pMarker = new L.Marker(latlng, {
        title: feature.properties.name
      });

      pMarker = new L.CircleMarker(latlng, {
        title: feature.properties.name,
        radius: 10,
        color: '#FFFFFF',
        weight: 2,
        fillOpacity: 0.5,
        status: feature.properties.status,
        fillColor: fct.getColorFromStatus(feature.properties.status)
      });
      pMarker.bindPopup(label);
      markers.addLayer(pMarker);

      return pMarker;
    }
  });

  // Add geoJsonLayer to markercluster group

  markers.on('clusterclick', function(a) {
    console.log('Cluster Clicked:' + a);
  });
  markers.on('click', function(a) {
    console.log('Marker Clicked:' + a);
  });

  // Add the markercluster group to the map
  map.addLayer(markers);

});