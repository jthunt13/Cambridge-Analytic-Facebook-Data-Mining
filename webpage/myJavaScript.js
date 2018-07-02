// graphics variables
var windowMargins = {left : 80,
        right: 80,
        top : 200,
        bottom : 100};

var figMargin = {
        top : 40,
        bottom : 80,
        left : 60,
        right : 20
        };

var nytBarChart = "nytCamAnalytop50.csv";
var twitterBarChart = "twitterCamAnalytop50.csv";
var term = [];
var tm = [];
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

    if(searchTerm === "Cambridge Analytic"){
        term = "CamAnaly";
    }else{
        term = "Facebook";
    };

    if(timeTerm === "1 Week"){
        tm = "Full";
    }else{
        tm = "Partial"
    }
    nytBarChart = "./data/nyt" + term + tm +"top"+ amountTerm +".csv";
    twitterBarChart = "./data/twitter" + term + tm +"top" + amountTerm +".csv";
    nytWordCloud = "./data/nyt" + term + tm + "top50.csv";
    twitterWordCloud = "./data/twitter" + term + tm + "top50.csv";
    nytCooccurance = "./data/nyt" + term + tm + "Co.csv";
    twitterCooccurance = "./data/twitter" + term + tm + "Co.csv";

    [graphWidth, graphHeight] = graphicSize();

    // change titles
    wordCountSearchTerm.innerText = "Search Term: " + searchTerm;
    wordCountSearchTerm2.innerText = "Search Term: " + searchTerm;
    wordCountSearchTerm3.innerText = "Search Term: " + searchTerm;
    //clear old plots
    d3.selectAll("#area1 > *").remove();
    d3.selectAll("#area2 > *").remove();
    d3.selectAll("#area3 > *").remove();
    //create bar charts
    barGraphV3("#area1",twitterBarChart,graphHeight,graphWidth,"Twitter");
    barGraphV3("#area1",nytBarChart,graphHeight,graphWidth,"New York Times Article");

    wordCloud("#area2",twitterWordCloud,graphHeight,graphWidth,"Twitter");
    wordCloud("#area2",nytWordCloud,graphHeight,graphWidth,"New York Times Article");
    //co-occurance word cloud
    wordCloud("#area3",twitterCooccurance,graphHeight,graphWidth,"Twitter");
    wordCloud("#area3",nytCooccurance,graphHeight,graphWidth,"New York Times Article")

};

function barGraphV3(fig,csv,h,w,title){

    // make padded dimensions to put plot into
    var width = w - figMargin.left - figMargin.right;
    var height = h - figMargin.top - figMargin.bottom;

    //create x-axis
    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    // create y-axis
    var y = d3.scale.linear()
        .range([height,0]);

    // create x-axis
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    // create y-axis
    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    // create a tooltip
    var div = d3.select(fig).append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    // call and initiailize figure to use
    var plot = d3.select(fig)
        .append("svg") // initialize graphics window
            .attr("width", w)
            .attr("height", h)
        .append("g") // add padding
            .attr("transform",
                "translate(" + figMargin.left + "," + figMargin.top + ")");

    // get data
    d3.csv(csv, function(error, data) {
    // map the data to correct types
    data.forEach(function(d) {
        d.word = d.word;
        d.count = +d.count;
        });

    // define the domain of the axis based on the  data
    x.domain(data.map(function(d) { return d.word; }));
    y.domain([0, d3.max(data, function(d) { return d.count; })]);

    // add x-axis
    plot.append("g")
          .attr("class", "axis") // assign axis line style
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis)
        .selectAll("text") //grab all text and rotate
          .attr("class","axisLabel") // assign text style
          .attr("y", 0)
          .attr("x", 9) // increase center of rotation
          .attr("dy", ".35em")
          .attr("transform", "rotate(70)")
          .style("text-anchor", "start");
          //.append("text")

        // add the y axis
      plot.append("g")
          .attr("class", "axis")
          .call(yAxis)
        .selectAll("text")
          .attr("class","axisLabel");

        // add bars
      plot.selectAll(".bar")
          .data(data)
        .enter().append("rect")
            .attr("class","bar")
          .attr("x", function(d) { return x(d.word); })
          .attr("width", x.rangeBand())
          .attr("y", function(d) { return y(d.count); })
          .attr("height", function(d) { return height - y(d.count); })
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
              .style("top", (d3.event.pageY-28) + "px");});

      //add y-label
      plot.append("text")
          .attr("class",".plotLabel") //define style0
          .attr("transform", "translate(" + (0-3*figMargin.left/4) + "," + ((h - figMargin.top)/2) + ") rotate(-90)")
          .text("Frequency");

    //add a title
      plot.append("text")
          .attr("class",".plotTitle") // defines style
          .attr("x", (width / 2))
          .attr("y", 0 - (figMargin.top / 2))
          .style("text-anchor", "middle") // center the title
          .text(title);

    });
} // end barGraphV3


function wordCloud(fig,csv,h,w,title){

    var cloudMargin = {
            top : 30,
            bottom : 0,
            left : 0,
            right : 0
            };

    var width = w - cloudMargin.left - cloudMargin.right;
    var height = h - cloudMargin.top - cloudMargin.bottom;

    //define colorscale
    var colorScale = d3.scale.category20();

    d3.csv(csv, function(d) {
        return { // for each csv row return an object with text and size
          text: d.word,
          size: +d.count
        }
    },function(data){

        // get largest count
        var max = d3.max(data, function(d) {return d.size});

        d3.layout.cloud()
            .size([width, height])
            .words(data)
            .rotate(function() {return ~~(Math.random() * 180);})
            .fontSize(function (d) {return Math.floor((d.size/max)*30);})
            .on("end",draw)
            .start();

        function draw(words){

            var plot = d3.select(fig).append("svg") // initialize figure
                .attr("width", width)
                .attr("height", height)
              .append("g") // shift for padding
                .attr("transform",
                    "translate(" + w/2 + "," + h/2 +")");

              plot.selectAll("text") // grab words
                .data(words)
              .enter().append("text") //apply scaling and filling
                .style("font-size", function(d)
                    {return d.size+ "px";}) // get size of text
                .style("font-family","Impact") // set font
                .style("fill", function(d,i)
                    {return colorScale(Math.floor(Math.random()*20) + 1);}) // fill word
                .attr("text-anchor","middle")
                .attr("transform",function(d) {
                    return "translate("+[d.x,d.y]+") rotate("+d.rotate+")";})
                .text(function(d) { return d.text;});

                plot.append("text")
                    .attr("class",".plotTitle") // defines style
                    .attr("y", 0 - (height / 2))
                    .style("text-anchor", "middle") // center the title
                    .text(title);

        }// end draw


    }); //end csv reader
} // end word cloud
