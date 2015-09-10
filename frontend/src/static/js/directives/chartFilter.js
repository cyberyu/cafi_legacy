SearchApp.directive('chartFilter', function () {
  // define constants and helpers used for the directive
  var margin = {top: 0, right: 8, bottom: 0, left: 8},
      height = 40 - margin.top - margin.bottom;

  formatForQuery = d3.time.format('%Y-%m-%d');
  formatDate = d3.time.format('%m/%d/%y');

  function getChartWidth () {
    return angular.element('.search_graph-filter').innerWidth()-30;
  }

  return {
    restrict: 'EA',
    scope: true,
    link: function (scope, element, attrs) {

      // On resize, re-render. This could be done with scope.$appy() but resize does
      // not change the scope on the chart so re-rendering without running the digest
      // cycle should be more performant across the DOM
      window.onresize = function() {
        scope.render();
      };

      // Render a new chart each time scope.chartData changes - this includes initial load
      // which was not covered by the previous watch on chartData alone
      scope.$watch('chartData', function(newVal, oldVal){
        setTimeout(function(){
          scope.render();
        }, 10);
      });

      scope.render = function () {
        var x = d3.time.scale().range([0, getChartWidth()]);

        var y = d3.scale.linear().range([height, 0]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient('bottom')
            .outerTickSize(0)
            .ticks(4);

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient('left')
            .outerTickSize(0);

        // the line for histogram data
        var line = d3.svg.line()
            .x(function(d) { return x(d.key); })
            .y(function(d) { return y(d.doc_count); })
          .interpolate('basis');

        // the shaded area under the line
        var area = d3.svg.area()
            .x(function(d) { return x(d.key); })
            .y0(height)
            .y1(function(d) { return y(d.doc_count); })
          .interpolate('basis');

        var chartTarget = '#date_chart';

        d3.select(chartTarget).selectAll("svg").remove();
        var svg = d3.select(chartTarget).append('svg')
            .attr('class', 'd3-chart-filter')
            .attr('width', getChartWidth() + margin.right + margin.left )
            .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

        // the histogram data
        var dd = scope.chartData;

        var xmin = d3.min(dd, function (d) {
          return d.key;
        });
        var xmax = d3.max(dd, function (d) {
          return d.key;
        });
        var ymin = d3.min(dd, function (d) {
          return d.doc_count;
        });
        var ymax = d3.max(dd, function (d) {
          return d.doc_count;
        });

        x.domain([xmin, xmax]);
        y.domain([ymin, ymax]);

        svg.append('path')
            .datum(dd)
            .attr('class', 'area')
            .attr('d', area);

        svg.append('g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0,' + (height + 0) + ')')
            .call(xAxis);

        ////// brush stuff ////////

        // minimum and largest date
        var startValue = dd[0].key;
        var endValue = dd[dd.length - 1].key;
        var brushFrom = startValue;
        var brushTo = endValue;

        var timeScale = d3.time.scale()
            .domain([startValue, endValue])
            .range([0, getChartWidth()]);

        if (scope.dateRange.from) {
          brushFrom = Date.parse(scope.dateRange.from);
        }

        if (scope.dateRange.to) {
          brushTo = Date.parse(scope.dateRange.to);
        }

        var brush = d3.svg.brush()
            .x(timeScale)
            .extent([brushFrom, brushTo])
            .on('brushstart', brushstart)
            .on('brush', brushmove)
            .on('brushend', brushend);

        var gBrush = svg.append('g')
            .attr('class', 'brush')
            .attr('id', 'brush')
            .call(brush);

        gBrush.selectAll('rect')
            .attr('height', height);

        gBrush.selectAll(".resize")
            .append("path")
            .attr("d", resizePath);

        function brushed () {
          var extent0 = brush.extent(),
              extent1;

          // if dragging, preserve the width of the extent
          if (d3.event.mode === 'move') {
            var d0 = d3.time.day.round(extent0[0]),
                d1 = d3.time.day.offset(d0, Math.round((extent0[1] - extent0[0]) / 864e5));
            extent1 = [d0, d1];
          }
          // otherwise, if resizing, round both dates
          else {
            extent1 = extent0.map(d3.time.day.round);

            // if empty when rounded, use floor & ceil instead
            if (extent1[0] >= extent1[1]) {
              extent1[0] = d3.time.day.floor(extent0[0]);
              extent1[1] = d3.time.day.ceil(extent0[1]);
            }
          }

          d3.select('brush').call(brush.extent(extent1));

          // Brush uses different format from ES filters, so generating them here
          start_date_filter = formatForQuery(extent1[0]);
          end_date_filter = formatForQuery(extent1[1]);

          //start and end date values for brush
          start_date = formatDate(extent1[0]);
          end_date = formatDate(extent1[1]);

          return [start_date_filter, end_date_filter];
        }

        brushstart();
        brushmove();

        function brushmove () {
          var ext = brush.extent();
        }
        function brushstart () {

        }
        function brushend () {
          var ext = brush.extent();
          var newExtent = brushed();
          setNewBrushFromChart( newExtent );
        }

        function resizePath(d) {
          // Style the brush resize handles. No idea what these vals do.
          var e = +(d == "e"),
              x = e ? 1 : -1,
              y = height / 4;
          return "M" + (.5 * x) + "," + y + "A6,6 0 0 " + e + " " + (6.5 * x) + "," + (y + 6) + "V" + (2 * y - 6) + "A6,6 0 0 " + e + " " + (.5 * x) + "," + (2 * y) + "Z" + "M" + (2.5 * x) + "," + (y + 8) + "V" + (2 * y - 8) + "M" + (4.5 * x) + "," + (y + 8) + "V" + (2 * y - 8);
        }

        function setNewBrushFromChart ( newExtent ) {
          scope.dateRange.from = newExtent[0];
          scope.dateRange.to = newExtent[1];
          scope.$apply();
          scope.sendQuery(true);
        }
      };

    },
        template: '<div id="date_chart"></div>'
  };
});
