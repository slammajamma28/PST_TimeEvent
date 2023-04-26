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

function showUser(evt, userName) {
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
    console.log(columns[0].innerText);
    if (columns[0].innerText == "MISSING") {
      activeRows[i].style.background = "red";
    }
  }
    
  btn = document.getElementsByClassName("dropbtn");
  for (i = 0; i < btn.length; i++) {
    btn[i].innerHTML = userName;
  }
}