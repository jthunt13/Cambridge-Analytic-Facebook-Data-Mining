// graphics variables
var windowMargins = {left : 80,
        right: 80,
        top : 200,
        bottom : 100};

var figMargin = {
        top : 40,
        bottom : 80,
        left : 50,
        right : 20
        };

// function to determine graphic sizes
function graphicSize() {
    var totalWindowWidth = window.innerWidth;
    var totalWindowHeight = window.innerHeight;

    var graphWidth = (totalWindowWidth - (windowMargins.left + windowMargins.right))/2;
    var graphHeight = (totalWindowHeight - (windowMargins.top + windowMargins.bottom))/2;

    return [graphWidth, 300];
};

function updateGraphs() {
    // get selected search terms
    var searchElem = document.getElementById("searchTerm");
    var searchTerm = searchElem.options[searchElem.selectedIndex].text;

    var timeElem = document.getElementById("timePeriod");
    var timeTerm = timeElem.options[timeElem.selectedIndex].text;

    var amountElem = document.getElementById("wordAmount");
    var amountTerm = amountElem.options[amountElem.selectedIndex].text;

    [graphWidth, graphHeight] = graphicSize();

    // change titles
    wordCountSearchTerm.innerText = "Search Term: " + searchTerm;
    wordCountSearchTerm2.innerText = "Search Term: " + searchTerm;

    //clear old plots
    d3.selectAll("#area1 > *").remove();
    d3.selectAll("#area2 > *").remove();

    //create bar charts
    barGraph("#area1","./data/tmpWordCount.csv",graphHeight,graphWidth,"Twitter");
    barGraph("#area1","./data/tmpWordCount.csv",graphHeight,graphWidth,"New York Times Article");
    // create pie charts
    //pieChart("#area2","./data/tmpWordCount.csv",graphHeight,graphWidth,"Twitter");
    //pieChart("#area2","./data/tmpWordCount.csv",graphHeight,graphWidth,"New York Times Article");

    //barGraph("#area2","./data/tmpWordCount.csv",graphHeight,graphWidth);
};

function barGraph(fig,csv,h,w,title){

    // make padded dimensions to put plot into
    var width = w - figMargin.left - figMargin.right;
    var height = h - figMargin.top - figMargin.bottom;

    // create x-axis
    var x = d3.scaleBand()
        .range([0,width])
        .padding(0.1);
    // create y-axis
    var y = d3.scale.linear()
        .range([height,0]);

    // create empty fig
    var plot = d3.select(fig)
        .append("svg") // initialize graphics window
            .attr("width", w)
            .attr("height", h)
        .append("g") // add padding
            .attr("transform",
                "translate(" + figMargin.left + "," + figMargin.top + ")");

    //add a tooltip
    var div = d3.select(fig).append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    // get data from csv
    d3.csv(csv,function(d){
        d.word = d.word;
        d.count = +d.count;

        return d;
    }, function(error,data){
        if (error) throw error;

        x.domain(data.map(function(d) {return d.word;}));
        y.domain([0, d3.max(data, function(d) {return d.count;})]);

        plot.selectAll(".bar")
            .data(data)
          .enter().append("rect")
            .attr("class","bar")
            .attr("x", function(d) { return x(d.word); })
            .attr("width", x.bandwidth())
            .attr("y", function(d) { return y(d.count); })
            .attr("height", function(d) { return height - y(d.count); })
            // add tool tip functionality
            .on("mouseover", function(d) {
                div.transition()
                    .duration(300)
                    .style("opacity", 1);
                div.html(d.word + "<br/>" + d.count)
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY-28) + "px");})
            .on("mouseout", function(d) {
                div.transition()
                    .duration(500)
                    .style("opacity", 0);})
            .on("mousemove", function(d) {
                div.html(d.word + "<br/>" + d.count)
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY-28) + "px");
            });

        //adds x-axis
        plot.append("g")
                .attr("class", "axis axis--x")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x))
            .selectAll("text") //grab all text and rotate
                .attr("y", 0)
                .attr("x", 9)
                .attr("dy", ".35em")
                .attr("transform", "rotate(60)")
                .style("text-anchor", "start");
            //.append("text")

        //adds y-axis
        plot.append("g")
            .call(d3.axisLeft(y));

        //add y-label
        plot.append("text")
            .attr("class",".plotLabel") //define style0
            .attr("transform", "translate(" + (0-2*figMargin.left/3) + "," + ((h - figMargin.top)/2) + ") rotate(-90)")
            .text("Frequency");

        //add x-label
        plot.append("text")
            .attr("class",".plotLabel") //define style0
            .attr("transform", "translate(" + ((w/2) -figMargin.left) + "," + (h - 3*figMargin.bottom/4) + ")")
            .text("Word");


        //add a title
        plot.append("text")
            .attr("class",".plotTitle") // defines style
            .attr("x", (width / 2))
            .attr("y", 0 - (figMargin.top / 2))
            .style("text-anchor", "middle") // center the title
            .text(title);

    });
}; // end of barGraphFunction



function pieChart(fig,csv,h,w,title){

    // make padded dimensions to put plot into
    var width = w - figMargin.left - figMargin.right;
    var height = h - figMargin.top - figMargin.bottom;

    // set radii
    var outerRadius = Math.min(width,height)/2;
    var innerRadius = 0.5*outerRadius;

    // define color scheme
    var colorScale =  d3.scaleOrdinal(d3.schemeCategory20b);

    var arc = d3.arc()
        .outerRadius(outerRadius)
        .innerRadius(innerRadius)
        .padAngle(0.01)
        .cornerRadius(4);

    var pie = d3.pie()
        .sort(null)
        .value(function(d) { return d.count; });

    // create empty fig
    var plot = d3.select(fig)
        .append("svg") // initialize graphics window
            .attr("width", w)
            .attr("height", h)
        .append("g") // add padding
            .attr("transform",
                "translate(" + width/2 + "," + height/2 + ")");

    //add a tooltip
    var div = d3.select(fig).append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    // get data from csv
    d3.csv(csv,function(d){
        d.word = d.word;
        d.count = +d.count;

        return d;

    }, function(error,data){
        if (error) throw error;

        var g = plot.selectAll(".arc")
            .data(pie(data))
          .enter().append("g")
            .attr("class","arc")
            // add tool tip functionality
            .on("mouseover", function(d) {
                div.transition()
                    .duration(300)
                    .style("opacity", 1);
                div.html(d.word + "<br/>" + d.count)
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY-28) + "px");})
            .on("mouseout", function(d) {
                div.transition()
                    .duration(500)
                    .style("opacity", 0);})
            .on("mousemove", function(d) {
                div.html(d.word + "<br/>" + d.count)
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY-28) + "px");
            });

        // fill slices
        g.append("path")
            .attr("d",arc)
            .style("fill",function(d) {return colorScale(d.count);});

        //add a title
        g.append("text")
            .attr("class",".plotTitle") // defines style
            .attr("x", (width / 2))
            .attr("y", 0 - (figMargin.top / 2))
            .style("text-anchor", "middle") // center the title
            .text(title);

    });
}; // end of barGraphFunction
