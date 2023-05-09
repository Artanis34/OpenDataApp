const svg = d3.select('svg');
const bbox = svg.node().getBoundingClientRect();
const svgWidth = bbox.width;
const svgHeight = bbox.height;

/* Deine Lösung zu Aufgabe 1 Start */
svg.append('circle')
    .classed('circle', true)
    .attr('cx', 0)
    .attr('cy', 0)
    .attr('r', 50)

/* Deine Lösung zu Aufgabe 1 Ende */

/* Deine Lösung zu Aufgabe 2 Start */
d3.select('circle')
    .transition()
    .duration(2000)
    .attr('cx', svgWidth + 50)
    .attr('cy', svgHeight + 50)
    .style('fill', 'blue')

/* Deine Lösung zu Aufgabe 2 Ende */

/**
 * Returns a randomly filled circle object array
 */
function generateRandomData(size) {
    var data = [];
    for (var i = 0; i < size; i++) {
        data.push({
            cx: Math.random() * svgWidth,
            cy: Math.random() * svgHeight,
            r: Math.random() * 20
        });
    }
    return data;
}

const circleGroup = svg.append('g')
    .attr('id', 'circleGroup');


function addNewElements(data) {
    /* Deine Lösung zu Aufgabe 3 Start */
    const circles = circleGroup.selectAll('circle')
        .data(data)
        .enter()
        .append('circle')
        .attr('cx', d => d.cx)
        .attr('cy', d => d.cy)
        .attr('r', d => d.r)
        .classed('circle', true)
        /* Deine Lösung zu Aufgabe 3 Ende */
}


/*
 * Update Selection
 */
function updateExistingElements(data) {
    /* Deine Lösung zu Aufgabe 4 Start */
    const circles = circleGroup.selectAll('circle')
        .data(data)

    circles.transition()
        .duration(2000)
        .attr('cx', d => d.cx)
        .attr('cy', d => d.cy)
        .style('fill', 'blue')

    /* Deine Lösung zu Aufgabe 4 Ende */
}


function removeResidualElements(data) {
    /* Deine Lösung zu Aufgabe 5 Start */
    const circles = circleGroup.selectAll('circle')
        .data(data)

    circles.exit()
        .transition()
        .duration(2000)
        .attr('r', 0)
        .remove()
        /* Deine Lösung zu Aufgabe 5 Ende */
}



function addListenerToCircles() {
    /* Deine Lösung zu Aufgabe 6 Start */
    circleGroup.selectAll('circle')
        .on('mouseenter', function() {
            d3.select(this).style('opacity', 0.5)
        })
        .on('mouseleave', function() {
            d3.select(this).style('opacity', 1)
        })
        /* Deine Lösung zu Aufgabe 6 Ende */
}


/**
 * Updates the DOM based on passed data Array.
 */
function update(data) {
    addNewElements(data);
    updateExistingElements(data);
    removeResidualElements(data);
}

/**
 * Adds click listener to trigger the update function with
 * randomly generated data.
 */
d3.select('#updateData').on('click', function() {
    var random = Math.random() * 100;
    update(generateRandomData(random));
    addListenerToCircles();
});

var firstData = generateRandomData(100); //Ich habe das hier auf 100 gewechselt
update(firstData);
addListenerToCircles();