-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 15-10-2025 a las 23:08:58
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gamematch`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `agent_state`
--

CREATE TABLE `agent_state` (
  `user_id` int(11) NOT NULL,
  `epsilon` float DEFAULT 0.2,
  `decay` float DEFAULT 0.995,
  `min_epsilon` float DEFAULT 0.05,
  `pulls` int(11) DEFAULT 0,
  `rewards` int(11) DEFAULT 0,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `agent_state`
--

INSERT INTO `agent_state` (`user_id`, `epsilon`, `decay`, `min_epsilon`, `pulls`, `rewards`, `updated_at`) VALUES
(1, 0.05, 0.995, 0.05, 659, 13, '2025-09-11 07:06:00'),
(2, 0.187382, 0.995, 0.05, 13, 0, '2025-09-11 06:48:00'),
(3, 0.150295, 0.995, 0.05, 57, 0, '2025-09-11 06:52:56');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `interacciones`
--

CREATE TABLE `interacciones` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `juego_id` int(11) NOT NULL,
  `rating` int(11) DEFAULT NULL,
  `liked` tinyint(1) DEFAULT NULL,
  `clicked` tinyint(1) DEFAULT NULL,
  `ts` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `interacciones`
--

INSERT INTO `interacciones` (`id`, `usuario_id`, `juego_id`, `rating`, `liked`, `clicked`, `ts`) VALUES
(1, 1, 2, 5, 1, 1, '2025-09-10 23:16:29'),
(2, 1, 2, 5, 1, 1, '2025-09-10 23:16:31'),
(3, 1, 2, 5, 1, 1, '2025-09-10 23:54:03'),
(4, 1, 3, 5, 1, 1, '2025-09-11 02:44:15'),
(5, 1, 1, 5, 1, 1, '2025-09-11 02:51:28'),
(6, 1, 2, 5, 1, 1, '2025-09-11 02:51:30'),
(7, 1, 6, 5, 1, 1, '2025-09-11 02:51:40'),
(8, 1, 5, 5, 1, 1, '2025-09-11 02:51:42'),
(9, 1, 10, 5, 1, 1, '2025-09-11 02:51:44'),
(10, 1, 1, 4, 1, 1, '2025-09-11 02:52:50'),
(11, 1, 4, 5, 1, 1, '2025-09-11 02:53:49'),
(12, 1, 1, 5, 1, 1, '2025-09-11 06:39:28'),
(13, 1, 143, 5, 1, 1, '2025-09-11 06:39:40'),
(14, 1, 155, 5, 1, 1, '2025-09-11 06:39:46'),
(15, 1, 146, 5, 1, 1, '2025-09-11 06:40:23'),
(16, 1, 143, 5, 1, 1, '2025-09-11 06:40:41'),
(17, 1, 154, 5, 1, 1, '2025-09-11 07:04:53'),
(18, 1, 120, 5, 1, 1, '2025-09-11 07:04:58'),
(19, 1, 14, 5, 1, 1, '2025-09-11 07:05:06'),
(20, 1, 13, 5, 1, 1, '2025-09-11 07:05:07'),
(21, 1, 73, 5, 1, 1, '2025-09-11 07:05:48'),
(22, 1, 259, 1, 0, 1, '2025-09-11 07:05:51');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `juegos`
--

CREATE TABLE `juegos` (
  `id` int(11) NOT NULL,
  `titulo` varchar(200) NOT NULL,
  `generos` text DEFAULT NULL,
  `tags` text DEFAULT NULL,
  `plataforma` varchar(50) DEFAULT 'PC'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `juegos`
--

INSERT INTO `juegos` (`id`, `titulo`, `generos`, `tags`, `plataforma`) VALUES
(1, 'Elden Ring', 'RPG;Soulslike', 'dificil;fantasia;singleplayer', 'PC'),
(2, 'Hades', 'Roguelike;Action', 'accion;isometrico;rapido', 'PC'),
(3, 'Hollow Knight', 'Metroidvania;Indie', 'plataformas;oscuro;singleplayer', 'PC'),
(4, 'Stardew Valley', 'Simulacion;Indie', 'granjas;relajante;pixelart', 'PC'),
(5, 'Elden Ring', 'RPG;Soulslike', 'dificil;fantasia;singleplayer', 'PC'),
(6, 'Hades', 'Roguelike;Action', 'accion;isometrico;rapido', 'PC'),
(10, 'Hades', 'Roguelike;Action', 'accion;isometrico;rapido', 'PC'),
(13, 'Elden Ring', 'RPG;Soulslike', 'dificil;fantasia;singleplayer', 'PC'),
(14, 'Hades', 'Roguelike;Action', 'accion;isometrico;rapido', 'PC'),
(15, 'Hollow Knight', 'Metroidvania;Indie', 'plataformas;oscuro;singleplayer', 'PC'),
(16, 'Stardew Valley', 'Simulacion;Indie', 'granjas;relajante;pixelart', 'PC'),
(17, 'Hades (2016)', 'Platformer', '', 'PC'),
(18, 'Hades\' Star', 'Strategy;Massively Multiplayer;Simulation', '', 'PC;iOS;Android;macOS'),
(19, 'Hades II', 'Indie;Adventure;Action;RPG', '', 'PC'),
(20, 'Hades 2 (2001)', 'Shooter', '', 'PC'),
(21, 'Hades vs. Satan', 'Platformer;Action', '', 'PC'),
(22, 'Hade', 'Casual;Strategy;Indie', '', 'PC'),
(23, 'Arc-Hades', 'Action', '', 'PC'),
(24, 'Hades Tigers Cross-Stitch Logo', 'Simulation;Sports', '', 'PC'),
(25, 'Jade\'s Journey', 'Adventure;RPG;Casual;Strategy;Indie', '', 'PC'),
(26, 'Hades Nebula', '', '', 'Commodore / Amiga;Atari ST'),
(27, 'Hades Raceway', 'Racing', '', 'PC'),
(28, 'Dark Messiah of Might & Magic Single Player', '', '', 'PC'),
(29, 'Dark Messiah of Might & Magic Multi-Player', '', '', 'PC'),
(30, 'Garry\'s Mod', '', '', 'PC'),
(31, 'Half-Life 2', '', '', 'PC'),
(32, 'Half-Life 2: Deathmatch', '', '', 'PC'),
(33, 'Half-Life Deathmatch: Source', '', '', 'PC'),
(34, 'Portal', '', '', 'PC'),
(35, 'The Witcher: Enhanced Edition', '', '', 'PC'),
(36, 'Left 4 Dead 2', '', '', 'PC'),
(37, 'Just Cause 2', '', '', 'PC'),
(38, 'Fallout: New Vegas', '', '', 'PC'),
(39, 'Dragon Age: Origins - Ultimate Edition', '', '', 'PC'),
(40, 'Two Worlds II HD', '', '', 'PC'),
(41, 'Portal 2', '', '', 'PC'),
(42, 'Terraria', '', '', 'PC'),
(43, 'The Witcher 2: Assassins of Kings Enhanced Edition', '', '', 'PC'),
(44, 'Hotline Miami', '', '', 'PC'),
(45, 'Warframe', '', '', 'PC'),
(46, 'Path of Exile', '', '', 'PC'),
(47, 'No More Room in Hell', '', '', 'PC'),
(48, 'The Forest', '', '', 'PC'),
(49, 'PAYDAY 2', '', '', 'PC'),
(50, 'Pirates of Black Cove Gold', '', '', 'PC'),
(51, 'Arma 3', '', '', 'PC'),
(52, 'Grim Dawn', '', '', 'PC'),
(53, 'Earth 2150: The Moon Project', '', '', 'PC'),
(54, 'Heli Heroes', '', '', 'PC'),
(55, 'Project Zomboid', '', '', 'PC'),
(56, 'Age of Mythology: Extended Edition', '', '', 'PC'),
(57, 'DayZ', '', '', 'PC'),
(58, 'Hotline Miami 2: Wrong Number', '', '', 'PC'),
(59, 'Aragami', '', '', 'PC'),
(60, 'Fable Anniversary', '', '', 'PC'),
(61, 'Trove', '', '', 'PC'),
(62, 'Unturned', '', '', 'PC'),
(63, 'The Expendabros', '', '', 'PC'),
(64, 'Lords Of The Fallen', '', '', 'PC'),
(65, 'Ryse: Son of Rome', '', '', 'PC'),
(66, 'Move or Die', '', '', 'PC'),
(67, 'Sleeping Dogs: Definitive Edition', '', '', 'PC'),
(68, 'Homebrew - Patent Unknown', '', '', 'PC'),
(69, 'Undefeated', '', '', 'PC'),
(70, 'Transformice', '', '', 'PC'),
(71, 'The Binding of Isaac: Rebirth', '', '', 'PC'),
(72, 'VEGA Conflict', '', '', 'PC'),
(73, 'ARK: Survival Evolved', '', '', 'PC'),
(74, 'ARK: Survival Of The Fittest', '', '', 'PC'),
(75, 'Black Mesa', '', '', 'PC'),
(76, 'Dragon\'s Dogma: Dark Arisen', '', '', 'PC'),
(77, 'Magicka 2', '', '', 'PC'),
(78, 'Magicka 2: Spell Balance Beta', '', '', 'PC'),
(79, 'Don\'t Starve Together', '', '', 'PC'),
(80, 'SMITE', '', '', 'PC'),
(81, 'SMITE - Public Test', '', '', 'PC'),
(82, 'Ultimate Chicken Horse', '', '', 'PC'),
(83, 'Brawlhalla', '', '', 'PC'),
(84, 'Undertale', '', '', 'PC'),
(85, 'We Are The Dwarves', '', '', 'PC'),
(86, 'NARUTO SHIPPUDEN: Ultimate Ninja STORM 4', '', '', 'PC'),
(87, 'Furi', '', '', 'PC'),
(88, 'Iron Snout', '', '', 'PC'),
(89, 'VRChat', '', '', 'PC'),
(90, 'No Man\'s Sky', '', '', 'PC'),
(91, 'Worms W.M.D', '', '', 'PC'),
(92, 'Dishonored 2', '', '', 'PC'),
(93, 'Hunger Dungeon', '', '', 'PC'),
(94, 'The Witcher 3: Wild Hunt', '', '', 'PC'),
(95, 'Zombie Defense', '', '', 'PC'),
(96, 'Digimon Masters Online', '', '', 'PC'),
(97, 'World of Tanks Blitz', '', '', 'PC'),
(98, 'EVE Online', '', '', 'PC'),
(99, 'Super Blue Boy Planet', '', '', 'PC'),
(100, 'Monopoly Plus', '', '', 'PC'),
(101, 'Bulletstorm: Full Clip Edition', '', '', 'PC'),
(102, 'BRAIN / OUT', '', '', 'PC'),
(103, 'Dungeons of Sundaria', '', '', 'PC'),
(104, 'Fallout Shelter', '', '', 'PC'),
(105, 'Hunt: Showdown 1896', '', '', 'PC'),
(106, 'Hunt: Showdown 1896 (Test Server)', '', '', 'PC'),
(107, 'Clone Drone in the Danger Zone', '', '', 'PC'),
(108, 'The Blackout Club', '', '', 'PC'),
(109, 'Yu-Gi-Oh! Duel Links', '', '', 'PC'),
(110, 'Barotrauma', '', '', 'PC'),
(111, 'Defence to death', '', '', 'PC'),
(112, 'Devil May Cry HD Collection', '', '', 'PC'),
(113, 'Risk of Rain 2', '', '', 'PC'),
(114, 'Drunken Wrestlers 2', '', '', 'PC'),
(115, 'BattleBit Remastered', '', '', 'PC'),
(116, 'Time Lock VR 1', '', '', 'PC'),
(117, 'SUPERHOT: MIND CONTROL DELETE', '', '', 'PC'),
(118, 'Fallout 4', '', '', 'PC'),
(119, 'SCP: Secret Laboratory', '', '', 'PC'),
(120, 'Divinity: Original Sin 2', '', '', 'PC'),
(121, 'Dark Devotion', '', '', 'PC'),
(122, 'Deceit', '', '', 'PC'),
(123, 'Phasmophobia', '', '', 'PC'),
(124, 'Middle-earth™: Shadow of Mordor™', '', '', 'PC'),
(125, 'Outer Wilds', '', '', 'PC'),
(126, 'Kingdom Defense', '', '', 'PC'),
(127, 'Kingdom: Classic', '', '', 'PC'),
(128, 'Blasphemous', '', '', 'PC'),
(129, 'JUMP FORCE', '', '', 'PC'),
(130, 'For Honor', '', '', 'PC'),
(131, 'For Honor - Public Test', '', '', 'PC'),
(132, 'Warhammer: Vermintide 2', '', '', 'PC'),
(133, 'Tell Me Everything', '', '', 'PC'),
(134, 'The Cycle: Frontier', '', '', 'PC'),
(135, 'Noita', '', '', 'PC'),
(136, 'Overcooked! 2', '', '', 'PC'),
(137, 'Middle-earth™: Shadow of War™', '', '', 'PC'),
(138, 'Counter-Strike 2', '', '', 'PC'),
(139, 'The Dungeon Of Naheulbeuk: The Amulet Of Chaos', '', '', 'PC'),
(140, 'SYNTHETIK: Arena', '', '', 'PC'),
(141, 'Metro Exodus', '', '', 'PC'),
(142, 'Metro Exodus Enhanced Edition', '', '', 'PC'),
(143, 'Hollow Knight: Silksong', 'Indie;Platformer;Adventure;Action', '', 'PC'),
(144, 'Phantasy Star Online 2 New Genesis', '', '', 'PC'),
(145, 'Embr', '', '', 'PC'),
(146, 'Albion Online', '', '', 'PC'),
(147, 'Before Your Eyes', '', '', 'PC'),
(148, 'Cyberpunk 2077', '', '', 'PC'),
(149, 'Kingdom Come: Deliverance', '', '', 'PC'),
(150, 'RISK: Global Domination', '', '', 'PC'),
(151, 'Ready or Not', '', '', 'PC'),
(152, 'Destiny 2', '', '', 'PC'),
(153, 'Apex Legends', '', '', 'PC'),
(154, 'Red Dead Redemption 2', '', '', 'PC'),
(155, 'Monster Hunter: World', '', '', 'PC'),
(156, 'Pathfinder: Wrath of the Righteous - Enhanced Edition', '', '', 'PC'),
(157, 'Enshrouded', '', '', 'PC'),
(158, 'Dragon Age™ Inquisition', '', '', 'PC'),
(159, 'ULTRAKILL', '', '', 'PC'),
(160, 'Merry Snowballs', '', '', 'PC'),
(161, 'Battlefield™ 1', '', '', 'PC'),
(162, 'Black Desert', '', '', 'PC'),
(163, 'Black Desert SA (Retired)', '', '', 'PC'),
(164, 'GOAT OF DUTY', '', '', 'PC'),
(165, 'Headsnatchers', '', '', 'PC'),
(166, 'Deiland', '', '', 'PC'),
(167, 'Drawful 2', '', '', 'PC'),
(168, 'Tomb Raider', '', '', 'PC'),
(169, 'Lara Croft and the Temple of Osiris', '', '', 'PC'),
(170, 'DEVOUR', '', '', 'PC'),
(171, 'tModLoader', '', '', 'PC'),
(172, 'Keyboard Killers', '', '', 'PC'),
(173, 'Devolverland Expo', '', '', 'PC'),
(174, 'SUPERVIVE', '', '', 'PC'),
(175, 'Sclash', '', '', 'PC'),
(176, 'Regions Of Ruin', '', '', 'PC'),
(177, 'PAC-MAN™ CHAMPIONSHIP EDITION 2', '', '', 'PC'),
(178, 'The Outlast Trials', '', '', 'PC'),
(179, 'Showdown Bandit', '', '', 'PC'),
(180, '10 Second Ninja X', '', '', 'PC'),
(181, 'The LEGO® NINJAGO® Movie Video Game', '', '', 'PC'),
(182, 'Interkosmos', '', '', 'PC'),
(183, 'Injustice: Gods Among Us Ultimate Edition', '', '', 'PC'),
(184, 'Unfortunate Spacemen', '', '', 'PC'),
(185, 'In Silence', '', '', 'PC'),
(186, 'Relicta', '', '', 'PC'),
(187, 'Scrap Garden', '', '', 'PC'),
(188, 'SEGA Mega Drive & Genesis Classics', '', '', 'PC'),
(189, 'The Walking Dead: The Telltale Definitive Series', '', '', 'PC'),
(190, 'Yu-Gi-Oh!  Master Duel', '', '', 'PC'),
(191, 'FOREWARNED', '', '', 'PC'),
(192, 'Pro Soccer Online', '', '', 'PC'),
(193, 'V Rising', '', '', 'PC'),
(194, 'Resident Evil Village', '', '', 'PC'),
(195, 'Resident Evil Re:Verse', '', '', 'PC'),
(196, 'Spellmasons', '', '', 'PC'),
(197, 'Company of Heroes 2', '', '', 'PC'),
(198, 'Tell Me Why', '', '', 'PC'),
(199, 'Little Nightmares', '', '', 'PC'),
(200, 'Kenshi', '', '', 'PC'),
(201, 'Orcs Must Die! 3', '', '', 'PC'),
(202, 'Devil May Cry 5', '', '', 'PC'),
(203, 'Crysis Remastered', '', '', 'PC'),
(204, 'Halo Infinite', '', '', 'PC'),
(205, 'Titan Quest Anniversary Edition', '', '', 'PC'),
(206, 'Jagged Alliance Gold', '', '', 'PC'),
(207, 'Dying Light', '', '', 'PC'),
(208, 'Crab Game', '', '', 'PC'),
(209, 'Tower Princess: Knight\'s Trial', '', '', 'PC'),
(210, 'Vampire Survivors', '', '', 'PC'),
(211, 'The Elder Scrolls II: Daggerfall', '', '', 'PC'),
(212, 'STALCRAFT: X', '', '', 'PC'),
(213, 'MultiVersus', '', '', 'PC'),
(214, 'Outward', '', '', 'PC'),
(215, 'Call of Juarez Gunslinger', '', '', 'PC'),
(216, 'Omega Strikers', '', '', 'PC'),
(217, 'PUBG: BATTLEGROUNDS', '', '', 'PC'),
(218, 'Lost Ark', '', '', 'PC'),
(219, 'Stumble Guys', '', '', 'PC'),
(220, 'Lethal Company', '', '', 'PC'),
(221, 'THE FINALS', '', '', 'PC'),
(222, 'Shatterline', '', '', 'PC'),
(223, 'Soulstone Survivors: Prologue', '', '', 'PC'),
(224, 'Sifu', '', '', 'PC'),
(225, 'Mafia', '', '', 'PC'),
(226, 'Your Only Move Is HUSTLE', '', '', 'PC'),
(227, 'Grapples Galore', '', '', 'PC'),
(228, 'We Were Here Expeditions: The FriendShip', '', '', 'PC'),
(229, 'Tiny Tina\'s Assault on Dragon Keep: A Wonderlands One-shot Adventure', '', '', 'PC'),
(230, 'Landfall Archives', '', '', 'PC'),
(231, 'Remnant II', '', '', 'PC'),
(232, 'Balatro', '', '', 'PC'),
(233, 'THRONE AND LIBERTY', '', '', 'PC'),
(234, 'Metro: Last Light Complete Edition', '', '', 'PC'),
(235, 'Hue', '', '', 'PC'),
(236, 'Dungeonborne', '', '', 'PC'),
(237, 'Dungeon of the ENDLESS™', '', '', 'PC'),
(238, 'NARAKA: BLADEPOINT', '', '', 'PC'),
(239, 'Baldur\'s Gate 3', '', '', 'PC'),
(240, 'Mortal Kombat 1', '', '', 'PC'),
(241, 'For The King II', '', '', 'PC'),
(242, 'EA SPORTS FC™ 25', '', '', 'PC'),
(243, 'Dragon\'s Dogma 2 Character Creator & Storage', '', '', 'PC'),
(244, 'Dead Island Riptide Definitive Edition', '', '', 'PC'),
(245, 'Marvel Rivals', '', '', 'PC'),
(246, 'Content Warning', '', '', 'PC'),
(247, 'DRAGON BALL: Sparking! ZERO', '', '', 'PC'),
(248, 'ENDLESS™ Legend', '', '', 'PC'),
(249, 'Dark and Darker', '', '', 'PC'),
(250, 'Monster Hunter Wilds Beta test', '', '', 'PC'),
(251, 'Battlefield™ 6 Open Beta', '', '', 'PC'),
(252, 'R.E.P.O.', '', '', 'PC'),
(253, 'Dark Sector', '', '', 'PC'),
(254, 'PEAK', '', '', 'PC'),
(255, 'Mage Arena', '', '', 'PC'),
(256, 'Team Fortress 2', '', '', 'PC'),
(257, 'Dota 2', '', '', 'PC'),
(258, 'Hollow', 'Indie;Adventure;Action', '', 'PC;Xbox One;Nintendo Switch'),
(259, 'Hollow\'s Land', 'Action;RPG', '', 'PC'),
(260, 'Grimm\'s Hollow', 'Indie;Adventure;RPG', '', 'PC'),
(261, 'Hollowed', 'Indie;Adventure;Action', '', 'PC'),
(262, 'Hollow Follow', 'Strategy', '', 'Web'),
(263, 'The Esoterica: Hollow Earth', 'Casual;Adventure', '', 'PC'),
(264, 'Yellow: The Yellow Artifact', 'Casual;Indie;Adventure;Action', '', 'PC;macOS;Linux'),
(265, 'Hollow 2 (itch)', 'Platformer', '', 'PC'),
(266, 'Two Inns at Miller\'s Hollow', 'Casual;Strategy;Indie;RPG', '', 'PC;macOS;Linux'),
(267, 'Sword Art Online -Hollow Fragment', 'Action;RPG', '', 'PS Vita'),
(268, 'SWORD ART ONLINE: Hollow Realization', 'RPG', '', 'PC;PlayStation 4;PS Vita'),
(269, 'Hollow Priest - LD44', 'Shooter', '', 'PC'),
(270, 'Hollow Survivors: Prologue', 'Casual;Indie;Adventure;RPG', '', 'PC;macOS;Linux'),
(271, 'Hollow: Cook Off', 'Indie;Action', '', 'PC'),
(272, 'Drake Hollow', 'Indie;Adventure;Action', '', 'PC;Xbox One'),
(273, 'Scarlet Hollow', 'Casual;Indie;Adventure;RPG', '', 'PC;macOS;Linux'),
(274, 'Sword Art Online Re: Hollow Fragment', 'Action;RPG', '', 'PC;PlayStation 4'),
(275, 'Hollow Knight: Silksong DEMAKE', 'Platformer', '', 'PC'),
(276, 'Left 4 Dead', '', '', 'PC'),
(277, 'Resident Evil 6', '', '', 'PC'),
(278, 'Resident Evil Revelations', '', '', 'PC'),
(279, 'Resident Evil 4 (2005)', '', '', 'PC'),
(280, 'Geometry Dash', '', '', 'PC'),
(281, 'DARK SOULS™ II: Scholar of the First Sin', '', '', 'PC'),
(282, 'Resident Evil', '', '', 'PC'),
(283, 'Resident Evil 5', '', '', 'PC'),
(284, 'Resident Evil Revelations 2', '', '', 'PC'),
(285, 'Resident Evil 0', '', '', 'PC'),
(286, 'Tom Clancy\'s Rainbow Six® Siege X', '', '', 'PC'),
(287, 'Tom Clancy\'s Rainbow Six Siege - Test Server', '', '', 'PC'),
(288, 'Wallpaper Engine', '', '', 'PC'),
(289, 'DARK SOULS™ III', '', '', 'PC'),
(290, 'Resident Evil 7 Biohazard', '', '', 'PC'),
(291, 'Doki Doki Literature Club', '', '', 'PC'),
(292, 'Zula Global', '', '', 'PC'),
(293, 'Age of Empires II: Definitive Edition', '', '', 'PC'),
(294, 'DARK SOULS™: REMASTERED', '', '', 'PC'),
(295, 'Resident Evil 2', '', '', 'PC'),
(296, 'Aimlabs', '', '', 'PC'),
(297, 'Sekiro™: Shadows Die Twice', '', '', 'PC'),
(298, 'CreativeDestruction', '', '', 'PC'),
(299, 'OMORI', '', '', 'PC'),
(300, 'LEWDAPOCALYPSE', '', '', 'PC'),
(301, 'STAR WARS™: The Old Republic™', '', '', 'PC'),
(302, 'MY HERO ULTRA RUMBLE', '', '', 'PC'),
(303, 'Find Love or Die Trying', '', '', 'PC'),
(304, 'Back 4 Blood', '', '', 'PC'),
(305, 'MONSTER HUNTER RISE', '', '', 'PC'),
(306, 'Resident Evil 4', '', '', 'PC'),
(307, 'The Last of Us™ Part I', '', '', 'PC'),
(308, 'SILENT HILL 2', '', '', 'PC'),
(309, 'Zort', '', '', 'PC'),
(310, 'Metro 2033 Redux', '', '', 'PC');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user_game_stats`
--

