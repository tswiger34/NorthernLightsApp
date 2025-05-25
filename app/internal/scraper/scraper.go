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

type Forecast struct  {
	Dates       []string    // Dates for the three days
	TimePeriods []string    // Time periods for the forecast
	Values      [][]float64 // Kp index values for each time period
	ScrapedAt   time.Time   // Timestamp when the forecast was scraped
}
const forecastURL = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"

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
			idx = i + 2
			break
		}
	}
	if idx == 0 {
		return nil, fmt.Errorf("header not found, got %s lines", lines)
	}

	var endIdx int = idx + 9
	if len(lines) < endIdx {
		panic("insufficient data lines")
	}

	dataLines := lines[idx : endIdx]

	// 2. Extract the three dates from the first data line
	parts := strings.Fields(dataLines[0])
	if len(parts) != 6{
		return nil, fmt.Errorf("expected 3 date parts, got %d", len(parts))
	}
	var dates []string
	for i := range 3 {
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
		if len(chunks) < 1+len(dates) {
			return nil, fmt.Errorf("insufficient data in line: %q", l)
		}
		timePeriods = append(timePeriods, chunks[0])
	
		var row []float64
		dataFieldsProcessed := 0
		
		// Process all chunks after the time period, but skip annotations
		for i := 1; i < len(chunks) && dataFieldsProcessed < len(dates); i++ {
			v := strings.TrimSpace(chunks[i])
			
			// Skip annotation fields that start with "("
			if strings.HasPrefix(v, "(") {
				continue
			}
			
			// Remove any trailing annotations like "(G1)" from the value
			if idx := strings.Index(v, "("); idx != -1 {
				v = v[:idx]
				v = strings.TrimSpace(v)
			}
			
			if v == "" {
				return nil, fmt.Errorf("empty value in data line: %q", l)
			}
			
			f, err := strconv.ParseFloat(v, 64)
			if err != nil {
				return nil, fmt.Errorf("parse %q: %w", v, err)
			}
			row = append(row, f)
			dataFieldsProcessed++
		}
		
		if dataFieldsProcessed < len(dates) {
			return nil, fmt.Errorf("insufficient numeric values in line: %q", l)
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