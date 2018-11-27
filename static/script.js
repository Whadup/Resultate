// Get pre-computed histogram data

	
function initHistogram(json,tag) 
{
	
	
	var binInc = json[0].data[1].bin;
	var maxBin = json[0].data[json[0].data.length-1].bin;
	var binInc = json[0].data[1].bin-json[0].data[0].bin;
	//console.log(maxBin,binInc);
	var i = 0;
		
	// use the name of the group to initialize the array
	var group = json[i].name;
	var data = [];
	
	// we have a max bin for our histogram, must ensure
	// that any bins > maximum bin are rolled into the 
	// last bin that we have
	var binCounts = {};
	for( var j = 0; j < json[i].data.length; j++) {
		var xValue = json[i].data[j].bin;
		// bin cannot exceed the maximum bin
		// xValue = ( xValue > maxBin ? maxBin : xValue);
		var yValue = json[i].data[j].count;
		
		if(binCounts[xValue] === undefined) {
			binCounts[xValue] = 0;
		}
		binCounts[xValue] += yValue;
	}
	
	// add the bin counts in
	var it = 0;
	for( var bin in binCounts) {
		data.push({"i": it,"x": bin, "y": binCounts[bin]});
		it++;
	}
	
	// add the histogram
	initial = createHistogram(tag,data, maxBin+binInc, binInc, group);
	transitionTo(json,initial,1);
	// console.log(initial.height)
}

var transitionTo = function(json,initial,i){
	speed = 500
	var minBin = json[i].data[0].bin;
	var maxBin = json[i].data[json[i].data.length-1].bin;
	var binInc = json[i].data[1].bin-json[i].data[0].bin;
	initial.x.domain([0, maxBin + binInc]);
			// .range([0, initial.width]);

	//console.log(d3.max(json[i].data,function(d){return d.count}));
	initial.y.domain([0,d3.max(json[i].data,function(d){return d.count})]);

	initial.bar.transition().duration(speed)
			.attr("height",function(d){return 2*(json[i].data[d.i].count>0)+initial.height - initial.y(json[i].data[d.i].count)})
			.attr("y",function(d){return -2*(json[i].data[d.i].count>0)+initial.y(json[i].data[d.i].count)});
	initial.bar.on("mouseover", function(d) {
				var barWidth = parseFloat(d3.select(this).attr("width"));
				var xPosition = parseFloat(d3.select(this).attr("x")) + (barWidth / 2);
				var yPosition = parseFloat(d3.select(this).attr("y")) - 10;
				
				initial.svg.append("text")
					.attr("id", "tooltip")
					.attr("x", xPosition)
					.attr("y", yPosition)
					.attr("text-anchor", "middle")
					.text(json[i].data[d.i].count);
			})
			.on("mouseout", function(d) {
				d3.select('#tooltip').remove();
			});
	initial.title.transition().duration(speed).text(json[i].name);
	initial.svg.select(".y")
			.transition().duration(speed)
			.call(initial.yaxis.scale(initial.y).orient("left"));
	initial.svg.select(".x")
            .transition().duration(speed)
            .call(initial.xaxis.scale(initial.x).orient("bottom").tickValues(json[i].ticks))
            .each("end",function(){setTimeout(function(){transitionTo(json,initial,(i+1)%json.length)},100)});
}

var createHistogram = function(tag,data, maxBin, binInc, title) {

	// A formatter for counts.
	var formatCount = d3.format(",.0f");
	var totalWidth = d3.select(tag).node().getBoundingClientRect().width;
	var totalHeight = 400;
	var margin = {top: 40, right: 60, bottom: 50, left: 70},
			width = totalWidth - margin.left - margin.right,
			height = totalHeight - margin.top - margin.bottom;
	
	var binArray = [];
	for (var i = 0; i <= maxBin + binInc; i += binInc) {
		binArray.push(i);
	}
	var binTicks = [];
	for (var i = 0; i <= maxBin + binInc; i += binInc) {
		binTicks.push(i);
	}
	
	var x = d3.scale.linear()
			.domain([0, maxBin + binInc])
			.range([2, width]);
	var binWidth = parseFloat(width / (binArray.length - 1));
	
	var y = d3.scale.linear()
			.domain([0, d3.max(data, function(d) { return d.y; })])
			.range([height, 0]);
	
	var xAxis = d3.svg.axis()
			.scale(x)
			.orient("bottom")
			.tickValues(binTicks);
			
	var yAxis = d3.svg.axis()
			.scale(y)
			.orient("left");
	
	var svg = d3.select(tag).append("svg")
			.attr("width", width + margin.left + margin.right)
			.attr("height", height + margin.top + margin.bottom)
			.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	
	var bar = svg.selectAll(".bar")
			.data(data)
			.enter()
			.append("rect")
			.attr("class", "bar")
			.attr("x", function(d) { return x(d.x); })
			.attr("width", binWidth)
			.attr("y", function(d) { return y(d.y); })
			.attr("height", function(d) { return height - y(d.y); })
			.on("mouseover", function(d) {
				var barWidth = parseFloat(d3.select(this).attr("width"));
				var xPosition = parseFloat(d3.select(this).attr("x")) + (barWidth / 2);
				var yPosition = parseFloat(d3.select(this).attr("y")) - 10;
				
				svg.append("text")
					.attr("id", "tooltip")
					.attr("x", xPosition)
					.attr("y", yPosition)
					.attr("text-anchor", "middle")
					.text(d.y);
			})
			.on("mouseout", function(d) {
				d3.select('#tooltip').remove();
			});
	
	
	svg.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0," + height + ")")
			.call(xAxis);
			
	svg.append("g")
			.attr("class", "y axis")
			//.attr("transform", "translate(0," + height + ")")
			.call(yAxis);
			
	// Add axis labels
	svg.append("text")
			.attr("class", "x label")
			.attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom - 15) + ")")
			//.attr("dy", "1em")
			.attr("text-anchor", "middle")
			.text("Eigenvalues");
			
	svg.append("text")
			.attr("class", "y label")
			.attr("transform", "rotate(-90)")
			.attr("y", 0 - margin.left)
			.attr("x", 0 - (height / 2))
			.attr("dy", "1em")
			.attr("text-anchor", "middle")
			.text("Count");
			
	// Add title to chart
	titleText = svg.append("text")
			.attr("class", "title")
			.attr("transform", "translate(" + (width / 2) + " ," + (-20) + ")")
			//.attr("dy", "1em")
			.attr("text-anchor", "middle")
			.text(title);  
	return {x:x, xaxis :xAxis,y:y,yaxis:yAxis,bar:bar,title:titleText,height:height,width:width,svg:svg}
};


