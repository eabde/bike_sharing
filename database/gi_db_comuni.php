<?php
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "gi_db_comuni";

    // Creazione della connessione
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Verifica della connessione
    if ($conn->connect_error) {
        die("Connessione al database fallita: " . $conn->connect_error);
    }

    // Impostazione del charset per la corretta gestione dei caratteri speciali
    $conn->set_charset("utf8");
?>
