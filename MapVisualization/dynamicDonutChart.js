export class DynamicDonutChart {
    constructor() {
      console.log("Initialize Donutchart");
  
      this.width = document.getElementById('my_dataviz').offsetWidth;
      this.height = this.width;
      this.margin = 20;
  
      this.radius = Math.min(this.width, this.height) / 2 - this.margin;
  
      this.svg = d3.select("#my_dataviz")
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)
        .append("g")
        .attr("transform", `translate(${this.width / 2},${this.height / 2})`);
  
      this.data = { 0: 20, 1: 10, 2: 0 };
  
      this.color = d3.scaleOrdinal()
        .domain(["0", "1", "2"])
        .range(["#e41a1c", "#4daf4a", "#ff7f00"]);
  
      // The arc generator
      this.arc = d3.arc()
        .innerRadius(this.radius * 0.5)         // This is the size of the donut hole
        .outerRadius(this.radius * 0.8);
  
      // Another arc that won't be drawn. Just for labels positioning
      this.outerArc = d3.arc()
        .innerRadius(this.radius * 0.9)
        .outerRadius(this.radius * 0.9);
  
      this.updateChart(this.data);
      // Add percentage text in the middle of the chart
      const total = d3.sum(Object.values(this.data));
      const percentage = Math.round((this.data[1] / total) * 100); // Modify this line to calculate the desired percentage
      this.svg.append("text")
        .attr("class", "percentage-text")
        .attr("text-anchor", "middle")
        .attr("dy", ".35em")
        .text(`${percentage}%`)
        .style("font-size", "24px");
    
      
    }
  
    updateChart(newData) {
      // Update the data property with the new data
      this.data = newData;
  
      // Compute the position of each group on the pie with the new data:
      const pie = d3.pie()
        .sort(null) // Do not sort group by size
        .value(d => d[1]);
      const data_ready = pie(Object.entries(this.data));
  
      // Update the existing slices with the new data
      const slice = this.svg.selectAll('path')
        .data(data_ready);
  
      // Update existing slices
      const arc = this.arc; // Store reference to 'this.arc'
      slice.transition()
        .duration(500)
        .attrTween('d', function (d) {
          const interpolate = d3.interpolate(this._current, d);
          this._current = interpolate(0);
          return function (t) {
            return arc(interpolate(t));
          };
        });
  
      // Add new slices
      const newSlice = slice.enter()
        .append('path')
        .attr('d', this.arc)
        .attr('fill', (d) => this.color(d.data[1]))
        .attr('stroke', 'white')
        .style('stroke-width', '2px')
        .style('opacity', 0)
        .each(function (d) { this._current = { startAngle: 0, endAngle: 0 }; })
        .transition()
        .duration(500)
        .styleTween('opacity', (d) => {
          const i = d3.interpolate(0, 0.7);
          return (t) => i(t);
        })
        .style('pointer-events', 'visible')
        .attrTween('d', function (d) {
          const startAngleInterpolation = d3.interpolate(this._current, d);
          const endAngleInterpolation = d3.interpolate(this._current, d);
          this._current = d;
          return function (t) {
            const startAngle = startAngleInterpolation(t);
            const endAngle = endAngleInterpolation(t);
            d.startAngle = startAngle.startAngle;
            d.endAngle = endAngle.endAngle;
            return arc(d);
          };
        });
  
      // Add percentage text in the middle of the chart
      const total = d3.sum(Object.values(this.data));
      const percentage = Math.round((this.data[1] / total) * 100); // Modify this line to calculate the desired percentage
      const t = this.svg.select("text")
        .transition()
        .duration(1000)
        .text(`${percentage}%`)

  
      // Remove old slices
      slice.exit()
        .transition()
        .duration(500)
        .styleTween('opacity', (d) => {
          const i = d3.interpolate(0.7, 0);
          return (t) => i(t);
        })
        .remove();

    }

    
  }
  