CREATE TABLE `user_game_stats` (
  `user_id` int(11) NOT NULL,
  `game_id` int(11) NOT NULL,
  `playtime_hours` float DEFAULT 0,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `user_game_stats`
--

INSERT INTO `user_game_stats` (`user_id`, `game_id`, `playtime_hours`, `updated_at`) VALUES
(1, 1, 25.95, '2025-09-11 03:57:46'),
(1, 2, 12.85, '2025-09-11 03:57:46'),
(1, 4, 2.03333, '2025-09-11 03:57:46'),
(1, 28, 1.65, '2025-09-11 03:57:46'),
(1, 29, 0, '2025-09-11 03:57:46'),
(1, 30, 40.7167, '2025-09-11 03:57:46'),
(1, 31, 0, '2025-09-11 03:57:46'),
(1, 32, 0, '2025-09-11 03:57:46'),
(1, 33, 0, '2025-09-11 03:57:46'),
(1, 34, 0, '2025-09-11 03:57:46'),
(1, 35, 21.7, '2025-09-11 03:57:46'),
(1, 36, 59.65, '2025-09-11 03:57:46'),
(1, 37, 2.38333, '2025-09-11 03:57:46'),
(1, 38, 2.15, '2025-09-11 03:57:46'),
(1, 39, 9.41667, '2025-09-11 03:57:46'),
(1, 40, 0, '2025-09-11 03:57:46'),
(1, 41, 8.55, '2025-09-11 03:57:46'),
(1, 42, 186.533, '2025-09-11 03:57:46'),
(1, 43, 4.96667, '2025-09-11 03:57:46'),
(1, 44, 0.45, '2025-09-11 03:57:46'),
(1, 45, 5, '2025-09-11 03:57:46'),
(1, 46, 0.75, '2025-09-11 03:57:46'),
(1, 47, 1.61667, '2025-09-11 03:57:46'),
(1, 48, 0, '2025-09-11 03:57:46'),
(1, 49, 5.28333, '2025-09-11 03:57:46'),
(1, 50, 0, '2025-09-11 03:57:46'),
(1, 51, 3.2, '2025-09-11 03:57:46'),
(1, 52, 39.2667, '2025-09-11 03:57:46'),
(1, 53, 0.0166667, '2025-09-11 03:57:46'),
(1, 54, 0.0166667, '2025-09-11 03:57:46'),
(1, 55, 16.1167, '2025-09-11 03:57:46'),
(1, 56, 52.25, '2025-09-11 03:57:46'),
(1, 57, 10.3667, '2025-09-11 03:57:46'),
(1, 58, 1.15, '2025-09-11 03:57:46'),
(1, 59, 7.21667, '2025-09-11 03:57:46'),
(1, 60, 1.36667, '2025-09-11 03:57:46'),
(1, 61, 17.9, '2025-09-11 03:57:46'),
(1, 62, 44.0667, '2025-09-11 03:57:46'),
(1, 63, 0, '2025-09-11 03:57:46'),
(1, 64, 0, '2025-09-11 04:15:41'),
(1, 65, 0, '2025-09-11 03:57:46'),
(1, 66, 1.85, '2025-09-11 03:57:46'),
(1, 67, 14.2167, '2025-09-11 03:57:46'),
(1, 68, 0, '2025-09-11 03:57:46'),
(1, 69, 0, '2025-09-11 03:57:46'),
(1, 70, 5.8, '2025-09-11 03:57:46'),
(1, 71, 83.4167, '2025-09-11 03:57:46'),
(1, 72, 3.31667, '2025-09-11 03:57:46'),
(1, 73, 205.5, '2025-09-11 03:57:46'),
(1, 74, 0, '2025-09-11 03:57:46'),
(1, 75, 8, '2025-09-11 03:57:46'),
(1, 76, 44.6333, '2025-09-11 03:57:46'),
(1, 77, 0.316667, '2025-09-11 03:57:46'),
(1, 78, 0, '2025-09-11 03:57:46'),
(1, 79, 1.36667, '2025-09-11 03:57:46'),
(1, 80, 2.13333, '2025-09-11 03:57:46'),
(1, 81, 0, '2025-09-11 03:57:46'),
(1, 82, 6.01667, '2025-09-11 03:57:46'),
(1, 83, 226.283, '2025-09-11 03:57:46'),
(1, 84, 0, '2025-09-11 03:57:46'),
(1, 85, 0, '2025-09-11 03:57:46'),
(1, 86, 7.38333, '2025-09-11 03:57:46'),
(1, 87, 0, '2025-09-11 03:57:46'),
(1, 88, 0.466667, '2025-09-11 03:57:46'),
(1, 89, 1.08333, '2025-09-11 03:57:46'),
(1, 90, 0, '2025-09-11 03:57:46'),
(1, 91, 1.75, '2025-09-11 03:57:46'),
(1, 92, 6.73333, '2025-09-11 03:57:46'),
(1, 93, 0.366667, '2025-09-11 03:57:46'),
(1, 94, 1.73333, '2025-09-11 03:57:46'),
(1, 95, 2.83333, '2025-09-11 03:57:46'),
(1, 96, 11.4833, '2025-09-11 03:57:46'),
(1, 97, 0.633333, '2025-09-11 03:57:46'),
(1, 98, 0.0833333, '2025-09-11 03:57:46'),
(1, 99, 0, '2025-09-11 03:57:46'),
(1, 100, 1.1, '2025-09-11 03:57:46'),
(1, 101, 6.06667, '2025-09-11 03:57:46'),
(1, 102, 11.4, '2025-09-11 03:57:46'),
(1, 103, 3.16667, '2025-09-11 03:57:46'),
(1, 104, 0.216667, '2025-09-11 03:57:46'),
(1, 105, 42.1833, '2025-09-11 03:57:46'),
(1, 106, 0, '2025-09-11 03:57:46'),
(1, 107, 2.63333, '2025-09-11 03:57:46'),
(1, 108, 2.2, '2025-09-11 03:57:46'),
(1, 109, 1.55, '2025-09-11 03:57:46'),
(1, 110, 3.93333, '2025-09-11 03:57:46'),
(1, 111, 0, '2025-09-11 03:57:46'),
(1, 112, 0, '2025-09-11 03:57:46'),
(1, 113, 76.85, '2025-09-11 03:57:46'),
(1, 114, 1.48333, '2025-09-11 03:57:46'),
(1, 115, 10.3667, '2025-09-11 03:57:46'),
(1, 116, 0, '2025-09-11 03:57:46'),
(1, 117, 5.65, '2025-09-11 03:57:46'),
(1, 118, 0, '2025-09-11 03:57:46'),
(1, 119, 35.8333, '2025-09-11 03:57:46'),
(1, 120, 89.45, '2025-09-11 03:57:46'),
(1, 121, 0, '2025-09-11 03:57:46'),
(1, 122, 10.3667, '2025-09-11 03:57:46'),
(1, 123, 22.1333, '2025-09-11 03:57:46'),
(1, 124, 0, '2025-09-11 03:57:46'),
(1, 125, 7.95, '2025-09-11 03:57:46'),
(1, 126, 0, '2025-09-11 03:57:46'),
(1, 127, 0, '2025-09-11 03:57:46'),
(1, 128, 0, '2025-09-11 03:57:46'),
(1, 129, 3.35, '2025-09-11 03:57:46'),
(1, 130, 8.3, '2025-09-11 03:57:46'),
(1, 131, 0, '2025-09-11 03:57:46'),
(1, 132, 0.85, '2025-09-11 03:57:46'),
(1, 133, 0, '2025-09-11 03:57:46'),
(1, 134, 0.1, '2025-09-11 03:57:46'),
(1, 135, 3.01667, '2025-09-11 03:57:46'),
(1, 136, 2.08333, '2025-09-11 03:57:46'),
(1, 137, 31.0833, '2025-09-11 03:57:46'),
(1, 138, 37.1667, '2025-09-11 03:57:46'),
(1, 139, 0, '2025-09-11 03:57:46'),
(1, 140, 0.166667, '2025-09-11 03:57:46'),
(1, 141, 0, '2025-09-11 03:57:46'),
(1, 142, 0, '2025-09-11 03:57:46'),
(1, 143, 1.71667, '2025-09-11 03:57:46'),
(1, 144, 0, '2025-09-11 03:57:46'),
(1, 145, 4, '2025-09-11 03:57:46'),
(1, 146, 166.467, '2025-09-11 03:57:46'),
(1, 147, 1.7, '2025-09-11 03:57:46'),
(1, 148, 68.5, '2025-09-11 03:57:46'),
(1, 149, 19.25, '2025-09-11 03:57:46'),
(1, 150, 3.83333, '2025-09-11 03:57:46'),
(1, 151, 10.55, '2025-09-11 03:57:46'),
(1, 152, 22.25, '2025-09-11 03:57:46'),
(1, 153, 53.5833, '2025-09-11 03:57:46'),
(1, 154, 99.5833, '2025-09-11 03:57:46'),
(1, 155, 192.017, '2025-09-11 03:57:46'),
(1, 156, 0, '2025-09-11 03:57:46'),
(1, 157, 13.0167, '2025-09-11 03:57:46'),
(1, 158, 2.78333, '2025-09-11 03:57:46'),
(1, 159, 4.45, '2025-09-11 03:57:46'),
(1, 160, 0, '2025-09-11 03:57:46'),
(1, 161, 8.3, '2025-09-11 03:57:46'),
(1, 162, 1.85, '2025-09-11 03:57:46'),
(1, 163, 1.5, '2025-09-11 03:57:46'),
(1, 164, 0, '2025-09-11 03:57:46'),
(1, 165, 0, '2025-09-11 03:57:46'),
(1, 166, 0, '2025-09-11 03:57:46'),
(1, 167, 0, '2025-09-11 03:57:46'),
(1, 168, 0.0833333, '2025-09-11 03:57:46'),
(1, 169, 0, '2025-09-11 03:57:46'),
(1, 170, 1.28333, '2025-09-11 03:57:46'),
(1, 171, 211.433, '2025-09-11 03:57:46'),
(1, 172, 0, '2025-09-11 03:57:46'),
(1, 173, 0, '2025-09-11 03:57:46'),
(1, 174, 7.38333, '2025-09-11 03:57:46'),
(1, 175, 0.7, '2025-09-11 03:57:46'),
(1, 176, 0, '2025-09-11 03:57:46'),
(1, 177, 0, '2025-09-11 03:57:46'),
(1, 178, 8.01667, '2025-09-11 03:57:46'),
(1, 179, 0, '2025-09-11 03:57:46'),
(1, 180, 0, '2025-09-11 03:57:46'),
(1, 181, 0, '2025-09-11 03:57:46'),
(1, 182, 0, '2025-09-11 03:57:46'),
(1, 183, 0.0833333, '2025-09-11 03:57:46'),
(1, 184, 0.3, '2025-09-11 03:57:46'),
(1, 185, 0.05, '2025-09-11 03:57:46'),
(1, 186, 0, '2025-09-11 03:57:46'),
(1, 187, 0, '2025-09-11 03:57:46'),
(1, 188, 0, '2025-09-11 03:57:46'),
(1, 189, 0, '2025-09-11 03:57:46'),
(1, 190, 4.1, '2025-09-11 03:57:46'),
(1, 191, 1.61667, '2025-09-11 03:57:46'),
(1, 192, 19.8667, '2025-09-11 03:57:46'),
(1, 193, 16.0833, '2025-09-11 03:57:46'),
(1, 194, 0, '2025-09-11 03:57:46'),
(1, 195, 0, '2025-09-11 03:57:46'),
(1, 196, 1.43333, '2025-09-11 03:57:46'),
(1, 197, 0, '2025-09-11 03:57:46'),
(1, 198, 0, '2025-09-11 03:57:46'),
(1, 199, 3.15, '2025-09-11 03:57:47'),
(1, 200, 111.917, '2025-09-11 03:57:47'),
(1, 201, 4.11667, '2025-09-11 03:57:47'),
(1, 202, 18.8167, '2025-09-11 03:57:47'),
(1, 203, 0, '2025-09-11 03:57:47'),
(1, 204, 1.01667, '2025-09-11 03:57:47'),
(1, 205, 0, '2025-09-11 03:57:47'),
(1, 206, 0, '2025-09-11 03:57:47'),
(1, 207, 9.31667, '2025-09-11 03:57:47'),
(1, 208, 2.63333, '2025-09-11 03:57:47'),
(1, 209, 0, '2025-09-11 03:57:47'),
(1, 210, 17.4, '2025-09-11 03:57:47'),
(1, 211, 0, '2025-09-11 03:57:47'),
(1, 212, 2.61667, '2025-09-11 03:57:47'),
(1, 213, 2.43333, '2025-09-11 03:57:47'),
(1, 214, 30.6, '2025-09-11 03:57:47'),
(1, 215, 1.76667, '2025-09-11 03:57:47'),
(1, 216, 0.433333, '2025-09-11 03:57:47'),
(1, 217, 10.85, '2025-09-11 03:57:47'),
(1, 218, 0.983333, '2025-09-11 03:57:47'),
(1, 219, 8.53333, '2025-09-11 03:57:47'),
(1, 220, 31.6167, '2025-09-11 03:57:47'),
(1, 221, 0.7, '2025-09-11 03:57:47'),
(1, 222, 0.133333, '2025-09-11 03:57:47'),
(1, 223, 4.45, '2025-09-11 03:57:47'),
(1, 224, 16.5833, '2025-09-11 03:57:47'),
(1, 225, 0, '2025-09-11 03:57:47'),
(1, 226, 12.9333, '2025-09-11 03:57:47'),
(1, 227, 0, '2025-09-11 03:57:47'),
(1, 228, 0, '2025-09-11 03:57:47'),
(1, 229, 0.483333, '2025-09-11 03:57:47'),
(1, 230, 0, '2025-09-11 03:57:47'),
(1, 231, 7.23333, '2025-09-11 03:57:47'),
(1, 232, 41.7333, '2025-09-11 03:57:47'),
(1, 233, 0.183333, '2025-09-11 03:57:47'),
(1, 234, 0, '2025-09-11 03:57:47'),
(1, 235, 0, '2025-09-11 03:57:47'),
(1, 236, 0.716667, '2025-09-11 03:57:47'),
(1, 237, 0.0166667, '2025-09-11 03:57:47'),
(1, 238, 0.6, '2025-09-11 03:57:47'),
(1, 239, 86.75, '2025-09-11 03:57:47'),
(1, 240, 17.1, '2025-09-11 03:57:47'),
(1, 241, 8.26667, '2025-09-11 03:57:47'),
(1, 242, 97.6333, '2025-09-11 03:57:47'),
(1, 243, 0.15, '2025-09-11 03:57:47'),
(1, 244, 0, '2025-09-11 03:57:47'),
(1, 245, 1.05, '2025-09-11 03:57:47'),
(1, 246, 8.58333, '2025-09-11 03:57:47'),
(1, 247, 12.3167, '2025-09-11 03:57:47'),
(1, 248, 0, '2025-09-11 03:57:47'),
(1, 249, 6.15, '2025-09-11 03:57:47'),
(1, 250, 2.73333, '2025-09-11 03:57:47'),
(1, 251, 0.0333333, '2025-09-11 03:57:47'),
(1, 252, 0, '2025-09-11 03:57:47'),
(1, 253, 0, '2025-09-11 03:57:47'),
(1, 254, 30.2, '2025-09-11 03:57:47'),
(1, 255, 2.48333, '2025-09-11 03:57:47'),
(1, 256, 1.56667, '2025-09-11 03:57:47'),
(1, 257, 17.9667, '2025-09-11 03:57:47'),
(3, 1, 131.017, '2025-09-11 06:51:36'),
(3, 30, 29.8667, '2025-09-11 06:51:36'),
(3, 36, 842.433, '2025-09-11 06:51:36'),
(3, 42, 181.717, '2025-09-11 06:51:36'),
(3, 49, 0.216667, '2025-09-11 06:51:36'),
(3, 51, 1.05, '2025-09-11 06:51:36'),
(3, 56, 82.3167, '2025-09-11 06:51:36'),
(3, 61, 29.5, '2025-09-11 06:51:36'),
(3, 62, 5.13333, '2025-09-11 06:51:36'),
(3, 70, 99.6333, '2025-09-11 06:51:36'),
(3, 73, 65.5, '2025-09-11 06:51:36'),
(3, 74, 0, '2025-09-11 06:51:36'),
(3, 76, 4.53333, '2025-09-11 06:51:36'),
(3, 83, 166.05, '2025-09-11 06:51:36'),
(3, 84, 4.63333, '2025-09-11 06:51:36'),
(3, 89, 3.5, '2025-09-11 06:51:36'),
(3, 105, 6.21667, '2025-09-11 06:51:36'),
(3, 106, 0.366667, '2025-09-11 06:51:36'),
(3, 113, 16.9333, '2025-09-11 06:51:36'),
(3, 119, 2.16667, '2025-09-11 06:51:36'),
(3, 132, 0, '2025-09-11 06:51:36'),
(3, 138, 25.2833, '2025-09-11 06:51:36'),
(3, 146, 2.16667, '2025-09-11 06:51:36'),
(3, 153, 56.75, '2025-09-11 06:51:36'),
(3, 154, 5.38333, '2025-09-11 06:51:36'),
(3, 155, 122.517, '2025-09-11 06:51:36'),
(3, 162, 0, '2025-09-11 06:51:36'),
(3, 171, 91.5667, '2025-09-11 06:51:36'),
(3, 174, 2.13333, '2025-09-11 06:51:36'),
(3, 192, 26.0333, '2025-09-11 06:51:36'),
(3, 199, 0, '2025-09-11 06:51:36'),
(3, 202, 2.96667, '2025-09-11 06:51:36'),
(3, 217, 26.3833, '2025-09-11 06:51:36'),
(3, 220, 7.21667, '2025-09-11 06:51:36'),
(3, 245, 1.8, '2025-09-11 06:51:36'),
(3, 246, 3.05, '2025-09-11 06:51:36'),
(3, 254, 18.7833, '2025-09-11 06:51:36'),
(3, 255, 2.41667, '2025-09-11 06:51:36'),
(3, 256, 13.2167, '2025-09-11 06:51:36'),
(3, 257, 31.4333, '2025-09-11 06:51:36'),
(3, 276, 0.266667, '2025-09-11 06:51:36'),
(3, 277, 2.11667, '2025-09-11 06:51:36'),
(3, 278, 0, '2025-09-11 06:51:36'),
(3, 279, 0, '2025-09-11 06:51:36'),
(3, 280, 19.5833, '2025-09-11 06:51:36'),
(3, 281, 34.5833, '2025-09-11 06:51:36'),
(3, 282, 0, '2025-09-11 06:51:36'),
(3, 283, 0, '2025-09-11 06:51:36'),
(3, 284, 0, '2025-09-11 06:51:36'),
(3, 285, 0, '2025-09-11 06:51:36'),
(3, 286, 8.06667, '2025-09-11 06:51:36'),
(3, 287, 0, '2025-09-11 06:51:36'),
(3, 288, 3.48333, '2025-09-11 06:51:36'),
(3, 289, 12.5333, '2025-09-11 06:51:36'),
(3, 290, 0, '2025-09-11 06:51:36'),
(3, 291, 0, '2025-09-11 06:51:36'),
(3, 292, 78.5667, '2025-09-11 06:51:36'),
(3, 293, 2.96667, '2025-09-11 06:51:36'),
(3, 294, 40.8833, '2025-09-11 06:51:36'),
(3, 295, 11.6, '2025-09-11 06:51:36'),
(3, 296, 2.68333, '2025-09-11 06:51:36'),
(3, 297, 47.4167, '2025-09-11 06:51:36'),
(3, 298, 16.0333, '2025-09-11 06:51:36'),
(3, 299, 20.5667, '2025-09-11 06:51:36'),
(3, 300, 0.0666667, '2025-09-11 06:51:36'),
(3, 301, 9.93333, '2025-09-11 06:51:36'),
(3, 302, 2.06667, '2025-09-11 06:51:36'),
(3, 303, 2.46667, '2025-09-11 06:51:36'),
(3, 304, 0.716667, '2025-09-11 06:51:36'),
(3, 305, 3.26667, '2025-09-11 06:51:36'),
(3, 306, 6.98333, '2025-09-11 06:51:36'),
(3, 307, 3.15, '2025-09-11 06:51:36'),
(3, 308, 5.76667, '2025-09-11 06:51:36'),
(3, 309, 3.03333, '2025-09-11 06:51:36'),
(3, 310, 0, '2025-09-11 06:51:36');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `hashed_password` varchar(255) NOT NULL,
  `rol` varchar(32) DEFAULT 'jugador'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `hashed_password`, `rol`) VALUES
