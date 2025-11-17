// src/App.js
// Main React component for our single-page weather app.
// Responsibilities:
// - Show a search bar for entering a UK city
// - Call our Python backend to get weather data
// - Display loading/error states and the result

// src/App.js
// Main React component for our weather app.
//
// Flow:
// - User types a UK city name
// - We call our Python backend: GET /api/weather?city=<name>
// - Backend calls WeatherAPI.com and returns simplified JSON
// - We display the result or an error

import React, { useState } from "react";
import "./App.css";

function App() {
  const [city, setCity] = useState("");

  const [weather, setWeather] = useState(null);

  const [error, setError] = useState("");

  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!city.trim()) {
      setError("Please enter a UK city name.");
      setWeather(null);
      return;
    }

    setLoading(true);
    setError("");
    setWeather(null);

    try {
      const response = await fetch(`/api/weather?city=${city}`);

      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.detail || "Failed to fetch weather.");
      }

      const data = await response.json();

      // We expect "data" to look like:
      // {
      //   city: "London",
      //   country: "United Kingdom",
      //   localtime: "2025-11-17 11:16",
      //   temperature: 6.2,
      //   feels_like: 2.8,
      //   humidity: 75,
      //   description: "Sunny",
      //   icon: "https://..."
      // }

      setWeather(data);
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1 className="title">UK Weather Finder</h1>

      {/* Search form */}
      <form className="search-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter a UK city, e.g. London"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          className="search-input"
        />
        <button type="submit" className="search-button">
          Search
        </button>
      </form>

      {/* Loading / error messages */}
      {loading && <p className="info">Loading...</p>}
      {error && !loading && <p className="error">{error}</p>}

      {/* Weather result (only show when we have data and not loading) */}
      {weather && !loading && (
        <div className="weather-card">
          <h2>
            {weather.city}, {weather.country}
          </h2>

          {weather.localtime && (
            <p className="localtime">Local time: {weather.localtime}</p>
          )}

          <p className="description">{weather.description}</p>

          <p className="temp">
            {Math.round(weather.temperature)}°C
            <span className="feels-like">
              {" "}
              (feels like {Math.round(weather.feels_like)}°C)
            </span>
          </p>

          <p>Humidity: {weather.humidity}%</p>

          {weather.icon && (
            <img
              src={weather.icon}
              alt={weather.description}
              className="weather-icon"
            />
          )}
        </div>
      )}
    </div>
  );
}

export default App;
