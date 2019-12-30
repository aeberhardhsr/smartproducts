<!DOCTYPE html>
<html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/3/w3.css">
<head>
    <title>Smart Products</title>
    <link rel='icon' href='favico.ico' type='image/x-icon'/ >


<style>
th, td {
    padding: 8px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

table {
    border-collapse: collapse;
    width: 80%;
    margin: 0 auto;
}

tr:nth-child(even){background-color: #f2f2f2}

th {
    background-color: #4a69bb;
    color: white;
}

h2 {
  color: black;
  font-family: verdana;
  font-size: 250%;
  text-align: center;
  
}
p  {
  color: black;
  font-family: Verdana;
  font-size: 160%;
  text-align: center;
  font-style: normal;
}
  #demoFont {
font-family: Impact, Charcoal, sans-serif;
font-size: 25px;
letter-spacing: 1px;
word-spacing: 0.8px;
color: #000000;
font-weight: 400;
text-decoration: overline solid rgb(68, 68, 68);
font-style: normal;
font-variant: small-caps;
text-transform: capitalize;
text-align: center;
}

img {
  width: 25%; 
  height: auto;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

input[type=submit] {
background-color: #f44336; /* Red */
border: 2px solid #f44336;
color: white;
padding: 15px 20px;
text-align: center;
text-decoration: none;
border-radius: 4px;
display: block;
font-size: 16px;
margin-top: 20px;
margin-left: auto;
margin-right: auto;
cursor: pointer;
transition-duration: 0.4s;
}

input[type=submit]:hover {
background-color: white; /* Red */
color: red;
}

</style>
</head>
<body>

<h2>HSR Rapperswil</h2>
    <p><i>Smart Products</i></p>


<span style="display:inline-block; width: 10px;"></span>

<?php
$servername = "localhost";
$username = "spuser";
$password = "spuser";
$dbname = "smartproducts";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT records.p_id, products.p_name, products.p_weight, products.p_price FROM (records INNER JOIN products ON records.p_id = products.p_id)";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    echo "<table><tr><th>Product ID</th><th>Product Name</th><th>Weight</th><th>Price</th></tr>";
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<tr><td>" . $row["p_id"]. "</td><td>" . $row["p_name"]. "</td><td>" . $row["p_weight"]. "</td><td>" . $row["p_price"]. "</td></tr>";
    }
    echo "</table>";
} else {
    //echo "0 results";
}

$conn->close();


$dbc = mysqli_connect($servername, $username, $password, $dbname) or die('Error connecting to MySQL server.'); 
if(isset($_POST['submit_button']))
{
    mysqli_query($dbc, 'TRUNCATE TABLE `records`');
    header("Location: " . $_SERVER['PHP_SELF']);
    exit();
}

?>

<form method="post" action="">
    <input name="submit_button" type="submit" value=" Clear Shopping Cart " />
</form>

<span style="display:inline-block; height: 20px;"></span>

      <img src="cart.png" alt="Einkaufswagen">

<span style="display:inline-block; height: 20px;"></span>

<div id="demoFont">B&amp;E Development</div>

</body>
</html>