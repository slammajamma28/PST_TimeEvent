/******************************************
/
/ jQuery run on page load
/
******************************************/

$(document).ready(function () {
  const currentVal = document.getElementById("goalPercentage").innerText;
  $(".percentageFill").css(
      {"color": "white",
      "border": "1px solid black",
      "background": `-webkit-linear-gradient(left, blue ${currentVal}, black ${currentVal})`,
      "background":    `-moz-linear-gradient(left, blue ${currentVal}, black ${currentVal})`,
      "background":     `-ms-linear-gradient(left, blue ${currentVal}, black ${currentVal})`,
      "background":      `-o-linear-gradient(left, blue ${currentVal}, black ${currentVal})`,
      "background":     `linear-gradient(to right, blue ${currentVal}, black ${currentVal})`});

  $(".complete").each(function() {
    var txt = $(this).text() + " ✅"
    $(this).text(txt)});
  
  $(".individualPercentage").each(function() {
    var indiVal = $(this).attr("value")+'%';
    $(this).css(
      {"color": "white",
      "border": "1px solid black",
      "background": `-webkit-linear-gradient(left, blue ${indiVal}, black ${indiVal})`,
      "background":    `-moz-linear-gradient(left, blue ${indiVal}, black ${indiVal})`,
      "background":     `-ms-linear-gradient(left, blue ${indiVal}, black ${indiVal})`,
      "background":      `-o-linear-gradient(left, blue ${indiVal}, black ${indiVal})`,
      "background":     `linear-gradient(to right, blue ${indiVal}, black ${indiVal})`});
  });

  var hour_now = new Date().getUTCHours();
  document.getElementById('hour_'+hour_now).style.display = "block";
  $('#cell_'+hour_now).addClass('active');
});

/******************************************
/
/ Show content for different tabs
/
******************************************/

function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
  } 

/******************************************
/
/ Swap between individual goal tables
/
******************************************/

function showUser(evt, userName, completedGoal, percentageGoal) {
  // Declare all variables
  var i, user_table, columns, activeTable, activeRows, btn;
  
  // Get all elements with class="user_table" and hide them
  user_table = document.getElementsByClassName("user_table");
  for (i = 0; i < user_table.length; i++) {
    user_table[i].style.display = "none";
  }

  // Show the selected table
  activeTable = document.getElementById(userName);
  activeTable.style.display = "block";
  thisTable = activeTable.getElementsByTagName('tbody')
  activeRows = thisTable[0].getElementsByTagName('tr')
  for (i = 0; i < activeRows.length; i++){
    columns = activeRows[i].getElementsByTagName('td');
    if (columns[0].innerText == "MISSING") {
      activeRows[i].style.background = "red";
    }
  }

  document.getElementById("dropbtn_individual").innerHTML = userName + ' - ' + completedGoal;

  $("#dropbtn_individual").css(
    {"color": "white",
      "border": "1px solid black",
      "background": `-webkit-linear-gradient(left, blue ${percentageGoal}%, black ${percentageGoal}%)`,
      "background":    `-moz-linear-gradient(left, blue ${percentageGoal}%, black ${percentageGoal}%)`,
      "background":     `-ms-linear-gradient(left, blue ${percentageGoal}%, black ${percentageGoal}%)`,
      "background":      `-o-linear-gradient(left, blue ${percentageGoal}%, black ${percentageGoal}%)`,
      "background":     `linear-gradient(to right, blue ${percentageGoal}%, black ${percentageGoal}%)`});
}

/******************************************
/
/ Table switching to show different stats
/
******************************************/

function showStat(evt, stat) {
  // Declare all variables
  var i, stats_table, activeTable;
  
  // Get all elements with class="user_table" and hide them
  stats_table = document.getElementsByClassName("stats_table");
  for (i = 0; i < stats_table.length; i++) {
    stats_table[i].style.display = "none";
  }

  document.getElementById("dropbtn_stat").innerHTML = stat;

  // Show the selected table
  activeTable = document.getElementById(stat+'_stats');
  activeTable.style.display = "block";
}

/******************************************
/
/ Swap update time between UTC and local
/
******************************************/

function swapTime(evt) {
  var time, index, zone, timestr, ampm;

  time = document.getElementsByTagName("h4")[0].innerHTML;
  index = time.search("/");
  timestr = time.substring(index-4, time.length);
  zone = document.getElementsByTagName("h3");
  if (zone[0].getAttribute("value") == "utc") {
    zone[0].setAttribute("value", "local");
    date_year = new Date(timestr).getFullYear();
    date_month = new Date(timestr).getMonth() + 1;
    date_day = new Date(timestr).getDate();
    date_hour = new Date(timestr).getHours();
    if (date_hour > 12 ) {
      ampm = "PM";
      date_hour = date_hour - 12;
    } else if (date_hour == 12) { 
      ampm = "PM";
    } else if (date_hour == 0) {
      ampm = "AM";
      date_hour = 12;
    }
     else {
      ampm = "AM";
    }
    date_minute = new Date(timestr).getMinutes();
    date_second = new Date(timestr).getSeconds();
    
    date = date_year + "/" + String(date_month).padStart(2, "0") + "/" + String(date_day).padStart(2, "0") + " " + String(date_hour).padStart(2, "0") + ":" + String(date_minute).padStart(2, "0") + ":" + String(date_second).padStart(2, "0") + " " + ampm + " " + new Date(timestr).toLocaleTimeString('en-us',{timeZoneName:'short'}).split(' ')[2];
    document.getElementsByTagName("h3")[0].innerHTML = "as of " + date;
  } else {
    zone[0].setAttribute("value", "utc");
    document.getElementsByTagName("h3")[0].innerHTML = time;
  }
}

/******************************************
/
/ Update overall hourly summary table
/
******************************************/

function showHourSummary(evt, hourNum) {
  var tableLinks;

  tables = document.getElementsByClassName("hour_summary");
  tableLinks = document.getElementsByClassName("sum_cell");
  for (i = 0; i < tableLinks.length; i++) {
    tableLinks[i].className = tableLinks[i].className.replace(" active", "");
  }

  for (i = 0; i < tables.length; i++) {
    tables[i].style.display = "none";
  }
  document.getElementById(hourNum).style.display = "block";
  evt.currentTarget.className += " active";
}