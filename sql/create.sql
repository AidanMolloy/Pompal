DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS friends;
DROP TABLE IF EXISTS notes;
DROP TABLE IF EXISTS timers;
DROP TABLE IF EXISTS music;

CREATE TABLE users 
(
    username VARCHAR(20) NOT NULL,
    password VARCHAR(64) NOT NULL,
    email VARCHAR(64) NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE friends 
(
    friendID INT AUTO_INCREMENT,
    userOne VARCHAR(20) NOT NULL,
    userTwo VARCHAR(20) NOT NULL,
    status INT NOT NULL,
    PRIMARY KEY (friendID)
);

CREATE TABLE notes 
(
    noteID INT AUTO_INCREMENT,
    userID VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (noteID)
);

CREATE TABLE timers 
(
    timerID INT AUTO_INCREMENT,
    userID VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    noteID INT,
    musicID VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    over_at DATETIME NOT NULL,
    PRIMARY KEY (timerID)
);

CREATE TABLE music (
    musicID varchar(255) NOT NULL,
    musicCredit text,
    musicLink text,
    plays int(11) NOT NULL,
    PRIMARY KEY (musicID)
)

INSERT INTO `music` (`musicID`, `musicCredit`, `musicLink`, `plays`) VALUES
('Carefree - Kevin MacLeod', 'Carefree by Kevin MacLeod<br>\nLink: https://incompetech.filmmusic.io/song/3476-carefree<br>\nLicense: http://creativecommons.org/licenses/by/4.0/', 'carefree-by-kevin-macleod-from-filmmusic-io.mp3', 20),
('Cheery Monday - Kevin MacLeod', 'Cheery Monday by Kevin MacLeod<br>\nLink: https://incompetech.filmmusic.io/song/3495-cheery-monday<br>\nLicense: http://creativecommons.org/licenses/by/4.0/', 'cheery-monday-by-kevin-macleod-from-filmmusic-io.mp3', 24),
('Funkorama - Kevin MacLeod', 'Funkorama by Kevin MacLeod<br>\nLink: https://incompetech.filmmusic.io/song/3788-funkorama<br>\nLicense: http://creativecommons.org/licenses/by/4.0/', 'funkorama-by-kevin-macleod-from-filmmusic-io.mp3', 16),
('Ice Flow - Kevin MacLeod', 'Ice Flow by Kevin MacLeod<br>\nLink: https://incompetech.filmmusic.io/song/3898-ice-flow<br>\nLicense: http://creativecommons.org/licenses/by/4.0/', 'ice-flow-by-kevin-macleod-from-filmmusic-io.mp3', 28),
('Inspired - Kevin MacLeod', 'Inspired by Kevin MacLeod<br>\nLink: https://incompetech.filmmusic.io/song/3918-inspired<br>\nLicense: http://creativecommons.org/licenses/by/4.0/', 'inspired-by-kevin-macleod-from-filmmusic-io.mp3', 17),
('Monkeys Spinning Monkeys - Kevin MacLeod', 'Monkeys Spinning Monkeys by Kevin MacLeod<br>\nLink: https://incompetech.filmmusic.io/song/4071-monkeys-spinning-monkeys<br>\nLicense: http://creativecommons.org/licenses/by/4.0/', 'monkeys-spinning-monkeys-by-kevin-macleod-from-filmmusic-io.mp3', 19),
('Rain - Mother Nature', 'Music from https://www.zapsplat.com', 'pm_rd_rain_6_intense_foliage_drippy.wav_361.mp3', 15),
('Sneaky Snitch - Kevin MacLeod', 'Sneaky Snitch by Kevin MacLeod<br>\nLink: https://incompetech.filmmusic.io/song/4384-sneaky-snitch<br>\nLicense: http://creativecommons.org/licenses/by/4.0/', 'sneaky-snitch-by-kevin-macleod-from-filmmusic-io.mp3', 23),
('The Descent - Kevin MacLeod', 'The Descent by Kevin MacLeod<br>\nLink: https://incompetech.filmmusic.io/song/4490-the-descent<br>\nLicense: http://creativecommons.org/licenses/by/4.0/', 'the-descent-by-kevin-macleod-from-filmmusic-io.mp3', 27),
('The Entertainer - Kevin MacLeod', 'The Entertainer by Kevin MacLeod<br>\nLink: https://incompetech.filmmusic.io/song/5765-the-entertainer<br>\nLicense: http://creativecommons.org/licenses/by/4.0/', 'the-entertainer-by-kevin-macleod-from-filmmusic-io.mp3', 13),
('Wholesome - Kevin MacLeod', 'Wholesome by Kevin MacLeod<br>\nLink: https://incompetech.filmmusic.io/song/5050-wholesome<br>\nLicense: http://creativecommons.org/licenses/by/4.0/', 'wholesome-by-kevin-macleod-from-filmmusic-io.mp3', 32),
('Wind - Mother Nature', '	\nMusic from https://www.zapsplat.com', 'zapsplat_nature_wind_blustery_against_window_slightly_open_occ_howling_gusts_47143.mp3', 12);
