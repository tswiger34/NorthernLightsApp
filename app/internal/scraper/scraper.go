package scraper

import (
	"bufio"
	"bytes"
	"fmt"
	"strconv"
	"strings"
	"time"

	"github.com/gocolly/colly/v2"
)

const forecastURL = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"

type Forecast struct {
	Dates []string
	TimePeriods []string
	Values [][]float64
	ScrapedAt time.Time
}

func parse(raw []byte) (*Forecast, error) {
	scanner := bufio.NewScanner(bytes.NewReader(raw))

	var lines []string
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		return nil, err
	}

	// 1. Locate the header line
	var idx int
	for i, l := range lines {
		if strings.Contains(l, "NOAA Kp index breakdown") {
			idx = i + 2 // skip header + separator
			break
		}
	}
	if idx == 0 {
		return nil, fmt.Errorf("header not found")
	}
	dataLines := lines[idx : idx+9]

	// 2. Extract the five dates from the first data line
	parts := strings.Fields(dataLines[0])
	var dates []string
	for i := range 5 {
		dates = append(dates, fmt.Sprintf("%s-%s", parts[2*i], parts[2*i+1]))
	}

	// 3. Loop through the remaining lines
	var timePeriods []string
	var values [][]float64
	for _, l := range dataLines[1:] {
		if strings.TrimSpace(l) == "" {
			continue
		}
		chunks := strings.Fields(l)
		timePeriods = append(timePeriods, chunks[0])

		var row []float64
		for _, v := range chunks[1:] {
			f, err := strconv.ParseFloat(v, 64)
			if err != nil {
				return nil, fmt.Errorf("parse %q: %w", v, err)
			}
			row = append(row, f)
		}
		values = append(values, row)
	}

	return &Forecast{
		Dates:       dates,
		TimePeriods: timePeriods,
		Values:      values,
		ScrapedAt:   time.Now().UTC(),
	}, nil
}

func FetchForecast() (*Forecast, error) {
	c := colly.NewCollector()
	var body []byte
	var scrapeErr error

	c.OnResponse(func(r *colly.Response) {
		body = r.Body
	})
	c.OnError(func(_ *colly.Response, err error) { scrapeErr = err })
	if err := c.Visit(forecastURL); err != nil {
		return nil, err
	}
	if scrapeErr != nil {
		return nil, scrapeErr
	}
	return parse(body)
}