(1, 'Gus', 'gus@example.com', '$2b$12$s86fjjADudYhugKD01kwKumGOg5J1XYWb.cLSCEjPJMC99fZ5ux52', 'jugador'),
(2, 'pepetoño', 'pepetoño@gmail.com', '$2b$12$OpEs1RYrsCMJb2.UvMG3ZOlCb9sxeSGH72bmWUbWPAMtRiBKMiGEC', 'jugador'),
(3, 'pepe reyes ', 'gorzen@gmail.com', '$2b$12$55VzwghCws2/1zJmukGWSOxBokER14yexkh/VZ1Be1HJBVkMGndYa', 'jugador');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `agent_state`
--
ALTER TABLE `agent_state`
  ADD PRIMARY KEY (`user_id`);

--
-- Indices de la tabla `interacciones`
--
ALTER TABLE `interacciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user` (`usuario_id`),
  ADD KEY `fk_game` (`juego_id`);

--
-- Indices de la tabla `juegos`
--
ALTER TABLE `juegos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `user_game_stats`
--
ALTER TABLE `user_game_stats`
  ADD PRIMARY KEY (`user_id`,`game_id`),
  ADD KEY `fk_ugs_game` (`game_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `interacciones`
--
ALTER TABLE `interacciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `juegos`
--
ALTER TABLE `juegos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=311;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `agent_state`
--
ALTER TABLE `agent_state`
  ADD CONSTRAINT `fk_agent_usuario` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `interacciones`
--
ALTER TABLE `interacciones`
  ADD CONSTRAINT `fk_game` FOREIGN KEY (`juego_id`) REFERENCES `juegos` (`id`),
  ADD CONSTRAINT `fk_user` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `user_game_stats`
--
ALTER TABLE `user_game_stats`
  ADD CONSTRAINT `fk_ugs_game` FOREIGN KEY (`game_id`) REFERENCES `juegos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_ugs_user` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
