let mapOptions = {
    center: [46.7135, 7.9706],
    zoom: 9
}


let map = new L.map('map', mapOptions);

let layer = new L.TileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}{r}.png');
map.addLayer(layer);

/*

//default marker:
let marker = new L.Marker([46.95124,7.43873]);
marker.addTo(map);*/





//Once leaflet is set up I create a SVG to use with D3.js and add it to the map
var svgLayer = L.svg();
svgLayer.addTo(map);

//Then I use d3 to get the specific SVG and the grouping that is implicitly created by Leaflet
var svg = d3.select("#map").select("svg");
var g = svg.select('g')//.attr("class", "leaflet-zoom-hide");

//Load the json file and once loaded, process it
d3.json("data.json", function(pointsOfInterest) {

    //create the LatLng objects required by the mapping functions
    pointsOfInterest.forEach(function(d) {
        d.latLong = new L.LatLng(d.x, d.y);
    });

    //Create the circles with the appropriate colour, opacity and radius.
    var feature = g.selectAll("circle")
        .data(pointsOfInterest)
        .enter()
        .append("circle")
        //.style("stroke", "black")
        .style("opacity", 1)
        .style("fill", function(d) {
            if (d.status == 1) { return "red"; }
            if (d.status == 2) { return "orange"; }
            if (d.status == 3) { return "green"; }
            if (d.status == 0) { return "gray"; }
        })
        .attr("r", getZoom());

    //Function which sets the transformation attribute to move the circles to the correct location on the map
    function drawAndUpdateCircles() {
        feature.attr("transform",
            function(d) {
                var layerPoint = map.latLngToLayerPoint(d.latLong);
                return "translate("+ layerPoint.x +","+ layerPoint.y +")";
            }
        )
        
        feature.attr("r", getZoom())
    }

    function getZoom() {
        return map.getZoom();
    }
    //Finally set up the initial circles and bind the update
    drawAndUpdateCircles();
    map.on("moveend", drawAndUpdateCircles);

});

