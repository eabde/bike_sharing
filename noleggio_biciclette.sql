-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Mag 23, 2024 alle 23:18
-- Versione del server: 10.4.28-MariaDB
-- Versione PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `noleggio_biciclette`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `admin`
--

CREATE TABLE `admin` (
  `ID` int(11) NOT NULL,
  `email` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dump dei dati per la tabella `admin`
--

INSERT INTO `admin` (`ID`, `email`, `password`) VALUES
(5, 'admin@gmail.com', '21232f297a57a5a743894a0e4a801fc3');

-- --------------------------------------------------------

--
-- Struttura della tabella `biciclette`
--

CREATE TABLE `biciclette` (
  `ID` int(11) NOT NULL,
  `codiceTag` varchar(32) NOT NULL,
  `latitudine` varchar(32) DEFAULT '0',
  `longitudine` varchar(32) DEFAULT '0',
  `distanzaPercorsa` float DEFAULT 0,
  `gps` varchar(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `biciclette`
--

INSERT INTO `biciclette` (`ID`, `codiceTag`, `latitudine`, `longitudine`, `distanzaPercorsa`, `gps`) VALUES
(5, 'bCeFgF', '45.46608189999999', '9.183102399999992', 2.77204, 'u4Mci7'),
(6, 'uepfRz', '45.4481546', '9.1958296', 0, '8SbrRt'),
(8, 'mWjweO', '45.480416999999996', '9.1714975', 9.5223, '3LDhvM'),
(9, '4Uxaxc', '45.4781834', '9.2108714', 1.28127, 'Qqs2Ld'),
(10, 'kMJp6M', '45.4481546', '9.1958296', 0, '1CJGy9'),
(11, 'jexa0D', '45.4481546', '9.1958296', 0, 'pgSts1'),
(13, 'oUCJLS', '45.4481546', '9.1958296', 0, 'jQCz2I'),
(14, 'mXZDG6', '0', '0', 0, 'gCDDK4'),
(15, 'uFu8dA', '0', '0', 0, 'NN8kH0'),
(16, 'tkhtWZ', '0', '0', 0, 'Y8FIXX');

-- --------------------------------------------------------

--
-- Struttura della tabella `operazioni`
--

CREATE TABLE `operazioni` (
  `ID` int(11) NOT NULL,
  `tipo` enum('noleggio','riconsegna') NOT NULL,
  `data` date NOT NULL DEFAULT current_timestamp(),
  `ora` time NOT NULL DEFAULT current_timestamp(),
  `distanzaPercorsa` int(11) NOT NULL,
  `idUtente` int(11) NOT NULL,
  `idBicicletta` int(11) NOT NULL,
  `idStazione` int(11) NOT NULL,
  `tariffa` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `operazioni`
--

INSERT INTO `operazioni` (`ID`, `tipo`, `data`, `ora`, `distanzaPercorsa`, `idUtente`, `idBicicletta`, `idStazione`, `tariffa`) VALUES
(4, 'noleggio', '2024-05-23', '15:19:23', 0, 17, 5, 11, NULL),
(5, 'noleggio', '2024-05-23', '16:22:29', 0, 16, 6, 12, NULL),
(6, 'noleggio', '2024-05-23', '16:53:32', 0, 16, 6, 12, NULL),
(7, 'noleggio', '2024-05-23', '19:10:43', 0, 16, 6, 13, NULL),
(8, 'noleggio', '2024-05-23', '19:11:41', 0, 16, 6, 13, NULL),
(9, 'noleggio', '2024-05-23', '19:21:02', 0, 16, 6, 13, NULL),
(10, 'noleggio', '2024-05-23', '19:21:58', 0, 16, 6, 13, NULL),
(11, 'noleggio', '2024-05-23', '19:23:30', 0, 16, 6, 13, NULL),
(12, 'noleggio', '2024-05-23', '19:24:42', 0, 16, 8, 13, NULL),
(13, 'noleggio', '2024-05-23', '19:30:10', 0, 16, 8, 13, NULL),
(14, 'noleggio', '2024-05-23', '19:32:33', 0, 16, 8, 13, NULL),
(15, 'noleggio', '2024-05-23', '19:35:06', 0, 16, 8, 13, NULL),
(16, 'noleggio', '2024-05-23', '19:37:31', 0, 16, 8, 13, NULL),
(17, 'noleggio', '2024-05-23', '19:57:24', 0, 16, 9, 18, NULL),
(18, 'riconsegna', '2024-05-23', '19:58:43', 0, 16, 9, 18, NULL),
(19, 'riconsegna', '2024-05-23', '20:28:29', 0, 17, 6, 14, NULL),
(20, 'noleggio', '2024-05-23', '20:37:46', 0, 17, 10, 14, NULL),
(21, 'riconsegna', '2024-05-23', '20:39:13', 0, 17, 10, 14, NULL),
(22, 'noleggio', '2024-05-23', '20:42:15', 0, 17, 11, 14, NULL),
(23, 'riconsegna', '2024-05-23', '20:43:11', 0, 17, 11, 14, NULL),
(24, 'noleggio', '2024-05-23', '20:48:56', 0, 17, 13, 14, NULL),
(25, 'noleggio', '2024-05-23', '20:50:14', 0, 17, 13, 14, NULL),
(26, 'noleggio', '2024-05-23', '20:52:26', 0, 17, 13, 14, NULL),
(27, 'noleggio', '2024-05-23', '20:55:20', 0, 17, 13, 14, NULL),
(28, 'riconsegna', '2024-05-23', '20:56:43', 0, 17, 11, 14, NULL),
(29, 'riconsegna', '2024-05-23', '20:57:05', 0, 17, 13, 14, NULL),
(30, 'noleggio', '2024-05-23', '21:03:30', 0, 17, 8, 14, NULL),
(31, 'riconsegna', '2024-05-23', '21:05:15', 0, 17, 8, 14, NULL),
(32, 'riconsegna', '2024-05-23', '21:05:28', 0, 17, 8, 14, NULL),
(33, 'noleggio', '2024-05-23', '21:27:53', 0, 17, 8, 13, NULL),
(34, 'noleggio', '2024-05-23', '21:29:22', 0, 17, 8, 13, NULL),
(35, 'noleggio', '2024-05-23', '21:29:37', 0, 17, 8, 13, NULL),
(36, 'riconsegna', '2024-05-23', '21:31:56', 0, 17, 13, 14, NULL),
(37, 'noleggio', '2024-05-23', '21:33:31', 0, 17, 8, 13, NULL),
(38, 'riconsegna', '2024-05-23', '21:34:44', 0, 17, 8, 14, NULL),
(39, 'riconsegna', '2024-05-23', '21:35:00', 0, 17, 8, 13, NULL);

-- --------------------------------------------------------

--
-- Struttura della tabella `stazioni`
--

CREATE TABLE `stazioni` (
  `ID` int(11) NOT NULL,
  `numSlot` int(11) NOT NULL,
  `numBiciclette` int(11) NOT NULL,
  `via` varchar(32) NOT NULL,
  `città` varchar(32) NOT NULL,
  `provincia` varchar(32) NOT NULL,
  `regione` varchar(32) NOT NULL,
  `latitudine` double NOT NULL,
  `longitudine` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `stazioni`
--

INSERT INTO `stazioni` (`ID`, `numSlot`, `numBiciclette`, `via`, `città`, `provincia`, `regione`, `latitudine`, `longitudine`) VALUES
(11, 34, 5, 'Via Marina', 'Milano', 'Milano', 'Lombardia', 45.4711419, 9.1992624),
(12, 43, 36, 'Via San Vittore', 'Milano', 'Milano', 'Lombardia', 45.4634515, 9.1700282),
(13, 54, 42, 'Via Paolo Lomazzo, 1', 'Milano', 'Milano', 'Lombardia', 45.481317, 9.1729375),
(14, 32, 18, 'Via Cesare Balbo, 16', 'Milano', 'Milano', 'Lombardia', 45.4481546, 9.1958296),
(18, 56, 44, 'Corso Buenos Aires, 33', 'Milano', 'Milano', 'Lombardia', 45.4794434, 9.2097914);

-- --------------------------------------------------------

--
-- Struttura della tabella `utenti`
--

CREATE TABLE `utenti` (
  `id` int(11) NOT NULL,
  `nome` varchar(32) NOT NULL,
  `cognome` varchar(32) NOT NULL,
  `email` varchar(32) NOT NULL,
  `numTelefono` varchar(32) NOT NULL,
  `cartaCredito` varchar(32) NOT NULL,
  `smartCard` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL,
  `via` varchar(32) NOT NULL,
  `città` varchar(32) NOT NULL,
  `provincia` varchar(32) NOT NULL,
  `regione` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `utenti`
--

INSERT INTO `utenti` (`id`, `nome`, `cognome`, `email`, `numTelefono`, `cartaCredito`, `smartCard`, `password`, `via`, `città`, `provincia`, `regione`) VALUES
(16, 'Mario', 'Mario', 'mario@gmail.com', '123456789', '4023123456789012', '1234', 'de2f15d014d40b93578d255e6221fd60', 'Via Dante Alighieri, 7', 'Cabiate', 'Como', 'Lombardia'),
(17, 'simone', 'simone', 'simone@gmail.com', '1234567890', '1234567890123456', 'smartCard', '47eb752bac1c08c75e30d9624b3e58b7', 'Via Cina', 'Pozzaglio ed Uniti', 'Arezzo', 'Puglia'),
(18, 'luca', 'rossi', 'luca.rossi@email.it', '3201234567', '4532876509871234', '001122334455', 'ff377aff39a9345a9cca803fb5c5c081', 'Via Roma', 'Roma', 'Roma', 'Lazio'),
(19, 'maria', 'bianchi', 'maria.bianchi@email.it', '3201234568', '4532876509871235', '001122334456', '263bce650e68ab4e23f28263760b9fa5', 'Via Milano', 'Milano', 'Milano', 'Lombardia'),
(20, 'giuseppe', 'verdi', 'giuseppe.verdi@email.it', '3201234569', '4532876509871236', '001122334457', '353f9bfab2d01dbb1db343fdaf9ab02e', 'Via Napoli', 'Napoli', 'Napoli', 'Campania'),
(21, 'sara', 'gialli', 'sara.gialli@email.it', '3201234570', '4532876509871237', '001122334458', '5bd537fc3789b5482e4936968f0fde95', 'Via Torino', 'Torino', 'Torino', 'Piemonte'),
(22, 'marco', 'neri', 'marco.neri@email.it', '3201234571', '4532876509871238', '001122334459', 'f5888d0bb58d611107e11f7cbc41c97a', 'Via Palermo', 'Palermo', 'Palermo', 'Sicilia');

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`ID`);

--
-- Indici per le tabelle `biciclette`
--
ALTER TABLE `biciclette`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `codiceTag` (`codiceTag`);

--
-- Indici per le tabelle `operazioni`
--
ALTER TABLE `operazioni`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `idUtente` (`idUtente`),
  ADD KEY `idBicicletta` (`idBicicletta`),
  ADD KEY `idStazione` (`idStazione`);

--
-- Indici per le tabelle `stazioni`
--
ALTER TABLE `stazioni`
  ADD PRIMARY KEY (`ID`);

--
-- Indici per le tabelle `utenti`
--
ALTER TABLE `utenti`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `admin`
--
ALTER TABLE `admin`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT per la tabella `biciclette`
--
ALTER TABLE `biciclette`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT per la tabella `operazioni`
--
ALTER TABLE `operazioni`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT per la tabella `stazioni`
--
ALTER TABLE `stazioni`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT per la tabella `utenti`
--
ALTER TABLE `utenti`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `operazioni`
--
ALTER TABLE `operazioni`
  ADD CONSTRAINT `operazioni_ibfk_1` FOREIGN KEY (`idBicicletta`) REFERENCES `biciclette` (`ID`),
  ADD CONSTRAINT `operazioni_ibfk_3` FOREIGN KEY (`idUtente`) REFERENCES `utenti` (`id`),
  ADD CONSTRAINT `operazioni_ibfk_4` FOREIGN KEY (`idStazione`) REFERENCES `stazioni` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
