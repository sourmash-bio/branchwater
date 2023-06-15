function createdashboard(jsonData, paragraphElement, navElement) {
  //   const endTime = performance.now();
  //   const duration = endTime - startTime;
  //   console.log(`Fetch request took ${duration} milliseconds.`);
  paragraphElement.textContent = `Your query returned ${
    Object.keys(jsonData).length
  } accession IDs.`;

  const textElement = document.createElement("p");
  textElement.contentEditable = true; // Make the text editable
  textElement.textContent = `You can filter data for a .csv download or to alter the plots below plotting using the table. Your filtered dataset currently includes ###IDs`;
  navElement.appendChild(textElement);

  ///////INSERT TO INDEX HTML HERE
  var plot_color = "rgba(100, 200, 102, 1)";

  // Add an event listener to the <p> element to handle text changes
  paragraphElement.addEventListener("input", (event) => {
    console.log(`New text: ${event.target.textContent}`);
  });
  // Add the <nav> element to the DOM
  dashboard.appendChild(navElement);

  // Download button////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////

  // add a break and then a button to trigger the CSV download
  // Create a new <br> element
  const lineBreak = document.createElement("br");
  // Append the <br> element to the document's <body> element
  dashboard.appendChild(lineBreak);

  var downloadButton = document.createElement("button");
  downloadButton.innerHTML = "Download CSV";
  downloadButton.className = "btn btn-success";
  downloadButton.addEventListener("click", function () {
    table.download("csv", "SRAmetadata.csv");
  });
  downloadButton.style.width = "200px";
  downloadButton.style.height = "50px";

  dashboard.appendChild(downloadButton);

  // Divs for elements////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////

  // TableDiv setup
  const tableDiv = document.createElement("div");

  // Set the <div>'s attributes and styles
  tableDiv.id = "my-table";
  tableDiv.style.margin = "30px";
  // Append the <div> to the document's <body> element
  dashboard.appendChild(tableDiv);

  // create div for the maps and add them to the dashboard
  const mapDiv = document.createElement("div");
  mapDiv.setAttribute("id", "mapDiv");
  dashboard.appendChild(mapDiv);

  // create div for the maps and add them to the container
  const mapDiv2 = document.createElement("div");
  mapDiv.setAttribute("id", "mapDiv2");
  dashboard.appendChild(mapDiv2);

  // create div for the containment and add them to the container
  const contDiv = document.createElement("div");
  contDiv.setAttribute("id", "contDiv");
  dashboard.appendChild(contDiv);

  // create div for the count barplots and add them to the container
  const barDiv = document.createElement("div");
  barDiv.setAttribute("id", "barDiv");
  dashboard.appendChild(barDiv);

  // Functions  ////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////

  //Table filters
  var minMaxFilterEditor = function (
    cell,
    onRendered,
    success,
    cancel,
    editorParams
  ) {
    var end;
    var container = document.createElement("span");
    //create and style start input for table filters
    var start = document.createElement("input");
    start.setAttribute("type", "number");
    start.setAttribute("placeholder", "Min");
    start.setAttribute("min", 0);
    start.setAttribute("max", 100);
    start.setAttribute("step", 0.01); // Set the step increment to 0.01
    start.style.padding = "4px";
    start.style.width = "50%";
    start.style.boxSizing = "border-box";
    start.value = cell.getValue();
    function buildValues() {
      success({
        start: start.value,
        end: end.value,
      });
    }
    function keypress(e) {
      if (e.keyCode == 13) {
        buildValues();
      }
      if (e.keyCode == 27) {
        cancel();
      }
    }
    end = start.cloneNode();
    end.setAttribute("placeholder", "Max");

    start.addEventListener("change", buildValues);
    start.addEventListener("blur", buildValues);
    start.addEventListener("keydown", keypress);

    end.addEventListener("change", buildValues);
    end.addEventListener("blur", buildValues);
    end.addEventListener("keydown", keypress);

    container.appendChild(start);
    container.appendChild(end);

    return container;
  };

  //custom max min filter function
  function minMaxFilterFunction(headerValue, rowValue, rowData, filterParams) {
    //headerValue - the value of the header filter element
    //rowValue - the value of the column in this row
    //rowData - the data for the row being filtered
    //filterParams - params object passed to the headerFilterFuncParams property
    if (rowValue) {
      if (headerValue.start != "") {
        if (headerValue.end != "") {
          return rowValue >= headerValue.start && rowValue <= headerValue.end;
        } else {
          return rowValue >= headerValue.start;
        }
      } else {
        if (headerValue.end != "") {
          return rowValue <= headerValue.end;
        }
      }
    }
    return true; //must return a boolean, true if it passes the filter.
  }
  ///funtion to count values for barplots
  function countUniqueValuesAndOccurrences(valueList) {
    const counts = {};
    const uniqueValues = [...new Set(valueList)];

    for (let i = 0; i < uniqueValues.length; i++) {
      const val = uniqueValues[i];
      counts[val] = valueList.filter((value) => value === val).length;
    }

    const countVal = uniqueValues.map((key) => counts[key]);

    return {
      uniqueValues,
      countVal,
    };
  }

  ///function to create plots from strings
  // write function that makes bar traces for each plot and puts them in a list

  function createPlotData(stringKeys, stringValues) {
    var plotData = [];

    for (let i = 0; i < stringKeys.length; i++) {
      const visible = i === 0 ? true : false;
      const { uniqueValues, countVal } = countUniqueValuesAndOccurrences(
        stringValues[i]
      );
      plotData.push({
        x: uniqueValues,
        y: countVal,
        type: "bar",
        width: 0.2,
        marker: {
          color: "rgba(100, 200, 102, 0.7)",
          line: {
            color: plot_color,
            width: 1,
          },
        },
        name: stringKeys[i],
        visible: visible,
      });
    }

    return plotData;
  }

  // Data prep for plots  ////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////
  const keys = Object.keys(jsonData[0]);

  // Create column attributes; filter based on numeric vs string
  const columns = Object.keys(jsonData[0]).map((key) => {
    const isNumericColumn = jsonData.every(
      (row) => !isNaN(parseFloat(row[key]))
    ); // check if all values in the column are numeric
    const headerFilterOptions = isNumericColumn
      ? {
          headerFilter: minMaxFilterEditor,
          headerFilterFunc: minMaxFilterFunction,
        }
      : {
          headerFilter: "input",
        };

    return {
      title: key,
      field: key,
      sorter: isNumericColumn ? "number" : "string",
      ...headerFilterOptions,
      headerFilterLiveFilter: false,
    };
  });

  //common keys and values
  const commonKeys = Object.keys(jsonData[0]);
  const values = Array.from({ length: commonKeys.length }, () => []);
  commonKeys.forEach((key, j) => {
    values[j] = jsonData.map((obj) => obj[key]);
  });

  // Create Table  ////////////////////////////////////////////////
  /////////////////////////////////////////////////////////////////
  // Define the data for the table
  const data = jsonData;

  // Set up the table options
  const options = {
    pagination: "local",
    paginationSize: 10,
    paginationSizeSelector: [10, 25, 50, 100],
  };

  // Create the table
  const table = new Tabulator("#my-table", {
    columns: columns,
    data: data,
    layout: "fitColumns",
    pagination: "local",
    paginationSize: 10,
    paginationSizeSelector: [10, 25, 50, 100],
  });
  // Barplot setup////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////
  ///add in containment histogram
  // Histogram setup////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////

  ///add in containment histogram
  var cont_hist = {
    x: values[commonKeys.indexOf("containment")],
    type: "histogram",
    autobinx: false,
    xbins: { size: 0.1 },
    name: "containment", // Add a name to identify this trace
    visible: true, // Set the visibility of this trace to true initially
    marker: {
      color: "rgba(100, 200, 102, 0.7)",
      line: {
        color: plot_color,
        width: 1,
      },
    },
  };

  var ANI_hist = {
    x: values[commonKeys.indexOf("cANI_est")],
    type: "histogram",
    autobinx: false,
    xbins: { size: 0.02 },
    name: "cANI_est", // Add a name to identify this trace
    visible: false, // Set the visibility of this trace to false initially
    marker: {
      color: "rgba(100, 200, 102, 0.7)",
      line: {
        color: plot_color,
        width: 1,
      },
    },
  };

  var dropdown = {
    x: 0.05,
    y: 1.2,
    xanchor: "left",
    yanchor: "top",
    buttons: [
      {
        method: "update",
        args: [{ visible: [true, false] }],
        label: "containment",
      },
      {
        method: "update",
        args: [{ visible: [false, true] }],
        label: "cANI_est",
      },
    ],
    direction: "down",
    showactive: true,
  };

  var layout = {
    bargap: 0.05,
    bargroupgap: 0.2,
    title: "Match similarity scores",
    xaxis: { title: "Score" },
    yaxis: { title: "Frequency" },
    updatemenus: [dropdown],
  };

  Plotly.newPlot("contDiv", [cont_hist, ANI_hist], layout, {
    scrollZoom: true,
    displaylogo: false,
    responsive: true,
  });

  ////INITIAL BARPLOT

  let stringKeys = [];
  let stringValues = [];

  for (let i = 0; i < values.length; i++) {
    if (
      values[i].every(
        (val) =>
          typeof val === "string" &&
          commonKeys[i] !== "acc" &&
          commonKeys[i] !== "biosample_link"
      )
    ) {
      stringKeys.push(commonKeys[i]);
      stringValues.push(values[i]);
    }
  }

  //use custom function to create list of plot data for all strings
  var Plotdata = createPlotData(stringKeys, stringValues);

  // Create dropdown buttons for each trace
  var dropdownButtons = stringKeys.map((key, i) => {
    // For the first trace, set args to show only the first trace, otherwise set to show only the current trace
    var args = [{ visible: stringKeys.map((_, idx) => idx === i) }];
    return {
      method: "update",
      args: args,
      label: key,
    };
  });
  // Create dropdown menu layout
  var stringDD = {
    x: 0.05,
    y: 1.2,
    xanchor: "left",
    yanchor: "top",
    buttons: dropdownButtons,
    direction: "down",
    showactive: true,
  };

  var barlayout = {
    bargap: 0.05,
    bargroupgap: 0.2,
    title: "Summary counts of categorical metadata",
    xaxis: { automargin: true, title: "Score" },
    yaxis: {
      automargin: true,
      title: { text: "Counts" },
    },
    updatemenus: [stringDD],
    //height: 500,
    //margin: { t: 50, l: 100, r: 100, b: 200, pad: 4 }
  };

  //add the plots to the
  Plotly.newPlot(barDiv, Plotdata, barlayout, {
    scrollZoom: true,
    displaylogo: false,
    responsive: true,
  });

  ///////////MAPS

  let country_map = {};
  let ll_map = {};

  for (let i = 0; i < values.length; i++) {
    if (commonKeys[i] === "geo_loc_name_country_calc") {
      const countryCounts = countUniqueValuesAndOccurrences(
        values[commonKeys.indexOf("geo_loc_name_country_calc")]
      );
      const countryData = countryCounts.uniqueValues.map(function (
        country,
        index
      ) {
        return {
          country: country,
          count: countryCounts.countVal[index],
        };
      });
      country_map = {
        name: "geo_loc_name_country_calc",
        type: "choropleth",
        locationmode: "country names",
        locations: countryData.map(function (d) {
          return d.country;
        }),
        z: countryData.map(function (d) {
          return d.count;
        }),
        text: countryData.map(function (d) {
          return d.country + ": " + d.count;
        }),
        autocolorscale: true,
        marker: {
          line: {
            color: "rgb(255,255,255)",
            width: 2,
          },
        },
      };
    } else if (commonKeys[i] === "lat_lon") {
      // fix syntax
      var arr = values[commonKeys.indexOf("lat_lon")];

      //filter to just lat/long format
      //doesn't include 'acc' ID in tooltips because should auto-update
      let filteredArr = arr.filter(function (item) {
        return (
          Array.isArray(item) &&
          item.length === 2 &&
          typeof item[0] === "number" &&
          typeof item[1] === "number"
        );
      });
      ll_map = {
        name: "lat_lon",
        type: "scattergeo",
        mode: "markers",
        marker: {
          color: plot_color,
        },
        lon: filteredArr.map(function (item) {
          return item[1];
        }),
        lat: filteredArr.map(function (item) {
          return item[0];
        }),
      };
    }
  }

  let map_dd = {};
  map_dd = {
    x: 0.05,
    y: 1.2,
    xanchor: "left",
    yanchor: "top",
    buttons: [
      {
        method: "update",
        args: [{ visible: [true, false] }],
        label: "geo_loc_name_country_calc",
      },
      {
        method: "update",
        args: [{ visible: [false, true] }],
        label: "lat_lon",
      },
    ],
    direction: "down",
    showactive: true,
  };
  var ll_layout = {
    title: "Accession locations",
    colorbar: true,
    // updatemenus: [map_dd],
    geo: {
      scope: "world",
      showcountries: true,
      countrycolor: "rgb(255, 255, 255)",
      countrywidth: 1,
      showframe: false,
      projection: {
        type: "robinson",
      },
      width: 800,
      height: 600,
      showland: true,
      landcolor: "rgb(250,250,250)",
      subunitcolor: "rgb(217,217,217)",
      countrycolor: "rgb(217,217,217)",
    },
  };

  if (Object.keys(country_map).length > 0 && Object.keys(ll_map).length > 0) {
    Plotly.newPlot(mapDiv, [country_map, ll_map], ll_layout, {
      scrollZoom: true,
      displaylogo: false,
      responsive: true,
    });
  } else if (Object.keys(country_map).length > 0) {
    Plotly.newPlot(mapDiv, [country_map], ll_layout, {
      scrollZoom: true,
      displaylogo: false,
      responsive: true,
    });
  } else if (Object.keys(ll_map).length > 0) {
    Plotly.newPlot(mapDiv, [ll_map], ll_layout, {
      scrollZoom: true,
      displaylogo: false,
      responsive: true,
    });
  }

  // FILTER LISTENER ////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////
  table.on("dataFiltered", function (filters, rows) {
    //update keys
    var filteredData = rows.map(function (row) {
      return row.getData();
    });
    // add row count to HTML document
    textElement.textContent = `The returned metadata can be pre-filtered prior to .CSV download and plotting with the table below. Your filtered table contains ${rows.length} accession IDs`;

    //Get needed data from filtered table
    const FiltcommonKeys = Object.keys(filteredData[0]);
    const Filtvalues = Array.from({ length: FiltcommonKeys.length }, () => []);
    FiltcommonKeys.forEach((key, j) => {
      Filtvalues[j] = filteredData.map((obj) => obj[key]);
    });

    // update histogram plot with new index values
    Plotly.update("contDiv", {
      x: [
        Filtvalues[FiltcommonKeys.indexOf("containment")],
        Filtvalues[FiltcommonKeys.indexOf("cANI_est")],
      ],
    });

    // update bar plot with new index values
    ///////////

    //loop to map filtered values to stringKeys
    let FiltstringValues = stringKeys.map((key) => {
      const index = FiltcommonKeys.indexOf(key);
      return index !== -1 ? Filtvalues[index] : [];
    });

    //update each plot with a loop
    for (let i = 0; i < stringKeys.length; i++) {
      const { uniqueValues, countVal } = countUniqueValuesAndOccurrences(
        FiltstringValues[i]
      );
      // Update the x and y values for the i-th trace in the barDiv plot
      Plotly.update("barDiv", { x: [uniqueValues], y: [countVal] }, {}, i);
    }

    ///update maps
    let Filt_country_map = {};
    let Filt_ll_map = {};

    for (let i = 0; i < Filtvalues.length; i++) {
      if (FiltcommonKeys[i] === "geo_loc_name_country_calc") {
        const countryCounts = countUniqueValuesAndOccurrences(
          Filtvalues[commonKeys.indexOf("geo_loc_name_country_calc")]
        );
        const countryData = countryCounts.uniqueValues.map(function (
          country,
          index
        ) {
          return {
            country: country,
            count: countryCounts.countVal[index],
          };
        });
        Filt_country_map = {
          name: "geo_loc_name_country_calc",
          type: "choropleth",
          locationmode: "country names",
          locations: countryData.map(function (d) {
            return d.country;
          }),
          z: countryData.map(function (d) {
            return d.count;
          }),
          text: countryData.map(function (d) {
            return d.country + ": " + d.count;
          }),
          autocolorscale: true,
          marker: {
            line: {
              color: "rgb(255,255,255)",
              width: 2,
            },
          },
        };
      } else if (FiltcommonKeys[i] === "lat_lon") {
        // fix syntax
        var latLonArr = Filtvalues[FiltcommonKeys.indexOf("lat_lon")];
        var accArr = Filtvalues[FiltcommonKeys.indexOf("acc")];

        //filter to just lat/long format
        let filteredArr = latLonArr
          .map(function (item, index) {
            return [item, accArr[index]];
          })
          .filter(function (item) {
            return (
              Array.isArray(item[0]) &&
              item[0].length === 2 &&
              typeof item[0][0] === "number" &&
              typeof item[0][1] === "number"
            );
          });
        Filt_ll_map = {
          name: "lat_lon",
          type: "scattergeo",
          mode: "markers",
          marker: {
            color: plot_color,
          },
          lon: filteredArr.map(function (item) {
            return item[0][1];
          }),
          lat: filteredArr.map(function (item) {
            return item[0][0];
          }),
          text: filteredArr.map(function (item) {
            // Return a custom tooltip string for each marker
            return `acc: ${item[1]}`;
          }),
        };
      }
    }

    if (
      Object.keys(Filt_country_map).length > 0 &&
      Object.keys(Filt_ll_map).length > 0
    ) {
      Plotly.newPlot(mapDiv, [Filt_country_map, Filt_ll_map], ll_layout);
    } else if (Object.keys(Filt_country_map).length > 0) {
      Plotly.newPlot(mapDiv, [Filt_country_map]);
    } else if (Object.keys(Filt_ll_map).length > 0) {
      Plotly.newPlot(mapDiv, [Filt_ll_map]);
    }
  });
}
