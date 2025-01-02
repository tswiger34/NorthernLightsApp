CREATE TABLE Date_dim(
    [DateID] INT PRIMARY KEY,
    [USDate] VARCHAR(10),
    FOREIGN KEY(DateID)
)
CREATE TABLE MoonPhases(
    [DateID] INT PRIMARY KEY,
    [Time] VARCHAR(10),
    [MoonPhase] VARCHAR(15),
    [Lunation] SMALLINT,
    FOREIGN KEY(DateID)
),

CREATE TABLE LightPollution(

);

CREATE TABLE Locations(

);

CREATE TABLE SolarWeather(

);

CREATE TABLE EarthWeather(

);

CREATE TABLE NorthernLightEvents(

);

CREATE TABLE MasterTable(
    [DateID] INT PRIMARY KEY,
    [LunarLuminosity] REAL NULL,
    [NorthernLightEvent] BIT,
    [NorthernLightRating] REAL,
    FOREIGN KEY(DateID)
)