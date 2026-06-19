<?php
// Auteur: Dion Breur
// Functie: Functies declareren

// Initialisatie
include_once 'config.php';

// Main
// Verbinden met database
function connectDb(){
    try{
        // Verbinding maken met de database
        $conn = new PDO("mysql:host=" . SERVERNAME. ";dbname=" . DATABASE, USER, PASSWORD);

        // Errormode naar acceptatie
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Database verbinding teruggeven
        return $conn;
    } catch(PDOException $e) {
        // Foutmelding
        echo "Connection failed: " . $e->getMessage();
    }
}

// Ophalen van data
function getData($table, $selection = "*", $conditions = [], $orderBy = null) {
    // Verbinding maken met database
    $conn = connectDb();

    // SQL-Query opstellen
    $sql = "SELECT $selection FROM `$table` ";

    // Parameters
    $params = [];

    // Where conditie toevoegen
    if(!empty($conditions)){
        $sql .= " WHERE ";
        $whereParts = [];
        foreach($conditions as $column => $value){
            $whereParts[] = "`$column` = ?";
            $params[] = $value;
        }
        $sql .= implode(" AND ", $whereParts);
    }

    // Order by toevoegen aan SQL-Query
    if($orderBy){
        $sql .= " ORDER BY " . $orderBy;
    }

    // SQL-Query verzenden naar database server
    $stmt = $conn->prepare($sql);

    // SQL-Query uitvoeren
    $stmt->execute($params);

    $data = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Resultaten teruggeven
    return $data;
}
?>